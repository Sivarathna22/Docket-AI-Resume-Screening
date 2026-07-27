import os
import shutil
from chat_rag import chat_query
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from resume_parser import parse_resume
from vector_store import index_resume, collection
from rag_scorer import get_all_candidates, screen_all_candidates

app = FastAPI(title="AI Resume Screening API")

# Allow the React frontend (running on a different port) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Vite's default dev port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

RESUMES_FOLDER = "data/resumes"
os.makedirs(RESUMES_FOLDER, exist_ok=True)


class ScreenRequest(BaseModel):
    job_description: str

class ChatRequest(BaseModel):
    question: str

@app.post("/chat")
def chat_with_candidates(request: ChatRequest):
    """
    Ask a free-form question across the entire candidate pool.
    Returns an answer grounded in retrieved resume excerpts, plus sources.
    """
    if not get_all_candidates():
        raise HTTPException(status_code=400, detail="No candidates indexed yet. Upload resumes first.")

    result = chat_query(request.question)
    return result

@app.get("/")
def root():
    return {"status": "AI Resume Screening API is running"}


@app.post("/upload-resumes")
async def upload_resumes(files: list[UploadFile] = File(...)):
    """
    Upload one or more resume PDFs. Each is saved to disk, parsed,
    and indexed into ChromaDB automatically.
    """
    uploaded = []
    errors = []

    for file in files:
        if not file.filename.lower().endswith(".pdf"):
            errors.append({"file": file.filename, "error": "Only PDF files are supported"})
            continue

        save_path = os.path.join(RESUMES_FOLDER, file.filename)

        try:
            # Save file to disk
            with open(save_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # Parse + index immediately
            index_resume(save_path)
            uploaded.append(file.filename)

        except Exception as e:
            errors.append({"file": file.filename, "error": str(e)})

    return {
        "uploaded": uploaded,
        "errors": errors,
        "total_indexed_chunks": collection.count()
    }


@app.get("/candidates")
def list_candidates():
    """List all currently indexed candidates."""
    candidates = get_all_candidates()
    return {"candidates": candidates, "count": len(candidates)}


@app.post("/screen")
def screen_candidates(request: ScreenRequest):
    """
    Score every indexed candidate against the given job description,
    returning ranked results with match_score, verdict, strengths, gaps.
    """
    candidates = get_all_candidates()
    if not candidates:
        raise HTTPException(status_code=400, detail="No candidates indexed yet. Upload resumes first.")

    results = screen_all_candidates(request.job_description)
    return {"results": results}


@app.delete("/candidates/{file_name}")
def delete_candidate(file_name: str):
    """Remove a candidate's chunks from the vector store and delete their file."""
    all_data = collection.get()
    ids_to_delete = [
        id_ for id_, meta in zip(all_data["ids"], all_data["metadatas"])
        if meta["file_name"] == file_name
    ]

    if not ids_to_delete:
        raise HTTPException(status_code=404, detail="Candidate not found")

    collection.delete(ids=ids_to_delete)

    file_path = os.path.join(RESUMES_FOLDER, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)

    return {"deleted": file_name, "chunks_removed": len(ids_to_delete)}