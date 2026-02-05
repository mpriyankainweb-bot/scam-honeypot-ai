import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Scam Detection UI")

st.title("🛡 Scam Detection System")

# 🔗 BACKEND API (Render)
API_URL = "https://scam-honeypot-ai-relh.onrender.com/honeypot"

message = st.text_area("Enter suspicious message:")

if st.button("Analyze"):
    if message.strip() == "":
        st.warning("Please enter a message")
    else:
        headers = {
            "x-api-key": "mysecret123",
            "Content-Type": "application/json"
        }

        payload = {
            "sessionId": "ui-demo-001",
            "message": {
                "sender": "scammer",
                "text": message,
                "timestamp": datetime.utcnow().isoformat()
            },
            "conversationHistory": [],
            "metadata": {
                "channel": "Web",
                "language": "English",
                "locale": "IN"
            }
        }

        try:
            response = requests.post(API_URL, json=payload, headers=headers)

            if response.status_code == 200:
                data = response.json()

                st.success("Analysis Complete")

                st.subheader("🚨 Scam Detected")
                st.write(data["scamDetected"])

                st.subheader("📊 Engagement Metrics")
                st.json(data["engagementMetrics"])

                st.subheader("🕵 Extracted Intelligence")
                st.json(data["extractedIntelligence"])

                st.subheader("🤖 Agent Reply")
                st.info(data["agentNotes"])

            else:
                st.error(f"Backend error: {response.status_code}")
                st.write(response.text)

        except Exception as e:
            st.error("Failed to connect to backend")
            st.write(str(e))
