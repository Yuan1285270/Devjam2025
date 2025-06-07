from fastapi import FastAPI, Request
from google import genai
import os

app = FastAPI()

# 取得 API 金鑰
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        message = data.get("message")
        if not message:
            return {"error": "請提供 message 欄位"}

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=message
        )
        return {"response": response.text}
    except Exception as e:
        return {"error": str(e)}
@app.get("/")
async def root():
    return {"message": "歡迎使用 Gemini API 聊天機器人！請 POST 到 /chat 端點進行對話。"}