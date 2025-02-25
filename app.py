from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from query_processing_agent import *
from faiss_query import hybrid_search

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

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

        expanded_query = expand_query(query)
        results = hybrid_search(expanded_query, top_k)

        for result in results:
            text = result["sentence"]
            clean_text, urls = remove_urls(text)
            summary = summarize_text(clean_text)
            result["sentence"] = summary
            result["links"] = urls

        return jsonify({
            "query": query,
            "results": results,
            "expanded_query": expanded_query,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)