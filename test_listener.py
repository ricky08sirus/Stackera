import asyncio
from app.binance_listener import listen_to_binance

if __name__ == "__main__":
    try:
        asyncio.run(listen_to_binance())
    except KeyboardInterrupt:
        print("\n[Stopped by user]")
