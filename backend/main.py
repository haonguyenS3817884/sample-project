from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

app = FastAPI()

class WebsocketService:
    def __init__(self):
        self.connections: list[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)
    
    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def broadcast_message(self, message: str):
        for connection in self.connections:
            await connection.send_text(message)

@app.get("/")
async def index():
    return {"message": "place"}

websocket_service: WebsocketService = WebsocketService()

@app.websocket("/ws/{client_id}")
async def websocket_index(websocket: WebSocket, client_id: str):
    await websocket_service.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket_service.send_message(data, websocket)
            await websocket_service.broadcast_message(data)
    except WebSocketDisconnect:
        websocket_service.disconnect(websocket)
        await websocket_service.broadcast_message("Client {client_id} has left the conversation".format(client_id=client_id))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)