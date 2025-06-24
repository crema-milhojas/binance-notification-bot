import os
import requests

def send_message(mensaje: str):
    url = f"https://api.telegram.org/bot{os.environ.get("TOKEN_TELEGRAM")}/sendMessage"
    payload = {
        "chat_id": os.environ.get("CHAT_ID_TELEGRAM"),
        "text": mensaje,
        "parse_mode": "HTML"  # opcional, para formato de texto
    }

    response = requests.post(url, json=payload)
    if response.ok:
        print("✅ Mensaje enviado")
    else:
        print(f"❌ Error al enviar mensaje: {response.text}")