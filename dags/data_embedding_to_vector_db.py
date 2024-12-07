from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from embedding_model.bert_model import get_bert_embeddings
from scripts.store_embeddings_in_chromadb import store_embeddings_in_chroma
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 12, 6),
}

dag = DAG(
    'data_embedding_to_vector_db',
    default_args=default_args,
)


def read_file(file_path):
    try:
        with open(file_path, 'r') as f:
            text = f.read()
        return text, file_path
    except Exception as e:
        # Code to handle the exception
        print(f"An error occurred: {e}")
        return None, None

def dag_job():
    print("sannd debugger")
    texts, file_path = read_file("data/input_files/data.txt")
    # texts = ["Hello, how are you?", "BERT is a powerful model for NLP."]
    print(f"texts={texts}, file_path={file_path}")
    ids, embeddings = get_bert_embeddings(texts)
    print(f"Embedding for sentence {embeddings}")
    store_embeddings_in_chroma(file_path=file_path, embeddings=embeddings, ids=ids)

# Airflow task to detect new files and process them
detect_files_task = PythonOperator(
    task_id='file_to_vector_chroma_db',
    python_callable=dag_job,
    dag=dag,
)
