"""
Нарезка видео на клипы фиксированной длины (секунды).
Пример:
  python scripts/split_clips.py --input D:/vc/dataset/raw/match1.mp4 --out D:/vc/dataset/clips/match1 --sec 10
"""
import os, cv2, argparse

def split_video(input_path:str, out_dir:str, sec:int=10):
    os.makedirs(out_dir, exist_ok=True)
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise RuntimeError(f"Не удалось открыть видео: {input_path}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    clip_fr = max(1, int(round(fps*sec)))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    idx = 0; written = 0
    out = cv2.VideoWriter(os.path.join(out_dir, f"part_{idx:04d}.mp4"), fourcc, fps, (w,h))
    while True:
        ok, frame = cap.read()
        if not ok: break
        out.write(frame); written += 1
        if written >= clip_fr:
            out.release(); idx += 1; written = 0
            out = cv2.VideoWriter(os.path.join(out_dir, f"part_{idx:04d}.mp4"), fourcc, fps, (w,h))
    out.release(); cap.release()
    print(f"[split_clips] done -> {out_dir}, clip_len={sec}s")

if name == "main":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--sec", type=int, default=10)
    args = ap.parse_args()
    split_video(args.input, args.out, args.sec)
