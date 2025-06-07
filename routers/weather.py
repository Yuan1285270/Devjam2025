from fastapi import APIRouter, HTTPException, Query
import requests
import os
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

@router.get("/weather")
def get_weather(city: str = Query(..., description="城市名稱")):
    if not WEATHER_API_KEY:
        raise HTTPException(status_code=500, detail="缺少天氣 API 金鑰")

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=zh_tw"
    )
    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            return {"error": "查不到此城市的天氣資料"}

        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return {
            "city": city,
            "temperature": f"{temp}°C",
            "description": weather
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查詢天氣失敗：{e}")
