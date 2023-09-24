import sys
sys.path.append("..")

from ultralytics import YOLO

model = YOLO("train_results\weights\last.pt")

def detect_human(file):
    result = model.predict(source=file,conf=0.30,iou=0.5)
    return result[0].verbose()
