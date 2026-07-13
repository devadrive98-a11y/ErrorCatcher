from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()
@app.get("/")
def root():
    return {"status": "ok"}
# isi dengan punyamu
BOT_TOKEN = "8850208766:AAGbViUjrEMZ0dZpXgOu30c-dAJdgm3X4E8"
CHAT_ID = "1007355104"

def send_telegram(message: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, json=payload)


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/error")
async def receive_error(request: Request):
    data = await request.json()

    message = f"""
🚨 ERROR APP

Message: {data.get("message")}
StackTrace: {data.get("stackTrace")}
Device: {data.get("device")}
Time: {data.get("time")}
"""

    send_telegram(message)

    return {"status": "sent"}
