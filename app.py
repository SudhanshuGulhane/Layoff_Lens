from flask import Flask, request, jsonify, render_template
import json
import faiss
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel
from flask_cors import CORS


app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

tokenizer = AutoTokenizer.from_pretrained('BAAI/bge-small-en-v1.5')
model = AutoModel.from_pretrained('BAAI/bge-small-en-v1.5')

faiss_index = faiss.read_index("faiss_index.bin")
with open("faiss_meta.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

def convert_query_to_embedding(query):
    tokens = tokenizer([query], padding=True, truncation=True, return_tensors="pt", max_length=512)
    with torch.no_grad():
        outputs = model(**tokens)

    embeddings = outputs.last_hidden_state
    attention_mask = tokens['attention_mask']

    mask = attention_mask.unsqueeze(-1).expand(embeddings.size()).float()
    masked_embeddings = embeddings * mask
    summed = torch.sum(masked_embeddings, 1)
    summed_mask = torch.clamp(mask.sum(1), min=1e-9)
    mean_pooled = summed / summed_mask

    return mean_pooled.numpy()

def search_faiss(query, top_k=5):
    query_embedding = convert_query_to_embedding(query)

    D, I = faiss_index.search(query_embedding, top_k)

    results = [{"sentence": metadata[str(idx)]["sentence"], "url": metadata[str(idx)]["url"]} 
               for i, idx in enumerate(I[0])]

    unique_results = []
    seen_sentences = set()

    for res in results:
        if res["sentence"] not in seen_sentences:
            unique_results.append(res)
            seen_sentences.add(res["sentence"])

    return unique_results

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    try:
        query = request.args.get('query', '').strip()
        top_k = int(request.args.get('top_k'))

        if not query:
            return jsonify({"error": "Query parameter is required"}), 400

        results = search_faiss(query, top_k)
        return jsonify({"query": query, "results": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)