from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import joblib
import numpy as np
import time
import json
import os
import smtplib
import secrets
from collections import deque
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage
from pydantic import BaseModel
from train_model import MODEL_PATH, _features, train
from src.data_preprocessing.create_spectrograms import iq_to_spectrogram

BASE_DIR = Path(__file__).resolve().parent
INDEX_FILE = BASE_DIR / "index.html"
CONTACT_LOG = BASE_DIR / "data" / "contact_submissions.jsonl"
analysis_history = deque(maxlen=20)
active_sessions: dict[str, datetime] = {}
SESSION_TTL = timedelta(hours=8)


class ContactRequest(BaseModel):
    name: str
    email: str
    subject: str
    message: str


class IQScanRequest(BaseModel):
    iq: list[list[float]]
    sample_rate: float = 1_000_000.0


class LoginRequest(BaseModel):
    email: str
    password: str


class SignupRequest(BaseModel):
    name: str
    email: str
    password: str

app = FastAPI(title="CEWSIS PRO 2.0 - Spectrum Intelligence API")

# Enable CORS for frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return FileResponse(
        INDEX_FILE,
        media_type="text/html",
        headers={"Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"},
    )


@app.get("/api/status")
def api_status():
    model_ready = MODEL_PATH.exists()
    return {
        "status": "Online" if model_ready else "Training required",
        "service": "CEWSIS PRO 2.0 Spectrum Intelligence Platform",
        "version": "2.0.0",
        "model_ready": model_ready,
        "message": "Public-data and synthetic-data research demonstrator",
        "sdr": {"hardware_connected": False, "adapter": "Synthetic IQ source", "sample_rate": 1000000},
    }


def _session_from_request(request):
    token = request.cookies.get("cewsis_session")
    expires_at = active_sessions.get(token or "")
    if not expires_at or expires_at <= datetime.now(timezone.utc):
        if token:
            active_sessions.pop(token, None)
        return None
    return token


@app.post("/api/login")
def login(credentials: LoginRequest):
    configured_email = os.getenv("CEWSIS_ADMIN_EMAIL")
    configured_password = os.getenv("CEWSIS_ADMIN_PASSWORD")
    if not configured_email or not configured_password:
        return {"authenticated": False, "message": "Login is not configured on this deployment."}
    if not secrets.compare_digest(credentials.email, configured_email) or not secrets.compare_digest(credentials.password, configured_password):
        return {"authenticated": False, "message": "Email or password is incorrect."}
    token = secrets.token_urlsafe(32)
    active_sessions[token] = datetime.now(timezone.utc) + SESSION_TTL
    return {"authenticated": True, "token": token, "user": {"email": configured_email}}


@app.post("/api/signup")
def signup(credentials: SignupRequest):
    if len(credentials.password) < 8:
        return {"authenticated": False, "message": "Password must contain at least 8 characters."}
    token = secrets.token_urlsafe(32)
    active_sessions[token] = datetime.now(timezone.utc) + SESSION_TTL
    return {"authenticated": True, "token": token, "user": {"email": credentials.email, "name": credentials.name}}


@app.post("/api/logout")
def logout(request):
    token = request.cookies.get("cewsis_session")
    if token:
        active_sessions.pop(token, None)
    return {"authenticated": False}


@app.get("/api/session")
def session(request):
    return {"authenticated": bool(_session_from_request(request))}


def _telemetry(iq: np.ndarray, sample_rate: float) -> dict:
    spectrum = np.abs(np.fft.fftshift(np.fft.fft(iq)))
    spectrum = spectrum / (float(spectrum.max()) + 1e-8)
    spectrogram = iq_to_spectrogram(iq, n_fft=128, hop_length=32)
    spectrogram = spectrogram / (float(spectrogram.max()) + 1e-8)
    return {
        "sample_rate": sample_rate,
        "iq": [[round(float(value.real), 4), round(float(value.imag), 4)] for value in iq[::8]],
        "spectrum": [round(float(value), 4) for value in spectrum[::4]],
        "spectrogram": [[round(float(value), 4) for value in row[::2]] for row in spectrogram[::2]],
        "peak_bin": int(np.argmax(spectrum)),
        "power_db": round(float(10 * np.log10(np.mean(np.abs(iq) ** 2) + 1e-8)), 2),
    }


def _synthetic_iq() -> np.ndarray:
    rng = np.random.default_rng()
    samples = np.arange(1024)
    tones = (0.72 * np.exp(2j * np.pi * 0.11 * samples)
             + 0.28 * np.exp(2j * np.pi * 0.28 * samples))
    return tones + 0.12 * (rng.normal(size=1024) + 1j * rng.normal(size=1024))


@app.get("/api/telemetry")
def telemetry():
    return _telemetry(_synthetic_iq(), 1_000_000.0)


@app.post("/api/sdr/scan")
def sdr_scan(request: IQScanRequest):
    values = np.asarray(request.iq, dtype=np.float32)
    if values.ndim != 2 or values.shape[1] != 2 or not 128 <= len(values) <= 100_000:
        return {"accepted": False, "message": "IQ must contain 128 to 100000 [I, Q] samples"}
    iq = values[:, 0] + 1j * values[:, 1]
    return {"accepted": True, "source": "external SDR IQ", "telemetry": _telemetry(iq, request.sample_rate)}

@app.get("/analyze")
def analyze():
    if not MODEL_PATH.exists():
        train(samples=1400)
    artifact = joblib.load(MODEL_PATH)
    rng = np.random.default_rng()
    iq = rng.normal(size=1024) + 1j * rng.normal(size=1024)
    probabilities = artifact["model"].predict_proba([_features(iq)])[0]
    index = int(np.argmax(probabilities))
    label = artifact["model"].classes_[index]
    confidence = float(probabilities[index])
    threat_level = "High" if label in {"GFSK", "GMSK"} else "Low"
    response = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "sensor_id": "RF-SENSOR-NODE-01",
        "analysis": {"result": f"{label} modulation", "confidence": confidence,
                      "threat_level": threat_level, "model": "RandomForest RF feature classifier"},
    }
    analysis_history.appendleft(response)
    return response


@app.get("/api/history")
def history():
    return {"items": list(analysis_history)}


@app.post("/api/contact")
def contact(request: ContactRequest):
    payload = {"received_at": time.strftime("%Y-%m-%d %H:%M:%S"), **request.model_dump()}
    CONTACT_LOG.parent.mkdir(parents=True, exist_ok=True)
    with CONTACT_LOG.open("a", encoding="utf-8") as output:
        output.write(json.dumps(payload) + "\n")

    smtp_host = os.getenv("CEWSIS_SMTP_HOST")
    smtp_user = os.getenv("CEWSIS_SMTP_USER")
    smtp_password = os.getenv("CEWSIS_SMTP_PASSWORD")
    recipient = os.getenv("CEWSIS_CONTACT_TO", smtp_user or request.email)
    delivered = False
    if smtp_host and smtp_user and smtp_password:
        email = EmailMessage()
        email["Subject"] = f"CEWSIS contact: {request.subject}"
        email["From"] = smtp_user
        email["To"] = recipient
        email["Reply-To"] = request.email
        email.set_content(f"From: {request.name} <{request.email}>\n\n{request.message}")
        with smtplib.SMTP(smtp_host, int(os.getenv("CEWSIS_SMTP_PORT", "587"))) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(email)
        delivered = True
    return {"accepted": True, "delivered": delivered, "message": "Request recorded"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
