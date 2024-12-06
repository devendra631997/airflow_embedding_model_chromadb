# scripts/generate_embeddings.py

import chromadb
from embedding_model.model import generate_embeddings_from_text

def store_embeddings_in_chroma(file_path):
    embeddings = generate_embeddings_from_text(file_path)
    client = chromadb.Client()
    collection = client.get_or_create_collection("file_embeddings")
    
    # Store the embedding along with the file name
    collection.add(
        documents=[file_path],
        embeddings=embeddings
    )
