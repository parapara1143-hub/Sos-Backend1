
import os, json
import firebase_admin
from firebase_admin import credentials, messaging

# Initialize app once
if not firebase_admin._apps:
    creds_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
    creds_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if creds_json:
        cred = credentials.Certificate(json.loads(creds_json))
    elif creds_file and os.path.exists(creds_file):
        cred = credentials.Certificate(creds_file)
    else:
        raise RuntimeError("Firebase credentials not configured. Set FIREBASE_CREDENTIALS_JSON or GOOGLE_APPLICATION_CREDENTIALS")
    firebase_admin.initialize_app(cred)

def send_push_v1(tokens, title, body, data=None):
    tokens = list(tokens or [])
    if not tokens:
        return {"sent": 0, "responses": []}
    data = {str(k): str(v) for k, v in (data or {}).items()}
    responses = []
    for t in tokens:
        msg = messaging.Message(
            notification=messaging.Notification(title=title, body=body),
            data=data,
            token=t,
        )
        try:
            mid = messaging.send(msg)
            responses.append({"token": t, "id": mid})
        except Exception as e:
            responses.append({"token": t, "error": str(e)})
    sent = len([r for r in responses if "id" in r])
    return {"sent": sent, "responses": responses}
