from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
import os

router = APIRouter()

# Gemini API 設定
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent?key={GEMINI_API_KEY}"

class Message(BaseModel):
    role: str
    message: str

class ChatRequest(BaseModel):
    messages: list[Message]

@router.post("/chat")
async def chat(chat: ChatRequest):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="❌ 缺少 Gemini API 金鑰")

    if not chat.messages or len(chat.messages) == 0:
        raise HTTPException(status_code=400, detail="❌ 請提供至少一筆聊天訊息")

    # 組成 Gemini API 格式
    formatted = [
        {
            "role": msg.role,
            "parts": [{ "text": msg.message }]
        } for msg in chat.messages
    ]

    try:
        response = requests.post(
            GEMINI_URL,
            headers={ "Content-Type": "application/json" },
            json={ "contents": formatted }
        )
        result = response.json()
        if "candidates" not in result:
            return {
                "error": result.get("error", {}),
                "message": "Gemini 回傳錯誤格式，請確認 API key 或傳送內容。"
            }

        reply = result["candidates"][0]["content"]["parts"][0]["text"]
        return { "reply": reply }

    except Exception as e:
        raise HTTPException(status_code=500, detail="Gemini API 錯誤：" + str(e))
