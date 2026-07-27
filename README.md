# 🚀 Docket — AI Resume Screening with RAG using Local LLMs via Ollama

An AI-powered resume screening system that uses **Retrieval-Augmented Generation (RAG)** to evaluate candidates against a job description, explain its reasoning, and allow recruiters to ask free-form questions across the entire candidate pool — all running completely offline using free local Large Language Models (LLMs) served through **Ollama**.

---

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green?logo=fastapi)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react)
![Vite](https://img.shields.io/badge/Vite-Build-purple?logo=vite)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-black)
![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-orange)

# 📖 Project Overview

Traditional Applicant Tracking Systems (ATS) usually rely on keyword matching or a pre-trained classifier that simply predicts whether a candidate should be shortlisted. These systems often provide little or no explanation behind their decisions.

**Docket** takes a completely different approach.

Instead of relying on fixed rules, it retrieves the most relevant sections from every candidate's resume using semantic search and asks a **local Large Language Model (LLM)** to reason over that evidence. The model then produces:

- Candidate Match Score
- Strong / Possible / Weak Match
- Candidate Strengths
- Missing Skills
- Explanation for the decision

Since every decision is grounded in the actual resume content retrieved from the vector database, the system provides transparent and explainable AI-powered recruitment assistance.

Unlike cloud AI services, the entire pipeline runs **locally using Ollama**, ensuring complete privacy, zero API cost, and offline functionality.

---

## 📑 Table of Contents

- [Project Overview](#-project-overview)
- [Features](#-features)
- [System Architecture](#-system-architecture)
- [How the System Works](#️-how-the-system-works)
- [Technology Stack](#-technology-stack)
- [APIs Used](#-apis-used)
- [Project Structure](#-project-structure)
- [System Requirements](#-system-requirements)
- [Installation Guide](#-installation-guide)
- [Running the Project](#️-running-the-project)
- [Backend API Endpoints](#-backend-api-endpoints)
- [Future Enhancements](#-future-enhancements)
- [Known Limitations](#-known-limitations)


# ✨ Features

- 📄 Upload multiple Resume PDFs
- 📑 Automatic Resume Parsing
- 👤 Candidate Information Extraction
- 🛠 Skill Extraction
- 📚 Resume Section Chunking
- 🔍 Semantic Resume Search using ChromaDB
- 🤖 RAG-based Candidate Scoring
- 📊 Candidate Ranking Dashboard
- 💬 Chat with Candidate Database
- ⚡ Local AI using Ollama
- 🔒 Fully Offline (No API Keys Required)

---

# 🏗 System Architecture

```text
                   React Frontend
                          │
                          ▼
                  FastAPI Backend
                          │
      ┌───────────────────┼───────────────────┐
      ▼                   ▼                   ▼
 Resume Parser      Vector Database      Chat Engine
      │                   │                   │
      ▼                   ▼                   ▼
 Resume Sections      ChromaDB          Ollama LLM
                          │
                          ▼
              Candidate Screening & Ranking
```

---

# ⚙️ How the System Works

```text
Resume PDF
     │
     ▼
PDF Parsing
     │
     ▼
Extract Candidate Information
     │
     ▼
Split Resume into Sections
     │
     ▼
Generate Embeddings
     │
     ▼
Store in ChromaDB
     │
     ▼
Job Description Input
     │
     ▼
Semantic Retrieval
     │
     ▼
LLM Reasoning (Qwen2.5)
     │
     ▼
Candidate Score
     │
     ▼
Dashboard + Chat Interface
```

---

# 🛠 Technology Stack

| Category | Technology |
|----------|------------|
| Frontend | React + Vite |
| Backend | FastAPI |
| Programming Language | Python |
| LLM Runtime | Ollama |
| Reasoning Model | Qwen2.5 3B Instruct |
| Embedding Model | nomic-embed-text |
| Vector Database | ChromaDB |
| Resume Parser | pdfplumber |
| HTTP Client | Axios |
| Styling | CSS |

---

# 📡 APIs Used

This project **does not use any paid cloud AI API**.

All AI inference is performed locally through **Ollama**, which exposes an OpenAI-compatible local API.

| Component | Model | Purpose |
|-----------|-------|----------|
| LLM | qwen2.5:3b-instruct | Candidate scoring & reasoning |
| Embeddings | nomic-embed-text | Semantic vector generation |

---

## 📂 Project Structure

```text
Resume-Screening/
│
├── backend/
│   ├── data/
│   │   ├── chroma_db/          # Persistent vector database
│   │   └── resumes/            # Uploaded resume PDFs
│   │
│   ├── venv/                   # Python virtual environment (ignored by Git)
│   │
│   ├── chat_rag.py             # Chat with candidate database
│   ├── main.py                 # FastAPI backend and API endpoints
│   ├── rag_scorer.py           # RAG-based candidate scoring
│   ├── resume_parser.py        # Resume parsing and section extraction
│   ├── test_ollama.py          # Ollama connection testing
│   └── vector_store.py         # ChromaDB indexing & semantic retrieval
│
├── frontend/
│   ├── public/
│   │   ├── favicon.svg
│   │   └── icons.svg
│   │
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   │   ├── CandidateCard.jsx
│   │   │   ├── ChatPanel.jsx
│   │   │   └── IntakePanel.jsx
│   │   │
│   │   ├── api.js
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.js
│   └── index.html
│
├── ollama_models/              # Local LLM models (ignored by Git)
├── .gitignore
└── README.md
```

---

# 💻 System Requirements

- Python 3.10+
- Node.js 18+
- npm
- Git
- Ollama
- 4 GB RAM (Minimum)
- Windows / Linux / macOS

---

# 📥 Installation Guide

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/AI-Resume-Screening-System.git

cd AI-Resume-Screening-System
```

---

## 2️⃣ Install Ollama

Download and install Ollama from:

https://ollama.com/download

---

## 3️⃣ Download Required Models

```bash
ollama pull qwen2.5:3b-instruct

ollama pull nomic-embed-text
```

---

## 4️⃣ Backend Setup

```bash
cd backend

python -m venv venv
```

### Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## 5️⃣ Frontend Setup

```bash
cd ../frontend

npm install
```

---

# ▶️ Running the Project

You need **three terminals**.

---

### Terminal 1

Run Ollama

```bash
ollama serve
```

---

### Terminal 2

Backend

```bash
cd backend

venv\Scripts\activate

uvicorn main:app --reload
```

Runs on

```
http://127.0.0.1:8000
```

Swagger API Documentation

```
http://127.0.0.1:8000/docs
```

---

### Terminal 3

Frontend

```bash
cd frontend

npm run dev
```

Runs on

```
http://localhost:5173
```

---

Open

```
http://localhost:5173
```

Upload resumes, enter a Job Description, and click **Screen Candidates**.

---

# 📡 Backend API Endpoints

| Endpoint | Method | Description |
|----------|--------|------------|
| `/upload-resumes` | POST | Upload Resume PDFs |
| `/screen` | POST | Screen Candidates |
| `/chat` | POST | Ask Questions to AI |
| `/candidates` | GET | View Candidate List |
| `/candidates/{file_name}` | DELETE | Delete Candidate |


# 🔮 Future Enhancements

- User Authentication
- HR Dashboard
- Multiple Company Support
- Candidate Experience Extraction
- Education & CGPA Analysis
- Interview Recommendation Engine
- Email Notification System
- Resume Summarization
- Explainable AI Dashboard
- Docker Deployment
- Cloud Deployment

---

# ⚠ Known Limitations

- Resume parsing depends on text-based PDFs and may struggle with scanned resumes or complex multi-column layouts.
- Small local LLMs (3B parameters) provide efficient offline inference but may not capture every nuanced hiring decision compared to larger models.
- Comparative reasoning across multiple candidates is limited during chat mode; the primary ranking interface should be used for side-by-side evaluation.

---
