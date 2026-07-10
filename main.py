from fastapi import FastAPI, Request, HTTPException
import requests
import os

app = FastAPI()

# ambil dari environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# validasi saat startup
@app.on_event("startup")
def startup():
    print("🚀 APP STARTED")

    if not BOT_TOKEN:
        print("❌ BOT_TOKEN tidak ditemukan di ENV")
    if not CHAT_ID:
        print("❌ CHAT_ID tidak ditemukan di ENV")


def send_telegram(message: str):
    if not BOT_TOKEN or not CHAT_ID:
        print("❌ ENV belum diset, skip kirim telegram")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        res = requests.post(url, json=payload, timeout=10)
        print("Telegram response:", res.status_code, res.text)
    except Exception as e:
        print("❌ Gagal kirim ke Telegram:", str(e))


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/error")
async def receive_error(request: Request):
    try:
        data = await request.json()
    except:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    message = f"""
🚨 <b>ERROR APP</b>

<b>Message:</b> {data.get("message")}
<b>StackTrace:</b> {data.get("stackTrace")}
<b>Device:</b> {data.get("device")}
<b>Time:</b> {data.get("time")}
"""

    send_telegram(message)

    return {"status": "sent"}
