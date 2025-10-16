from typing import Dict, List
from fastapi import WebSocket
import asyncio

latest_price: Dict[str,any] = {}

price_update_queue = asyncio.Queue()
connected_clients: List[WebSocket] = []