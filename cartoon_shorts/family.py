"""육아·일상 쇼츠용 캐릭터/배경/소품 (파스텔 톤 집 안 풍경).

squire.py 의 그림체(굵은 외곽선 + 흰 동그란 얼굴)를 그대로 따르고,
아기 캐릭터와 집 안 배경(침실/부엌/현관), 소품(침대, 아기 의자, 저금통, 하트)을 더한다.
모든 캐릭터 좌표는 발 중심이 원점(위쪽 -y).
"""
import math
import random

import cairo

from . import squire as S
from .engine import H, W, clamp, draw_text, ellipse, rrect, set_rgb

CHEEK = "#F4A7B0"
PINK, PINK_D = "#F6B9C4", "#E392A3"
SKY, SKY_D = "#BFE0F2", "#9CCBE4"


# ================================================================ 아기
class Baby:
    def __init__(self, onesie="#FFD978", hair_color="#5A3C2C", bib="#FFFFFF"):
        self.onesie, self.hair_color, self.bib = onesie, hair_color, bib

    # 포즈: (뒤팔 [어깨, 팔꿈치, 손], 앞팔 [...])
    def _arms(self, pose, t):
        if pose == "cheer":
            w = math.sin(t * 10) * 18
            return ([(-60, -175), (-105, -235), (-118 + w, -300)],
                    [(60, -175), (105, -235), (118 - w, -300)])
        if pose == "wave":
            w = math.sin(t * 11) * 35
            return ([(-60, -175), (-82, -130), (-86, -92)],
                    [(60, -175), (115, -240), (135 + w, -320)])
        if pose == "reach":
            return ([(-60, -175), (5, -195), (70, -215)],
                    [(60, -175), (125, -205), (185, -235)])
        if pose == "pull":
            return ([(-60, -175), (20, -150), (105, -150)],
                    [(60, -175), (120, -160), (175, -165)])
        if pose == "hold":  # 가슴 앞에 무언가 들고 있기
            return ([(-60, -175), (-55, -120), (-5, -150)],
                    [(60, -175), (55, -120), (5, -150)])
        if pose == "offer":  # 두 손으로 앞으로 내밀기
            return ([(-60, -175), (20, -185), (95, -205)],
                    [(60, -175), (125, -175), (165, -205)])
        return ([(-60, -175), (-82, -130), (-86, -92)],
                [(60, -175), (82, -130), (86, -92)])

    def draw(self, ctx, x, y, s=1.0, facing=1, pose="down", expr="neutral", mouth=0.0,
             t=0.0, rot=0.0, bob=True, legs=True):
        ctx.save()
        ctx.translate(x, y)
        ctx.rotate(rot)
        ctx.scale(s * facing, s)
        if bob:
            ctx.translate(0, -abs(math.sin(t * 3.0)) * 5)
        back, front = self._arms(pose, t)
        dark = S._shade(self.onesie, 0.85)
        if legs:
            for dx in (-36, 36):
                rrect(ctx, dx - 27, -72, 54, 66, 24)
                S.fs(ctx, dark)
                ellipse(ctx, dx + 6, -10, 34, 15)
                S.fs(ctx, "#FFFFFF", lw=5)
        S.tube(ctx, back, 36, dark)
        ellipse(ctx, *back[-1], 23, 23)
        S.fs(ctx, S.FACE, lw=6)
        # 몸통 (우주복)
        ctx.new_path()
        ctx.move_to(-62, -195)
        ctx.curve_to(-95, -150, -100, -85, -82, -55)
        ctx.curve_to(-30, -40, 30, -40, 82, -55)
        ctx.curve_to(100, -85, 95, -150, 62, -195)
        ctx.curve_to(25, -208, -25, -208, -62, -195)
        ctx.close_path()
        S.fs(ctx, self.onesie)
        # 턱받이 + 하트
        ctx.new_path()
        ctx.move_to(-50, -196)
        ctx.curve_to(-50, -130, 50, -130, 50, -196)
        ctx.close_path()
        S.fs(ctx, self.bib, lw=5)
        heart(ctx, 0, -168, 0.5, "#F08A9B", lw=3)
        self._head(ctx, expr, mouth, t)
        S.tube(ctx, front, 36, self.onesie)
        ellipse(ctx, *front[-1], 24, 24)
        S.fs(ctx, S.FACE, lw=6)
        ctx.restore()

    def _head(self, ctx, expr, mouth, t):
        hx, hy = 0, -318
        ellipse(ctx, hx, hy, 132, 122)
        S.fs(ctx, S.FACE)
        ctx.save()
        ellipse(ctx, hx, hy, 128, 118)
        ctx.clip()
        ellipse(ctx, hx + 160, hy + 50, 90, 170)
        set_rgb(ctx, S.FACE_SH)
        ctx.fill()
        ctx.restore()
        ellipse(ctx, hx, hy, 132, 122)
        S.fs(ctx, None)
        # 앞머리 몇 가닥 + 꼬불 머리
        set_rgb(ctx, self.hair_color)
        ctx.set_line_width(9)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.new_path()
        ctx.move_to(-10, hy - 120)
        ctx.curve_to(-30, hy - 175, 40, hy - 195, 35, hy - 150)
        ctx.curve_to(30, hy - 125, 5, hy - 135, 12, hy - 150)
        ctx.stroke()
        for dx in (-60, -30):
            ctx.move_to(dx, hy - 112)
            ctx.curve_to(dx + 8, hy - 95, dx + 18, hy - 92, dx + 26, hy - 100)
        ctx.stroke()
        fx = 14
        ey = hy + 2
        ex1, ex2 = -40 + fx, 46 + fx
        # 볼터치
        for cx in (ex1 - 30, ex2 + 30):
            ellipse(ctx, cx, hy + 46, 26, 15)
            set_rgb(ctx, CHEEK, 0.75)
            ctx.fill()
        set_rgb(ctx, S.OUT)
        if expr in ("happy", "kiss"):
            for ex in (ex1, ex2):
                ctx.new_path()
                ctx.arc(ex, ey + 8, 17, math.pi * 1.1, math.pi * 1.9)
                ctx.set_line_width(7)
                ctx.stroke()
        else:
            blink = (t * 0.55) % 1.0 > 0.95 and expr != "sparkle"
            big = 1.25 if expr == "sparkle" else 1.0
            for ex in (ex1, ex2):
                if blink:
                    ctx.move_to(ex - 12, ey)
                    ctx.line_to(ex + 12, ey)
                    ctx.set_line_width(6)
                    ctx.stroke()
                else:
                    ellipse(ctx, ex, ey, 16 * big, 20 * big)
                    set_rgb(ctx, S.OUT)
                    ctx.fill()
                    ellipse(ctx, ex + 5, ey - 7, 6 * big, 6 * big)
                    set_rgb(ctx, "#FFFFFF")
                    ctx.fill()
                    if expr == "sparkle":
                        ellipse(ctx, ex - 6, ey + 8, 3, 3)
                        ctx.fill()
                    set_rgb(ctx, S.OUT)
            if expr in ("sad", "pout"):
                sg = -1 if expr == "sad" else 1
                for ex, d in ((ex1, 1), (ex2, -1)):
                    ctx.move_to(ex - 14, ey - 32 - 6 * d * sg)
                    ctx.line_to(ex + 14, ey - 32 + 6 * d * sg)
                ctx.set_line_width(6)
                ctx.stroke()
            if expr == "sad":
                k = (t * 0.9) % 1.0
                tx, ty = ex2 + 6, ey + 24 + k * 40
                ctx.new_path()
                ctx.move_to(tx, ty - 14)
                ctx.curve_to(tx + 10, ty, tx + 8, ty + 9, tx, ty + 9)
                ctx.curve_to(tx - 8, ty + 9, tx - 10, ty, tx, ty - 14)
                S.fs(ctx, "#A9D8F2", lw=3, alpha=1 - 0.6 * k)
        # 입
        mx, my = fx + 4, hy + 52
        m = clamp(mouth)
        if expr == "kiss" and m < 0.3:
            ellipse(ctx, mx + 6, my, 13, 11)
            S.fs(ctx, "#E77E86", lw=5)
        elif m > 0.05:
            h = 6 + 30 * m
            ctx.new_path()
            ctx.move_to(mx - 20, my - 3)
            ctx.curve_to(mx - 20, my + h, mx + 20, my + h, mx + 20, my - 3)
            ctx.close_path()
            S.fs(ctx, "#7B2730", lw=5)
            if h > 16:
                ellipse(ctx, mx, my + h * 0.5, 10, h * 0.16)
                set_rgb(ctx, "#E77E86")
                ctx.fill()
        elif expr in ("happy", "sparkle"):
            ctx.new_path()
            ctx.move_to(mx - 18, my - 2)
            ctx.curve_to(mx - 16, my + 22, mx + 16, my + 22, mx + 18, my - 2)
            ctx.close_path()
            S.fs(ctx, "#7B2730", lw=5)
        elif expr == "pout":
            ctx.new_path()
            ctx.move_to(mx - 8, my - 6)
            ctx.curve_to(mx + 6, my - 4, mx + 6, my + 4, mx - 4, my + 2)
            ctx.curve_to(mx + 8, my + 4, mx + 8, my + 12, mx - 8, my + 12)
            set_rgb(ctx, S.OUT)
            ctx.set_line_width(5)
            ctx.stroke()
        else:
            ctx.new_path()
            if expr == "sad":
                ctx.move_to(mx - 14, my + 10)
                ctx.curve_to(mx - 5, my + 2, mx + 5, my + 2, mx + 14, my + 10)
            else:
                ctx.move_to(mx - 14, my)
                ctx.curve_to(mx - 5, my + 10, mx + 5, my + 10, mx + 14, my)
            set_rgb(ctx, S.OUT)
            ctx.set_line_width(5)
            ctx.stroke()


def lying_head(ctx, person, x, y, s, expr="neutral", mouth=0.0, t=0.0):
    """베개 위에 누운 머리 (정수리가 왼쪽, 얼굴이 위를 봄). (x, y) = 머리 중심."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.rotate(-math.pi / 2)
    ctx.translate(0, 485)
    person._head(ctx, expr, mouth, t, False)
    ctx.restore()


# ================================================================ 배경
def wall(ctx, base, dot, floor_y=1250, floor="#D9B48A", floor_d="#C49C70", seed=1):
    """파스텔 벽지(물방울 무늬) + 마룻바닥."""
    ctx.rectangle(-200, -200, W + 400, floor_y + 200)
    set_rgb(ctx, base)
    ctx.fill()
    set_rgb(ctx, dot, 0.5)
    for r in range(0, floor_y // 90 + 2):
        for c in range(-1, W // 90 + 2):
            ellipse(ctx, c * 90 + (45 if r % 2 else 0), r * 90 + 30, 9, 9)
            ctx.fill()
    # 걸레받이
    ctx.rectangle(-200, floor_y - 34, W + 400, 34)
    S.fs(ctx, "#FFFFFF", lw=5)
    ctx.rectangle(-200, floor_y, W + 400, H - floor_y + 200)
    set_rgb(ctx, floor)
    ctx.fill()
    rnd = random.Random(seed)
    set_rgb(ctx, floor_d)
    ctx.set_line_width(5)
    y = floor_y + 70
    gap = 70
    while y < H + 100:
        ctx.move_to(-200, y)
        ctx.line_to(W + 200, y)
        off = rnd.uniform(0, 300)
        for xx in range(-1, 5):
            bx = off + xx * 330
            ctx.move_to(bx, y - gap)
            ctx.line_to(bx, y)
        y += gap
        gap *= 1.12
    ctx.stroke()


def window(ctx, x, y, w, h, sky_top="#9ED3F0", sky_bot="#FFE9B8", t=0.0, sun_k=1.0):
    rrect(ctx, x - 18, y - 18, w + 36, h + 36, 18)
    S.fs(ctx, "#FFFFFF")
    ctx.save()
    rrect(ctx, x, y, w, h, 8)
    ctx.clip()
    g = cairo.LinearGradient(0, y, 0, y + h)
    g.add_color_stop_rgb(0, *_rgb(sky_top))
    g.add_color_stop_rgb(1, *_rgb(sky_bot))
    ctx.rectangle(x, y, w, h)
    ctx.set_source(g)
    ctx.fill()
    if sun_k > 0:
        sun(ctx, x + w * 0.62, y + h * 0.95 - h * 0.55 * sun_k, 70, t)
    S.cloud(ctx, x + 20 + (t * 12) % 60, y + 60, 0.45, "#FFFFFF", 0.9)
    ctx.restore()
    rrect(ctx, x, y, w, h, 8)
    S.fs(ctx, None, lw=8)
    ctx.move_to(x + w / 2, y)
    ctx.line_to(x + w / 2, y + h)
    ctx.move_to(x, y + h / 2)
    ctx.line_to(x + w, y + h / 2)
    set_rgb(ctx, "#FFFFFF")
    ctx.set_line_width(14)
    ctx.stroke()
    # 커튼
    for sx, sg in ((x - 30, 1), (x + w + 30, -1)):
        ctx.new_path()
        ctx.move_to(sx, y - 40)
        ctx.line_to(sx + sg * 90, y - 40)
        ctx.curve_to(sx + sg * 40, y + h * 0.5, sx + sg * 70, y + h * 0.8, sx + sg * 50, y + h + 40)
        ctx.line_to(sx, y + h + 40)
        ctx.close_path()
        S.fs(ctx, "#F7C9C2")


def sun(ctx, x, y, r, t):
    set_rgb(ctx, "#FFC94A")
    ctx.set_line_width(10)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for i in range(10):
        a = i * math.pi / 5 + t * 0.4
        ctx.move_to(x + math.cos(a) * (r + 16), y + math.sin(a) * (r + 16))
        ctx.line_to(x + math.cos(a) * (r + 40), y + math.sin(a) * (r + 40))
    ctx.stroke()
    ellipse(ctx, x, y, r, r)
    S.fs(ctx, "#FFD95A", lw=6)
    set_rgb(ctx, S.OUT)
    for ex in (-22, 22):
        ctx.new_path()
        ctx.arc(x + ex, y - 4, 10, math.pi * 1.1, math.pi * 1.9)
        ctx.set_line_width(5)
        ctx.stroke()
    ctx.new_path()
    ctx.arc(x, y + 14, 16, math.pi * 0.15, math.pi * 0.85)
    ctx.stroke()
    for ex in (-38, 38):
        ellipse(ctx, x + ex, y + 16, 11, 7)
        set_rgb(ctx, CHEEK, 0.8)
        ctx.fill()
    set_rgb(ctx, S.OUT)


def frame_pic(ctx, x, y, w, h, kind=0, rot=0.0):
    """벽에 걸린 액자 (아기 손바닥 / 하트 / 집)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    rrect(ctx, -w / 2, -h / 2, w, h, 10)
    S.fs(ctx, "#E9C89B")
    rrect(ctx, -w / 2 + 16, -h / 2 + 16, w - 32, h - 32, 6)
    S.fs(ctx, "#FFFDF5", lw=5)
    if kind == 0:
        heart(ctx, 0, 0, 1.1, "#F08A9B", lw=4)
    elif kind == 1:
        ellipse(ctx, 0, 6, 26, 30)
        S.fs(ctx, "#9CCBE4", lw=4)
        for i in range(5):
            a = math.pi * (1.05 + i * 0.22)
            ellipse(ctx, math.cos(a) * 40, 6 + math.sin(a) * 44, 9, 13)
            S.fs(ctx, "#9CCBE4", lw=4)
    else:
        ctx.new_path()
        ctx.move_to(-40, 0)
        ctx.line_to(0, -36)
        ctx.line_to(40, 0)
        ctx.close_path()
        S.fs(ctx, "#E3826F", lw=4)
        ctx.rectangle(-30, 0, 60, 40)
        S.fs(ctx, "#FFE6A8", lw=4)
    ctx.restore()


def bed(ctx, x0, x1, y_top, floor_y):
    """침대 (헤드보드 왼쪽). 매트리스 윗면 y_top."""
    rrect(ctx, x0 - 30, y_top - 330, 70, 330 + floor_y - y_top, 24)
    S.fs(ctx, "#C99A6B")
    rrect(ctx, x0, y_top - 20, x1 - x0, 60, 26)
    S.fs(ctx, "#FFFFFF")
    rrect(ctx, x0, y_top + 30, x1 - x0, floor_y - y_top - 60, 14)
    S.fs(ctx, "#D7AE7D")
    for lx in (x0 + 20, x1 - 60):
        rrect(ctx, lx, floor_y - 40, 40, 50, 8)
        S.fs(ctx, "#B88A5C")


def pillow(ctx, x, y, w, h):
    rrect(ctx, x - w / 2, y - h / 2, w, h, h / 2.2)
    S.fs(ctx, "#FFFFFF")
    ctx.move_to(x - w / 2 + 30, y + h * 0.15)
    ctx.curve_to(x - 20, y + h * 0.3, x + 20, y + h * 0.3, x + w / 2 - 30, y + h * 0.15)
    set_rgb(ctx, "#D9DCE3")
    ctx.set_line_width(5)
    ctx.stroke()


def blanket(ctx, x0, y0, x1, y1, color="#BFE0F2", dots="#FFFFFF", lump=0.0):
    ctx.new_path()
    ctx.move_to(x0, y0 + 40)
    ctx.curve_to(x0 + (x1 - x0) * 0.3, y0 - 30 - lump, x0 + (x1 - x0) * 0.7, y0 - 30 - lump,
                 x1, y0 + 20)
    ctx.line_to(x1 + 20, y1)
    ctx.line_to(x0 - 10, y1)
    ctx.close_path()
    S.fs(ctx, color)
    ctx.save()
    ctx.new_path()
    ctx.move_to(x0, y0 + 40)
    ctx.curve_to(x0 + (x1 - x0) * 0.3, y0 - 30 - lump, x0 + (x1 - x0) * 0.7, y0 - 30 - lump,
                 x1, y0 + 20)
    ctx.line_to(x1 + 20, y1)
    ctx.line_to(x0 - 10, y1)
    ctx.close_path()
    ctx.clip()
    set_rgb(ctx, dots, 0.8)
    for r in range(8):
        for c in range(12):
            star(ctx, x0 + c * 70 + (35 if r % 2 else 0), y0 + r * 70, 12)
            ctx.fill()
    ctx.restore()
    # 이불 접힌 단
    ctx.new_path()
    ctx.move_to(x0 + 6, y0 + 40)
    ctx.curve_to(x0 + 30, y0 + 70, x0 + 40, y1 - 60, x0 + 20, y1)
    set_rgb(ctx, S.OUT, 0.25)
    ctx.set_line_width(6)
    ctx.stroke()


def kitchen(ctx, floor_y=1300, t=0.0):
    wall(ctx, "#D9F0E3", "#B6DEC8", floor_y=floor_y, floor="#E6C9A0", floor_d="#CDAE84", seed=4)
    # 타일 줄눈 (조리대 뒤)
    ctx.rectangle(-50, 560, W + 100, 280)
    set_rgb(ctx, "#FFFFFF")
    ctx.fill()
    set_rgb(ctx, "#CFE3DA")
    ctx.set_line_width(4)
    for i in range(0, W + 100, 70):
        ctx.move_to(i, 560)
        ctx.line_to(i, 840)
    for j in range(560, 841, 70):
        ctx.move_to(-50, j)
        ctx.line_to(W + 50, j)
    ctx.stroke()
    # 위쪽 찬장
    for i in range(4):
        rrect(ctx, 40 + i * 255, 120, 235, 330, 14)
        S.fs(ctx, "#FFF7E8")
        ellipse(ctx, 40 + i * 255 + (200 if i % 2 == 0 else 35), 400, 9, 9)
        S.fs(ctx, "#C9A26E", lw=4)
    # 조리대
    rrect(ctx, -40, 830, W + 80, 50, 10)
    S.fs(ctx, "#F2EAD8")
    ctx.rectangle(-40, 880, W + 80, floor_y - 880)
    S.fs(ctx, "#9CCBB2")
    for i in range(5):
        rrect(ctx, 20 + i * 215, 910, 195, floor_y - 950, 10)
        S.fs(ctx, "#B4DCC6", lw=5)
    # 냄비 + 김
    rrect(ctx, 760, 720, 170, 115, 18)
    S.fs(ctx, "#E3826F")
    rrect(ctx, 740, 705, 210, 30, 12)
    S.fs(ctx, "#C96B5A")
    set_rgb(ctx, "#FFFFFF", 0.7)
    ctx.set_line_width(10)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for i, dx in enumerate((810, 860, 905)):
        ph = t * 2 + i
        ctx.move_to(dx, 690)
        ctx.curve_to(dx + 18 * math.sin(ph), 650, dx - 18 * math.sin(ph), 610, dx, 570)
    ctx.stroke()


def table(ctx, y, x0=-40, x1=W + 40, color="#E9C89B"):
    """식탁 (앞판이 화면 아래까지 내려와 뒤에 선 인물의 하체를 가림)."""
    rrect(ctx, x0, y, x1 - x0, 46, 14)
    S.fs(ctx, color)
    ctx.rectangle(x0 + 20, y + 46, x1 - x0 - 40, H - y)
    S.fs(ctx, S._shade(color, 0.88))
    set_rgb(ctx, S._shade(color, 0.78))
    ctx.set_line_width(5)
    for yy in range(int(y) + 140, H, 120):
        ctx.move_to(x0 + 20, yy)
        ctx.line_to(x1 - 20, yy)
    ctx.stroke()


def high_chair_back(ctx, x, y, w=300, h=420):
    """아기 의자 등받이 (아기보다 먼저 그림). (x, y) = 좌석 중심."""
    rrect(ctx, x - w / 2, y - h, w, h + 40, 60)
    S.fs(ctx, "#F7A8A0")
    rrect(ctx, x - w / 2 + 26, y - h + 26, w - 52, h - 30, 44)
    S.fs(ctx, "#FFD3CC", lw=5)


def bowl(ctx, x, y, s=1.0, color="#9CCBE4", food="#FFF4D6"):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ellipse(ctx, 0, -40, 90, 26)
    S.fs(ctx, food, lw=6)
    for dx, dy in ((-30, -48), (0, -54), (28, -46), (-10, -40), (40, -38)):
        ellipse(ctx, dx, dy, 12, 8)
        S.fs(ctx, "#FFFFFF", lw=3)
    ctx.new_path()
    ctx.move_to(-92, -40)
    ctx.curve_to(-85, 30, 85, 30, 92, -40)
    ctx.close_path()
    S.fs(ctx, color)
    ctx.restore()


def spoon(ctx, x, y, s=1.0, rot=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    rrect(ctx, -9, 0, 18, 120, 9)
    S.fs(ctx, "#F08A9B", lw=5)
    ellipse(ctx, 0, -10, 28, 36)
    S.fs(ctx, "#F2F2F2", lw=5)
    ctx.restore()


def ice_cream(ctx, x, y, s=1.0, rot=0.0, scoops=("#F6B9C4", "#FFF0C2")):
    if s < 0.01:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    ctx.new_path()
    ctx.move_to(-50, 0)
    ctx.line_to(0, 140)
    ctx.line_to(50, 0)
    ctx.close_path()
    S.fs(ctx, "#E7B36A")
    set_rgb(ctx, "#C98F45")
    ctx.set_line_width(4)
    for k in (-30, 0, 30):
        ctx.move_to(-40 + k * 0.3, 10 + abs(k))
        ctx.line_to(30 + k * 0.3, 60 + abs(k))
    ctx.stroke()
    for i, c in enumerate(scoops):
        ellipse(ctx, 0, -38 - i * 62, 58, 48)
        S.fs(ctx, c)
    for dx, dy, c in ((-20, -60, "#7FC8E8"), (18, -40, "#F7D35E"), (5, -110, "#9AD88A")):
        rrect(ctx, dx - 5, dy - 12, 10, 24, 5)
        set_rgb(ctx, c)
        ctx.fill()
    ellipse(ctx, 6, -170 - (len(scoops) - 2) * 62, 16, 16)
    S.fs(ctx, "#E2504F", lw=5)
    ctx.restore()


def think_bubble(ctx, x, y, w, h, tail, k=1.0):
    if k <= 0.01:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(k, k)
    for i in range(10):
        a = i * math.pi / 5
        ellipse(ctx, math.cos(a) * w * 0.42, math.sin(a) * h * 0.38, w * 0.22, h * 0.24)
    set_rgb(ctx, S.OUT)
    ctx.fill()
    ellipse(ctx, 0, 0, w * 0.5, h * 0.44)
    ctx.fill()
    for i in range(10):
        a = i * math.pi / 5
        ellipse(ctx, math.cos(a) * w * 0.42, math.sin(a) * h * 0.38, w * 0.22 - 7, h * 0.24 - 7)
    set_rgb(ctx, "#FFFFFF")
    ctx.fill()
    ellipse(ctx, 0, 0, w * 0.5 - 7, h * 0.44 - 7)
    ctx.fill()
    tx, ty = tail[0] - x, tail[1] - y
    for i, r in enumerate((26, 18, 11)):
        f = 0.55 + i * 0.18
        ellipse(ctx, tx * f, ty * f, r, r)
        S.fs(ctx, "#FFFFFF", lw=6)
    ctx.restore()


def door(ctx, x, y, w, h, open_k=0.0, t=0.0):
    """현관문. open_k 0→1 이면 문이 열리며 바깥 햇살이 보임."""
    rrect(ctx, x - 24, y - 24, w + 48, h + 24, 12)
    S.fs(ctx, "#FFFFFF")
    ctx.rectangle(x, y, w, h)
    g = cairo.LinearGradient(0, y, 0, y + h)
    g.add_color_stop_rgb(0, *_rgb("#9ED3F0"))
    g.add_color_stop_rgb(0.75, *_rgb("#FFF3CF"))
    g.add_color_stop_rgb(0.75, *_rgb("#BFD98A"))
    g.add_color_stop_rgb(1, *_rgb("#A7C873"))
    ctx.set_source(g)
    ctx.fill()
    if open_k > 0:
        ctx.save()
        ctx.rectangle(x, y, w, h)
        ctx.clip()
        S.cloud(ctx, x + 30, y + 160, 0.5, "#FFFFFF")
        sun(ctx, x + w * 0.7, y + 140, 50, t)
        ctx.restore()
    dw = w * (1 - 0.82 * open_k)
    rrect(ctx, x, y, dw, h, 8)
    S.fs(ctx, "#B9805A")
    if dw > 120:
        for py in (y + 60, y + h * 0.55):
            rrect(ctx, x + 40, py, dw - 80, h * 0.33, 10)
            S.fs(ctx, "#A9714C", lw=5)
        ellipse(ctx, x + dw - 50, y + h * 0.52, 18, 18)
        S.fs(ctx, "#F2C14E", lw=5)


def shoe_rack(ctx, x, y):
    rrect(ctx, x, y - 170, 300, 170, 12)
    S.fs(ctx, "#E9C89B")
    for i, (c, s) in enumerate((("#5A6B7D", 1.0), ("#E3826F", 0.6), ("#F6B9C4", 0.6))):
        cx = x + 60 + i * 95
        ctx.new_path()
        ctx.move_to(cx - 40 * s, y - 175)
        ctx.curve_to(cx - 40 * s, y - 175 - 50 * s, cx + 10 * s, y - 175 - 40 * s, cx + 40 * s, y - 185)
        ctx.line_to(cx + 40 * s, y - 175)
        ctx.close_path()
        S.fs(ctx, c, lw=5)


def briefcase(ctx, x, y, s=1.0, rot=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    rrect(ctx, -26, -12, 52, 28, 10)
    S.fs(ctx, None, lw=8)
    rrect(ctx, -75, 10, 150, 105, 14)
    S.fs(ctx, "#7A4E33")
    ctx.move_to(-75, 45)
    ctx.line_to(75, 45)
    set_rgb(ctx, S.OUT)
    ctx.set_line_width(5)
    ctx.stroke()
    rrect(ctx, -12, 36, 24, 18, 4)
    S.fs(ctx, "#F2C14E", lw=4)
    ctx.restore()


def piggy(ctx, x, y, s=1.0, rot=0.0, t=0.0):
    if s < 0.01:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    for dx in (-45, 35):
        rrect(ctx, dx - 14, 30, 28, 40, 10)
        S.fs(ctx, PINK_D, lw=5)
    for dx in (-35, 20):
        ctx.new_path()
        ctx.move_to(dx, -55)
        ctx.line_to(dx + 18, -95)
        ctx.line_to(dx + 36, -50)
        ctx.close_path()
        S.fs(ctx, PINK_D, lw=5)
    ellipse(ctx, 0, 0, 100, 72)
    S.fs(ctx, PINK)
    ellipse(ctx, 92, 6, 26, 30)
    S.fs(ctx, PINK_D, lw=5)
    for dy in (-6, 14):
        ellipse(ctx, 92, dy, 4, 6)
        set_rgb(ctx, S.OUT)
        ctx.fill()
    ellipse(ctx, 48, -18, 7, 9)
    ctx.fill()
    rrect(ctx, -30, -66, 50, 10, 5)
    ctx.fill()
    # 동전 반짝
    k = (t * 1.3) % 1.0
    ellipse(ctx, -5, -90 - 40 * k, 18, 18)
    S.fs(ctx, "#F7D35E", lw=4, alpha=1 - k)
    ctx.restore()


# ================================================================ 효과
def heart(ctx, x, y, s, color="#F08A9B", lw=6, alpha=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.new_path()
    ctx.move_to(0, 30)
    ctx.curve_to(-60, -10, -40, -60, 0, -30)
    ctx.curve_to(40, -60, 60, -10, 0, 30)
    ctx.close_path()
    ctx.restore()
    S.fs(ctx, color, lw=lw, alpha=alpha)


def hearts(ctx, x, y, t, t0, n=7, spread=220, seed=1, dur=2.2):
    """t0 부터 위로 떠오르는 하트들."""
    if t < t0:
        return
    rnd = random.Random(seed)
    for i in range(n):
        d = rnd.uniform(0, 0.6)
        k = (t - t0 - d) / dur
        if not 0 < k < 1:
            continue
        hx = x + rnd.uniform(-spread, spread) * 0.5 + math.sin(k * 6 + i) * 25
        hy = y - k * rnd.uniform(260, 420)
        sc = (0.5 + 0.5 * rnd.random()) * min(1, k * 5)
        heart(ctx, hx, hy, sc, rnd.choice(("#F08A9B", "#F6B9C4", "#E2504F")), lw=5,
              alpha=1 - k ** 2)


def star(ctx, x, y, r):
    ctx.new_path()
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        ctx.line_to(x + math.cos(a) * rr, y + math.sin(a) * rr)
    ctx.close_path()


def sparkles(ctx, x, y, t, n=5, r=120, seed=2, color="#FFD54A"):
    rnd = random.Random(seed)
    for i in range(n):
        a = rnd.uniform(0, math.tau)
        ph = (t * 1.6 + rnd.random()) % 1.0
        sc = math.sin(ph * math.pi)
        star(ctx, x + math.cos(a) * r, y + math.sin(a) * r * 0.8, 22 * sc + 1)
        S.fs(ctx, color, lw=4)


def pop_text(ctx, text, x, y, k, size=110, fill="#F08A9B", rot=-0.12):
    """튀어나오는 의성어 ('쪽!', '번쩍!')."""
    if k <= 0:
        return
    from .engine import ease_out_back
    sc = ease_out_back(clamp(k * 2.2), 2.6)
    a = 1.0 if k < 0.8 else (1 - k) / 0.2
    draw_text(ctx, text, x, y, size, font="black", fill=fill, stroke=12, stroke_fill=S.OUT,
              scale=sc, rot=rot, alpha=a)


def _rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
