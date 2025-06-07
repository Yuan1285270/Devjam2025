from fastapi import FastAPI, Request
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# 設定 Gemini API 的 URL 和金鑰
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        message = data.get("message")
        if not message:
            return {"error": "請提供 message 欄位"}

        # 構建符合 Gemini API 的格式
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": message
                        }
                    ]
                }
            ]
        }

        response = requests.post(
            GEMINI_URL,
            headers={"Content-Type": "application/json"},
            json=payload
        )

        result = response.json()
        print("📦 Gemini 回傳內容：", result)

        if "candidates" in result:
            reply = result["candidates"][0]["content"]["parts"][0]["text"]
            return {"response": reply}
        else:
            return {"error": result.get("error", {}), "message": "❌ Gemini API 回傳錯誤格式"}

    except Exception as e:
        return {"error": f"❌ 請求失敗：{str(e)}"}
