"""채널 브랜딩 이미지 생성 (프로필 800x800, 배너 2560x1440).

사용법:
    python branding.py            # → samples/branding/profile.png, banner.png
"""
import math
import os

import cairo

from cartoon_shorts import squire as S
from cartoon_shorts.engine import draw_text, ellipse, rrect, set_rgb

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "samples", "branding")

CHANNEL = "오늘의 만평"
TAGLINE = "긴 뉴스, 30초 만평으로 끝내드림"

CIT = S.Person(coat="#6F7F63", hair="beanie", hood=True, pants="#3D4656")
A = S.Person(coat="#4E5A6B", tie="#3E8E87", hair="part", hair_color="#4A3426", badge=True)
B = S.Person(coat="#3B3F48", tie="#5B6E8C", hair="part", hair_color="#8E8E8E", badge=True)


def _canvas(w, h):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    return surf, cairo.Context(surf)


def profile(path, size=800):
    surf, ctx = _canvas(size, size)
    S.planks(ctx, base=S.SLATE, dark=S.SLATE_D, seed=9, ww=size, hh=size)
    # 후광
    ctx.save()
    ctx.translate(size / 2, size * 0.42)
    for _ in range(12):
        ctx.rotate(math.pi / 6)
        ctx.move_to(0, 0)
        ctx.line_to(-60, -700)
        ctx.line_to(60, -700)
        ctx.close_path()
    set_rgb(ctx, "#FFF3C4", 0.18)
    ctx.fill()
    ctx.restore()
    # 시민 캐릭터 (원형으로 잘려도 얼굴이 중앙에 오도록)
    CIT.draw(ctx, size * 0.5, size * 1.62, 1.8, 1, pose="wave", expr="smug", t=0.3, bob=False)
    # 하단 라벨 (작게 보여도 읽히도록 크림색 판 위에)
    ctx.save()
    ctx.translate(size * 0.5, size * 0.865)
    ctx.rotate(-0.04)
    rrect(ctx, -190, -62, 380, 124, 30)
    S.fs(ctx, "#F3EBD5", lw=9)
    draw_text(ctx, "만평", 0, 4, 96, font="black", fill=S.RUST)
    ctx.restore()
    surf.write_to_png(path)


def banner(path, w=2560, h=1440):
    """모든 기기에서 보이는 안전 영역: 중앙 1546x423 (y 508~931)."""
    surf, ctx = _canvas(w, h)
    S.planks(ctx, base=S.SLATE, dark=S.SLATE_D, w=160, seed=5, ww=w, hh=h)
    cy = h / 2
    floor = cy + 200
    ctx.rectangle(0, floor, w, h)
    set_rgb(ctx, "#8C7A5E")
    ctx.fill()
    ctx.move_to(0, floor)
    ctx.line_to(w, floor)
    set_rgb(ctx, S.OUT)
    ctx.set_line_width(8)
    ctx.stroke()
    px0, px1, py0, py1 = w / 2 - 560, w / 2 + 560, cy - 170, cy + 150  # 제목 패널
    # 양옆 정치인이 채널 제목을 줄다리기 (데스크톱 넓은 화면에서 보임)
    s = 0.62
    for P, x, f in ((A, 420, 1), (B, w - 420, -1)):
        r = -0.18 * f
        hx = x + (215 * s * f) * math.cos(r) - (-285 * s) * math.sin(r)
        hy = floor + 5 + (215 * s * f) * math.sin(r) + (-285 * s) * math.cos(r)
        S.tube(ctx, [(hx, hy), ((hx + (px0 if f > 0 else px1)) / 2, cy + 40),
                     (px0 if f > 0 else px1, cy)], 14, "#C89B5C", lw=5)
        P.draw(ctx, x, floor + 5, s, f, pose="pull", expr="angry", mouth=0.4, t=0.2,
               rot=r, bob=False, sweat=True)
        for i in range(3):  # 흙먼지
            ellipse(ctx, x - f * (60 + 55 * i), floor - 8 - 10 * i, 40 + 12 * i, 20 + 6 * i)
            S.fs(ctx, "#D8CBB0", lw=5, alpha=0.9 - 0.25 * i)
    rrect(ctx, px0, py0, px1 - px0, py1 - py0, 40)
    S.fs(ctx, "#F3EBD5", lw=10)
    draw_text(ctx, CHANNEL, w / 2, cy - 40, 190, font="black", fill="#2E3A4A")
    draw_text(ctx, TAGLINE, w / 2, cy + 90, 70, font="black", fill=S.RUST)
    S.stamp(ctx, px1 - 40, py0 + 10, "매주 업로드", 1.0, size=50, rot=0.1)
    surf.write_to_png(path)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    profile(os.path.join(OUT, "profile.png"))
    banner(os.path.join(OUT, "banner.png"))
    print("done:", OUT)
