import uvicorn
from fastapi import FastAPI , APIRouter
import socketio
from schema import Message

app = FastAPI()
connected_clients ={}
sio = socketio.AsyncServer(async_mode='asgi')
socket_app = socketio.ASGIApp(sio, app)


@sio.event
async def connect(sid,environ):
    """Handle client connections."""
    try:
        print(f"Client connected: {sid}")
        # connected_clients[sid] = sid  
        # await sio.emit("response", {"data": "Welcome to the server!"})
    except Exception as e:
        await sio.emit("error", {'data': f"Error in connection {e} {sid}"})

@sio.event
async def disconnect(sid):
    """Handle client disconnections."""
    try:
        print(f"Client disconnected: {sid}")
        if sid in connected_clients:
            del connected_clients[sid]  
        await sio.emit("error", {'data': f"Error in disconnect {e} {sid}"})
    except Exception as e:
        print(e)

@sio.event
async def message(sid, data):
    """Handle incoming messages from clients."""
    print(f"Received message from {sid}: {data}")
    await sio.emit("response", {"data": "Message received!"})


async def send_message_to_client(socket_id: str, msg: str):
    """Send a message to a specific client."""
    if socket_id in connected_clients:
        await sio.emit("response", {"data": msg}, to=socket_id)
        print(f"Message sent to client {socket_id}: {msg}")
    else:
        print(f"Client with socket_id {socket_id} not connected")


@app.post("/send-message/")
async def send_message(msg: Message):
    """Handle the POST request to send a message."""
    if msg.socket_id:
        await send_message_to_client(msg.socket_id, msg.msg)
        return {"status": "Message sent to specific client", "message": msg.msg, "socket_id": msg.socket_id}
    else:
        for client_id in connected_clients:
            await send_message_to_client(client_id, msg.msg)
        return {"status": "Message broadcasted to all clients", "message": msg.msg}



# Run the server using Uvicorn
if __name__ == "__main__":
    uvicorn.run(socket_app, host="0.0.0.0", port=8000)

