
import os
import sys

import argparse

import asyncio

from fastapi import FastAPI, WebSocket
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.requests import Request
import FastapiControllers

import uvicorn

from OkatronServer import OkatronServer
from OkatronState import OkatronState

def myArgParser() -> argparse.Namespace:
    """引数を処理する"""
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--config', type=str,
                        default='../resource/config/config.yml')

    args = parser.parse_args()
    return args



"""アプリを起動する"""
print("OkatronAI Boot")
args: argparse.Namespace = myArgParser()

app = FastAPI(title='Okatron AI')
current = str(os.path.dirname(os.path.abspath(__file__)))
app.mount("/", StaticFiles(directory=current + "FastAPI/", html=True), name="fastapi")

templates = Jinja2Templates(directory="fastapi")
jinja_env = templates.env  # Jinja2.Environment : filterやglobalの設定用

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('auto.html',
                                      {'request': request})

# @app.get('/video_feed')
# async def video_feed():
#     """Video streaming route. Put this in the src attribute of an img tag."""
#     return  StreamingResponse(gen(mp.MainProcessing(CONFIG)),
#                     media_type='multipart/x-mixed-replace; boundary=frame')

# @app.websocket("/ws/req") # 画像とユーザリクエスト
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     async with websockets.connect('ws://172.18.0.10:8050') as okatron_server_sock:
#         while True:
#             await okatron_server_sock.send(json.dumps({"type": "connection"}))
#             img = await okatron_server_sock.recv()
#             await websocket.send_bytes(img)

state: OkatronState = OkatronState(args.config)
server: OkatronServer = OkatronServer(state)

asyncio.run(server.run())
uvicorn.run(app=app, host="0.0.0.0", port=8000)