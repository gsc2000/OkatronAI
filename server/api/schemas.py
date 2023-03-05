"""schemas"""
from pydantic import BaseModel

class UseAI(BaseModel):
    switch: bool

class ModelSize(BaseModel):
    model: str

class ModelParam(BaseModel):
    classes: str
    imgsize: str
    iou: str
    conf: str

class ManualReq(BaseModel):
    kind: str
    direction: str