from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import tickets, upload, auth, users, dashboard, ai, documents
from app.database import engine, Base
import app.models

Base.metadata.create_all(bind=engine)
app = FastAPI(title="AI Ticket Resolution Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],  # Allows all origins during development
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to AI Ticket Resolution Platform API",
        "docs": "/docs",
        "status": "healthy",
    }


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tickets.router)
app.include_router(upload.router)
app.include_router(documents.router)
app.include_router(dashboard.router)
app.include_router(ai.router)
