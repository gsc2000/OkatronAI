"""クライアントのリクエスト内容と、サーバーの処理内容を紐付ける作業"""
from fastapi import APIRouter, WebSocket





import websockets
import json
import asyncio
import time

import numpy as np
import cv2
import base64

router = APIRouter()







@router.websocket("/ws/img") # 画像のみ要求
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        async with websockets.connect('ws://172.18.0.10:8050') as okatron_server_sock:
                # print("img1")
                await okatron_server_sock.send(json.dumps({"img": "req"}))
                img = await okatron_server_sock.recv()
                # print("img1 recv")
                await websocket.send_bytes(img)


