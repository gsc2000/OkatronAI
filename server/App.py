
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

import cv2

from OkatronServer import OkatronServer
from OkatronState import OkatronState, Mode, Status

app = FastAPI(title='Okatron AI')
current = str(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory="templates")
jinja_env = templates.env  # Jinja2.Environment : filterやglobalの設定用
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

def myArgParser() -> argparse.Namespace:
    """引数を処理する"""
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--config', type=str,
                        default='../resource/config/config.yml')

    args = parser.parse_args()
    return args



@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html',
                                      {'request': request}) #, "button2_active": True})

@app.get("/mode/{button_id}")
async def toggle_button(request: Request, button_id: int):
    if button_id == 1:
        state.mode = Mode.AUTO
        return templates.TemplateResponse("auto.html",
                                          {"request": request,
                                           "btn1_mode_active": True})
    elif button_id == 2:
        return templates.TemplateResponse("index.html",
                                          {"request": request})

@app.get("/auto/ai/{button_id}")
async def toggle_button(request: Request, button_id: int):
    button1_active = False
    button2_active = False
    if button_id == 1:
        button1_active = True
        state.status = Status.WORKING
    elif button_id == 2:
        button2_active = True
        state.status = Status.IDLE
    return templates.TemplateResponse("auto.html",
                                      {"request": request,
                                       "btn1_ai_active": button1_active,
                                       "btn2_ai_active": button2_active})
@app.get("/auto/class/{button_id}")
async def toggle_button(request: Request, button_id: int):
    button1_active = False
    button2_active = False
    button3_active = False
    if button_id == 1:
        button1_active = True
        state.yolo_info["det_class"] = 0
    elif button_id == 2:
        button2_active = True
        state.yolo_info["det_class"] = 16
    elif button_id == 3:
        button3_active = True
        state.yolo_info["det_class"] = 67
    state.resetInferencerInfo()
    return templates.TemplateResponse("auto.html",
                                      {"request": request,
                                       "btn1_class_active": button1_active,
                                       "btn2_class_active": button2_active,
                                       "btn3_class_active": button3_active})

async def gen():
    while True:
        frame = server.run()
        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        await asyncio.sleep(0)

@app.get('/video_feed')
async def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return  StreamingResponse(gen(),
                    media_type='multipart/x-mixed-replace; boundary=frame')

# @app.websocket("/ws/req") # 画像とユーザリクエスト
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     async with websockets.connect('ws://172.18.0.10:8050') as okatron_server_sock:
#         while True:
#             await okatron_server_sock.send(json.dumps({"type": "connection"}))
#             img = await okatron_server_sock.recv()
#             await websocket.send_bytes(img)


"""アプリを起動する"""
print("OkatronAI Boot")
args: argparse.Namespace = myArgParser()
state: OkatronState = OkatronState(args.config)
server: OkatronServer = OkatronServer(state)

uvicorn.run(app=app, host="0.0.0.0", port=8000)