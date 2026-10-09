"""만평 쇼츠 렌더러.

사용법:
    python render.py ep01_gridlock                  # samples/ep01_gridlock.mp4 생성
    python render.py ep01_gridlock --stills 3,9,16  # 지정 시각 스틸컷 PNG 만 생성
"""
import argparse
import importlib
import os
import subprocess
import sys
import time

from cartoon_shorts import audio
from cartoon_shorts.engine import FPS, H, W, new_frame, surface_bytes

ROOT = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--out", default=None)
    ap.add_argument("--stills", default=None, help="쉼표로 구분한 초 단위 시각")
    args = ap.parse_args()

    ep = importlib.import_module(f"cartoon_shorts.episodes.{args.episode}")
    out_dir = os.path.join(ROOT, "samples")
    os.makedirs(out_dir, exist_ok=True)

    if args.stills:
        for s in args.stills.split(","):
            t = float(s)
            surf, ctx = new_frame()
            ep.render_frame(ctx, t)
            p = os.path.join(out_dir, f"{args.episode}_{t:05.1f}s.png")
            surf.write_to_png(p)
            print("still:", p)
        return

    out = args.out or os.path.join(out_dir, f"{args.episode}.mp4")
    wav = out[:-4] + ".wav"
    print("audio...")
    audio.write_wav(wav, audio.mix(ep.DURATION, ep.cues()))

    n = int(ep.DURATION * FPS)
    cmd = ["ffmpeg", "-y", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", wav,
           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart",
           "-metadata", f"title={ep.TITLE}", out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    t0 = time.time()
    for i in range(n):
        surf, ctx = new_frame()
        ep.render_frame(ctx, i / FPS)
        proc.stdin.write(surface_bytes(surf))
        if i % FPS == 0:
            sys.stdout.write(f"\rframe {i}/{n}  ({time.time() - t0:.0f}s)")
            sys.stdout.flush()
    proc.stdin.close()
    proc.wait()
    os.remove(wav)
    print(f"\ndone: {out}")


if __name__ == "__main__":
    main()
