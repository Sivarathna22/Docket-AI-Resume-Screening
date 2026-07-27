import os
import chromadb
import ollama
from resume_parser import parse_resume

# Persistent ChromaDB client - stores data on disk in data/chroma_db
client = chromadb.PersistentClient(path="data/chroma_db")

# One collection holds all resume chunks across all candidates
collection = client.get_or_create_collection(name="resumes")

EMBED_MODEL = "nomic-embed-text"


def embed_text(text):
    """Get an embedding vector for a piece of text using Ollama."""
    response = ollama.embeddings(model=EMBED_MODEL, prompt=text)
    return response["embedding"]


def index_resume(pdf_path):
    """
    Parse a resume, embed each section separately, and store in ChromaDB.
    Each section becomes its own 'document' so retrieval can be precise
    (e.g. just the Skills section, just the Experience section).
    """
    result = parse_resume(pdf_path)
    file_name = result["file_name"]
    candidate_name = result["candidate_name"]
    sections = result["sections"]

    for section_name, section_text in sections.items():
        if not section_text.strip():
            continue

        # Skip the header section for embedding (just contact info, not useful for matching)
        if section_name == "header":
            continue

        embedding = embed_text(section_text)

        # Unique ID per chunk: filename + section name
        chunk_id = f"{file_name}::{section_name}"

        collection.upsert(
            ids=[chunk_id],
            embeddings=[embedding],
            documents=[section_text],
            metadatas=[{
                "file_name": file_name,
                "candidate_name": candidate_name,
                "section": section_name
            }]
        )
        print(f"  Indexed [{section_name}] from {file_name}")


def index_all_resumes(resumes_folder="data/resumes"):
    """Index every PDF in the resumes folder."""
    for file_name in os.listdir(resumes_folder):
        if file_name.lower().endswith(".pdf"):
            path = os.path.join(resumes_folder, file_name)
            print(f"Indexing {file_name}...")
            index_resume(path)


def search(query, top_k=5):
    """
    Search across all indexed resume chunks for the most relevant matches
    to a query (e.g. a job description, or a specific question).
    """
    query_embedding = embed_text(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    matches = []
    for i in range(len(results["ids"][0])):
        matches.append({
            "id": results["ids"][0][i],
            "file_name": results["metadatas"][0][i]["file_name"],
            "section": results["metadatas"][0][i]["section"],
            "text": results["documents"][0][i],
            "distance": results["distances"][0][i]
        })
    return matches


if __name__ == "__main__":
    print("=== Indexing all resumes ===")
    index_all_resumes()

    print(f"\nTotal chunks in collection: {collection.count()}")

    print("\n=== Test search ===")
    test_query = "Looking for a backend engineer with Python and AWS experience"
    results = search(test_query, top_k=5)

    print(f"Query: {test_query}\n")
    for r in results:
        print(f"[{r['file_name']} - {r['section']}] (distance: {r['distance']:.4f})")
        print(f"  {r['text'][:150]}...\n")