import json
import ollama
from vector_store import collection, embed_text

LLM_MODEL = "qwen2.5:3b-instruct"


def get_all_candidates():
    """Get the list of unique candidate file_names currently indexed."""
    all_data = collection.get()
    file_names = set()
    for meta in all_data["metadatas"]:
        file_names.add(meta["file_name"])
    return sorted(file_names)


def get_candidate_context(jd_text, file_name, top_k=4):
    """
    Retrieve the most relevant sections for ONE specific candidate,
    ranked by relevance to the job description.
    """
    jd_embedding = embed_text(jd_text)

    results = collection.query(
        query_embeddings=[jd_embedding],
        n_results=top_k,
        where={"file_name": file_name}  # restrict search to this candidate only
    )

    chunks = []
    for i in range(len(results["ids"][0])):
        section = results["metadatas"][0][i]["section"]
        text = results["documents"][0][i]
        chunks.append(f"[{section.upper()}]\n{text}")

    return "\n\n".join(chunks)


def build_prompt(jd_text, candidate_context, file_name):
    return f"""You are an expert technical recruiter. Evaluate how well this candidate matches the job description below, using ONLY the resume excerpts provided.

JOB DESCRIPTION:
{jd_text}

CANDIDATE RESUME EXCERPTS ({file_name}):
{candidate_context}

Respond with ONLY a valid JSON object, no other text, no markdown formatting, in this exact structure:
{{
  "match_score": <integer 0-100>,
  "verdict": "<one of: Strong Match, Possible Match, Weak Match>",
  "strengths": ["<short phrase>", "<short phrase>", "<short phrase>"],
  "gaps": ["<short phrase>", "<short phrase>"]
}}

Base match_score on how well the candidate's actual skills and experience align with the job requirements. Be honest and critical - do not inflate scores."""


def score_candidate(jd_text, file_name):
    """Get a structured RAG-based evaluation for one candidate against a JD."""
    context = get_candidate_context(jd_text, file_name)
    prompt = build_prompt(jd_text, context, file_name)

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.2}  # lower temperature = more consistent scoring
    )

    raw_output = response["message"]["content"].strip()

    # Clean up in case the model wraps output in markdown code fences anyway
    if raw_output.startswith("```"):
        raw_output = raw_output.strip("`")
        if raw_output.startswith("json"):
            raw_output = raw_output[4:]
        raw_output = raw_output.strip()

    try:
        parsed = json.loads(raw_output)
    except json.JSONDecodeError:
        parsed = {
            "match_score": None,
            "verdict": "Error",
            "strengths": [],
            "gaps": [],
            "raw_error_output": raw_output
        }

    parsed["file_name"] = file_name
    return parsed


def screen_all_candidates(jd_text):
    """Score every indexed candidate against the JD, ranked by match_score."""
    candidates = get_all_candidates()
    results = []

    for file_name in candidates:
        print(f"Scoring {file_name}...")
        result = score_candidate(jd_text, file_name)
        results.append(result)

    # Sort by match_score descending, putting errors/None at the bottom
    results.sort(key=lambda x: x["match_score"] if x["match_score"] is not None else -1, reverse=True)
    return results


if __name__ == "__main__":
    sample_jd = """
We are hiring a Backend Software Engineer with 2+ years of experience.
Required: strong Python skills, experience with REST API frameworks (FastAPI or Django),
familiarity with cloud platforms (AWS preferred), and containerization (Docker).
Nice to have: CI/CD experience, PostgreSQL, unit testing practices.
"""

    print("=== Screening all candidates ===\n")
    ranked_results = screen_all_candidates(sample_jd)

    print("\n\n=== RANKED RESULTS ===\n")
    for i, r in enumerate(ranked_results, 1):
        print(f"{i}. {r['file_name']}")
        print(f"   Score: {r['match_score']}  |  Verdict: {r['verdict']}")
        print(f"   Strengths: {r['strengths']}")
        print(f"   Gaps: {r['gaps']}")
        print()