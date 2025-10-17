"""
Нарезка кадров из видео.
Пример:
  python scripts/extract_frames.py --input D:/vc/dataset/raw/match1.mp4 --out D:/vc/dataset/frames/match1 --mode fps --n 1
"""
import os, cv2, argparse

def extract(input_path: str, out_dir: str, mode: str="fps", n: int=1, quality:int=92):
    os.makedirs(out_dir, exist_ok=True)
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise RuntimeError(f"Не удалось открыть видео: {input_path}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    step = max(1, int(round(fps / max(1,n)))) if mode=="fps" else max(1,n)

    frame_id = saved = 0
    print(f"[extract_frames] source={input_path} fps~{fps:.2f} mode={mode} n={n} step={step}")
    while True:
        ok, frame = cap.read()
        if not ok: break
        if frame_id % step == 0:
            out = os.path.join(out_dir, f"frame_{frame_id:06d}.jpg")
            cv2.imwrite(out, frame, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
            saved += 1
        frame_id += 1
    cap.release()
    print(f"[extract_frames] done: {saved} frames -> {out_dir}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out",   required=True)
    ap.add_argument("--mode",  choices=["fps","every_nth"], default="fps")
    ap.add_argument("--n",     type=int, default=1)
    ap.add_argument("--quality", type=int, default=92)
    args = ap.parse_args()
    extract(args.input, args.out, args.mode, args.n, args.quality)
