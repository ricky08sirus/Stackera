from fastapi import FastAPI,WebSocket
from app.config import settings
from app.logger import logger
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from app.binance_listener import listen_to_binance
from app.websocket_server import websocket_endpoint, broadcast_price_updates

import asyncio

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
async def startup_event():
    logger.info("Starting Crypto Streamer App...")
    logger.info(f"Connecting to Binance WebSocket: {settings.BINANCE_WS_URL}")
    asyncio.create_task(listen_to_binance())
    asyncio.create_task(broadcast_price_updates())   
    # Binance Listener and WebSocket server will be added later

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Crypto Streamer App...")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_handler(websocket: WebSocket):
    await websocket_endpoint(websocket)
