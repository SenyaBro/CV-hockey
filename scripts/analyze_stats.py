"""
Простой расчёт времени на льду (TOI) по трекам.
Пример:
  python scripts/analyze_stats.py --tracks D:/vc/out/tracks.json --fps 60 --out D:/vc/out/toi.csv
"""
import argparse, json, csv, os
from collections import defaultdict

def segments_from_tracks(tracks, fps:int, min_gap:int=5):
    frames_by_id = defaultdict(list)
    for t in tracks:
        if t.get("id",-1) >= 0 and t.get("cls",-1) == 0:
            frames_by_id[t["id"]].append(t["frame"])
    segs = []
    for pid, frs in frames_by_id.items():
        frs = sorted(set(frs))
        start = frs[0]; prev = frs[0]
        for f in frs[1:]:
            if f - prev > min_gap:
                segs.append((pid, start, prev))
                start = f
            prev = f
        segs.append((pid, start, prev))
    return [{"player_id": pid, "t_start_s": s/fps, "t_end_s": e/fps, "dur_s": (e-s+1)/fps} for pid,s,e in segs]

def main(tracks_path:str, fps:int, out_csv:str):
    with open(tracks_path, "r", encoding="utf-8") as f:
        tracks = json.load(f)
    segs = segments_from_tracks(tracks, fps=fps)
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["player_id","t_start_s","t_end_s","dur_s"])
        w.writeheader(); w.writerows(segs)
    print(f"[analyze_stats] {len(segs)} segments -> {out_csv}")

if name == "main":
    ap = argparse.ArgumentParser()
    ap.add_argument("--tracks", required=True)
    ap.add_argument("--fps", type=int, default=60)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    main(args.tracks, args.fps, args.out)
