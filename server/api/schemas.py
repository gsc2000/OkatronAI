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

class UploadJson(BaseModel):
    unit1: str
    value1: str
    unit2: str
    value2: str
    unit3: str
    value3: str
    unit4: str
    value4: str
    unit5: str
    value5: str