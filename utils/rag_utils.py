
import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

def build_or_load_vector_db(base_dir=".", db_dir="chroma_db", model="mistral"):
    embeddings = OllamaEmbeddings(model=model)
    if os.path.exists(db_dir):
        db = Chroma(persist_directory=db_dir, embedding_function=embeddings)
        return db

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs, metas = [], []
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".py") and "venv" not in root and "__pycache__" not in root:
                path = os.path.join(root, file)
                try:
                    text = open(path, "r", encoding="utf-8", errors="ignore").read()
                    for chunk in splitter.split_text(text):
                        docs.append(chunk)
                        metas.append({"source": path})
                except Exception:
                    pass
    db = Chroma.from_texts(docs, embedding=embeddings, metadatas=metas, persist_directory=db_dir)
    db.persist()
    return db

def retrieve_context(db, query, k=3):
    return db.similarity_search(query, k=k)
