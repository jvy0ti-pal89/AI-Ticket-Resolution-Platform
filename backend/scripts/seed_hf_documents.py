import os
import sys

# Ensure backend root is in Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
from sqlalchemy.orm import Session
from datasets import load_dataset

from app.database import SessionLocal
from app.models.document import Document
from app.services.parser_service import ParserService

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()


def seed_hf_documents():
    db: Session = SessionLocal()
    parser = ParserService()
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    print("1. Fetching dataset from Hugging Face...")
    try:
        # Example using a standard public IT support/ticket dataset
        dataset = load_dataset(
            "Amod/mental_health_counseling_conversations", split="train[:10]"
        )
        # Note: Replace dataset name with your specific IT/ticket dataset if needed
    except Exception as e:
        print(f"Failed to load dataset: {e}")
        return

    print(f"2. Ingesting {len(dataset)} documents into backend...")

    for idx, item in enumerate(dataset):
        # Build text sample from dataset fields
        text_content = f"Title: Sample Ticket #{idx+1}\nDescription: {item.get('Context', item.get('text', ''))}"
        filename = f"hf_ticket_{idx+1}.txt"
        filepath = os.path.join(upload_dir, filename)

        # Write sample file to uploads/
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(text_content)

        # Store record in PostgreSQL
        doc = Document(
            filename=filename,
            filepath=filepath,
            parsed_text=text_content,
            status="parsed",
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)

        # Split text into chunks & upsert to Pinecone
        chunks = text_splitter.split_text(text_content)
        metadatas = [
            {"document_id": doc.id, "filename": doc.filename, "chunk_index": c_idx}
            for c_idx in range(len(chunks))
        ]

        PineconeVectorStore.from_texts(
            texts=chunks,
            embedding=embeddings,
            metadatas=metadatas,
            index_name=os.getenv("PINECONE_INDEX", "ai-ticket-platform"),
        )

        print(
            f"  └─ Ingested & indexed '{filename}' (DB ID: {doc.id}, {len(chunks)} chunks)"
        )

    print("✅ Seeding completed successfully!")
    db.close()


if __name__ == "__main__":
    seed_hf_documents()
