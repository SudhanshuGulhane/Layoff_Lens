import json
import faiss
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel

# Load Transformer Model
tokenizer = AutoTokenizer.from_pretrained('BAAI/bge-small-en-v1.5')
model = AutoModel.from_pretrained('BAAI/bge-small-en-v1.5')

# Load FAISS Index
faiss_index = faiss.read_index("faiss_index.bin")

# Load Metadata
with open("faiss_meta.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

# Convert Query to Embedding
def convert_query_to_embedding(query):
    tokens = tokenizer([query], padding=True, truncation=True, return_tensors="pt", max_length=512)
    with torch.no_grad():
        outputs = model(**tokens)
    
    embeddings = outputs.last_hidden_state
    attention_mask = tokens['attention_mask']

    # Apply mean pooling
    mask = attention_mask.unsqueeze(-1).expand(embeddings.size()).float()
    masked_embeddings = embeddings * mask
    summed = torch.sum(masked_embeddings, 1)
    summed_mask = torch.clamp(mask.sum(1), min=1e-9)
    mean_pooled = summed / summed_mask

    return mean_pooled.numpy()

# Perform Search in FAISS
def search_faiss(query, top_k=5):
    query_embedding = convert_query_to_embedding(query)
    
    # Search FAISS Index
    D, I = faiss_index.search(query_embedding, top_k)

    # Retrieve Results
    results = [{"sentence": metadata[str(idx)]["sentence"], "url": metadata[str(idx)]["url"], "score": float(D[0][i])} 
               for i, idx in enumerate(I[0])]

    unique_results = []
    seen_sentences = set()

    for res in results:
        if res["sentence"] not in seen_sentences:
            unique_results.append(res)
            seen_sentences.add(res["sentence"])

    return unique_results

if __name__ == "__main__":
    query = input("Enter your search query: ")
    results = search_faiss(query, top_k=5)

    print("\n🔍 Search Results:")
    for res in results:
        print(f"👉 Sentence: {res['sentence']}")
        print(f"🔗 URL: {res['url']}")
        print(f"⭐ Score: {res['score']}")
        print("-" * 50)