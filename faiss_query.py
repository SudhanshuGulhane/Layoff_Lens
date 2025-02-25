import json
import faiss
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel
from rank_bm25 import BM25Okapi

# Load Transformer Model
tokenizer = AutoTokenizer.from_pretrained('BAAI/bge-small-en-v1.5')
model = AutoModel.from_pretrained('BAAI/bge-small-en-v1.5')

# Load FAISS Index
faiss_index = faiss.read_index("faiss_index.bin")

# Load Metadata
with open("faiss_meta.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

# Load BM25 Corpus
with open("post_sentences.txt", "r", encoding="utf-8") as f:
    data = json.load(f)

corpus = [entry["sentence"] for entry in data]

# Tokenize the corpus for BM25
bm25 = BM25Okapi([doc.split() for doc in corpus])

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
def search_faiss(query, top_k):
    query_embedding = convert_query_to_embedding(query)
    
    # Search FAISS Index
    D, I = faiss_index.search(query_embedding, top_k)

    # Retrieve Results
    results = [{"sentence": metadata[str(idx)]["sentence"], "url": metadata[str(idx)]["url"], "faiss_score": float(D[0][i])} 
               for i, idx in enumerate(I[0])]

    unique_results = []
    seen_sentences = set()

    for res in results:
        if res["sentence"] not in seen_sentences:
            unique_results.append(res)
            seen_sentences.add(res["sentence"])

    return unique_results

def bm25_search(query, top_k):
    scores = bm25.get_scores(query.split())
    top_indices = np.argsort(scores)[::-1][:top_k]

    results = [{"sentence": corpus[idx], "bm25_score": float(scores[idx])} for idx in top_indices]

    return results

def hybrid_search(query, top_k):
    faiss_results = search_faiss(query, top_k)
    bm25_results = bm25_search(query, top_k)

    # Merge results based on scores
    results = {}
    for res in faiss_results:
        sentence = res["sentence"]
        results[sentence] = {"sentence": sentence, "url": res.get("url", ""), "faiss_score": res["faiss_score"], "bm25_score": 0}

    for res in bm25_results:
        sentence = res["sentence"]
        if sentence in results:
            results[sentence]["bm25_score"] = res["bm25_score"]
        else:
            results[sentence] = {"sentence": sentence, "url": "", "faiss_score": 0, "bm25_score": res["bm25_score"]}

    # Rank results by combined FAISS + BM25 scores
    ranked_results = sorted(results.values(), key=lambda x: (x["faiss_score"] + x["bm25_score"]), reverse=True)[:top_k]

    return ranked_results

if __name__ == "__main__":
    query = input("Enter your search query: ")
    results = search_faiss(query, top_k=5)

    print("\n🔍 Search Results:")
    for res in results:
        print(f"👉 Sentence: {res['sentence']}")
        print(f"🔗 URL: {res['url']}")
        print(f"⭐ Score: {res['score']}")
        print("-" * 50)