from fastapi import FastAPI, Request
import google.generativeai as genai
import os

app = FastAPI()

# 使用環境變數讀取 Gemini API 金鑰
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    message = body.get("message", "")
    
    if not message:
        return {"error": "No message provided"}
    
    try:
        response = model.generate_content(message)
        return {"response": response.text}
    except Exception as e:
        return {"error": str(e)}
