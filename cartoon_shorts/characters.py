"""캐리커처 캐릭터 (정치인 / 시민). 모든 좌표는 발 중심이 원점, 위쪽이 -y."""
import math

from .engine import (INK, draw_text, ellipse, fill_stroke, rrect, set_rgb,
                     thick_line, hexc)

SKIN = "#F4C9A1"
SKIN_DARK = "#E2A97F"


def _xf(p, x, y, s, facing, lean):
    """로컬 좌표 → 월드 좌표 (캐릭터 transform 과 동일한 순서)."""
    lx, ly = p
    lx *= s
    ly *= s
    ca, sa = math.cos(lean), math.sin(lean)
    rx, ry = lx * ca - ly * sa, lx * sa + ly * ca
    return x + rx * facing, y + ry


class Politician:
    """양복 입은 정치인. facing=1 이면 오른쪽을 봄."""

    def __init__(self, color, badge, hair="#2B2B33", tie="#C62F3A", seed=0):
        self.color, self.badge, self.hair, self.tie, self.seed = color, badge, hair, tie, seed

    def hand_world(self, x, y, s, facing, lean, hand_local):
        return _xf(hand_local, x, y, s, facing, lean)

    def draw(self, ctx, x, y, s=1.0, facing=1, lean=0.0, mood="angry", t=0.0,
             hands=((150, -300), (120, -285)), mouth_open=0.0, squash=1.0,
             leg_phase=None, sweat=False):
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(facing * s, s * squash)
        ctx.rotate(lean)

        # 다리
        k = math.sin(leg_phase) * 22 if leg_phase is not None else 0
        for dx, dk in ((-45, k), (45, -k)):
            thick_line(ctx, [(dx * 0.8, -170), (dx + dk, -18)], 52, "#34343D", outline=5)
            ellipse(ctx, dx + dk + 18, -12, 50, 20)
            fill_stroke(ctx, "#15151A", 5)

        # 뒤쪽 팔
        sh_b = (-70, -360)
        hb = hands[1]
        el_b = ((sh_b[0] + hb[0]) / 2 - 10, (sh_b[1] + hb[1]) / 2 + 40)
        thick_line(ctx, [sh_b, el_b, hb], 46, _shade(self.color, 0.82), outline=5)
        ellipse(ctx, hb[0], hb[1], 28, 26)
        fill_stroke(ctx, SKIN_DARK, 5)

        # 몸통
        ctx.new_path()
        ctx.move_to(-115, -385)
        ctx.curve_to(-140, -300, -120, -200, -105, -150)
        ctx.line_to(105, -150)
        ctx.curve_to(120, -200, 140, -300, 115, -385)
        ctx.curve_to(60, -405, -60, -405, -115, -385)
        ctx.close_path()
        fill_stroke(ctx, self.color, 7)
        # 셔츠 V + 넥타이
        ctx.new_path()
        ctx.move_to(-45, -392)
        ctx.line_to(0, -280)
        ctx.line_to(45, -392)
        ctx.close_path()
        fill_stroke(ctx, "#FFFFFF", 5)
        ctx.new_path()
        ctx.move_to(-13, -385)
        ctx.line_to(13, -385)
        ctx.line_to(20, -300)
        ctx.line_to(0, -275)
        ctx.line_to(-20, -300)
        ctx.close_path()
        fill_stroke(ctx, self.tie, 4)
        # 단추
        for by in (-235, -190):
            ellipse(ctx, 0, by, 6, 6)
            set_rgb(ctx, INK)
            ctx.fill()
        # 배지
        ellipse(ctx, -62, -330, 30, 30)
        fill_stroke(ctx, "#FFFFFF", 5)
        ctx.save()
        ctx.translate(-62, -330)
        if facing < 0:
            ctx.scale(-1, 1)
        draw_text(ctx, self.badge, 0, 2, 30, font="black", fill="#111111")
        ctx.restore()

        # 머리
        self._head(ctx, mood, t, mouth_open, sweat)

        # 앞쪽 팔
        sh_f = (80, -360)
        hf = hands[0]
        el_f = ((sh_f[0] + hf[0]) / 2 + 5, (sh_f[1] + hf[1]) / 2 + 45)
        thick_line(ctx, [sh_f, el_f, hf], 48, self.color, outline=6)
        ellipse(ctx, hf[0], hf[1], 30, 28)
        fill_stroke(ctx, SKIN, 6)
        ctx.restore()

    def _head(self, ctx, mood, t, mouth_open, sweat):
        hx, hy = 0, -490
        # 목
        rrect(ctx, -26, -420, 52, 40, 12)
        fill_stroke(ctx, SKIN_DARK, 5)
        # 귀
        ellipse(ctx, -92, hy + 5, 20, 26)
        fill_stroke(ctx, SKIN, 6)
        # 얼굴
        ctx.new_path()
        ctx.move_to(hx - 95, hy - 20)
        ctx.curve_to(hx - 100, hy - 110, hx + 95, hy - 120, hx + 95, hy - 30)
        ctx.curve_to(hx + 100, hy + 50, hx + 70, hy + 95, hx, hy + 98)
        ctx.curve_to(hx - 70, hy + 95, hx - 98, hy + 50, hx - 95, hy - 20)
        ctx.close_path()
        fill_stroke(ctx, SKIN, 7)
        # 머리카락 (빗어넘긴 2:8)
        ctx.new_path()
        ctx.move_to(hx - 98, hy - 10)
        ctx.curve_to(hx - 110, hy - 110, hx - 10, hy - 140, hx + 70, hy - 105)
        ctx.curve_to(hx + 100, hy - 90, hx + 105, hy - 60, hx + 92, hy - 45)
        ctx.curve_to(hx + 40, hy - 95, hx - 30, hy - 80, hx - 70, hy - 50)
        ctx.curve_to(hx - 80, hy - 35, hx - 85, hy - 20, hx - 98, hy - 10)
        ctx.close_path()
        fill_stroke(ctx, self.hair, 6)

        # 눈썹
        brow = {"angry": 0.35, "smug": -0.15, "shock": -0.35, "dizzy": 0.0}.get(mood, 0)
        for ex, sgn in ((15, -1), (70, 1)):
            ctx.save()
            ctx.translate(ex, hy - 45)
            ctx.rotate(brow * sgn * -1)
            rrect(ctx, -24, -7, 48, 14, 7)
            set_rgb(ctx, INK)
            ctx.fill()
            ctx.restore()
        # 눈
        for ex in (15, 70):
            if mood == "dizzy":
                ctx.save()
                ctx.translate(ex, hy - 12)
                ctx.rotate(t * 8)
                ctx.new_path()
                for i in range(30):
                    a = i * 0.6
                    r = i * 0.7
                    ctx.line_to(math.cos(a) * r, math.sin(a) * r)
                set_rgb(ctx, INK)
                ctx.set_line_width(4)
                ctx.stroke()
                ctx.restore()
                continue
            ellipse(ctx, ex, hy - 12, 17, 20 if mood != "shock" else 24)
            fill_stroke(ctx, "#FFFFFF", 4)
            px = 5 if mood != "shock" else 0
            ellipse(ctx, ex + px, hy - 10, 7, 8)
            set_rgb(ctx, INK)
            ctx.fill()
        # 코 (캐리커처)
        ctx.new_path()
        ctx.move_to(hx + 40, hy - 5)
        ctx.curve_to(hx + 115, hy + 5, hx + 120, hy + 45, hx + 55, hy + 40)
        fill_stroke(ctx, SKIN_DARK, 6)
        # 볼 홍조
        ellipse(ctx, hx - 20, hy + 35, 18, 10)
        set_rgb(ctx, "#E77A7A", 0.55)
        ctx.fill()
        # 입
        mo = mouth_open
        if mood in ("angry", "shock") or mo > 0.05:
            h = 10 + 32 * max(mo, 0.4 if mood == "shock" else mo)
            ellipse(ctx, hx + 45, hy + 68, 26, h / 2 + 4)
            fill_stroke(ctx, "#7A1A22", 5)
            ellipse(ctx, hx + 48, hy + 68 + h / 4, 14, h / 5 + 2)
            set_rgb(ctx, "#E35D6A")
            ctx.fill()
        else:
            ctx.new_path()
            if mood == "smug":
                ctx.move_to(hx + 15, hy + 62)
                ctx.curve_to(hx + 40, hy + 80, hx + 65, hy + 70, hx + 78, hy + 52)
            else:
                ctx.move_to(hx + 20, hy + 75)
                ctx.curve_to(hx + 40, hy + 60, hx + 60, hy + 62, hx + 75, hy + 75)
            set_rgb(ctx, INK)
            ctx.set_line_width(6)
            ctx.stroke()
        if mood == "angry":
            # 핏대
            ctx.save()
            ctx.translate(hx - 40, hy - 75)
            for a in range(4):
                ctx.save()
                ctx.rotate(a * math.pi / 2 + math.pi / 4)
                ctx.move_to(4, 0)
                ctx.curve_to(10, -4, 14, 4, 16, 0)
                ctx.restore()
            set_rgb(ctx, "#D7263D")
            ctx.set_line_width(5)
            ctx.stroke()
            ctx.restore()
        if sweat:
            _sweat(ctx, hx - 85, hy - 60, t)


def _sweat(ctx, x, y, t):
    for i, (dx, ph) in enumerate(((0, 0.0), (-25, 0.5))):
        k = (t * 1.6 + ph) % 1.0
        sy = y + k * 60
        ctx.new_path()
        ctx.move_to(x + dx, sy - 18)
        ctx.curve_to(x + dx + 14, sy, x + dx + 10, sy + 12, x + dx, sy + 12)
        ctx.curve_to(x + dx - 10, sy + 12, x + dx - 14, sy, x + dx, sy - 18)
        fill_stroke(ctx, "#8FD3FF", 4, alpha=1 - k * 0.6)


def _shade(c, k):
    r, g, b = hexc(c)
    return (r * k, g * k, b * k)


class Citizen:
    """평범한 시민 (후드티). 원점 = 발 중심."""

    def __init__(self, color="#7C8FA6", label="국민"):
        self.color, self.label = color, label

    def draw(self, ctx, x, y, s=1.0, sx=1.0, mood="worried", t=0.0, arms="up",
             rot=0.0, label=True):
        ctx.save()
        ctx.translate(x, y)
        ctx.rotate(rot)
        ctx.scale(s * sx, s / max(sx, 0.01) ** 0.5)

        sit = arms == "sign"
        # 다리
        if sit:
            for dx in (-32, 32):
                thick_line(ctx, [(dx, -60), (dx + 50 * (1 if dx > 0 else -1), -10)], 40, "#3B4A63", 5)
        else:
            kick = math.sin(t * 14) * 18 if arms == "up" else 0
            for dx, k in ((-28, kick), (28, -kick)):
                thick_line(ctx, [(dx, -110), (dx + k, -15)], 40, "#3B4A63", 5)
                ellipse(ctx, dx + k, -10, 30, 15)
                fill_stroke(ctx, "#F1F1F1", 5)
        base = -40 if sit else -100
        # 팔
        if arms == "up":
            wav = math.sin(t * 16) * 0.35
            for sgn in (-1, 1):
                a = -math.pi / 2 + sgn * (0.8 + wav * sgn)
                sh = (sgn * 55, base - 150)
                hand = (sh[0] + math.cos(a) * 110, sh[1] + math.sin(a) * 110)
                thick_line(ctx, [sh, hand], 34, self.color, 5)
                ellipse(ctx, hand[0], hand[1], 20, 20)
                fill_stroke(ctx, SKIN, 5)
        # 몸통 (후드티)
        rrect(ctx, -75, base - 190, 150, 200, 50)
        fill_stroke(ctx, self.color, 7)
        rrect(ctx, -40, base - 60, 80, 40, 14)
        fill_stroke(ctx, _shade(self.color, 0.85), 4)
        if label and self.label:
            draw_text(ctx, self.label, 0, base - 110, 44, font="black", fill="#FFFFFF",
                      stroke=4, stroke_fill="#111111")
        # 머리
        hy = base - 255
        ellipse(ctx, 0, hy, 82, 78)
        fill_stroke(ctx, SKIN, 7)
        ctx.new_path()
        ctx.arc(0, hy - 8, 84, math.pi * 1.05, math.pi * 1.95)
        ctx.curve_to(60, hy - 60, -40, hy - 40, -80, hy - 28)
        ctx.close_path()
        fill_stroke(ctx, "#3A2A22", 6)
        for ex in (-28, 28):
            if mood == "blank":
                ctx.new_path()
                ctx.move_to(ex - 12, hy + 2)
                ctx.line_to(ex + 12, hy + 2)
                set_rgb(ctx, INK)
                ctx.set_line_width(6)
                ctx.stroke()
            else:
                ellipse(ctx, ex, hy, 13, 17)
                fill_stroke(ctx, "#FFFFFF", 4)
                ellipse(ctx, ex, hy + 3, 6, 7)
                set_rgb(ctx, INK)
                ctx.fill()
            # 걱정 눈썹
            ctx.new_path()
            sg = 1 if ex > 0 else -1
            ctx.move_to(ex - 14 * sg, hy - 22)
            ctx.line_to(ex + 14 * sg, hy - 32)
            set_rgb(ctx, INK)
            ctx.set_line_width(6)
            ctx.stroke()
        ctx.new_path()
        if mood == "worried":
            ellipse(ctx, 0, hy + 40, 16, 12 + 4 * math.sin(t * 20))
            fill_stroke(ctx, "#7A1A22", 5)
        else:
            ctx.move_to(-20, hy + 42)
            ctx.curve_to(-8, hy + 34, 8, hy + 50, 20, hy + 40)
            set_rgb(ctx, INK)
            ctx.set_line_width(6)
            ctx.stroke()
        _sweat(ctx, -78, hy - 30, t)
        ctx.restore()
