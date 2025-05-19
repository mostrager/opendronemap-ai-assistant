from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.rag_pipeline import get_qa_chain

app = FastAPI()
qa_chain = get_qa_chain()

class Query(BaseModel):
    question: str

@app.get("/")
def read_root():
    return {"message": "ODM AI Assistant backend is running."}

@app.post("/ask")
def ask_question(query: Query):
    try:
        result = qa_chain(query.question)
        return {
            "answer": result['result'],
            "sources": [doc.metadata for doc in result['source_documents']]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
