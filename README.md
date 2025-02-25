# Insight Lens - Intelligent Job Market Search Engine

🚀 **Insight Lens** is an AI-driven hybrid search engine that provides real-time insights into job market trends by combining semantic (FAISS) and keyword-based (BM25) retrieval. It scrapes data from Reddit, processes queries with Llama-3, and delivers concise summaries of the trends.

---

## **🚀 Features**
- 🔍 **Hybrid Search Enhancement** - BM25 (keyword-based) retrieval integrated with FAISS (semantic) for more accurate search results.
- 🤖 **BERT-Based Embeddings** - Uses **`bge-small-en-v1.5`** for dense retrieval.
- 🔗 **FAISS Indexing** - Enables fast nearest-neighbor searches for embeddings.
- 🧠 **Query Processing Agent** - Expands and refines user queries using Llama-3 for better retrieval.
- 📊 **Summarization Agent** - Condenses lengthy discussions using Llama-3 before returning results.
- 🏆 **Improved Ranking** - Results are merged, ranked, and summarized for better readability and relevance.
- 🚀 **Flask API** - Integrated Summarization Agent into Search Agent to provide concise responses.
- 🖥 **Interactive Web UI** - AJAX-based frontend for seamless query execution.

---

## **📂 Project Structure**
```
📦 Main Directory
├── query_processing_agent.py    # Expands and refines queries using Llama-3 & SymSpell
├── search_agent.py              # Hybrid search (FAISS + BM25) with improved ranking
├── summarization_agent.py       # Summarizes lengthy discussions (Llama-3)
├── faiss_store.py               # Stores FAISS index from scraped data
├── faiss_query.py               # Queries stored FAISS index
├── app.py                       # Flask Backend (Integrates Search & Summarization)
├── faiss_index.bin              # Stored FAISS index
├── faiss_meta.json              # Metadata mapping index → sentences & URLs
├── templates/
    ├── index.html               # Frontend UI (Search Page)
├── static/
    ├── style.css                # Styling for UI
    ├── app.js                   # AJAX logic for search API

```

---

## **⚡ Installation**
### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/SudhanshuGulhane/InsightLens.git
cd InsightLens
```

### **2️⃣ Install Dependencies**
Make sure Python **3.8+** is installed.
```sh
pip install -r requirements.txt
```

## **🔍 Usage**
- **Running Flask Backend**
  ```sh
  python app.py
  ```
  Opens UI at: http://127.0.0.1:5000/
  API Endpoint: /search?query=current job trends&top_k=5
---

## **🛠 Technologies Used**
- **Python** - Core programming language.
- **FAISS** - Efficient nearest-neighbor search.
- **Transformers (Hugging Face)** - BERT embeddings for semantic search.
- **Langchain** - OLlama model
- **PRAW** - Reddit scraping.
- **Docker** - Containerization for easy deployment.

---

## UI snippet

![Screenshot (2296)](https://github.com/user-attachments/assets/2029f4be-279c-4dc5-9ca5-bba264c63f34)


## **📜 License**
This project is licensed under the **MIT License**.

---
