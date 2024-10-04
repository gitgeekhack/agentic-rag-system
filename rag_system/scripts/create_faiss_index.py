import pickle
from app.embeddings import create_embeddings

# File paths
chunks_path = 'models/text_chunks.pkl'
index_path = 'models'

# Load the text chunks
print(f"Loading text chunks from {chunks_path}...")
with open(chunks_path, 'rb') as f:
    text_chunks = pickle.load(f)

# Generate embeddings for the text chunks
print("Generating embeddings...")
embeddings = create_embeddings(text_chunks)

# Save the FAISS index
embeddings.save_local(index_path, index_name='faiss_index')

print(f"FAISS index saved to {index_path}")
