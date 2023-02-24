
import os
import sys

import argparse


import asyncio

from fastapi import FastAPI, WebSocket
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.encoders import jsonable_encoder
from fastapi.requests import Request
from pydantic import BaseModel

import uvicorn

import cv2


from OkatronServer import OkatronServer
from OkatronState import OkatronState, Mode, Status
import queue

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

# Index
# ----------------------------------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html',
                                      {'request': request}) #, "button2_active": True})

@app.get("/mode/{button_id}")
async def toggle_button(request: Request, button_id: int):
    if button_id == 1:
        state.mode = Mode.AUTO
        return templates.TemplateResponse("auto.html",
                                          {"request": request})
    elif button_id == 2:
        state.mode = Mode.MANUAL
        return templates.TemplateResponse("manual.html",
                                          {"request": request})
    elif button_id == 3:
        state.mdoe = Mode.PROGRAM
        return templates.TemplateResponse("program.html",
                                          {"request": request})

# Common
# ----------------------------------------------------------------------------------------------------
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

# Auto
# ----------------------------------------------------------------------------------------------------
@app.post("/mode/1/ai_start")
async def ai_start():
    state.status = Status.WORKING

@app.post("/mode/1/ai_stop")
async def ai_stop():
    state.status = Status.IDLE

@app.post("/mode/1/class1")
async def class1():
    state.yolo_info["det_class"] = 0
    state.resetInferencerInfo()

@app.post("/mode/1/class2")
async def class2():
    state.yolo_info["det_class"] = 16
    state.resetInferencerInfo()

@app.post("/mode/1/class3")
async def class3():
    state.yolo_info["det_class"] = 67
    state.resetInferencerInfo()

# Manual
# ----------------------------------------------------------------------------------------------------
@app.get("/mode/2/move_top")
async def manual_move_top():
    print("move_top")
    messe = {}
    messe["key"] = "move_top"
    q_messe.put(messe)

@app.get("/mode/2/move_left")
async def manual_move_left():
    print("move_left")
    messe = {}
    messe["key"] = "move_left"
    q_messe.put(messe)

@app.get("/mode/2/move_right")
async def manual_move_right():
    print("move_right")
    messe = {}
    messe["key"] = "move_right"
    q_messe.put(messe)

@app.get("/mode/2/move_bottom")
async def manual_move_bottom():
    print("move_bottom")
    messe = {}
    messe["key"] = "move_bottom"
    q_messe.put(messe)

@app.get("/mode/2/camera_top")
async def manual_camera_top():
    print("camera_top")
    messe = {}
    messe["key"] = "camera_top"
    q_messe.put(messe)

@app.get("/mode/2/camera_left")
async def manual_camera_left():
    messe = {}
    messe["key"] = "camera_left"
    q_messe.put(messe)

@app.get("/mode/2/camera_right")
async def manual_camera_right():
    print("camera_right")
    messe = {}
    messe["key"] = "camera_right"
    q_messe.put(messe)

@app.get("/mode/2/camera_bottom")
async def manual_camera_bottom():
    print("camera_bottom")
    messe = {}
    messe["key"] = "camera_bottom"
    q_messe.put(messe)

# Program
# ----------------------------------------------------------------------------------------------------
class UploadJson(BaseModel):
    op: str
    content: str

@app.post("/mode/3/info")
async def prog_info(item: UploadJson):
    print(item)
    data = jsonable_encoder(item)
    print((data))


"""アプリを起動する"""
print("OkatronAI Boot")
args: argparse.Namespace = myArgParser()
state: OkatronState = OkatronState(args.config)
q_messe = queue.Queue(maxsize=1)
server: OkatronServer = OkatronServer(state, q_messe)

uvicorn.run(app=app, host="0.0.0.0", port=8000)