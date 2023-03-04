
"""Webサーバ、WebAPI"""
import os
import sys
import argparse

import asyncio

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.encoders import jsonable_encoder
from fastapi.requests import Request
from pydantic import BaseModel

from uvicorn import Config, Server

import cv2
from io import BytesIO

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

# Index
# ----------------------------------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    server.state.mode = Mode.NONE
    server.state.status = Status.NONE
    return templates.TemplateResponse('index.html',
                                      {'request': request})

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
async def updateImage():
    while True:
        try:
            frame = server.state.img.copy()
            frame = cv2.imencode('.jpg', frame)[1].tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            await asyncio.sleep(0.01)
        except:
            pass

@app.get('/video_feed')
async def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return  StreamingResponse(updateImage(), media_type='multipart/x-mixed-replace; boundary=frame')

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
class ManualReq(BaseModel):
    kind: str
    direction: str

@app.post("/mode/2/crosskey")
async def manual_req(req: ManualReq):
    if req.kind == "move":
        msg = [{req.kind: [req.direction, [-1, -1]]}]
    elif req.kind == "camera":
        msg = [{req.kind: [req.direction, -1]}]
    await state.q_user_req.put(msg)
    return {"kind": req.kind, "direction": req.direction}

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

if __name__ == "__main__":
    """アプリを起動する"""
    print("OkatronAI Boot")
    loop = asyncio.get_event_loop()

    args: argparse.Namespace = myArgParser()
    state: OkatronState = OkatronState(args.config)
    server: OkatronServer = OkatronServer(state)

    config = Config(app=app, host="0.0.0.0", port=8000)
    uvicorn_server = Server(config)

    task1 = loop.create_task(server.run())
    task2 = loop.create_task(uvicorn_server.serve())

    loop.run_until_complete(asyncio.gather(task1, task2))