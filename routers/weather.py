from fastapi import APIRouter, HTTPException, Query
import requests
import os
from dotenv import load_dotenv
import traceback

load_dotenv()
router = APIRouter()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

@router.get("/weather")
async def get_weather(lat: float = Query(...), lon: float = Query(...)):
    if not WEATHER_API_KEY:
        return {
            "氣溫": "無法查詢",
            "濕度": "無法查詢",
            "風速": "無法查詢",
            "天氣": "無法查詢",
            "降雨機率": "無法查詢",
            "錯誤": "❌ 找不到 WEATHER_API_KEY",
        }

    try:
        response = requests.get(
            "https://api.openweathermap.org/data/3.0/onecall",
            params={
                "lat": lat,
                "lon": lon,
                "appid": WEATHER_API_KEY,
                "units": "metric",
                "exclude": "minutely,daily,alerts",
                "lang": "zh_tw"
            }
        )

        if response.status_code != 200:
            return {
                "氣溫": "無法查詢",
                "濕度": "無法查詢",
                "風速": "無法查詢",
                "天氣": "無法查詢",
                "降雨機率": "無法查詢",
                "錯誤": f"OpenWeather 回傳失敗：{response.status_code}",
                "詳細": response.text
            }

        result = response.json()

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
            "降雨機率": f"{rain_prob}%",
        }

    except Exception as e:
        err_detail = traceback.format_exc()
        return {
            "氣溫": "無法查詢",
            "濕度": "無法查詢",
            "風速": "無法查詢",
            "天氣": "無法查詢",
            "降雨機率": "無法查詢",
            "錯誤": str(e),
            "追蹤": err_detail
        }
