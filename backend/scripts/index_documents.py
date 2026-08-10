import os
import sys

# Ensure backend root is added to python import paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.document import Document

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()


def index_all_documents():
    db: Session = SessionLocal()
    try:
        # Fetch parsed documents from PostgreSQL
        documents = db.query(Document).filter(Document.status == "parsed").all()

        if not documents:
            print("⚠️ No parsed documents found in the database with status 'parsed'.")
            return

        print(f"1. Found {len(documents)} parsed document(s) in DB.")

        # Initialize embedding model and text splitter
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

        total_chunks = 0
        for doc in documents:
            if not doc.parsed_text:
                continue

            # Split text into chunks
            chunks = text_splitter.split_text(doc.parsed_text)
            metadatas = [
                {"document_id": doc.id, "filename": doc.filename, "chunk_index": idx}
                for idx in range(len(chunks))
            ]

            # Upsert into Pinecone
            PineconeVectorStore.from_texts(
                texts=chunks,
                embedding=embeddings,
                metadatas=metadatas,
                index_name=os.getenv("PINECONE_INDEX", "ai-ticket-platform"),
            )

            total_chunks += len(chunks)
            print(
                f"  └─ Indexed document '{doc.filename}' (ID: {doc.id}) -> {len(chunks)} chunks"
            )

        print(
            f"✅ Finished! Successfully indexed {total_chunks} total chunks into Pinecone."
        )

    except Exception as e:
        print(f"❌ Indexing failed: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    index_all_documents()
