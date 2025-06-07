from fastapi import FastAPI, Request
import google.generativeai as genai
import os

app = FastAPI()

# 使用環境變數讀取 Gemini API 金鑰
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        message = data.get("message")
        if not message:
            return {"error": "請提供 message 欄位"}

        response = model.generate_content(message)
        return {"response": response.text}
    
    except Exception as e:
        return {"error": f"解析失敗，請提供正確的 JSON 結構：{str(e)}"}

