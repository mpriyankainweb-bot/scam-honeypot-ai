from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import time

# ==== IMPORT YOUR EXISTING MODULES ====
from detector import detect_scam
from agent import generate_agent_reply
from extractor import extract_intelligence

app = FastAPI()

# ==== ENABLE CORS ====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# REQUEST MODELS (Official Format)
# =========================

class Message(BaseModel):
    sender: str
    text: str
    timestamp: Optional[str] = None


class Metadata(BaseModel):
    channel: Optional[str] = None
    language: Optional[str] = None
    locale: Optional[str] = None


class HoneyPotRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: Optional[List[Message]] = []
    metadata: Optional[Metadata] = None


# =========================
# HEALTH CHECK
# =========================

@app.get("/")
def health():
    return {"status": "HoneyPot API Running"}


# =========================
# MAIN ENDPOINT
# =========================

@app.post("/honeypot")
def honeypot(
    request: HoneyPotRequest,
    x_api_key: str = Header(None, alias="x-api-key")
):

    # ✅ API KEY VALIDATION
    if x_api_key != "mysecret123":
        raise HTTPException(status_code=403, detail="Invalid API Key")

    start_time = time.time()

    scam_text = request.message.text

    # === YOUR EXISTING LOGIC ===
    detection = detect_scam(scam_text)
    agent_reply = generate_agent_reply(
    request.conversationHistory,
    scam_text
    )
    intelligence = extract_intelligence(scam_text)

    duration = int(time.time() - start_time)

    # ==== REQUIRED RESPONSE FORMAT ====
    return {
        "status": "success",
        "scamDetected": detection["scam_detected"],
        "engagementMetrics": {
            "engagementDurationSeconds": duration,
            "totalMessagesExchanged": len(request.conversationHistory) + 1
        },
        "extractedIntelligence": intelligence,
        "agentNotes": agent_reply
    }
