import os
import sys

from fastapi import FastAPI, Form
import uvicorn

import asyncio

from fastapi.responses import HTMLResponse, StreamingResponse
from starlette.templating import Jinja2Templates  # new
from starlette.requests import Request

from App import main_app
from UserIO import UserReq

app = FastAPI(title='Okatron AI', websocket_ping_interval=None)

templates = Jinja2Templates(directory="../resource/html")
jinja_env = templates.env  # Jinja2.Environment : filterやglobalの設定用
start_processing = False


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html',
                                      {'request': request})

okatron = main_app()
async def gen(okatron: main_app):
    while True:
        # if start_processing:
        # try:
        frame = okatron.server.run()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        await asyncio.sleep(0)
        # else:
        #     break
        # except asyncio.CancelledError:
        #     pass
        # except:
        #     break
            # print("caught cancelled error")

@app.get('/video_feed', response_class=HTMLResponse)
async def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return  StreamingResponse(gen(okatron), media_type='multipart/x-mixed-replace; boundary=frame')

@app.post("/", response_class=HTMLResponse)
async def process_image(request: Request, start: str = Form(default=''), stop: str = Form(default='')):
    if start == 'Start':
        okatron.server.user_io = UserReq.START
    elif stop == 'Stop':
        okatron.server.user_io = UserReq.STOP
    return templates.TemplateResponse("index.html", {"request": request})

uvicorn.run(app=app, port=8000)