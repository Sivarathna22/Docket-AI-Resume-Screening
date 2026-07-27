import ollama
from vector_store import collection, embed_text
from rag_scorer import get_all_candidates

LLM_MODEL = "qwen2.5:3b-instruct"
NO_MATCH_TOKEN = "NO_MATCH"


def get_candidate_name(file_name):
    """Look up a candidate's real name from any of their indexed chunks."""
    results = collection.get(where={"file_name": file_name}, limit=1)
    if results["metadatas"]:
        return results["metadatas"][0].get("candidate_name", file_name)
    return file_name


def retrieve_for_one_candidate(query_embedding, file_name, per_candidate_k=3):
    """Retrieve just this one candidate's most relevant chunks for the query."""
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=per_candidate_k,
        where={"file_name": file_name}
    )
    chunks = []
    for i in range(len(results["ids"][0])):
        chunks.append({
            "section": results["metadatas"][0][i]["section"],
            "text": results["documents"][0][i],
        })
    return chunks


def build_isolated_prompt(question, candidate_name, chunks):
    context_text = "\n\n".join(
        f"[{c['section'].upper()}]\n{c['text']}" for c in chunks
    )

    return f"""You are evaluating ONE candidate's resume against a recruiter's question.
Base your answer ONLY on the excerpts below for this candidate. Do not mention any other candidates.

CANDIDATE: {candidate_name}

RESUME EXCERPTS:
{context_text}

QUESTION: {question}

Respond with exactly ONE short sentence stating this candidate's relevant finding.
If nothing in these excerpts is relevant to the question, respond with exactly: {NO_MATCH_TOKEN}"""


def evaluate_candidate(question, file_name, candidate_name, per_candidate_k=3):
    """Evaluate a single candidate in isolation - no other candidates in context at all."""
    query_embedding = embed_text(question)
    chunks = retrieve_for_one_candidate(query_embedding, file_name, per_candidate_k)

    if not chunks:
        return None

    prompt = build_isolated_prompt(question, candidate_name, chunks)

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.1}
    )

    finding = response["message"]["content"].strip()

    if NO_MATCH_TOKEN in finding.upper():
        return None

    return finding


def chat_query(question, per_candidate_k=3):
    """
    Full RAG chat pipeline: evaluate every candidate INDEPENDENTLY against the
    question (no cross-candidate context), then assemble the final answer
    ourselves in Python - guaranteeing correct name-to-finding attribution.
    """
    all_candidates = get_all_candidates()

    if not all_candidates:
        return {
            "answer": "No candidates are indexed yet. Upload some resumes first.",
            "sources": []
        }

    findings = []
    sources = []

    for file_name in all_candidates:
        candidate_name = get_candidate_name(file_name)
        finding = evaluate_candidate(question, file_name, candidate_name, per_candidate_k)
        if finding:
            findings.append(f"- {candidate_name}: {finding}")
            sources.append({"file_name": file_name, "candidate_name": candidate_name})

    if not findings:
        answer = "None of the candidates on file appear to match this criteria based on their resumes."
    else:
        answer = "\n".join(findings)

    return {"answer": answer, "sources": sources}


if __name__ == "__main__":
    test_questions = [
        "Which candidates have experience with cloud platforms like AWS?",
        "Who has managed a team before?",
        "Does anyone have experience with Docker or containerization?",
    ]

    for q in test_questions:
        print(f"\nQ: {q}")
        result = chat_query(q)
        print(f"A:\n{result['answer']}")
        print(f"Sources: {[s['candidate_name'] for s in result['sources']]}")