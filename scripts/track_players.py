"""
Детекция + трекинг (ByteTrack через Ultralytics).
Пример:
  python scripts/track_players.py --weights runs/detect/exp/weights/best.pt --source D:/vc/dataset/raw/match1.mp4 --save D:/vc/out/tracks.json
"""
import argparse, json, os
from ultralytics import YOLO

def run(weights:str, source:str, save:str):
    model = YOLO(weights)
    results = model.track(source=source, stream=True, persist=True, tracker="bytetrack.yaml", verbose=False)

    os.makedirs(os.path.dirname(save), exist_ok=True)
    out = []
    frame_idx = 0
    for r in results:
        if r.boxes is not None:
            for b in r.boxes:
                item = dict(
                    frame=int(frame_idx),
                    id=int(b.id.item()) if b.id is not None else -1,
                    cls=int(b.cls.item()) if b.cls is not None else -1,
                    conf=float(b.conf.item()) if b.conf is not None else 0.0,
                    xyxy=[float(x) for x in b.xyxy[0].tolist()]
                )
                out.append(item)
        frame_idx += 1

    with open(save, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False)
    print(f"[track_players] saved {len(out)} records -> {save}")

if name == "main":
    ap = argparse.ArgumentParser()
    ap.add_argument("--weights", required=True)
    ap.add_argument("--source", required=True)
    ap.add_argument("--save",   required=True)
    args = ap.parse_args()
    run(args.weights, args.source, args.save)
