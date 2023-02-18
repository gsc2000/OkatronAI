"""YOLOv5"""

import os
import sys
from pathlib import Path
import numpy as np

import torch

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from yolov5_module.utils.augmentations import letterbox
from yolov5_module.utils.general import non_max_suppression, scale_boxes
from yolov5_module.utils.plots import Annotator, colors
from yolov5_module.models.common import DetectMultiBackend

class YOLOv5Detector():
    """YOLOv5の推論"""
    def __init__(self, config) -> None:
        self.device='cpu'  # cuda device, i.e. 0 or 0,1,2,3 or cpu
        self.setupModel(config["weight"])
        self.setupInfo(tuple(config["image"]), config["conf"],
                       config["iou"], config["det_class"])


    def setupModel(self, weight) -> None:
        """
        モデルの設定
        途中で変更する場合はこのメソッドを呼び出して変更する
        Args:
            weight: 使用する重み
        """
        weights = "../resource/model/yolov5/"+weight
        data=ROOT / 'data/coco128.yaml'  # dataset.yaml path
        dnn=False # use OpenCV DNN for ONNX inference
        half=False  # use FP16 half-precision inference

        self.model = DetectMultiBackend(weights, device=self.device, dnn=dnn, data=data, fp16=half)
        self.stride, self.names, self.pt = self.model.stride, self.model.names, self.model.pt

    def setupInfo(self, imgsz, conf_thres, iou_thres, classes) -> None:
        """
        検出設定
        Args:
            imsz: 推論画像サイズ
            conf_thres: コンフィデンス閾値
            iou_thres: IOU閾値
            classes: 検出クラスのフィルタ
        """
        self.imgsz = imgsz
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres
        self.classes = classes
        self.max_det = 5
        self.agnostic_nms = False
        self.augment = False
        self.visualize = False

    def detect(self, img = None) -> torch.Tensor:
        """
        検出処理
        Args:
            img: 推論する画像
        Returns:
            torch.Tensor: 検出結果
        """
        #入力データの前処理
        img, ratio, padding = self.preprocess(img, True)

        # Inference
        pred = self.model(img, augment=self.augment, visualize=self.visualize)
        # NMS
        pred = non_max_suppression(pred, self.conf_thres, self.iou_thres, self.classes, self.agnostic_nms, max_det=self.max_det)
        # 出力結果の事後処理
        # center_pix, num_human_det, obj = self.postprocess(pred, ratio, self.max_det)

        # return center_pix, num_human_det, obj
        return pred[0] # 複数画像を推論できる仕様になっているため、一枚目のみ抽出

    def preprocess(self, img: np.ndarray, fp16: bool=False) -> torch.Tensor:
        """
        前処理
        Args:
            img: 推論画像
            fp16: FP16の設定有無
        Returns:
            torch.Tensor: 処理後の画像s
        """
        # リサイズ結果を取得
        img, ratio, padding = letterbox(img, self.imgsz)
        # Convert
        img = img.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
        img = np.ascontiguousarray(img)
        img: torch.Tensor = torch.from_numpy(img).to(self.device)
        img = img.half() if fp16 else img.float()  # uint8 to fp16/32
        img /= 255  # 0 - 255 to 0.0 - 1.0
        if len(img.shape) == 3:
            img = img[None]  # expand for batch dim
        return img, ratio, padding,

    def postprocess(self, pred, ratio, max_det):
        """後処理"""
        # assert ratio != 0.0
        center_pix = []
        obj = []
        num_detected: int = min(len(pred[0]), max_det)
        num_human_det = 0

        if num_detected <= 0:
            return center_pix, num_human_det, obj

        for i in range(num_detected):
            if int(pred[0][i][5].item()) == 0:
                num_human_det += 1
                x1: float = pred[0][i][0].item() / ratio[0]
                # y0: float = (pred[0][i][1].item() - offset_y) / ratio[1]
                x2: float = pred[0][i][2].item() / ratio[0]
                # y1: float = (pred[0][i][3].item() - offset_y) / ratio[1]
                center_pix.append((x1 + x2)/2)
            elif int(pred[0][i][5].item()) != 0:
                tmp_obj = []
                x1: float = pred[0][i][0].item() / ratio[0]
                y1: float = pred[0][i][1].item() / ratio[1]
                x2: float = pred[0][i][2].item() / ratio[0]
                y2: float = pred[0][i][3].item() / ratio[1]
                center_x = int((x1+x2)/2)
                center_y = int((y1+y2)/2)
                tmp_obj.append(center_x)
                tmp_obj.append(center_y)
                tmp_obj.append(int(pred[0][i][5].item()))
                obj.append(tmp_obj)
        return center_pix, num_human_det, obj

    def showResult(self, img: np.ndarray, pred: torch.Tensor) -> np.ndarray:
        """
        推論結果を画像に表示
        Args:
            img: 表示する画像
            pred: 推論結果
        Returns:
            np.ndarray: 表示後の画像
        """
        line_thickness=3  # bounding box thickness (pixels)
        hide_labels=False  # hide labels
        hide_conf=False  # hide confidences

        im0 = img.copy()

        annotator = Annotator(im0, line_width=line_thickness, example=str(self.names))
        if len(pred):
            # Rescale boxes from img_size to im0 size
            pred[:, :4] = scale_boxes(img.shape[:2], pred[:, :4], im0.shape).round()

            for *xyxy, conf, cls in reversed(pred):
                c = int(cls)  # integer class
                label = None if hide_labels else (self.names[c] if hide_conf else f'{self.names[c]} {conf:.2f}')
                annotator.box_label(xyxy, label, color=colors(c, True))

        im0 = annotator.result()
        return im0
