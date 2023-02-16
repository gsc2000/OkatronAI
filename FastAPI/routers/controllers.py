"""クライアントのリクエスト内容と、サーバーの処理内容を紐付ける作業"""
from fastapi import APIRouter

from fastapi.responses import HTMLResponse, StreamingResponse
from starlette.templating import Jinja2Templates  # new
from starlette.requests import Request

import numpy as np
import cv2

router = APIRouter()

templates = Jinja2Templates(directory="html")
jinja_env = templates.env  # Jinja2.Environment : filterやglobalの設定用

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html',
                                      {'request': request})

tmp = np.zeros((320, 240, 3), dtype="uint8")
tmp = cv2.imencode('.jpg', tmp)[1].tobytes()
img = (b'--frame\r\n'
       b'Content-Type: image/jpeg\r\n\r\n' + tmp + b'\r\n')
@router.get('/video_feed', response_class=HTMLResponse)
async def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return  StreamingResponse(img, media_type='multipart/x-mixed-replace; boundary=frame')

def admin(request: Request):
    return templates.TemplateResponse('admin.html',
                                      {'request': request,
                                       'username': 'admin'})