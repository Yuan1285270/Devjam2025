from fastapi import APIRouter, HTTPException, Query
import requests
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

@router.get("/weather")
async def get_weather(lat: float = Query(...), lon: float = Query(...)):
    if not WEATHER_API_KEY:
        raise HTTPException(status_code=500, detail="❌ 缺少天氣 API 金鑰")

    try:
        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather",
            params={
                "lat": lat,
                "lon": lon,
                "appid": WEATHER_API_KEY,
                "units": "metric",
                "lang": "zh_tw"
            }
        )
        result = response.json()
        print("🌦️ 天氣資料：", result)

        if "main" not in result:
            raise HTTPException(status_code=500, detail="❌ 無法取得天氣資料")

        return {
            "氣溫": f"{result['main']['temp']}℃",
            "濕度": f"{result['main']['humidity']}%",
            "風速": f"{result['wind']['speed']} m/s",
            "天氣": result['weather'][0]['description']
        }

    except Exception as e:
        print("🚨 天氣 API 錯誤：", e)
        raise HTTPException(status_code=500, detail="❌ 天氣 API 查詢失敗")
