"""状態管理"""

import enum

from UserIO import UserIO
import DataBaseapi as db

class Mode(enum.Enum):
    """OkatronServerのモード"""
    NONE: str = ""
    OPERATION: str = "Operation"
    SETTING: str = "Setting"

class Status(enum.Enum):
    """Okatronのステータス"""
    NONE: str = "None"
    IDLE: str = "Idle"
    WORKING: str = "Working"

class OkatronState():
    """Okatronの内部状態"""

    def __init__(self, config_path) -> None:
        self._mode: Mode = Mode.NONE
        self._status: Status = Status.WORKING

        self.setting(config_path)

    def setting(self, path):
        config = db.readConfig(path)

        self._camera = config["camera"]
        self._yolov5 = config["yolov5"]
        self._yolov5["image"] = (config["yolov5"]["image"]["width"], config["yolov5"]["image"]["height"])


    @property
    def mode(self):
        return self._mode
    @property
    def status(self):
        return self._status
    @status.setter
    def status(self, status):
        self._status = status

    @property
    def camera(self):
        return self._camera
    @property
    def yolov5(self):
        return self._yolov5