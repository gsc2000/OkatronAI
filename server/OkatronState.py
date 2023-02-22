"""状態管理"""

import enum

from UserIO import UserIO
import DataBaseapi as db
from Captor.WebCamera import WebCamera
# from Captor.WebCamera import NullCamera as WebCamera
from Inferencer.YOLOv5Detector import YOLOv5Detector
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

        # self._user_io = UserIO()
        self._captor = WebCamera(config["camera"])
        self.yolov5 = YOLOv5Detector(config["yolov5"])
        self.yolo_info = config["yolov5"]
        self._cont = OkatronController()

        print("OkatronState Setup")

    def resetInferencerModel(self, weight: str) -> None:
        """AIモデルをリセット
        Args:
            weight: モデルの重み
        """
        self.yolov5.setupModel(weight)

    def resetInferencerInfo(self) -> None:
        """
        Args:
            info: YOLOの推論設定情報
        """
        self.yolov5.setupInfo(tuple(self.yolo_info["image"]), self.yolo_info["conf"],
                              self.yolo_info["iou"], self.yolo_info["det_class"])

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

    # @property
    # def user_io(self):
    #     return self._user_io
    @property
    def captor(self):
        return self._captor