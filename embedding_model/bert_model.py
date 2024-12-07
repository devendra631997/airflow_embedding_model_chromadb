from transformers import BertTokenizer, BertModel
import torch

def get_bert_embeddings(texts, model_name='bert-base-uncased'):
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertModel.from_pretrained(model_name)

    # Ensure the model is in evaluation mode
    model.eval()

    embeddings = []
    ids = []
    count = 1
    for text in texts:
        inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)

        with torch.no_grad():
            outputs = model(**inputs)
        cls_embedding = outputs.last_hidden_state[:, 0, :]
        ids.append(f'{count}_id')
        embeddings.append(cls_embedding.squeeze().cpu().numpy())
        count = count+1
    return ids, embeddings
