import os

project_dir = "/mnt/data/opendronemap-ai-assistant"
script_path = os.path.join(project_dir, "backend", "ingest", "chunk_and_embed.py")

script_code = '''
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Directory for source documents
SOURCE_DIR = "docs/"
PERSIST_DIRECTORY = "chroma_store"

def ingest_docs():
    print("[*] Loading documents...")
    docs = []
    for file_name in os.listdir(SOURCE_DIR):
        if file_name.endswith(".md") or file_name.endswith(".txt"):
            loader = TextLoader(os.path.join(SOURCE_DIR, file_name), encoding='utf-8')
            docs.extend(loader.load())

    print(f"[*] {len(docs)} documents loaded. Splitting...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    print(f"[*] {len(chunks)} chunks created. Generating embeddings...")
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )
    vectordb.persist()
    print("[✓] Ingestion complete. Embeddings saved to Chroma.")

if __name__ == "__main__":
    ingest_docs()
'''

# Create directory and write the script
os.makedirs(os.path.join(project_dir, "backend", "ingest"), exist_ok=True)
with open(script_path, "w") as f:
    f.write(script_code)

script_path
