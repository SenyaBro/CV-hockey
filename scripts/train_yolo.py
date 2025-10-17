"""
Запуск обучения YOLO (Ultralytics).
Пример:
  python scripts/train_yolo.py --data D:/vc/dataset.yaml --weights yolov8n.pt --epochs 30 --img 832 --batch 8
"""
import argparse
from ultralytics import YOLO

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="dataset.yaml")
    ap.add_argument("--weights", default="yolov8n.pt")
    ap.add_argument("--epochs", type=int, default=30)
    ap.add_argument("--img", type=int, default=640)
    ap.add_argument("--batch", type=int, default=8)
    args = ap.parse_args()

    model = YOLO(args.weights)
    model.train(data=args.data, epochs=args.epochs, imgsz=args.img, batch=args.batch)
if name == "main":
    main()
