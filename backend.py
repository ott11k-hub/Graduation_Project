import uvicorn
import chromadb
import logging
from groq import Groq
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# --- PROFESSIONAL LOGGING CONFIG ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- API CONFIG ---
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

app = FastAPI(title="Academic RAG Engine v2.0")

# --- DATABASE (Persistent Storage) ---
db_client = chromadb.PersistentClient(path="./project_data_db")
collection = db_client.get_or_create_collection(name="project_docs")

# Initialize data with academic rigor
if collection.count() == 0:
    collection.add(
        documents=[
            "Project Deadline: May 6, 2026, at 15:00. No late submissions accepted.",
            "Architecture: Hybrid Cloud (FastAPI Backend + Streamlit Frontend).",
            "Core Tech: ChromaDB for Vector Search, Groq Llama-3.3 for Inference.",
            "Project Scope: This AI is a secure retrieval system for graduation documentation."
        ],
        ids=["doc1", "doc2", "doc3", "doc4"]
    )

class QueryRequest(BaseModel):
    query: str

@app.post("/ask")
async def ask_ai(request: QueryRequest):
    try:
        # Context Retrieval
        results = collection.query(query_texts=[request.query], n_results=2)
        context = " ".join(results['documents'][0]) if results['documents'] else "None"

        # STRICT SECURITY PROMPT
        system_instruction = (
            "SYSTEM IDENTITY: You are the Official Graduation Project Research Assistant. "
            "RESTRICTIONS: "
            "1. Answer ONLY using the provided Context. "
            "2. If the user asks about recipes, lifestyle, or anything unrelated to the context, "
            "reply: 'ACCESS DENIED: My security protocols only allow for project-specific data retrieval.' "
            "3. Be concise, academic, and precise."
        )

        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"CONTEXT: {context}\n\nQUERY: {request.query}"}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.05, # Near-zero temperature for maximum factual consistency
        )

        answer = response.choices[0].message.content
        logger.info(f"Engine Processed Query: {request.query[:30]}...")
        return {"status": "success", "response": answer}

    except Exception as e:
        logger.error(f"System Failure: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal AI Engine Error")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)