from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI(title="Study Companion AI - Backend")

# Allow frontend (we'll add later) to call the API during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # tighten later for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello from Study Companion AI backend!"}

@app.get("/health")
def health():
    return {"status": "ok"}

# ---------------------------
# Input models
# ---------------------------
class SummarizeRequest(BaseModel):
    text: str

class QARequest(BaseModel):
    context: str
    question: str

# ---------------------------
# Load Hugging Face pipelines
# ---------------------------
summarizer = pipeline("summarization", model="t5-small")
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

# ---------------------------
# Routes
# ---------------------------

@app.post("/summarize")
def summarize(req: SummarizeRequest):
    summary = summarizer(req.text, max_length=60, min_length=15, do_sample=False)
    return {"summary": summary[0]["summary_text"]}

@app.post("/qa")
def question_answer(req: QARequest):
    answer = qa_pipeline(question=req.question, context=req.context)
    return {"answer": answer["answer"]}