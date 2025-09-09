from fastapi import FastAPI
from pydantic import BaseModel
from app.logic import handle_query

app = FastAPI(title="Hopkins Pharmacy Assistant")

# Track session state (simple in-memory for demo)
SESSION_STATE = {"patient": None}

class Query(BaseModel):
    text: str

@app.post("/ask")
def ask(query: Query):
    response, patient = handle_query(query.text, SESSION_STATE["patient"])
    if patient:
        SESSION_STATE["patient"] = patient
    return {"response": response}
