# Layoff Lens - Intelligent Job Market Search Engine

🚀 **Layoff Lens** is a hybrid search engine leveraging **PyLucene** and **FAISS** to provide **semantic and keyword-based search** over job market and layoff-related discussions. It scrapes data from **Reddit**, indexes it using **Lucene**, and enables efficient **dense retrieval** via a fine-tuned **BERT model**.

---

## **🚀 Features**
- 🔍 **Hybrid Search** - Combines **sparse (keyword)** and **dense (semantic)** search.
- 🤖 **BERT-Based Embeddings** - Uses **`bge-small-en-v1.5`** for dense retrieval.
- 🔗 **FAISS Indexing** - Enables fast nearest-neighbor searches for embeddings.
- 📜 **Lucene Indexing** - Facilitates keyword-based search for fast retrieval.
- 🌍 **Flask API** - Backend for handling search requests.
- 🖥 **Interactive Web UI** - AJAX-based frontend for seamless query execution.
- 🛠 **Docker Support** - Fully containerized for easy deployment.

---

## **📂 Project Structure**
```
📦 Layoff_Lens
├── BertFaiss.py                # Dense search using BERT + FAISS
├── createIndex.py               # Lucene index creation
├── main.py                      # Main search interface
├── Pylucene_parser.py           # Query parser for Lucene
├── scrapper.py                  # Reddit Scraper (PRAW-based)
├── sample_code.index            # FAISS index file
├── post_sentences.txt           # Preprocessed sentences from Reddit
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Containerization setup
├── README.md                    # Project documentation
├── data.json                    # Scraped Reddit data
|── .gitignore                   # Ignore unnecessary files
├── faiss_store.py               # Stores FAISS index from scraped data
├── faiss_query.py               # Queries stored FAISS index
├── app.py                       # Flask Backend (Serves API & Frontend)
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
git clone https://github.com/your-repo/Layoff_Lens.git
cd Layoff_Lens
```

### **2️⃣ Install Dependencies**
Make sure Python **3.8+** is installed.
```sh
pip install -r requirements.txt
```

## **🔍 Usage**
- **Scrape data from Reddit**
  ```sh
  python scrapper.py
  ```
- **Generate FAISS Index**
  ```sh
  python faiss_store.py
  ```
- **Running Flask Backend**
  ```sh
  python app.py
  ```
  Opens UI at: http://127.0.0.1:5000/
  API Endpoint: /search?query=tech layoffs&top_k=5
- **Create a Lucene index**
  ```sh
  python createIndex.py
  ```
- **Perform a search (interactive)**
  ```sh
  python main.py
  ```
  _Choose between sparse (Lucene) and dense (FAISS) search._

---

## **🛠 Technologies Used**
- **Python** - Core programming language.
- **FAISS** - Efficient nearest-neighbor search.
- **Transformers (Hugging Face)** - BERT embeddings for semantic search.
- **PyLucene** - Keyword-based retrieval.
- **PRAW** - Reddit scraping.
- **Docker** - Containerization for easy deployment.

---

## **📜 License**
This project is licensed under the **MIT License**.

---
