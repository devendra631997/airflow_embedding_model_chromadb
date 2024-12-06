# dags/process_files.py

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# from scripts.detect_new_files import watch_for_new_files
# from scripts.generate_embeddings import store_embeddings_in_chroma
from datetime import datetime


# embedding_model/model.py

from sentence_transformers import SentenceTransformer

import chromadb

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

class NewFileHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback

    def on_created(self, event):
        if not event.is_directory:
            print(f"New file detected: {event.src_path}")
            self.callback(event.src_path)

def watch_for_new_files(folder, callback):
    event_handler = NewFileHandler(callback)
    observer = Observer()
    observer.schedule(event_handler, folder, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()



# Load pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embeddings_from_text(file_path):
    with open(file_path, 'r') as f:
        text = f.read()
    embeddings = model.encode([text])
    return embeddings


def store_embeddings_in_chroma(file_path):
    embeddings = generate_embeddings_from_text(file_path)
    client = chromadb.Client()
    collection = client.get_or_create_collection("file_embeddings")
    
    # Store the embedding along with the file name
    collection.add(
        documents=[file_path],
        embeddings=embeddings
    )


def process_new_file(file_path):
    store_embeddings_in_chroma(file_path)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 12, 7),
}

dag = DAG(
    'process_files_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
)

def dag_test():
    print('dag ran')

# Airflow task to detect new files and process them
detect_files_task = PythonOperator(
    task_id='detect_new_files',
    # python_callable=dag_test,
    python_callable=watch_for_new_files,
    op_args=["/path/to/input_files", process_new_file],
    dag=dag,
)
