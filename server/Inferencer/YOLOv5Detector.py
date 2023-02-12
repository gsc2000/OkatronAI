"""
Run YOLOv5 detection inference on images, videos, directories, globs, YouTube, webcam, streams, etc.

Usage - sources:
    $ python detect.py --weights yolov5s.pt --source 0                               # webcam
                                                     img.jpg                         # image
                                                     vid.mp4                         # video
                                                     screen                          # screenshot
                                                     path/                           # directory
                                                     list.txt                        # list of images
                                                     list.streams                    # list of streams
                                                     'path/*.jpg'                    # glob
                                                     'https://youtu.be/Zgi9g1ksQHc'  # YouTube
                                                     'rtsp://example.com/media.mp4'  # RTSP, RTMP, HTTP stream

Usage - formats:
    $ python detect.py --weights yolov5s.pt                 # PyTorch
                                 yolov5s.torchscript        # TorchScript
                                 yolov5s.onnx               # ONNX Runtime or OpenCV DNN with --dnn
                                 yolov5s_openvino_model     # OpenVINO
                                 yolov5s.engine             # TensorRT
                                 yolov5s.mlmodel            # CoreML (macOS-only)
                                 yolov5s_saved_model        # TensorFlow SavedModel
                                 yolov5s.pb                 # TensorFlow GraphDef
                                 yolov5s.tflite             # TensorFlow Lite
                                 yolov5s_edgetpu.tflite     # TensorFlow Edge TPU
                                 yolov5s_paddle_model       # PaddlePaddle
"""

import argparse
import os
import platform
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
from yolov5_module.utils.general import non_max_suppression, xyxy2xywh, scale_boxes
from yolov5_module.utils.plots import Annotator, colors, save_one_box
from yolov5_module.models.common import DetectMultiBackend

class YOLOv5Detector():
    '''
    Yoloで推論
    '''
    def __init__(self, config):
        weights = "Inferencer/yolov5_module/weight/"+config["weight"]
        data=ROOT / 'data/coco128.yaml'  # dataset.yaml path
        device='cpu'  # cuda device, i.e. 0 or 0,1,2,3 or cpu
        dnn=False # use OpenCV DNN for ONNX inference
        half=False  # use FP16 half-precision inference

        self.device = device
        self.imgsz = config["image"]
        self.conf_thres = config["conf"]
        self.iou_thres = config["iou"]
        self.classes = config["det_class"]
        self.max_det = 5
        self.agnostic_nms = False
        self.augment = False
        self.visualize = False


        self.model = DetectMultiBackend(weights, device=self.device, dnn=dnn, data=data, fp16=half)
        self.stride, self.names, self.pt = self.model.stride, self.model.names, self.model.pt

    def detect(self, img = None):

        #入力データの前処理

        img, ratio, padding = self.preprocess(img, self.imgsz, False, self.device)

        # Inference
        pred = self.model(img, augment=self.augment, visualize=self.visualize)
        # NMS
        pred = non_max_suppression(pred, self.conf_thres, self.iou_thres, self.classes, self.agnostic_nms, max_det=self.max_det)
        # print(pred)
        # 出力結果の事後処理
        center_pix, num_human_det, obj = self.postprocess(pred, ratio, self.max_det)

        return center_pix, num_human_det, obj

    def preprocess(self, img, imgsz, fp16=False, device='cpu'):
        # リサイズ結果を取得
        img, ratio, padding = letterbox(img, imgsz)
        # Convert
        img = img.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img).to(device)
        img = img.half() if fp16 else img.float()  # uint8 to fp16/32
        img /= 255  # 0 - 255 to 0.0 - 1.0
        if len(img.shape) == 3:
            img = img[None]  # expand for batch dim
        return img, ratio, padding,


    def postprocess(self, pred, ratio, max_det):
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

    def showResult(self, img, pred):
        line_thickness=3,  # bounding box thickness (pixels)
        hide_labels=False,  # hide labels
        hide_conf=False,  # hide confidences

        im0 = img.copy()

        # GUI表示用画像作成
        for i, det in enumerate(pred):  # per image
            annotator = Annotator(im0, line_width=line_thickness, example=str(self.names))
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], im0.shape).round()

                for *xyxy, conf, cls in reversed(det):
                    c = int(cls)  # integer class
                    label = None if hide_labels else (self.names[c] if hide_conf else f'{self.names[c]} {conf:.2f}')
                    annotator.box_label(xyxy, label, color=colors(c, True))

            im0 = annotator.result()
        return im0
