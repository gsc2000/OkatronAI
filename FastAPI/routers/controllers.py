"""クライアントのリクエスト内容と、サーバーの処理内容を紐付ける作業"""
from fastapi import APIRouter, WebSocket

from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

import websockets
import json
import asyncio
import time

import numpy as np
import cv2
import base64

router = APIRouter()

templates = Jinja2Templates(directory="web")
jinja_env = templates.env  # Jinja2.Environment : filterやglobalの設定用

# class Okatronserver():
#     def __init__(self) -> None:
#         pass


#     async def okatronserver():
#         async with websockets.connect('ws://172.18.0.10:8050') as okatron_server_sock:
#             while True:
#                 await okatron_server_sock.send(json.dumps({"type": "connection"}))
#                 img = await okatron_server_sock.recv()

#                 yield img



@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html',
                                      {'request': request})

@router.websocket("/ws/img") # 画像のみ要求
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    async with websockets.connect('ws://172.18.0.10:8050') as okatron_server_sock:
        while True:
            await okatron_server_sock.send(json.dumps({"img": "req"}))
            img = await okatron_server_sock.recv()
            await websocket.send_bytes(img)

# @router.websocket("/ws/req") # 画像とユーザリクエスト
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     async with websockets.connect('ws://172.18.0.10:8050') as okatron_server_sock:
#         while True:
#             await okatron_server_sock.send(json.dumps({"type": "connection"}))
#             img = await okatron_server_sock.recv()
#             await websocket.send_bytes(img)
