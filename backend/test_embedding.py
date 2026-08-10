from sentence_transformers import SentenceTransformer

print("Loading model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model loaded!")

text = "How do I reset my VPN password?"

embedding = model.encode(text)

print("Embedding length:", len(embedding))
print(embedding[:10])  # first 10 values
