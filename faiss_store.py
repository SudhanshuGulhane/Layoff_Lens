import json
import faiss
import torch
from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained('BAAI/bge-small-en-v1.5')
model = AutoModel.from_pretrained('BAAI/bge-small-en-v1.5')

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    sentences = [item["sentence"] for item in data]
    urls = [item["url"] for item in data]
    return sentences, urls

def tokenize_sentences(sentences):
    tokens = {'input_ids': [], 'attention_mask': []}
    for sentence in sentences:
        new_tokens = tokenizer.encode_plus(sentence, max_length=512, truncation=True, 
                                           padding='max_length', return_tensors='pt')
        tokens['input_ids'].append(new_tokens['input_ids'][0])
        tokens['attention_mask'].append(new_tokens['attention_mask'][0])
    tokens['input_ids'] = torch.stack(tokens['input_ids'])
    tokens['attention_mask'] = torch.stack(tokens['attention_mask'])
    return tokens

def process_in_batches_and_pool(model, tokens, batch_size=8):
    print("Executing batch processing...")
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

    return torch.cat(pooled_outputs, dim=0).numpy()  # Convert final tensor to numpy

def store_faiss_index(sentences, urls, index_file="faiss_index.bin", meta_file="faiss_meta.json"):
    tokens = tokenize_sentences(sentences)  # Tokenize all sentences
    embeddings = process_in_batches_and_pool(model, tokens, batch_size=10)  # Process in batches

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    # Save FAISS Index
    faiss.write_index(index, index_file)

    # Save metadata (ID-to-Text Mapping)
    metadata = {idx: {"sentence": sentences[idx], "url": urls[idx]} for idx in range(len(sentences))}
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)

    print(f"✅ FAISS Index Stored Successfully in `{index_file}`")
    print(f"✅ Metadata Stored Successfully in `{meta_file}`")

if __name__ == "__main__":
    sentences, urls = load_data("post_sentences.txt")
    store_faiss_index(sentences, urls)