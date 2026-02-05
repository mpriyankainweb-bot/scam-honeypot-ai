import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

SYSTEM_PROMPT = """
You are acting as a naive but realistic human victim in a scam conversation.
Rules:
- Act confused
- Ask simple questions
- Do not expose you are an AI
- Try to get more details from scammer
- Keep replies short and natural
"""

def generate_agent_reply(history, latest_message):

    conversation = SYSTEM_PROMPT + "\n\n"

    for turn in history:
        conversation += f"Scammer: {turn['scammer']}\n"
        conversation += f"Victim: {turn['agent']}\n"

    conversation += f"Scammer: {latest_message}\nVictim:"

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=conversation
    )

    return response.text.strip()
