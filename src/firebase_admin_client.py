import logging

# Firebase desativado no ambiente local
logging.warning("⚠️ Firebase ignorado neste ambiente (sem credenciais).")

def send_push_v1(token, title, body, data=None):
    logging.warning("⚠️ Push ignorado (Firebase não configurado).")
    return None
