
import chromadb
def store_embeddings_in_chroma(file_path=None, embeddings=None):
    client = chromadb.Client()
    collection = client.get_or_create_collection("file_embeddings")
    
    # Store the embedding along with the file name
    collection.add(
        documents=[file_path],
        embeddings=embeddings
    )
