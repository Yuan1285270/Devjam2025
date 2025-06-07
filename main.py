from fastapi import FastAPI
from routers import chat
from routers import weather
from routers import lalo

app = FastAPI()
app.include_router(chat.router)
app.include_router(weather.router)
app.include_router(lalo.router)
