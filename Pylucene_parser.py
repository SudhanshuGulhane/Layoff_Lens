import lucene
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.store import SimpleFSDirectory
import sys

def perform_search(index_path, query_str, num_results):
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    
    directory = SimpleFSDirectory.open(Paths.get(index_path))
    reader = DirectoryReader.open(directory)
    searcher = IndexSearcher(reader)
    analyzer = StandardAnalyzer()
    query_parser = QueryParser("Body", analyzer)
    query = query_parser.parse(query_str)
    
    top_docs = searcher.search(query, num_results).scoreDocs
    topk_docs = []
    for hit in top_docs:
        doc = searcher.doc(hit.doc)
        topk_docs.append({
            "score": hit.score,
            "title": doc.get("Title"),
            "text": doc.get("Body")
        })
        
    for doc in topk_docs:
        print(doc)
    reader.close()
    directory.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python query_parser.py <query> <k> <index_path>")
        sys.exit(1)

    query_str = sys.argv[1]
    num_results = int(sys.argv[2])
    index_path = sys.argv[3]
    
    perform_search(index_path, query_str, num_results)