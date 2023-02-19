from fastapi import FastAPI
from fastapi.websockets import WebSocket as ws
import websockets

from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import uvicorn
import json

import asyncio

app = FastAPI()
templates = Jinja2Templates(directory="web")
jinja_env = templates.env  # Jinja2.Environment : filterやglobalの設定用

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index_tmp.html',
                                      {'request': request})

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: ws):
#     try:
#         await websocket.accept()

#         while True:
#             # 指定された画像をロードする
#             with open("test.jpg", "rb") as image_file:
#                 image_bytes = image_file.read()
#             print(type(image_bytes))

#             # WebSocketを使用して画像を送信する
#             await websocket.send_bytes(image_bytes)

#             await asyncio.sleep(0.1)
#     except ws.exceptions.WebSocketException:
#         await asyncio.sleep(1)

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: ws):
#     await websocket.accept()
#     async with ws.connect('ws://172.19.0.3:8050') as websocket_server:
#         print("bbb")
#         await websocket_server.send(json.dumps({"type": "connection"}))
#         while True:
#             data = await websocket_server.recv()
#             await websocket.send_text(data)
#             if data == "finish":
#                 break

@app.websocket("/ws1")
async def websocket_endpoint(websocket: ws):
    await websocket.accept()
    async with websockets.connect('ws://172.19.0.3:8050') as python_websocket:
        while True:
            print("bbb")
            await python_websocket.send(json.dumps({"type": "connection"}))
            img = await python_websocket.recv()
            print(type(img))
            await websocket.send_bytes(img)

@app.websocket("/ws2")
async def websocket_endpoint2(websocket: ws):
    await websocket.accept()
    async with websockets.connect('ws://172.19.0.3:8050') as python_websocket:
        while True:
            print("bbb")
            await python_websocket.send(json.dumps({"type": "connection"}))
            img = await python_websocket.recv()
            print(type(img))
            await websocket.send_bytes(img)



# コンソールで [$ uvicorn run:app --reload]でも可
uvicorn.run(app=app, host="0.0.0.0", port=8000)