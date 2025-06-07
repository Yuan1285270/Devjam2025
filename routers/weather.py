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
            "https://api.openweathermap.org/data/2.5/onecall",  # ✅ 使用 One Call API v2.5
            params={
                "lat": lat,
                "lon": lon,
                "appid": WEATHER_API_KEY,
                "units": "metric",
                "exclude": "minutely,daily,alerts",
                "lang": "zh_tw"
            }
        )
        result = response.json()
        print("🌦️ One Call 天氣資料：", result)

        if "current" not in result:
            raise HTTPException(status_code=500, detail="❌ 無法取得天氣資料")

        # 安全地取得降雨機率（pop）
        rain_prob = 0
        try:
            rain_prob = int(result.get("hourly", [{}])[0].get("pop", 0) * 100)
        except:
            rain_prob = 0

        return {
            "氣溫": f"{result['current'].get('temp', '暫無')}℃",
            "濕度": f"{result['current'].get('humidity', '暫無')}%",
            "風速": f"{result['current'].get('wind_speed', '暫無')} m/s",
            "天氣": result['current']['weather'][0].get('description', '暫無'),
            "降雨機率": f"{rain_prob}%"
        }

    except Exception as e:
        print("🚨 天氣 API 錯誤：", e)
        raise HTTPException(status_code=500, detail="❌ 天氣 API 查詢失敗")
