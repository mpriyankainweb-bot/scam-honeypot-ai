from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from sessions import get_session
from detector import detect_scam
from agent import generate_agent_reply
from extractor import extract_intelligence

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


API_KEY = "mysecret123"


class HoneyPotRequest(BaseModel):
    session_id: str
    message: str


@app.post("/honeypot")
def honeypot(
    request: HoneyPotRequest,
    x_api_key: str = Header(None, alias="x-api-key")
):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    session = get_session(request.session_id)

    detection = detect_scam(request.message)

    agent_reply = generate_agent_reply(
        session["history"],
        request.message
    )

    intelligence = extract_intelligence(request.message)

    session["history"].append({
        "scammer": request.message,
        "agent": agent_reply
    })

   return {
    "scam_detected": detection["scam_detected"],
    "risk_score": detection["risk_score"],
    "threat_level": detection["threat_level"], 
    "agent_reply": agent_reply,
    "intelligence": intelligence
}



@app.get("/health")
def health_check():
    return {"status": "healthy"}
