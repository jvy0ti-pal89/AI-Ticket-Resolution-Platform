from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/ai", tags=["AI"])


class AIQuery(BaseModel):
    question: str


@router.post("/query")
def query_ai(query: AIQuery):
    return {
        "answer": "AI query pipeline placeholder. Implement app.ai.llm and retriever logic here."
    }
