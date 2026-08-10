# AI Ticket Resolution Platform

An AI-assisted enterprise ticketing platform that combines automated ticket classification, document retrieval, grounded LLM resolution generation, and a human review workflow.

This release supports:
- ticket creation and AI enrichment
- RAG-powered suggested resolutions
- PENDING_REVIEW handoff to engineers
- approve / edit / escalate review actions
- dashboard metrics built around the actual workflow

---

## Workflow Summary

1. An employee creates a support ticket.
2. AI classifies category and priority.
3. The ticket is embedded and Pinecone is queried for relevant documentation.
4. A Groq-powered LLM generates a grounded resolution suggestion.
5. The ticket is marked `PENDING_REVIEW`.
6. An engineer reviews the recommendation.
7. The engineer can approve, edit, or escalate.
8. Final status becomes `RESOLVED` or `ESCALATED`.

---

## Ticket Data Model

Each ticket includes:
- `id`
- `title`
- `description`
- `category`
- `priority`
- `summary`
- `resolution`
- `status`
- `reviewed_by_id`
- `reviewed_at`
- `escalation_reason`

Ticket statuses:
- `OPEN`
- `PENDING_REVIEW`
- `RESOLVED`
- `ESCALATED`

---

## Key Features

### AI Ticket Enrichment

- AI classification of category, priority, and summary
- Retrieval-Augmented Generation for grounded resolutions
- Human-in-the-loop review before final ticket resolution
- Escalation workflow with escalation reason tracking

### Review Actions

Support engineers can:
- approve the AI-generated resolution
- edit the resolution and approve it
- escalate the ticket for further investigation

### Dashboard Metrics

The dashboard tracks:
- total tickets
- open tickets
- pending review tickets
- resolved tickets
- escalated tickets
- high-priority tickets
- category breakdown
- recent tickets
- high-priority ticket list

---

## RAG Pipeline

The platform uses Retrieval-Augmented Generation to ground AI suggestions in company documents.

- Ticket text → Sentence Transformer embedding
- Pinecone similarity search returns relevant chunks
- Groq LLM receives context and generates a grounded resolution

### Document processing

Uploaded documents are processed through:
- Docling for parsing
- text cleanup and chunking
- Sentence Transformer embeddings
- Pinecone indexing

Current embedding model:
- `all-MiniLM-L6-v2`

Embedding dimension:
- `384`

---

## System Architecture

Frontend:
- React
- TypeScript
- Vite
- JWT authentication
- Role-based access control

Backend:
- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL
- Pinecone
- Groq
- Sentence Transformers
- Docling

---

## API Endpoints

### Tickets
- `POST /tickets` — create ticket
- `GET /tickets` — list tickets
- `GET /tickets/{ticket_id}` — get ticket details
- `PUT /tickets/{ticket_id}` — update ticket
- `POST /tickets/{ticket_id}/review` — approve/edit/escalate ticket review

### Dashboard
- `GET /dashboard/metrics` — fetch dashboard KPIs and recent tickets

---

## Environment

Example `.env` values:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ai_ticket_db
JWT_SECRET_KEY=supersecret
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRES_MINUTES=60
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENVIRONMENT=your_pinecone_env
PINECONE_INDEX_NAME=ai-ticket-platform
GROQ_API_KEY=your_groq_key
GROQ_ENDPOINT=https://api.groq.ai/v1
```

---

## Run Locally

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Notes

- `resolution` stores the AI-generated suggestion and any engineer-edited final text.
- The workflow is intentionally human-in-the-loop, with review states and engineer actions.
- Dashboard metrics reflect the active review pipeline.
