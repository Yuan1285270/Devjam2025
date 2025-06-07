from fastapi import FastAPI
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv

# 載入 .env（僅本地有效）
load_dotenv()

app = FastAPI()

# 取得 API 金鑰
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# 請求資料模型
class MessageInput(BaseModel):
    message: str

@app.post("/chat", summary="與 Gemini 聊天", tags=["Gemini Chat"])
async def chat(data: MessageInput):
    message = data.message

    if not message:
        return {"error": "請提供 message 內容"}

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": message}
                ]
            }
        ]
    }

    try:
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

    except Exception as e:
        return {"error": f"請求失敗：{str(e)}"}
