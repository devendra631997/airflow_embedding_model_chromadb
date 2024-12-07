
import chromadb
from chromadb.config import Settings
# class ChromaDB:
#     def __init__(self):
#         self.client = chromadb.Client()
#
#
#     def create_collection_in_chroma(self, collection_name:str):
#         collection = self.client.create_collection(name=collection_name)
#     def inserting_document_embeddings_in_chroma(self, collection_name:str, documents:str=None, metadatas:dict=None, embeddings=None):
#         collection = self.client.get_or_create_collection(name=collection_name)
#         # Example: Inserting document embeddings
#         collection.add(
#             documents=[documents],
#             metadatas=[metadatas],
#             embeddings=[embeddings]  # Your generated embeddings here
#         )


def store_embeddings_in_chroma(file_path=None, embeddings=None, ids=None):
    client = chromadb.Client()
    collection = client.get_or_create_collection("file_embeddings")

    # Store the embedding along with the file name
    collection.add(
        ids=ids,
        # documents=[file_path],
        embeddings=embeddings
    )
