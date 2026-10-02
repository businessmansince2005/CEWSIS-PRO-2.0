from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Cognitive EW API")

class PredictRequest(BaseModel):
    filepath: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(req: PredictRequest):
    return {"filepath": req.filepath, "prediction": None, "note": "stub"}
