from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from embedding_model.bert_model import get_bert_embeddings
from scripts.store_embeddings_in_chromadb import store_embeddings_in_chroma
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 12, 9),
}

dag = DAG(
    'data_embedding_to_vector_db',
    default_args=default_args,
)

def dag_test():
    texts = ["Hello, how are you?", "BERT is a powerful model for NLP."]
    embeddings = get_bert_embeddings(texts)
    print(f"Embedding for sentence {embeddings}")
    store_embeddings_in_chroma(file_path="Dummy", embeddings=embeddings)

# Airflow task to detect new files and process them
detect_files_task = PythonOperator(
    task_id='detect_new_files',
    python_callable=dag_test,
    dag=dag,
)
