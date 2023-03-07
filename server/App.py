
"""Webサーバ、WebAPI"""
import os
import sys
import argparse
import asyncio
import cv2

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.requests import Request
from uvicorn import Config, Server

from api import schemas
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
    """初期画面"""
    server.state.mode = Mode.NONE
    server.state.status = Status.NONE
    return templates.TemplateResponse('index.html',
                                      {'request': request}) #, "button2_active": True})

@app.get("/mode/{button_id}")
async def swithPage(request: Request, button_id: int):
    """画面遷移"""
    state.status = Status.IDLE
    if button_id == 1:
        state.mode = Mode.AUTO
        return templates.TemplateResponse("auto.html",
                                          {"request": request})
    elif button_id == 2:
        state.mode = Mode.MANUAL
        return templates.TemplateResponse("manual.html",
                                          {"request": request})
    elif button_id == 3:
        state.mode = Mode.PROGRAM
        return templates.TemplateResponse("program.html",
                                          {"request": request})

# Common
# ----------------------------------------------------------------------------------------------------
async def updateImage():
    """画像更新"""
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
    """表示画像"""
    return  StreamingResponse(updateImage(), media_type='multipart/x-mixed-replace; boundary=frame')

# Auto
# ----------------------------------------------------------------------------------------------------
@app.post("/mode/1/ai")
async def switchAI(req: schemas.UseAI):
    if req.switch == True:
        state.status = Status.WORKING
    elif req.switch == False:
        state.status = Status.IDLE

    return {"Success": True}

@app.post("/mode/1/modelsize")
async def switchModelSize(req: schemas.ModelSize):
    if req.model == "nano":
        pass
    elif req.model == "small":
        pass
    elif req.model == "large":
        pass
    return {"Success": True}

@app.post("/mode/1/param")
async def selectParam(req: schemas.ModelParam):
    print(req)
    new_params = {}
    if req.classes == "1":
        new_params["det_class"] = 0
    elif req.classes == "2":
        new_params["det_class"] = 16
    elif req.classes == "3":
        new_params["det_class"] = 67

    new_params["image"] = (int(req.imgsize), int(req.imgsize))
    if req.iou == "":
        new_params["iou"] = float(state.yolo_info["iou"])
    else:
        new_params["iou"] = float(req.iou)
    if req.conf == "":
        new_params["conf"] = float(state.yolo_info["conf"])
    else:
        new_params["conf"] = float(req.conf)

    state.resetInferencerInfo(new_params)
    return {"Success": True}

# Manual
# ----------------------------------------------------------------------------------------------------
@app.post("/mode/2/crosskey")
async def manual_req(req: schemas.ManualReq):
    """サーバへメッセージ送付"""
    msg = [req.kind, req.direction, [None, None]]
    await state.q_user_req.put(msg)
    return {"kind": req.kind, "direction": req.direction}

# Program
# ----------------------------------------------------------------------------------------------------
# class UploadJson(BaseModel):
#     op: str
#     content: str

# @app.post("/mode/3/info")
# async def prog_info(item: UploadJson):
#     print(item)
#     data = jsonable_encoder(item)
#     print((data))

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