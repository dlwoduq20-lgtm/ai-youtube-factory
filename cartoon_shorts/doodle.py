"""'두둥실' 캐릭터 — 채널 고유 캐릭터 스타일 (ep04~).

특징: 몸에서 살짝 떠 있는 둥근 네모 머리, 막대 팔다리(졸라맨 느낌) + 동그란 손,
세로 점 눈 + 굵은 눈썹, 볼터치. squire.Person 과 같은 draw() 인터페이스라 샷 코드에서 바꿔 끼울 수 있다.
좌표: 발끝 (0, 0) 기준, 키 약 670.
"""
import math

import cairo

from . import squire as S
from .engine import clamp, ellipse, rrect, set_rgb

OUT = S.OUT
SKIN = "#FFF4E0"
BLUSH = "#F2A7A0"
HEAD_Y = -540  # 머리 중심
HEAD_W, HEAD_H, HEAD_R = 280, 250, 105


def _squircle(ctx, cx, cy, w=HEAD_W, h=HEAD_H, r=HEAD_R):
    rrect(ctx, cx - w / 2, cy - h / 2, w, h, r)


def _line(ctx, pts, width, color):
    ctx.new_path()
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    set_rgb(ctx, OUT)
    ctx.set_line_width(width + 12)
    ctx.stroke_preserve()
    set_rgb(ctx, color)
    ctx.set_line_width(width)
    ctx.stroke()


class Doodle:
    def __init__(self, coat="#4E5A6B", tie=None, hair="cap", hair_color="#3A2A20",
                 pants="#3A3F4A", badge=False, glasses=False, skin=SKIN, collar=True):
        self.coat, self.tie, self.hair, self.hair_color = coat, tie, hair, hair_color
        self.pants, self.badge, self.glasses, self.skin = pants, badge, glasses, skin
        self.collar = collar

    def draw(self, ctx, x, y, s=1.0, facing=1, pose="down", expr="neutral", mouth=0.0,
             t=0.0, rot=0.0, bob=True, sweat=False):
        ctx.save()
        ctx.translate(x, y)
        ctx.rotate(rot)
        ctx.scale(s * facing, s)
        hop = abs(math.sin(t * 2.4)) * 8 if bob else 0.0
        back, front = S.Person._arms(None, pose, t)
        back = [(px * 0.85, py + 10) for px, py in back]
        front = [(px * 0.85, py + 10) for px, py in front]
        # 다리 + 신발
        for dx in (-40, 40):
            _line(ctx, [(dx * 0.8, -150), (dx, -22)], 20, self.pants)
            rrect(ctx, dx - 22 + 8, -32, 56, 32, 16)
            S.fs(ctx, "#2E2A28", lw=6)
        ctx.translate(0, -hop)
        # 뒤팔
        _line(ctx, back, 20, S._shade(self.coat, 0.85))
        ellipse(ctx, *back[-1], 27, 27)
        S.fs(ctx, self.skin, lw=6)
        # 몸통: 아래가 살짝 넓은 둥근 사다리꼴
        ctx.new_path()
        ctx.move_to(-62, -372)
        ctx.curve_to(-98, -330, -106, -200, -98, -150)
        ctx.curve_to(-50, -132, 50, -132, 98, -150)
        ctx.curve_to(106, -200, 98, -330, 62, -372)
        ctx.curve_to(25, -386, -25, -386, -62, -372)
        ctx.close_path()
        S.fs(ctx, self.coat, lw=8)
        if self.collar:
            ctx.new_path()
            ctx.move_to(-34, -380)
            ctx.line_to(0, -318)
            ctx.line_to(34, -380)
            ctx.close_path()
            S.fs(ctx, "#F6F3EC", lw=6)
        if self.tie:
            ctx.new_path()
            ctx.move_to(-10, -372)
            ctx.line_to(10, -372)
            ctx.line_to(15, -300)
            ctx.line_to(0, -282)
            ctx.line_to(-15, -300)
            ctx.close_path()
            S.fs(ctx, self.tie, lw=5)
        if self.badge:
            ellipse(ctx, -60, -330, 13, 13)
            S.fs(ctx, "#E8B93E", lw=5)
        # 떠 있는 머리 (몸과 살짝 떨어짐 + 미세하게 둥실)
        ctx.save()
        ctx.translate(0, math.sin(t * 3.1) * 5)
        ctx.rotate(math.sin(t * 1.7) * 0.04)
        self._head(ctx, expr, mouth, t, sweat)
        ctx.restore()
        # 앞팔
        _line(ctx, front, 20, self.coat)
        ellipse(ctx, *front[-1], 28, 28)
        S.fs(ctx, self.skin, lw=6)
        ctx.restore()

    def _hair_back(self, ctx):
        if self.hair == "bob":
            rrect(ctx, -HEAD_W / 2 - 22, HEAD_Y - HEAD_H / 2 - 10, HEAD_W + 44, HEAD_H * 0.95, 90)
            S.fs(ctx, self.hair_color, lw=8)

    def _hair_front(self, ctx):
        top = HEAD_Y - HEAD_H / 2
        if self.hair in ("cap", "bob"):  # 앞머리: 머리 윗부분을 덮고 가르마 홈
            ctx.save()
            _squircle(ctx, 0, HEAD_Y)
            ctx.clip()
            ctx.new_path()
            ctx.move_to(-HEAD_W, top - 20)
            ctx.line_to(HEAD_W, top - 20)
            ctx.line_to(HEAD_W, top + 78)
            ctx.curve_to(80, top + 98, 40, top + 60, 10, top + 50)
            ctx.curve_to(-40, top + 92, -100, top + 100, -HEAD_W, top + 86)
            ctx.close_path()
            S.fs(ctx, self.hair_color, lw=0)
            ctx.restore()
        elif self.hair == "tuft":  # 정수리 한 가닥
            ctx.new_path()
            ctx.move_to(-10, top + 4)
            ctx.curve_to(-30, top - 70, 60, top - 90, 40, top - 40)
            ctx.curve_to(30, top - 20, 10, top - 40, 22, top - 52)
            set_rgb(ctx, OUT)
            ctx.set_line_width(10)
            ctx.stroke()
        elif self.hair == "beanie":
            rrect(ctx, -HEAD_W / 2 + 4, top - 78, HEAD_W - 8, 110, 50)
            S.fs(ctx, self.hair_color, lw=8)
            rrect(ctx, -HEAD_W / 2 - 8, top + 4, HEAD_W + 16, 40, 18)
            S.fs(ctx, S._shade(self.hair_color, 0.85), lw=8)
            ellipse(ctx, 0, top - 92, 28, 28)
            S.fs(ctx, "#F2E6CF", lw=7)
        elif self.hair == "gray":  # 옆머리만 남은 희끗한 머리
            for sg in (-1, 1):
                ellipse(ctx, sg * (HEAD_W / 2 - 4), HEAD_Y - 30, 30, 60)
                S.fs(ctx, self.hair_color, lw=7)

    def _head(self, ctx, expr, mouth, t, sweat):
        self._hair_back(ctx)
        _squircle(ctx, 0, HEAD_Y)
        S.fs(ctx, self.skin, lw=9)
        ctx.save()  # 한쪽 음영
        _squircle(ctx, 0, HEAD_Y)
        ctx.clip()
        ellipse(ctx, HEAD_W / 2 + 40, HEAD_Y + 30, 90, 170)
        set_rgb(ctx, (0, 0, 0, 0.06))
        ctx.fill()
        ctx.restore()
        self._hair_front(ctx)
        fx = 20
        ey = HEAD_Y + 2
        eyes = (fx - 42, fx + 48)
        set_rgb(ctx, OUT)
        if expr == "smug":
            for ex in eyes:
                ctx.new_path()
                ctx.arc(ex, ey + 8, 18, math.pi * 1.1, math.pi * 1.9)
                ctx.set_line_width(8)
                ctx.set_line_cap(cairo.LINE_CAP_ROUND)
                ctx.stroke()
        elif expr == "shock":
            for ex in eyes:
                ellipse(ctx, ex, ey, 20, 24)
                S.fs(ctx, "#FFFFFF", lw=6)
                ellipse(ctx, ex, ey, 7, 7)
                set_rgb(ctx, OUT)
                ctx.fill()
        else:
            blink = (t * 0.55) % 1.0 > 0.95
            for ex in eyes:
                if blink:
                    ctx.move_to(ex - 10, ey)
                    ctx.line_to(ex + 10, ey)
                    ctx.set_line_width(7)
                    ctx.stroke()
                else:
                    rrect(ctx, ex - 8, ey - 16, 16, 32, 8)
                    ctx.fill()
        # 굵은 눈썹
        tilt = {"angry": 0.35, "sad": -0.3, "shock": 0.0, "deadpan": 0.0}.get(expr, 0.08)
        lift = {"shock": -18, "deadpan": 6}.get(expr, 0)
        for ex, sg in ((eyes[0], 1), (eyes[1], -1)):
            ctx.save()
            ctx.translate(ex, ey - 40 + lift)
            ctx.rotate(tilt * sg)
            rrect(ctx, -22, -6, 44, 12, 6)
            set_rgb(ctx, OUT)
            ctx.fill()
            ctx.restore()
        if self.glasses:
            for ex in eyes:
                rrect(ctx, ex - 32, ey - 26, 64, 52, 14)
                set_rgb(ctx, "#FFFFFF", 0.2)
                ctx.fill_preserve()
                set_rgb(ctx, OUT)
                ctx.set_line_width(6)
                ctx.stroke()
            ctx.move_to(eyes[0] + 32, ey - 6)
            ctx.line_to(eyes[1] - 32, ey - 6)
            ctx.stroke()
        # 볼터치
        for ex in (eyes[0] - 18, eyes[1] + 22):
            ellipse(ctx, ex, ey + 40, 22, 12)
            set_rgb(ctx, BLUSH, 0.55)
            ctx.fill()
        # 입
        mx, my = fx + 4, HEAD_Y + 72
        m = clamp(mouth)
        if m > 0.05 or expr == "shock":
            h = 10 + 40 * max(m, 0.55 if expr == "shock" else 0)
            rrect(ctx, mx - 30, my - h / 2, 60, h, min(30, h / 2))
            S.fs(ctx, "#7B2730", lw=6)
        elif expr == "smug":
            ctx.new_path()
            ctx.arc(mx, my - 14, 30, math.pi * 0.15, math.pi * 0.85)
            set_rgb(ctx, OUT)
            ctx.set_line_width(8)
            ctx.stroke()
        elif expr in ("sad", "angry"):
            ctx.new_path()
            ctx.arc(mx, my + 22, 26, math.pi * 1.2, math.pi * 1.8)
            set_rgb(ctx, OUT)
            ctx.set_line_width(8)
            ctx.stroke()
        else:
            ctx.move_to(mx - 22, my)
            ctx.line_to(mx + 22, my)
            set_rgb(ctx, OUT)
            ctx.set_line_width(8)
            ctx.stroke()
        if sweat:
            k = (t * 1.3) % 1.0
            ellipse(ctx, -HEAD_W / 2 + 10, HEAD_Y - 40 + 60 * k, 13, 18)
            set_rgb(ctx, "#9FD3F0", 1 - k)
            ctx.fill()
