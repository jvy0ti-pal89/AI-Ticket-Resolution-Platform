import os
import sys

# Ensure parent directory is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datasets import load_dataset
from app.database import SessionLocal
from app.models.document import Document

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def seed_from_huggingface():
    print("Fetching dataset from Hugging Face...")
    dataset = load_dataset("squad", split="train[:10]")

    db = SessionLocal()
    count = 0

    try:
        for idx, item in enumerate(dataset):
            title_slug = item["title"].replace(" ", "_").lower()
            filename = f"hf_{title_slug}_{idx + 1}.txt"
            filepath = os.path.join(UPLOAD_DIR, filename)

            content = (
                f"Title: {item['title']}\n\nDocumentation Context:\n{item['context']}"
            )
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

            existing = db.query(Document).filter(Document.filename == filename).first()
            if not existing:
                doc = Document(
                    filename=filename,
                    filepath=filepath,
                    uploaded_by_id=None,
                )
                db.add(doc)
                count += 1

        db.commit()
        print(
            f"✅ Successfully seeded {count} Hugging Face documents into '{UPLOAD_DIR}/' and PostgreSQL!"
        )

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding documents: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_from_huggingface()
