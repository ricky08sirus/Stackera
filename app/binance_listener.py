import asyncio
import websockets
import json
from app.logger import logger
from app.config import settings
from app import state

async def listen_to_binance():
    url = settings.BINANCE_WS_URL

    while True:
        try:
            logger.info(f"Connecting to Binance WebSocket: {url}")
            async with websockets.connect(url) as websocket:
                while True:
                    msg = await websocket.recv()
                    data = json.loads(msg)

                    # Extract relevant fields
                    symbol = data.get("s")      # Symbol
                    price = data.get("c")       # Last price
                    change = data.get("P")      # 24h % change
                    ts = data.get("E")          # Event time

                    parsed = {
                        "symbol": symbol,
                        "price": price,
                        "change_percent": change,
                        "timestamp": ts
                    }

                    # Save to state
                    state.latest_price[symbol] = parsed

                    # Optional: publish to queue
                    await state.price_update_queue.put(parsed)

                    logger.info(f"Updated {symbol} price: {parsed}")

        except Exception as e:
            logger.error(f"Binance connection error: {e}. Reconnecting in 5 seconds...")
            await asyncio.sleep(5)
