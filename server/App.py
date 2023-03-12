
import os
import sys

import argparse


import asyncio
import threading

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
        state.status = Status.IDLE
        return templates.TemplateResponse("auto.html",
                                          {"request": request})
    elif button_id == 2:
        state.mode = Mode.MANUAL
        state.status = Status.IDLE
        return templates.TemplateResponse("manual.html",
                                          {"request": request})
    elif button_id == 3:
        state.mode = Mode.PROGRAM
        state.status = Status.IDLE
        return templates.TemplateResponse("program.html",
                                          {"request": request})

# Common
# ----------------------------------------------------------------------------------------------------
async def gen():
    while True:
        try:
            # frame = await q_img.get()
            frame = server.run()
            frame = cv2.imencode('.jpg', frame)[1].tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            await asyncio.sleep(0)
        except:
            pass

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
    # print("move_top")
    msg = {"move": ["top", -1], "camera": [None, None]}
    q_user_msg.put(msg)

@app.get("/mode/2/move_left")
async def manual_move_left():
    # print("move_left")
    msg = {"move": ["left", -1], "camera": [None, None]}
    q_user_msg.put(msg)

@app.get("/mode/2/move_right")
async def manual_move_right():
    # print("move_right")
    msg = {"move": ["right", -1], "camera": [None, None]}
    q_user_msg.put(msg)

@app.get("/mode/2/move_bottom")
async def manual_move_bottom():
    # print("move_bottom")
    msg = {"move": ["bottom", -1], "camera": [None, None]}
    q_user_msg.put(msg)

@app.get("/mode/2/move_stop")
async def manual_move_bottom():
    # print("move_stop")
    msg = {"move": ["stop", -1], "camera": [None, None]}
    q_user_msg.put(msg)

@app.get("/mode/2/camera_top")
async def manual_camera_top():
    # print("camera_top")
    msg = {"move": [None, None], "camera": ["top", -1]}
    q_user_msg.put(msg)

@app.get("/mode/2/camera_left")
async def manual_camera_left():
    msg = {"move": [None, None], "camera": ["left", -1]}
    q_user_msg.put(msg)

@app.get("/mode/2/camera_center")
async def manual_camera_center():
    msg = {"move": [None, None], "camera": ["center", -1]}
    q_user_msg.put(msg)

@app.get("/mode/2/camera_right")
async def manual_camera_right():
    # print("camera_right")
    msg = {"move": [None, None], "camera": ["right", -1]}
    q_user_msg.put(msg)

@app.get("/mode/2/camera_bottom")
async def manual_camera_bottom():
    # print("camera_bottom")
    msg = {"move": [None, None], "camera": ["bottom", -1]}
    q_user_msg.put(msg)

@app.get("/mode/2/camera_stop")
async def manual_camera_bottom():
    # print("camera_stop")
    msg = {"move": [None, None], "camera": ["stop", -1]}
    q_user_msg.put(msg)

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
q_user_msg = queue.Queue(maxsize=1) # FastAPI <-> OkatronServer
q_server_msg = queue.Queue(maxsize=1) # OkatronServer <-> OkatronController
server: OkatronServer = OkatronServer(state, q_user_msg, q_server_msg)

if __name__ == "__main__":
    th = threading.Thread(target=state.cont.run, args=(q_server_msg,))
    th.daemon = True
    th.start()
    uvicorn.run(app=app, host="0.0.0.0", port=8000)