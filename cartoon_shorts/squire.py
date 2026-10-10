"""해설 애니메이션 스타일 (흰 동그란 얼굴 캐릭터 + 차분한 톤 + 풀스크린 일러스트).

배경/캐릭터/소품 그리기 함수 모음. 모든 캐릭터 좌표는 발 중심이 원점(위쪽 -y).
"""
import math
import random

import cairo
import numpy as np
from PIL import Image

from .engine import (H, W, clamp, draw_text, ellipse, fill_stroke, hexc,
                     pil_to_surface, rrect, set_rgb, wobble)

OUT = "#26262B"
FACE = "#FAF8F2"
FACE_SH = "#E2DED3"
SLATE, SLATE_D = "#56718F", "#46607C"
CREAM = "#F3EBD5"
KHAKI, KHAKI_D = "#E5D3A6", "#CDB887"
WOOD, WOOD_D = "#8C5D3D", "#6A4429"
OLIVE = "#7F8C5C"
RUST = "#C9473B"
STORM, STORM_D = "#5B6574", "#4A5361"

LW = 7  # 기본 외곽선 두께


def fs(ctx, fill, lw=LW, alpha=1.0):
    fill_stroke(ctx, fill, lw, stroke=hexc(OUT), alpha=alpha)


def tube(ctx, pts, width, color, lw=LW):
    """외곽선이 있는 굵은 관 (팔, 밧줄)."""
    for w, c in ((width + lw * 2, OUT), (width, color)):
        ctx.new_path()
        ctx.move_to(*pts[0])
        for p in pts[1:]:
            ctx.line_to(*p)
        set_rgb(ctx, c)
        ctx.set_line_width(w)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.stroke()


# ================================================================ backgrounds
def planks(ctx, base=SLATE, dark=SLATE_D, w=140, seed=1, x0=0, y0=0, ww=W, hh=H):
    rnd = random.Random(seed)
    r, g, b = hexc(base)
    n = int(ww / w) + 2
    for i in range(n):
        k = 0.94 + 0.1 * rnd.random()
        ctx.rectangle(x0 + i * w, y0, w, hh)
        ctx.set_source_rgb(r * k, g * k, b * k)
        ctx.fill()
        # 나뭇결
        set_rgb(ctx, dark, 0.35)
        ctx.set_line_width(3)
        for _ in range(3):
            gx = x0 + i * w + rnd.uniform(15, w - 15)
            gy = y0 + rnd.uniform(0, hh)
            ctx.move_to(gx, gy)
            ctx.curve_to(gx + 6, gy + 120, gx - 6, gy + 240, gx + 3, gy + rnd.uniform(300, 600))
            ctx.stroke()
        ctx.move_to(x0 + i * w, y0)
        ctx.line_to(x0 + i * w, y0 + hh)
        set_rgb(ctx, dark)
        ctx.set_line_width(6)
        ctx.stroke()


def sky(ctx, top, bottom, h=H):
    g = cairo.LinearGradient(0, 0, 0, h)
    g.add_color_stop_rgb(0, *hexc(top))
    g.add_color_stop_rgb(1, *hexc(bottom))
    ctx.rectangle(-200, -200, W + 400, h + 400)
    ctx.set_source(g)
    ctx.fill()


def cloud(ctx, x, y, s, color, alpha=1.0):
    for dx, dy, r in ((0, 0, 90), (100, -40, 110), (210, 0, 85), (105, 30, 95)):
        ellipse(ctx, x + dx * s, y + dy * s, r * s, r * s * 0.75)
    set_rgb(ctx, color, alpha)
    ctx.fill()


def desk(ctx):
    planks(ctx, base="#9A6B47", dark="#6E4A2E", w=1920, seed=3)  # 큰 판재 하나
    rnd = random.Random(5)
    set_rgb(ctx, "#6E4A2E", 0.35)
    ctx.set_line_width(4)
    for i in range(26):
        y = i * 78 + rnd.uniform(-10, 10)
        ctx.move_to(-20, y)
        ctx.curve_to(300, y + rnd.uniform(-25, 25), 700, y + rnd.uniform(-25, 25), W + 20, y)
        ctx.stroke()


def rain(ctx, t, n=140, alpha=0.55, seed=2, speed=1900):
    rnd = random.Random(seed)
    set_rgb(ctx, "#E8EEF5", alpha)
    ctx.set_line_width(4)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for _ in range(n):
        x0, y0, ln = rnd.uniform(-200, W + 200), rnd.uniform(0, H), rnd.uniform(40, 90)
        y = (y0 + t * speed) % (H + 200) - 100
        x = x0 - (y * 0.25)
        ctx.move_to(x, y)
        ctx.line_to(x - ln * 0.25, y + ln)
    ctx.stroke()


_grain = {}


def grain(ctx, t, alpha=0.06):
    """종이 질감 그레인 (정적 패턴 — 프레임마다 바꾸면 영상 용량이 크게 늘어남)."""
    k = 0
    if k not in _grain:
        rng = np.random.default_rng(k)
        a = rng.integers(0, 255, (H // 2, W // 2), dtype=np.uint8)
        img = Image.fromarray(a, "L").resize((W, H), Image.NEAREST).convert("RGBA")
        _grain[k] = pil_to_surface(img)
    ctx.set_source_surface(_grain[k], 0, 0)
    ctx.paint_with_alpha(alpha)


def vignette(ctx, strength=0.45):
    g = cairo.RadialGradient(W / 2, H / 2, H * 0.3, W / 2, H / 2, H * 0.75)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, strength)
    ctx.rectangle(0, 0, W, H)
    ctx.set_source(g)
    ctx.fill()


def spotlight(ctx, x, y_top, w_top, w_bot, y_bot, alpha=0.35):
    ctx.new_path()
    ctx.move_to(x - w_top / 2, y_top)
    ctx.line_to(x + w_top / 2, y_top)
    ctx.line_to(x + w_bot / 2, y_bot)
    ctx.line_to(x - w_bot / 2, y_bot)
    ctx.close_path()
    g = cairo.LinearGradient(0, y_top, 0, y_bot)
    g.add_color_stop_rgba(0, 1, 0.97, 0.85, alpha)
    g.add_color_stop_rgba(1, 1, 0.97, 0.85, alpha * 0.4)
    ctx.set_source(g)
    ctx.fill()


# ================================================================ character
class Person:
    def __init__(self, coat="#4E5A6B", tie=None, hair="part", hair_color="#4A3426",
                 badge=False, hood=False, pants="#3A3F4A", name="", glasses=False):
        self.glasses = glasses
        self.coat, self.tie, self.hair, self.hair_color = coat, tie, hair, hair_color
        self.badge, self.hood, self.pants, self.name = badge, hood, pants, name

    # 포즈: (뒤팔 [어깨, 팔꿈치, 손], 앞팔 [...])
    def _arms(self, pose, t):
        if pose == "hips":
            return ([(-85, -330), (-175, -265), (-112, -205)],
                    [(85, -330), (175, -265), (112, -205)])
        if pose == "point":
            return ([(-85, -330), (-120, -250), (-110, -170)],
                    [(85, -330), (170, -390), (250, -440)])
        if pose == "pull":
            return ([(-85, -330), (40, -260), (150, -280)],
                    [(85, -330), (150, -250), (215, -285)])
        if pose == "shrug":
            return ([(-85, -330), (-165, -270), (-200, -360)],
                    [(85, -330), (165, -270), (200, -360)])
        if pose == "cheer":
            w = math.sin(t * 9) * 25
            return ([(-85, -330), (-150, -430), (-165 + w, -560)],
                    [(85, -330), (150, -430), (165 - w, -560)])
        if pose == "wave":
            w = math.sin(t * 10) * 45
            return ([(-85, -330), (-120, -250), (-110, -170)],
                    [(85, -330), (175, -400), (190 + w, -540)])
        if pose == "flail":
            a = math.sin(t * 16) * 50
            return ([(-85, -330), (-170, -380 + a), (-230, -470 - a)],
                    [(85, -330), (170, -380 - a), (230, -470 + a)])
        return ([(-85, -330), (-115, -250), (-110, -165)],
                [(85, -330), (115, -250), (110, -165)])

    def draw(self, ctx, x, y, s=1.0, facing=1, pose="down", expr="neutral", mouth=0.0,
             t=0.0, rot=0.0, bob=True, sweat=False):
        ctx.save()
        ctx.translate(x, y)
        ctx.rotate(rot)
        ctx.scale(s * facing, s)
        if bob:
            ctx.translate(0, -abs(math.sin(t * 2.2)) * 6)
        back, front = self._arms(pose, t)

        # 다리
        for dx in (-50, 50):
            rrect(ctx, dx - 30, -110, 60, 100, 18)
            fs(ctx, self.pants)
            ellipse(ctx, dx + 12, -10, 48, 20)
            fs(ctx, "#2E2A28")
        # 뒤팔
        tube(ctx, back, 48, _shade(self.coat, 0.85))
        ellipse(ctx, *back[-1], 31, 31)
        fs(ctx, "#F2F0EA")
        # 몸통 (코트)
        ctx.new_path()
        ctx.move_to(-95, -360)
        ctx.curve_to(-125, -280, -135, -150, -120, -80)
        ctx.curve_to(-40, -62, 40, -62, 120, -80)
        ctx.curve_to(135, -150, 125, -280, 95, -360)
        ctx.curve_to(40, -378, -40, -378, -95, -360)
        ctx.close_path()
        fs(ctx, self.coat)
        # 음영
        ctx.new_path()
        ctx.move_to(60, -360)
        ctx.curve_to(110, -280, 115, -150, 105, -85)
        ctx.line_to(120, -80)
        ctx.curve_to(135, -150, 125, -280, 95, -360)
        ctx.close_path()
        set_rgb(ctx, (0, 0, 0, 0.12))
        ctx.fill()
        if self.hood:
            ellipse(ctx, 0, -345, 85, 30)
            fs(ctx, _shade(self.coat, 0.85))
            for dx in (-25, 25):
                ctx.move_to(dx, -330)
                ctx.line_to(dx + 4, -260)
            set_rgb(ctx, "#EDEDED")
            ctx.set_line_width(6)
            ctx.stroke()
            rrect(ctx, -60, -190, 120, 55, 16)
            fs(ctx, _shade(self.coat, 0.9), lw=5)
        else:
            # 셔츠 + 넥타이
            ctx.new_path()
            ctx.move_to(-40, -372)
            ctx.line_to(0, -290)
            ctx.line_to(40, -372)
            ctx.close_path()
            fs(ctx, "#F4F2EC", lw=5)
            if self.tie:
                ctx.new_path()
                ctx.move_to(-11, -366)
                ctx.line_to(11, -366)
                ctx.line_to(16, -310)
                ctx.line_to(0, -288)
                ctx.line_to(-16, -310)
                ctx.close_path()
                fs(ctx, self.tie, lw=4)
            # 라펠
            for sg in (-1, 1):
                ctx.new_path()
                ctx.move_to(sg * 42, -372)
                ctx.line_to(sg * 8, -270)
                ctx.line_to(sg * 70, -330)
                ctx.close_path()
                fs(ctx, _shade(self.coat, 0.9), lw=5)
            for by in (-235, -175):
                ellipse(ctx, 0, by, 7, 7)
                set_rgb(ctx, OUT)
                ctx.fill()
        if self.badge:
            ellipse(ctx, -55, -320, 13, 13)
            fs(ctx, "#E8B93E", lw=4)
        # 머리
        self._head(ctx, expr, mouth, t, sweat)
        # 앞팔
        tube(ctx, front, 48, self.coat)
        ellipse(ctx, *front[-1], 32, 32)
        fs(ctx, "#F7F5F0")
        ctx.restore()

    def _head(self, ctx, expr, mouth, t, sweat):
        hx, hy = 0, -485
        if self.hair == "bob":
            ctx.new_path()
            ctx.move_to(-140, -400)
            ctx.curve_to(-170, -650, 170, -650, 140, -400)
            ctx.curve_to(100, -380, -100, -380, -140, -400)
            ctx.close_path()
            fs(ctx, self.hair_color)
        ellipse(ctx, hx, hy, 125, 118)
        fs(ctx, FACE)
        # 얼굴 음영
        ctx.save()
        ellipse(ctx, hx, hy, 121, 114)
        ctx.clip()
        ellipse(ctx, hx + 150, hy + 40, 90, 160)
        set_rgb(ctx, FACE_SH)
        ctx.fill()
        ctx.restore()
        ellipse(ctx, hx, hy, 125, 118)
        fs(ctx, None)
        # 머리카락
        if self.hair == "part":
            ctx.new_path()
            ctx.move_to(-123, -470)
            ctx.curve_to(-140, -620, 60, -660, 120, -540)
            ctx.curve_to(80, -575, 0, -575, -40, -545)
            ctx.curve_to(-60, -560, -80, -540, -100, -500)
            ctx.close_path()
            fs(ctx, self.hair_color)
        elif self.hair == "bob":
            ctx.new_path()
            ctx.move_to(-128, -470)
            ctx.curve_to(-120, -640, 120, -640, 128, -470)
            ctx.curve_to(80, -540, 20, -550, -30, -520)
            ctx.curve_to(-70, -545, -110, -520, -128, -470)
            ctx.close_path()
            fs(ctx, self.hair_color)
        elif self.hair == "beanie":
            ctx.new_path()
            ctx.move_to(-126, -530)
            ctx.curve_to(-118, -690, 118, -690, 126, -530)
            ctx.close_path()
            fs(ctx, "#B9573F")
            rrect(ctx, -132, -552, 264, 44, 20)
            fs(ctx, "#A24A35")
            ellipse(ctx, 0, -660, 26, 26)
            fs(ctx, "#E6D3B3")
        fx = 22  # 얼굴 방향 오프셋
        ey = hy - 5
        ex1, ex2 = -28 + fx, 42 + fx
        set_rgb(ctx, OUT)
        if expr == "smug":
            for ex in (ex1, ex2):
                ctx.new_path()
                ctx.arc(ex, ey + 6, 20, math.pi * 1.1, math.pi * 1.9)
                ctx.set_line_width(7)
                ctx.set_line_cap(cairo.LINE_CAP_ROUND)
                ctx.stroke()
            for ex in (ex1 - 30, ex2 + 18):
                for k in (0, 12):
                    ctx.move_to(ex + k, hy + 35)
                    ctx.line_to(ex + k - 7, hy + 50)
            set_rgb(ctx, "#E59A9A")
            ctx.set_line_width(4)
            ctx.stroke()
        elif expr == "shock":
            for ex in (ex1, ex2):
                ellipse(ctx, ex, ey, 22, 24)
                fs(ctx, "#FFFFFF", lw=5)
                ellipse(ctx, ex, ey, 6, 6)
                set_rgb(ctx, OUT)
                ctx.fill()
        else:
            blink = (t * 0.6) % 1.0 > 0.96
            for ex in (ex1, ex2):
                if blink:
                    ctx.move_to(ex - 10, ey)
                    ctx.line_to(ex + 10, ey)
                    ctx.set_line_width(6)
                    ctx.stroke()
                else:
                    ellipse(ctx, ex, ey, 10, 14)
                    ctx.fill()
            if expr == "deadpan":
                for ex in (ex1, ex2):
                    rrect(ctx, ex - 15, ey - 22, 30, 18, 3)
                    set_rgb(ctx, FACE)
                    ctx.fill()
                    ctx.move_to(ex - 16, ey - 4)
                    ctx.line_to(ex + 16, ey - 4)
                    set_rgb(ctx, OUT)
                    ctx.set_line_width(6)
                    ctx.stroke()
        if self.glasses:
            for ex in (ex1, ex2):
                ellipse(ctx, ex, ey, 30, 26)
                fs(ctx, (0.85, 0.93, 1.0, 0.35), lw=6)
            ctx.move_to(ex1 + 30, ey - 4)
            ctx.line_to(ex2 - 30, ey - 4)
            set_rgb(ctx, OUT)
            ctx.set_line_width(6)
            ctx.stroke()
        if expr in ("angry", "sad"):
            sg = 1 if expr == "angry" else -1
            for ex, d in ((ex1, 1), (ex2, -1)):
                ctx.move_to(ex - 18, ey - 30 - 8 * d * sg)
                ctx.line_to(ex + 18, ey - 30 + 8 * d * sg)
            set_rgb(ctx, OUT)
            ctx.set_line_width(7)
            ctx.stroke()
        # 입
        mx, my = fx + 8, hy + 52
        m = clamp(mouth)
        if expr == "smug" and m < 0.2:
            ctx.new_path()
            ctx.move_to(mx - 38, my - 8)
            ctx.curve_to(mx - 25, my + 40, mx + 30, my + 40, mx + 40, my - 10)
            ctx.close_path()
            fs(ctx, "#7B2730", lw=6)
            ctx.save()
            ctx.move_to(mx - 38, my - 8)
            ctx.curve_to(mx - 25, my + 40, mx + 30, my + 40, mx + 40, my - 10)
            ctx.close_path()
            ctx.clip()
            ellipse(ctx, mx + 5, my + 28, 22, 12)
            set_rgb(ctx, "#E77E86")
            ctx.fill()
            ctx.restore()
        elif m > 0.05 or expr == "shock":
            h = 8 + 46 * max(m, 0.5 if expr == "shock" else 0)
            ctx.new_path()
            ctx.move_to(mx - 30, my - 4)
            ctx.curve_to(mx - 30, my + h, mx + 30, my + h, mx + 30, my - 4)
            ctx.close_path()
            fs(ctx, "#7B2730", lw=6)
            if h > 20:
                ellipse(ctx, mx, my + h * 0.55, 16, h * 0.18)
                set_rgb(ctx, "#E77E86")
                ctx.fill()
        else:
            ctx.new_path()
            if expr in ("sad", "deadpan", "angry"):
                ctx.move_to(mx - 20, my + 12)
                ctx.curve_to(mx - 8, my + 2, mx + 8, my + 2, mx + 20, my + 12)
            else:
                ctx.move_to(mx - 20, my)
                ctx.curve_to(mx - 8, my + 12, mx + 8, my + 12, mx + 20, my)
            set_rgb(ctx, OUT)
            ctx.set_line_width(6)
            ctx.stroke()
        if sweat:
            k = (t * 1.2) % 1.0
            sx, sy = -105, hy - 60 + k * 50
            ctx.new_path()
            ctx.move_to(sx, sy - 22)
            ctx.curve_to(sx + 16, sy, sx + 12, sy + 14, sx, sy + 14)
            ctx.curve_to(sx - 12, sy + 14, sx - 16, sy, sx, sy - 22)
            fs(ctx, "#A9D8F2", lw=4, alpha=1 - k * 0.5)


def _shade(c, k):
    r, g, b = hexc(c)
    return (r * k, g * k, b * k)


# ================================================================ props
def calendar(ctx, x, y, s, title, sub, seed=0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rrect(ctx, -340, -420, 680, 840, 14)
    fs(ctx, WOOD)
    rrect(ctx, -300, -370, 600, 760, 6)
    fs(ctx, CREAM)
    for rx in (-120, 0, 120):
        rrect(ctx, rx - 10, -400, 20, 60, 10)
        fs(ctx, "#B9BEC6", lw=5)
    calendar_page(ctx, title, sub, seed)
    ctx.restore()


def calendar_page(ctx, title, sub, seed=0):
    draw_text(ctx, title, 0, -270, 120, font="black", fill="#2E3A4A")
    draw_text(ctx, sub, 0, -165, 64, font="black", fill=RUST)
    rnd = random.Random(seed)
    for i in range(28):
        cx = -240 + (i % 7) * 80
        cy = -60 + (i // 7) * 95
        draw_text(ctx, str(i + 1), cx, cy, 52, font="jua", fill="#2E2E33",
                  rot=rnd.uniform(-0.12, 0.12))


def flying_page(ctx, x, y, s, k, title, sub, seed=0, direction=-1):
    """뜯겨서 날아가는 달력 페이지 (k: 0→1)."""
    ctx.save()
    ctx.translate(x + direction * 900 * k ** 1.3, y - 700 * k + 300 * k * k)
    ctx.rotate(direction * 1.4 * k)
    ctx.scale(s * (1 - 0.15 * k), s * max(0.05, 1 - 0.5 * math.sin(k * math.pi)))
    ctx.translate(0, 370)
    rrect(ctx, -300, -370 - 370, 600, 740, 6)
    fs(ctx, CREAM)
    ctx.translate(0, -370)
    calendar_page(ctx, title, sub, seed)
    ctx.restore()


def folder(ctx, x, y, s, label, rot=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    rrect(ctx, -230, -190, 160, 60, 14)
    fs(ctx, "#D9B565")
    rrect(ctx, -230, -150, 460, 320, 16)
    fs(ctx, "#E6C477")
    rrect(ctx, -150, -60, 300, 110, 8)
    fs(ctx, "#FBF7EC", lw=5)
    draw_text(ctx, label, 0, -4, 66, font="black", fill=RUST)
    ctx.restore()


def paper(ctx, x, y, s, title, rot=0.0, lines=7):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    rrect(ctx, -230, -310, 460, 620, 8)
    fs(ctx, "#FBF8EF")
    draw_text(ctx, title, 0, -230, 64, font="black", fill="#2E3A4A")
    rnd = random.Random(len(title))
    set_rgb(ctx, "#9AA3AE")
    ctx.set_line_width(10)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for i in range(lines):
        yy = -130 + i * 55
        ctx.move_to(-170, yy)
        ctx.line_to(-170 + rnd.uniform(220, 340), yy)
    ctx.stroke()
    ctx.restore()


def stamp(ctx, x, y, text, k, color=RUST, rot=-0.2, size=90):
    """도장 찍기 (k: 0→1, 크게 시작해서 쾅)."""
    if k <= 0:
        return
    sc = 2.4 - 1.4 * min(1, k / 0.35)
    a = min(1, k / 0.2)
    tw = len(text) * size * 0.95 + 60
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(sc, sc)
    rrect(ctx, -tw / 2, -size * 0.75, tw, size * 1.5, 18)
    set_rgb(ctx, color, a)
    ctx.set_line_width(12)
    ctx.stroke()
    draw_text(ctx, text, 0, 4, size, font="black", fill=_hex(color), alpha=a)
    ctx.restore()


def _hex(c):
    return c if isinstance(c, str) else "#%02x%02x%02x" % tuple(int(v * 255) for v in c[:3])


def big_arrow(ctx, x, y, s, k, color=RUST, with_hand=True):
    """아래에서 솟아오르는 큰 화살표 (k: 0→1)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    length = 900 * k
    ctx.new_path()
    ctx.move_to(-70, 0)
    ctx.line_to(-70, -length)
    ctx.line_to(-200, -length)
    ctx.line_to(0, -length - 230)
    ctx.line_to(200, -length)
    ctx.line_to(70, -length)
    ctx.line_to(70, 0)
    ctx.close_path()
    fs(ctx, color, lw=9)
    rrect(ctx, -35, -length + 20, 20, max(0, length - 60), 10)
    set_rgb(ctx, "#FFFFFF", 0.25)
    ctx.fill()
    if with_hand:
        tube(ctx, [(60, 260), (20, 80)], 120, "#3F4A3A", lw=9)
        ellipse(ctx, 0, 40, 105, 75)
        fs(ctx, "#F2F0EA", lw=9)
    ctx.restore()


def graph_paper(ctx, x, y, w, h):
    rrect(ctx, x, y, w, h, 10)
    fs(ctx, "#F7F1DF")
    set_rgb(ctx, "#B9C9D6", 0.7)
    ctx.set_line_width(2)
    for i in range(int(w / 60) + 1):
        ctx.move_to(x + i * 60, y)
        ctx.line_to(x + i * 60, y + h)
    for j in range(int(h / 60) + 1):
        ctx.move_to(x, y + j * 60)
        ctx.line_to(x + w, y + j * 60)
    ctx.stroke()


def lamppost(ctx, x, y, t):
    g = cairo.RadialGradient(x, y - 640, 10, x, y - 640, 260)
    g.add_color_stop_rgba(0, 1, 0.85, 0.45, 0.55 + 0.05 * math.sin(t * 7))
    g.add_color_stop_rgba(1, 1, 0.85, 0.45, 0)
    ctx.arc(x, y - 640, 260, 0, 2 * math.pi)
    ctx.set_source(g)
    ctx.fill()
    rrect(ctx, x - 14, y - 600, 28, 600, 8)
    fs(ctx, "#3A3D45")
    ctx.new_path()
    ctx.move_to(x - 55, y - 600)
    ctx.line_to(x + 55, y - 600)
    ctx.line_to(x + 40, y - 690)
    ctx.line_to(x - 40, y - 690)
    ctx.close_path()
    fs(ctx, "#E9A447")
    for dx in (-15, 15):
        ctx.move_to(x + dx, y - 600)
        ctx.line_to(x + dx * 0.8, y - 690)
    set_rgb(ctx, OUT)
    ctx.set_line_width(5)
    ctx.stroke()
    rrect(ctx, x - 62, y - 712, 124, 26, 8)
    fs(ctx, "#3A3D45")


def gavel(ctx, x, y, s, ang):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ellipse(ctx, 0, 40, 210, 50)
    fs(ctx, WOOD_D)
    rrect(ctx, -170, -10, 340, 50, 20)
    fs(ctx, WOOD)
    ctx.translate(260, -60)
    ctx.rotate(ang)
    rrect(ctx, -10, -18, 380, 36, 16)
    fs(ctx, "#A87245")
    rrect(ctx, -110, -80, 120, 160, 26)
    fs(ctx, WOOD)
    for dx in (-85, -15):
        rrect(ctx, dx, -84, 14, 168, 6)
        set_rgb(ctx, "#E8B93E")
        ctx.fill()
    ctx.restore()


def confetti(ctx, t, t0, n=80, seed=3):
    if t < t0:
        return
    rnd = random.Random(seed)
    cols = ("#E8B93E", RUST, "#5FA8D3", "#7FB069", "#F2F0EA")
    for _ in range(n):
        x0 = rnd.uniform(0, W)
        vy = rnd.uniform(250, 520)
        ph = rnd.uniform(0, 6)
        age = t - t0 - rnd.uniform(0, 0.6)
        if age < 0:
            continue
        x = x0 + math.sin(age * 3 + ph) * 60
        y = -40 + age * vy
        if y > H + 40:
            continue
        ctx.save()
        ctx.translate(x, y)
        ctx.rotate(age * 5 + ph)
        ctx.scale(1, abs(math.cos(age * 6 + ph)) + 0.2)
        ctx.rectangle(-12, -7, 24, 14)
        set_rgb(ctx, rnd.choice(cols))
        ctx.fill()
        ctx.restore()


def assembly(ctx, cx, base_y, s=1.0):
    """국회의사당 (차분한 톤)."""
    ctx.save()
    ctx.translate(cx, base_y)
    ctx.scale(s, s)
    ctx.new_path()
    ctx.move_to(-260, -330)
    ctx.curve_to(-260, -560, 260, -560, 260, -330)
    ctx.close_path()
    fs(ctx, "#8FAF9F")
    ctx.new_path()
    ctx.move_to(-120, -505)
    ctx.curve_to(-60, -540, 60, -540, 120, -505)
    set_rgb(ctx, "#FFFFFF", 0.35)
    ctx.set_line_width(14)
    ctx.stroke()
    rrect(ctx, -300, -350, 600, 40, 8)
    fs(ctx, "#C6C2B6")
    rrect(ctx, -440, -315, 880, 260, 6)
    fs(ctx, "#DDD8CB")
    for i in range(12):
        rrect(ctx, -405 + i * 70, -290, 30, 215, 8)
        fs(ctx, "#F1EEE5", lw=5)
    for i in range(3):
        rrect(ctx, -480 - i * 30, -55 + i * 22, 960 + i * 60, 24, 4)
        fs(ctx, "#C6C2B6", lw=5)
    ctx.restore()


def sigh(ctx, x, y, t, t0, seed=0):
    """한숨 구름 (위로 떠오르며 사라짐)."""
    for i in range(3):
        k = ((t - t0) * 0.6 + i / 3) % 1.0
        if t < t0:
            return
        r = 26 + 40 * k
        ellipse(ctx, x + 60 * k + wobble(t, i + seed, 10), y - 220 * k, r, r * 0.8)
        fs(ctx, "#F2F2F2", lw=5, alpha=1 - k)
