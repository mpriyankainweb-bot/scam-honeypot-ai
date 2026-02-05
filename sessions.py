sessions = {}

def get_session(session_id: str):
    if session_id not in sessions:
        sessions[session_id] = {
            "history": []
        }
    return sessions[session_id]
