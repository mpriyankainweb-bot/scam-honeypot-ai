def detect_scam(message: str):
    message = message.lower()

    risk_score = 0
    threat_level = "low"

    if "otp" in message:
        risk_score += 3
    if "bank" in message:
        risk_score += 2
    if "urgent" in message:
        risk_score += 2
    if "click" in message or "http" in message:
        risk_score += 2

    if risk_score >= 5:
        threat_level = "high"
    elif risk_score >= 3:
        threat_level = "medium"

    return {
        "scam_detected": risk_score > 0,
        "risk_score": risk_score,
        "threat_level": threat_level
    }
