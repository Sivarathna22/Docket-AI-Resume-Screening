import pdfplumber
import re
import os

def extract_text_from_pdf(pdf_path):
    """Extract raw text from a PDF resume."""
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
    return full_text


def chunk_by_sections(text):
    """
    Split resume text into logical sections based on common resume headers.
    Returns a dict: {section_name: section_text}
    """
    # Common resume section headers (expand this list as you test more resumes)
    section_headers = [
        "experience", "work experience", "professional experience",
        "education", "skills", "technical skills", "projects",
        "certifications", "achievements", "summary", "objective",
        "publications", "extracurricular", "internships"
    ]

    lines = text.split("\n")
    sections = {}
    current_section = "header"  # catches name/contact info at the top
    sections[current_section] = []

    for line in lines:
        clean_line = line.strip().lower()
        matched_header = None

        # Check if this line looks like a section header
        for header in section_headers:
            if clean_line == header or clean_line.startswith(header):
                matched_header = header
                break

        if matched_header:
            current_section = matched_header
            sections[current_section] = []
        else:
            sections[current_section].append(line)

    # Join lines back into text per section
    return {sec: "\n".join(lines).strip() for sec, lines in sections.items() if "\n".join(lines).strip()}


def extract_candidate_name(raw_text):
    """
    Best-effort extraction of the candidate's name: assume it's the first
    non-empty line of the resume (true for the vast majority of resumes,
    since names are almost always at the very top).
    """
    for line in raw_text.split("\n"):
        clean = line.strip()
        if clean:
            return clean
    return "Unknown Candidate"


def parse_resume(pdf_path):
    """Full pipeline: PDF -> raw text -> sectioned chunks -> candidate name."""
    raw_text = extract_text_from_pdf(pdf_path)
    sections = chunk_by_sections(raw_text)
    candidate_name = extract_candidate_name(raw_text)
    return {
        "file_name": os.path.basename(pdf_path),
        "candidate_name": candidate_name,
        "raw_text": raw_text,
        "sections": sections
    }


if __name__ == "__main__":
    resumes_folder = "data/resumes"
    for file_name in os.listdir(resumes_folder):
        if file_name.lower().endswith(".pdf"):
            path = os.path.join(resumes_folder, file_name)
            result = parse_resume(path)
            print(f"\n{'='*50}")
            print(f"FILE: {result['file_name']}")
            print(f"{'='*50}")
            for section, content in result["sections"].items():
                print(f"\n--- {section.upper()} ---")
                print(content[:200] + ("..." if len(content) > 200 else ""))