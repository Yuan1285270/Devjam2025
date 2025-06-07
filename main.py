from fastapi import FastAPI
from routers import chat
from routers import weather

app = FastAPI()
app.include_router(chat.router)
app.include_router(weather.router)