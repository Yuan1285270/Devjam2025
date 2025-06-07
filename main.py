from fastapi import FastAPI
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv

# 載入本地環境變數（如 .env 中的 GEMINI_API_KEY）
load_dotenv()

app = FastAPI()

# Google Gemini API 設定
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# 定義接收資料格式
class MessageInput(BaseModel):
    message: str

@app.post("/chat")
async def chat(data: MessageInput):
    message = data.message
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": message}
                ]
            }
        ]
    }

    # 呼叫 Gemini API
    response = requests.post(
        GEMINI_URL,
        headers={"Content-Type": "application/json"},
        json=payload
    )

    result = response.json()
    if "candidates" in result:
        reply = result["candidates"][0]["content"]["parts"][0]["text"]
        return {"response": reply}
    else:
        return {
            "error": result.get("error", {}),
            "message": "Gemini API 回傳錯誤格式"
        }
