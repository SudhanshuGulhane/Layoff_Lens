from transformers import AutoTokenizer, AutoModel
import torch
import json
import faiss
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import sys
import argparse

tokenizer = AutoTokenizer.from_pretrained('BAAI/bge-small-en-v1.5')
model = AutoModel.from_pretrained('BAAI/bge-small-en-v1.5')

def load_sentences(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = json.load(file)
    sentences = [item["sentence"] for item in content]
    urls = [item["url"] for item in content]
    return sentences, urls

def tokenize_sentences(sentences):
    tokens = {'input_ids': [], 'attention_mask': []}
    for sentence in sentences:
        new_tokens = tokenizer.encode_plus(sentence, max_length=512,
                                           truncation=True, padding='max_length',
                                           return_tensors='pt')
        tokens['input_ids'].append(new_tokens['input_ids'][0])
        tokens['attention_mask'].append(new_tokens['attention_mask'][0])
    tokens['input_ids'] = torch.stack(tokens['input_ids'])
    tokens['attention_mask'] = torch.stack(tokens['attention_mask'])
    return tokens

def process_in_batches_and_pool(model, tokens, batch_size=8):
    print("Executing the batch processing")
    input_ids_batches = torch.split(tokens['input_ids'], batch_size)
    attention_mask_batches = torch.split(tokens['attention_mask'], batch_size)
    pooled_outputs = []

    for i in range(len(input_ids_batches)):
        batch_input_ids = input_ids_batches[i]
        batch_attention_mask = attention_mask_batches[i]

        with torch.no_grad():
            batch_outputs = model(input_ids=batch_input_ids, attention_mask=batch_attention_mask)
            embeddings = batch_outputs.last_hidden_state

            mask = batch_attention_mask.unsqueeze(-1).expand(embeddings.size()).float()
            masked_embeddings = embeddings * mask
            summed = torch.sum(masked_embeddings, 1)
            summed_mask = torch.clamp(mask.sum(1), min=1e-9)
            mean_pooled = summed / summed_mask

            pooled_outputs.append(mean_pooled)

    return pooled_outputs

def convert_to_embedding(query):
    tokens = tokenize_sentences([query])
    with torch.no_grad():
        outputs = model(**tokens)
    embeddings = outputs.last_hidden_state
    attention_mask = tokens['attention_mask']
    mask = attention_mask.unsqueeze(-1).expand(embeddings.size()).float()
    masked_embeddings = embeddings * mask
    summed = torch.sum(masked_embeddings, 1)
    summed_mask = torch.clamp(mask.sum(1), min=1e-9)
    mean_pooled = summed / summed_mask
    
    return mean_pooled[0] # assuming query is a single sentence

def main(query,k):
    
    file_path = 'post_sentences.txt'
    sentences, urls = load_sentences(file_path)
    print(sentences[0])
    print(urls[0])
    tokens = tokenize_sentences(sentences)
    print(tokens)
    pooled_embeddings = process_in_batches_and_pool(model, tokens, batch_size=10)
    pooled_embeddings_tensor = torch.cat(pooled_embeddings, dim=0).numpy()

    query_embedding = convert_to_embedding(query)

    base_index = faiss.IndexFlatL2(384)
    index = faiss.IndexIDMap(base_index)
    id_to_data = {} 

    if isinstance(pooled_embeddings_tensor, torch.Tensor):
        pooled_embeddings_tensor = pooled_embeddings_tensor.numpy()

    for idx, embedding in enumerate(pooled_embeddings_tensor):
        if embedding.ndim == 1:
            embedding = embedding.reshape(1, -1)
        
        faiss_id = np.array([idx], dtype=np.int64)
        index.add_with_ids(embedding, faiss_id)
        id_to_data[idx] = {"sentence": sentences[idx], "url": urls[idx]}

    faiss.write_index(index,"sample_code.index")

    index_loaded = faiss.read_index("sample_code.index")
    D, I = index_loaded.search(query_embedding[None, :], k)
    print(D) # scores of the results
    print("Search Results:\n")
    for idx in I[0]:
        print(idx)
        print(f"Post Data: {id_to_data[idx]}")
        print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("query", type=str, help="Search query")
    parser.add_argument("k", type=int, help="Number of search results to return")
    args = parser.parse_args()
    main(args.query, args.k)