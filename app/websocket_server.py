from fastapi import WebSocket, WebSocketDisconnect
from app import state
from app.logger import logger

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    state.connected_clients.append(websocket)
    logger.info(f"Client connected: {websocket.client}")

    try:
        while True:
            await websocket.receive_text()  # Optional: Keep connection alive
    except WebSocketDisconnect:
        logger.info(f"Client disconnected: {websocket.client}")
        state.connected_clients.remove(websocket)


async def broadcast_price_updates():
    while True:
        price_update = await state.price_update_queue.get()

        # Send to all connected clients
        disconnected = []
        for client in state.connected_clients:
            try:
                await client.send_json(price_update)
            except Exception as e:
                logger.warning(f"Failed to send to client: {e}")
                disconnected.append(client)

        # Remove disconnected clients
        for client in disconnected:
            if client in state.connected_clients:
                state.connected_clients.remove(client)
