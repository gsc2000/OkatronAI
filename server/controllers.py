"""クライアントのリクエスト内容と、サーバーの処理内容を紐付ける作業"""
import os
import sys

import asyncio

from fastapi import APIRouter

from fastapi.responses import HTMLResponse, StreamingResponse
from starlette.templating import Jinja2Templates  # new
from starlette.requests import Request

from App import main_app

router = APIRouter()

templates = Jinja2Templates(directory="../resource/html")
jinja_env = templates.env  # Jinja2.Environment : filterやglobalの設定用

start_processing = False

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html',
                                      {'request': request})

okatron = main_app()
async def gen(okatron: main_app):
    while True:
        if start_processing:
            frame = okatron.server.run()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            # await asyncio.sleep(0.01)
        else:
            break
        # except asyncio.CancelledError:
        #     print("caught cancelled error")

@router.get('/video_feed', response_class=HTMLResponse)
async def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return  StreamingResponse(gen(okatron), media_type='multipart/x-mixed-replace; boundary=frame')

@router.get("/start", response_class=HTMLResponse)
async def start(request: Request):
    okatron.server.user_io = True
    return templates.TemplateResponse('index.html',
                                      {'request': request})