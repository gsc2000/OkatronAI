"""状態管理"""
import enum
import numpy as np
import asyncio

import DataBaseapi as db
from Captor.WebCamera import WebCamera
# from Captor.DemoCamera import DemoCamera as WebCamera
# from Captor.WebCamera import NullCamera as WebCamera
from Inferencer.YOLOv5Detector import YOLOv5Detector
from Inferencer.FaceDetector import FaceDetector
from MotorController.OkatronController import OkatronController

class Mode(enum.Enum):
    """OkatronServerのモード"""
    NONE: str = ""
    AUTO: str = "Auto"
    MANUAL: str = "Manual"
    PROGRAM: str = "Program"

class Status(enum.Enum):
    """Okatronのステータス"""
    NONE: str = "None"
    IDLE: str = "Idle"
    WORKING: str = "Working"

class OkatronState():
    """Okatronの内部状態
    Okatronで使用する機能はここで制御する
    """

    def __init__(self, config_path) -> None:
        config = db.readConfig(config_path)

        self._mode: Mode = Mode(config["base"]["mode"])
        self._status: Status = Status.IDLE

        self.img = np.zeros((240, 320, 3), dtype="uint8")

        self.captor = WebCamera(config["camera"])

        self.yolov5 = YOLOv5Detector(config["yolov5"])
        self.yolo_info = config["yolov5"]

        self.facecascade = FaceDetector()

        self.q_user_req = asyncio.Queue() # FastAPI <-> Okatron
        self.q_cont_msg = asyncio.Queue() # Server <-> Controller
        self.cont = OkatronController(self.q_cont_msg)

        print("OkatronState Setup")

    def resetInferencerModel(self, weight: str) -> None:
        """AIモデルをリセット
        Args:
            weight: モデルの重み
        """
        self.yolov5.setupModel(weight)

    def resetInferencerInfo(self, new_params) -> None:
        """
        Args:
            info: YOLOの推論設定情報
        """
        print(new_params)
        self.yolov5.setupInfo(tuple(new_params["image"]), new_params["conf"],
                              new_params["iou"], new_params["det_class"])

    @property
    def mode(self):
        return self._mode
    @mode.setter
    def mode(self, mode):
        self._mode = mode
    @property
    def status(self):
        return self._status
    @status.setter
    def status(self, status):
        self._status = status