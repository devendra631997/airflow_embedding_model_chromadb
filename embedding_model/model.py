# embedding_model/model.py

from sentence_transformers import SentenceTransformer
import os

# Load pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embeddings_from_text(file_path):
    with open(file_path, 'r') as f:
        text = f.read()
    embeddings = model.encode([text])
    return embeddings
