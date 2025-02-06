# Layoff Lens - Intelligent Job Market Search Engine

🚀 **Layoff Lens** is a hybrid search engine leveraging **PyLucene** and **FAISS** to provide **semantic and keyword-based search** over job market and layoff-related discussions. It scrapes data from **Reddit**, indexes it using **Lucene**, and enables efficient **dense retrieval** via a fine-tuned **BERT model**.

---

## **🚀 Features**
- 🔍 **Hybrid Search** - Combines **sparse (keyword)** and **dense (semantic)** search.
- 🤖 **BERT-Based Embeddings** - Uses **`bge-small-en-v1.5`** for dense retrieval.
- 🔗 **FAISS Indexing** - Enables fast nearest-neighbor searches for embeddings.
- 📜 **Lucene Indexing** - Facilitates keyword-based search for fast retrieval.
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
├── README.md                     # Project documentation
├── data.json                     # Scraped Reddit data
|── .gitignore                    # Ignore unnecessary files
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

### **3️⃣ Install PyLucene**
PyLucene must be installed manually:
```sh
pip install pylucene
```

---

## **🐳 Running with Docker**
### **1️⃣ Build the Docker Image**
```sh
docker build -t layoff-lens .
```

### **2️⃣ Run the Container**
```sh
docker run -it layoff-lens
```

### **3️⃣ Run the Search Engine**
```sh
python main.py
```

---

## **🔍 Usage**
- **Scrape data from Reddit**
  ```sh
  python scrapper.py
  ```
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
