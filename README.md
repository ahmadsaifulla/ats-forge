# ATS Forge

ATS Forge is a production-oriented ATS resume optimizer built with FastAPI, React, Tailwind CSS, spaCy, sentence-transformers, and scikit-learn.

It accepts PDF or DOCX resumes, analyzes them against a target job description, scores ATS alignment across keyword, semantic, and structural signals, and generates a cleaner ATS-friendly version for download.

## Description

ATS Forge helps candidates turn a generic resume into a role-targeted, ATS-readable submission without inventing experience. The system combines resume parsing, weighted ATS scoring, evidence-aware resume optimization, and downloadable output in a modular full-stack architecture designed for real deployment rather than demo-only usage.

## Highlights

- FastAPI backend with clean service and parsing layers
- React + Vite frontend with upload, analysis, and optimized resume flows
- ATS scoring using keyword match, semantic similarity, and structure checks
- Evidence-aware optimization that avoids unsupported claim generation
- Deployment-ready setup for Vercel, Render, or Railway

## Architecture

```text
backend/
  app/
    api/        FastAPI routes and dependency wiring
    core/       settings and logging
    models/     Pydantic schemas
    nlp/        ATS scoring and lazy model loading
    parsers/    PDF/DOCX parsing
    services/   workflow, optimization, storage
    utils/      text normalization and error types
  tests/        unit and integration coverage

frontend/
  src/
    components/ UI building blocks
    pages/      Upload, analysis, optimized resume views
    services/   API access layer
    lib/        local persistence helpers
    types/      API type contracts
```

## Features

- Upload PDF and DOCX resumes with file-size validation
- Parse clean resume text and extract resume sections
- Score ATS fit with keyword, semantic, and structural signals
- Highlight matched and missing keywords
- Generate an ATS-friendly optimized resume without inventing experience
- Download the optimized resume as DOCX
- Handle scanned PDFs, empty files, short job descriptions, and oversized uploads

## Backend Setup

1. Use Python `3.11.x` or `3.12.x` for local development. Python `3.14` is not recommended yet because parts of the FastAPI and NLP dependency chain still lag behind that runtime.
2. Create a virtual environment.
3. Install dependencies:

```bash
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

4. Copy the environment template and adjust values if needed:

```bash
cp .env.example .env
```

5. Run the API:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API endpoints:

- `POST /api/upload-resume`
- `POST /api/analyze`
- `POST /api/optimize`
- `GET /api/download/{document_id}`
- `GET /health`

## Frontend Setup

1. Install Node.js 20+ dependencies:

```bash
cd frontend
npm install
```

2. Copy the environment template:

```bash
cp .env.example .env
```

3. Start the Vite development server:

```bash
npm run dev
```

The frontend expects the backend at `http://localhost:8000/api` by default.

## Testing

Run backend tests:

```bash
cd backend
pytest
```

Example coverage areas:

- Resume section extraction and normalization
- Keyword and structure scoring
- Optimizer behavior
- Upload/analyze/optimize/download API flow
- Edge cases for empty files, huge files, and invalid job descriptions

## Docker Deployment

Build and run the backend container:

```bash
cd backend
docker build -t ats-forge-api .
docker run -p 8000:8000 ats-forge-api
```

## Vercel + Render/Railway Deployment

### Frontend on Vercel

- Import the `frontend` directory as a Vercel project.
- Set `VITE_API_BASE_URL` to your deployed backend URL plus `/api`.
- Vercel SPA rewrites are configured in [`frontend/vercel.json`](/Users/mc/Desktop/Work/Portfolio Projects/ats-forge/frontend/vercel.json).

### Backend on Render

- Render can deploy directly from [`render.yaml`](/Users/mc/Desktop/Work/Portfolio Projects/ats-forge/render.yaml) or from the `backend` directory using the Dockerfile.
- Set environment values from [`backend/.env.example`](/Users/mc/Desktop/Work/Portfolio Projects/ats-forge/backend/.env.example).
- Keep persistent storage for `backend/storage` if you want generated files to survive restarts.

### Backend on Railway

- Deploy the `backend` directory as a Docker service.
- Expose port `8000`.
- Configure CORS origins to include the Vercel frontend URL.

## Notes for Production Hardening

- Swap the in-memory repository for Redis or PostgreSQL when multi-instance persistence is needed.
- Persist upload history and optimization sessions in a database for auditability.
- Add background jobs for large-document processing if throughput grows.
- Consider OCR integration for scanned PDFs in a later phase.
