from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
