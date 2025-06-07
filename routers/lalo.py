from fastapi import APIRouter, HTTPException
import os
import requests

router = APIRouter()

# 從環境變數中取得 OpenWeather API 金鑰
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
GEOCODING_URL = "http://api.openweathermap.org/geo/1.0/direct"

@router.get("/lalo")
async def get_coordinates(city: str = "Taichung"):
    if not WEATHER_API_KEY:
        raise HTTPException(status_code=500, detail="❌ 缺少 WEATHER_API_KEY")

    params = {
        "q": city,
        "limit": 1,
        "appid": WEATHER_API_KEY
    }

    try:
        response = requests.get(GEOCODING_URL, params=params)
        data = response.json()

        if response.status_code != 200 or not data:
            return {"error": "找不到該城市的經緯度，請確認名稱是否正確"}

        location = data[0]
        return {
            "城市": location.get("name"),
            "緯度": location.get("lat"),
            "經度": location.get("lon")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"📍 地理定位 API 錯誤：{str(e)}")
