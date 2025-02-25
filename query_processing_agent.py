from langchain_ollama.llms import OllamaLLM
from urlextract import URLExtract

llama3_model = OllamaLLM(model="mistral", temperature=0.3, top_k=20)

def expand_query(user_query):
    prompt = f"""
    Expand the given search query slightly for better retrieval accuracy while keeping it concise (no more than 7 words).  
    Preserve the original intent and improve clarity.
    Original Query: {user_query}
    Expanded Query:
    """
    response = llama3_model.invoke(prompt)
    expand_query = response.split("Expanded Query:")[-1].strip()
    return expand_query

def summarize_text(text):
    prompt = f"""
    Summarize the following text in one or two sentences {text}
    Summary:"""
    response = llama3_model.invoke(prompt)
    return response

def remove_urls(text):
    extractor = URLExtract()
    urls = extractor.find_urls(text)
    for url in urls:
        text = text.replace(url, '')
    
    url_set = set()
    list_urls = []
    for url in urls:
        if url not in url_set:
            list_urls.append(url)
            url_set.add(url)

    return ' '.join(text.split()), list_urls