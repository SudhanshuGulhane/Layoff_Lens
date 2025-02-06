import os
import sys
import json
import lucene
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, DirectoryReader
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.store import SimpleFSDirectory, NIOFSDirectory
from org.apache.lucene.queryparser.classic import QueryParser

def create_index(directory, json_data):
    if not os.path.exists(directory):
        os.mkdir(directory)
    store = SimpleFSDirectory(Paths.get(directory))
    analyzer = StandardAnalyzer()
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config)

    metaType = FieldType()
    metaType.setStored(True)
    metaType.setTokenized(False)

    contentType = FieldType()
    contentType.setStored(True)
    contentType.setTokenized(True)
    contentType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

    for entry in json_data:
        print('indexing for ', entry['Title'])
        doc = Document()
        doc.add(TextField("Title", entry["Title"], contentType))
        doc.add(TextField("Body", entry["Body"], contentType))
        doc.add(Field("Upvotes", str(entry["Upvotes"]), metaType))
        doc.add(Field("UpvoteRatio", str(entry["Upvote Ratio"]), metaType))
        doc.add(Field("PublishDate", str(entry["Publish_Date"]), metaType))
        writer.addDocument(doc)
        print('indexing done')

    writer.commit()
    writer.close()
    print('finally data is indexed')

def main():
    # base_path = '/home/cs242/'
    # json_file_path = os.path.join(base_path, 'data.json')
    # index_path = os.path.join(base_path, 'index_dir/')
    json_input_path = 'data.json'
    index_path = ''

    with open(json_input_path, 'r') as file:
        json_data = json.load(file)

    create_index(index_path, json_data)

if __name__ == "__main__":
    main()