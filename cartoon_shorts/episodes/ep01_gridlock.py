"""오늘의 만평 #01 — '협치'는 어디에?

정치권 줄다리기에 끌려다니는 국민을 풍자. 특정 정당을 지칭하지 않도록
가상의 'A당 / B당' 과 중립 색상(청록 / 자홍)을 사용한다.
"""
import math
import random

from ..characters import Citizen, Politician
from ..engine import (INK, W, draw_text, ease_in_cubic, ease_in_out,
                      ease_out_back, ease_out_bounce, ease_out_cubic,
                      ellipse, fill_stroke, halftone, lerp, paper_texture,
                      prog, rrect, set_rgb, speech_bubble, speed_lines,
                      star_burst, text_size, thick_line, wobble)

TITLE = "오늘의 만평 #01 - '협치'는 어디에?"
DURATION = 31.0

# 패널(만화 칸) 배치
PX, PY, PW, PH = 40, 340, 1000, 1060
GROUND = 930
CAP_Y = 1520

A = Politician("#2BA6A0", "A", hair="#26262E", tie="#F2B33D", seed=1)
B = Politician("#C2479B", "B", hair="#4A3328", tie="#3D7FF2", seed=2)
CIT = Citizen()

# (시작, 끝, 텍스트)
CAPTIONS = [
    (2.3, 8.0, "오늘도 국회는\n'민생법안' 처리에 열일 중..."),
    (8.6, 10.6, "...인 줄 알았는데?"),
    (10.6, 14.0, "물가, 집값, 금리는\n쉬지 않고 오르는 중"),
    (14.5, 17.0, "책임은 언제나 '저쪽'에"),
    (17.0, 20.0, "탓! 탓! 탓! 탓! 탓!"),
    (20.2, 22.8, "그렇게 시간은 흐르고..."),
    (23.0, 26.0, "결국 남은 건\n지친 국민뿐"),
]

TAGS = [(10.6, "물가", "#E9483B"), (11.4, "집값", "#F28C28"), (12.2, "금리", "#7B4FD6")]
SNAP_T = 22.8

_cache = {}


def _scale(ctx, sx, sy):
    """0 스케일(역행렬 불가) 방지."""
    ctx.scale(sx if abs(sx) > 0.01 else 0.01, sy if abs(sy) > 0.01 else 0.01)


def _static():
    if not _cache:
        _cache["paper"] = paper_texture(W, 1920)
        _cache["dots"] = halftone(W, 1920, (0.0, 0.0, 0.0, 0.06), step=30, rmax=5)
        _cache["dots_y"] = halftone(W, 1920, (0.85, 0.55, 0.0, 0.22), step=34, rmax=9)
    return _cache


# ============================================================ sound cues
def cues():
    c = [(0.15, "stamp"), (0.7, "pop"), (1.0, "whoosh"), (2.0, "slide"), (2.1, "slide"),
         (8.3, "snap"), (8.4, "fall"), (14.0, "whoosh"), (14.3, "stamp"),
         (14.6, "boing"), (15.8, "boing"), (20.0, "whoosh"),
         (SNAP_T, "snap"), (SNAP_T + 0.05, "fall"), (SNAP_T + 0.45, "thud"),
         (SNAP_T + 0.9, "thud"), (23.9, "pop"), (26.0, "whoosh"), (26.4, "stamp"),
         (26.9, "pop"), (27.6, "pop"), (28.9, "ding")]
    for t, _, _ in TAGS:
        c.append((t + 0.55, "thud"))
    for t0, t1, txt in CAPTIONS:
        for i in range(0, len(txt), 2):
            tt = t0 + i / 22
            if tt < t1:
                c.append((tt, "tick"))
    rnd = random.Random(9)
    t = 17.0
    while t < 19.8:
        if rnd.random() < 0.5:
            c.append((t, "pop"))
        t += 0.12
    for i in range(18):
        c.append((20.1 + i * 0.14, "flip"))
    return sorted(c)


# ============================================================ helpers
def _tug(t, speed=0.9, amp=26):
    return amp * math.sin(2 * math.pi * t * speed) + wobble(t, 3, 6, 3)


def _shake(t, amp):
    return wobble(t, 11, amp, 23), wobble(t, 17, amp, 29)


def _sky(ctx, t, top="#9FD8F5", bottom="#E8F7FF"):
    import cairo
    g = cairo.LinearGradient(0, 0, 0, PH)
    g.add_color_stop_rgb(0, *[int(top[i:i + 2], 16) / 255 for i in (1, 3, 5)])
    g.add_color_stop_rgb(1, *[int(bottom[i:i + 2], 16) / 255 for i in (1, 3, 5)])
    ctx.rectangle(0, 0, PW, PH)
    ctx.set_source(g)
    ctx.fill()
    for i, (cx, cy, s) in enumerate(((180, 160, 1.0), (760, 110, 0.8), (520, 260, 0.6))):
        x = (cx + t * 18 * (1 + i * 0.3)) % (PW + 300) - 150
        for dx, dy, r in ((0, 0, 50), (55, -20, 60), (115, 0, 48), (55, 15, 50)):
            ellipse(ctx, x + dx * s, cy + dy * s, r * s, r * s * 0.8)
        set_rgb(ctx, "#FFFFFF", 0.9)
        ctx.fill()


def _dome(ctx, rise=1.0):
    """국회의사당 실루엣."""
    oy = (1 - rise) * 500
    ctx.save()
    ctx.translate(0, oy)
    c_body, c_dome = "#DCE3EC", "#9FC3B8"
    # 돔
    ctx.new_path()
    ctx.move_to(290, 640)
    ctx.curve_to(290, 470, 710, 470, 710, 640)
    ctx.close_path()
    fill_stroke(ctx, c_dome, 6)
    rrect(ctx, 270, 630, 460, 40, 8)
    fill_stroke(ctx, "#C9D2DD", 6)
    # 본관
    rrect(ctx, 150, 665, 700, 210, 6)
    fill_stroke(ctx, c_body, 6)
    for i in range(10):
        x = 195 + i * 68
        rrect(ctx, x, 690, 26, 165, 6)
        fill_stroke(ctx, "#F4F7FA", 4)
    # 계단
    for i in range(3):
        rrect(ctx, 120 - i * 20, 870 + i * 20, 760 + i * 40, 22, 4)
        fill_stroke(ctx, "#C9D2DD", 4)
    ctx.restore()


def _ground(ctx):
    ctx.rectangle(0, GROUND, PW, PH - GROUND)
    set_rgb(ctx, "#8CCB6A")
    ctx.fill()
    ctx.move_to(0, GROUND)
    ctx.line_to(PW, GROUND)
    set_rgb(ctx, INK)
    ctx.set_line_width(6)
    ctx.stroke()


def _rope(ctx, pts):
    thick_line(ctx, pts, 14, "#C89B5C", outline=5)
    # 꼬임 무늬
    set_rgb(ctx, "#8A6533")
    ctx.set_line_width(3)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        d = math.hypot(x1 - x0, y1 - y0)
        n = int(d / 22)
        for i in range(n):
            k = (i + 0.5) / n
            x, y = lerp(x0, x1, k), lerp(y0, y1, k)
            ctx.move_to(x - 5, y - 6)
            ctx.line_to(x + 5, y + 6)
    ctx.stroke()


def _sag(p0, p1, sag=25, n=10):
    return [(lerp(p0[0], p1[0], i / n), lerp(p0[1], p1[1], i / n) + math.sin(math.pi * i / n) * sag)
            for i in range(n + 1)]


def _price_tag(ctx, x, y, label, color, rot=0.0, s=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    _scale(ctx, s, s)
    rrect(ctx, -95, -42, 190, 84, 18)
    fill_stroke(ctx, color, 6)
    draw_text(ctx, label, -18, 2, 48, font="black", fill="#FFFFFF")
    # 위쪽 화살표
    ctx.new_path()
    ctx.move_to(52, -26)
    ctx.line_to(78, 4)
    ctx.line_to(62, 4)
    ctx.line_to(62, 28)
    ctx.line_to(42, 28)
    ctx.line_to(42, 4)
    ctx.line_to(26, 4)
    ctx.close_path()
    fill_stroke(ctx, "#FFFFFF", 3)
    ctx.restore()


def _tug_world(ctx, t, off, lean_amp=0.06, pull=0.0, show_board=True, board_fall=0.0,
               cit_mode="hidden", tags_t=None, sweat=True):
    """줄다리기 와이드 샷 (씬 1, 2, 4 공용)."""
    s = 1.0
    lean = -0.2 - lean_amp * math.sin(2 * math.pi * t * 0.9 + 1.2) - pull
    ax, bx = 190 + off, 810 + off
    hands = ((160, -300), (125, -290))
    ha = A.hand_world(ax, GROUND, s, 1, lean, hands[0])
    hb = B.hand_world(bx, GROUND, s, -1, lean, hands[0])
    cx, cy = 500 + off * 1.15, 700 + wobble(t, 5, 6, 4)

    # 시민 (밧줄에 묶임)
    if cit_mode != "hidden":
        stretch = 1 + 0.14 * abs(math.sin(t * 5.6))
        CIT.draw(ctx, cx, cy + 165, s=0.85, sx=stretch, mood="worried", t=t, arms="up",
                 rot=wobble(t, 2, 0.06, 6))
    # 밧줄
    _rope(ctx, _sag(ha, (cx, cy + 62), 22) + _sag((cx, cy + 62), hb, 22)[1:])
    if cit_mode != "hidden":
        ellipse(ctx, cx, cy + 62, 72, 18)
        ctx.set_line_width(14)
        set_rgb(ctx, "#C89B5C")
        ctx.stroke()

    # 머리 위 가격표
    if tags_t is not None:
        stack_y = cy + 165 - 0.85 * 440
        for i, (t0, label, color) in enumerate(TAGS):
            k = prog(tags_t, t0, t0 + 0.55)
            if k <= 0:
                continue
            ty_end = stack_y - 40 - i * 78
            ty = lerp(-150, ty_end, ease_out_bounce(k))
            rot = wobble(t, i + 4, 0.08, 3) * (1 if k >= 1 else 3)
            _price_tag(ctx, cx + wobble(t, i, 6, 2), ty, label, color, rot=rot)
            if 0.85 < k and tags_t < t0 + 0.9:
                kk = prog(tags_t, t0 + 0.5, t0 + 0.9)
                draw_text(ctx, "퍽!", cx + 140, ty_end, 64, font="black", fill="#FFE14D",
                          stroke=6, stroke_fill="#111111", scale=ease_out_back(kk),
                          alpha=1 - kk * 0.3, rot=0.2)

    # 정치인
    mo = 0.3 + 0.3 * abs(math.sin(t * 7))
    A.draw(ctx, ax, GROUND, s, 1, lean, mood="angry", t=t, hands=hands, mouth_open=mo,
           sweat=sweat)
    B.draw(ctx, bx, GROUND, s, -1, lean, mood="angry", t=t + 0.4, hands=hands, mouth_open=mo,
           sweat=sweat)

    # 민생법안 팻말
    if show_board:
        fy = ease_in_cubic(board_fall) * 900
        rot = wobble(t, 8, 0.05, 3) + board_fall * 1.4
        ctx.save()
        ctx.translate(cx, cy + 25 + fy)
        ctx.rotate(rot)
        ctx.translate(0, 20)
        rrect(ctx, -170, 0, 340, 380, 22)
        fill_stroke(ctx, "#FFFDF4", 8)
        rrect(ctx, -150, 20, 300, 340, 14)
        fill_stroke(ctx, None, 4, stroke="#D7263D")
        draw_text(ctx, "민생\n법안", 0, 175, 104, font="black", fill="#D7263D", spacing=4)
        ellipse(ctx, 0, 0, 16, 16)
        fill_stroke(ctx, "#C89B5C", 5)
        ctx.restore()
    return (cx, cy), ha, hb


# ============================================================ scenes
def scene_tug(ctx, t):
    """씬1(2~8s) + 씬2(8~14s)."""
    _sky(ctx, t)
    _dome(ctx, ease_out_cubic(prog(t, 1.2, 2.2)))
    _ground(ctx)
    k_in = ease_out_back(prog(t, 2.0, 2.9), 1.4)
    off = _tug(t) * prog(t, 2.6, 3.2)
    zoom = 1 + 0.08 * ease_in_out(prog(t, 9.0, 14.0))
    ctx.save()
    ctx.translate(PW / 2, PH * 0.62)
    _scale(ctx, zoom, zoom)
    ctx.translate(-PW / 2, -PH * 0.62)
    if t < 2.9:
        # 양쪽에서 미끄러져 등장
        lean = -0.2
        hands = ((160, -300), (125, -290))
        ax = lerp(-260, 190, k_in)
        bx = lerp(1260, 810, k_in)
        A.draw(ctx, ax, GROUND, 1, 1, lean, mood="smug", t=t, hands=hands, leg_phase=t * 18)
        B.draw(ctx, bx, GROUND, 1, -1, lean, mood="smug", t=t, hands=hands, leg_phase=t * 18)
        if k_in > 0.85:
            ha = A.hand_world(ax, GROUND, 1, 1, lean, hands[0])
            hb = B.hand_world(bx, GROUND, 1, -1, lean, hands[0])
            _rope(ctx, _sag(ha, (500, 725), 22) + _sag((500, 725), hb, 22)[1:])
        # 팻말은 위에서 떨어져 밧줄에 걸림
        kb = ease_out_bounce(prog(t, 2.2, 2.9))
        ctx.save()
        ctx.translate(500, lerp(-500, 745, kb))
        rrect(ctx, -170, 0, 340, 380, 22)
        fill_stroke(ctx, "#FFFDF4", 8)
        rrect(ctx, -150, 20, 300, 340, 14)
        fill_stroke(ctx, None, 4, stroke="#D7263D")
        draw_text(ctx, "민생\n법안", 0, 175, 104, font="black", fill="#D7263D", spacing=4)
        ctx.restore()
    else:
        fall = prog(t, 8.3, 9.3)
        mode = "hidden" if t < 8.3 else "tied"
        (cx, cy), _, _ = _tug_world(ctx, t, off, show_board=fall < 1, board_fall=fall,
                                    cit_mode=mode, tags_t=t)
        if 8.25 < t < 8.9:
            kk = prog(t, 8.25, 8.9)
            draw_text(ctx, "찌익-!", cx + 150, cy - 40, 80, font="black", fill="#FFFFFF",
                      stroke=7, stroke_fill="#111111", scale=ease_out_back(kk), rot=-0.15,
                      alpha=1 - prog(t, 8.7, 8.9))
        if t > 8.9:
            k = ease_out_back(prog(t, 8.9, 9.3))
            # 국민 머리 위 '?!'
            draw_text(ctx, "?!", cx - 120, cy - 120, 90, font="black", fill="#FFE14D",
                      stroke=7, stroke_fill="#111111", scale=k * (1 if t < 10.4 else 0))
    ctx.restore()


def scene_blame(ctx, t):
    """씬3(14~20s): VS 클로즈업 + 탓 공방."""
    lt = t - 14.0
    sx, sy = _shake(t, 4 + 6 * prog(t, 17, 19.5))
    ctx.save()
    ctx.translate(sx, sy)
    # 대각선 분할 배경
    ctx.rectangle(-20, -20, PW + 40, PH + 40)
    set_rgb(ctx, "#BFEDEA")
    ctx.fill()
    ctx.move_to(PW * 0.62, -20)
    ctx.line_to(PW + 20, -20)
    ctx.line_to(PW + 20, PH + 20)
    ctx.line_to(PW * 0.38, PH + 20)
    ctx.close_path()
    set_rgb(ctx, "#F6C9E6")
    ctx.fill()
    speed_lines(ctx, 250, 640, 330, 1400, 60, t, color="#2BA6A0", alpha=0.25, seed=4)
    speed_lines(ctx, 750, 640, 330, 1400, 60, t, color="#C2479B", alpha=0.25, seed=8)
    ctx.move_to(PW * 0.62, -20)
    ctx.line_to(PW * 0.38, PH + 20)
    set_rgb(ctx, INK)
    ctx.set_line_width(10)
    ctx.stroke()

    k_a = ease_out_cubic(prog(lt, 0.0, 0.45))
    k_b = ease_out_cubic(prog(lt, 0.1, 0.55))
    point = ((150, -470), (-40, -230))
    talk_a = 14.6 < t < 15.8 or t > 17
    talk_b = 15.8 < t < 17.0 or t > 17
    ma = 0.5 + 0.5 * abs(math.sin(t * 19)) if talk_a else 0.1
    mb = 0.5 + 0.5 * abs(math.sin(t * 17 + 1)) if talk_b else 0.1
    A.draw(ctx, lerp(-400, 190, k_a), 1440, 1.55, 1, 0.08 + wobble(t, 1, 0.03, 5),
           mood="angry", t=t, hands=point, mouth_open=ma, sweat=True)
    B.draw(ctx, lerp(1400, 810, k_b), 1440, 1.55, -1, 0.08 + wobble(t, 2, 0.03, 5),
           mood="angry", t=t, hands=point, mouth_open=mb, sweat=True)

    # VS
    kv = ease_out_back(prog(lt, 0.3, 0.6), 2.5)
    if kv > 0:
        star_burst(ctx, PW / 2, 600, 120 * kv, 70 * kv, n=10, rot=t * 0.8, seed=5)
        fill_stroke(ctx, "#FFE14D", 7)
        draw_text(ctx, "VS", PW / 2, 600, 100, font="black", fill="#D7263D", stroke=6,
                  stroke_fill="#111111", scale=kv, rot=-0.12)

    # 말풍선
    for t0, x, y, txt, tail, seed in ((14.6, 270, 190, "전부\n저쪽 탓!", (230, 330), 3),
                                      (15.8, 730, 190, "아니,\n저쪽 탓!!", (770, 330), 6)):
        kb = ease_out_back(prog(t, t0, t0 + 0.35), 2.2)
        if kb <= 0:
            continue
        fade = 1 - prog(t, 17.0, 17.4) * 0.0
        ctx.save()
        ctx.translate(x, y)
        _scale(ctx, kb, kb)
        speech_bubble(ctx, 0, 0, 400, 260, (tail[0] - x, tail[1] - y + 40), spiky=True, seed=seed)
        draw_text(ctx, txt, 0, 4, 64, font="black", fill="#111111", spacing=2, alpha=fade)
        ctx.restore()

    # '탓' 폭주
    for tt, side, ang, dist, size, col, r0, spin in TAT:
        age = t - tt
        if not 0 <= age < 2.5:
            continue
        ox, oy = (300, 520) if side == 0 else (700, 520)
        k = ease_out_cubic(clamp01(age / 0.6))
        x = ox + math.cos(ang) * dist * k
        y = oy + math.sin(ang) * dist * k + age * age * 120
        draw_text(ctx, "탓!", x, y, size, font="black", fill=col, stroke=6,
                  stroke_fill="#111111", scale=ease_out_back(clamp01(age / 0.25)),
                  rot=r0 + age * spin)
    ctx.restore()


def clamp01(x):
    return 0.0 if x < 0 else 1.0 if x > 1 else x


def _make_tat():
    rnd = random.Random(21)
    out = []
    for i in range(int((19.8 - 17.0) / 0.12)):
        out.append((17.0 + i * 0.12, i % 2, rnd.uniform(-math.pi * 0.95, -math.pi * 0.05),
                    rnd.uniform(250, 520), rnd.choice((54, 64, 78)),
                    rnd.choice(("#FFFFFF", "#FFE14D", "#FF8A8A")),
                    rnd.uniform(-0.5, 0.5), rnd.uniform(-1, 1)))
    return out


TAT = _make_tat()


def scene_snap(ctx, t):
    """씬4(20~26s): 세월은 흐르고 밧줄은 끊어진다."""
    _sky(ctx, t, top="#F7B267", bottom="#FCE8C8")  # 노을
    _dome(ctx)
    _ground(ctx)

    # 달력
    kc = ease_out_back(prog(t, 20.0, 20.4))
    days = 100 + int(clamp01((t - 20.1) / 2.5) * 265)
    ctx.save()
    ctx.translate(PW / 2, 150)
    _scale(ctx, kc, kc)
    ctx.rotate(-0.04)
    rrect(ctx, -140, -95, 280, 210, 16)
    fill_stroke(ctx, "#FFFFFF", 7)
    rrect(ctx, -140, -95, 280, 60, 16)
    fill_stroke(ctx, "#D7263D", 7)
    draw_text(ctx, "국회 공전", 0, -65, 40, font="black", fill="#FFFFFF")
    draw_text(ctx, f"D+{days}", 0, 38, 84, font="black", fill="#111111")
    # 넘어가는 페이지
    if 20.1 < t < 22.6:
        ph = ((t - 20.1) / 0.14) % 1.0
        ctx.save()
        ctx.translate(0, -35)
        _scale(ctx, 1, 1 - ph)
        ctx.rotate(-ph * 0.4)
        rrect(ctx, -140, 0, 280, 150, 10)
        fill_stroke(ctx, "#FFFFFF", 5, alpha=1 - ph)
        ctx.restore()
    ctx.restore()
    if t > 20.6:
        blink = 1 if int(t * 4) % 2 == 0 or t > 22.6 else 0.35
        draw_text(ctx, "처리된 민생법안: 0건", PW / 2, 300, 50, font="black", fill="#D7263D",
                  stroke=5, stroke_fill="#FFFFFF", alpha=blink * prog(t, 20.6, 20.9))

    if t < SNAP_T:
        speed = 0.9 + 1.2 * prog(t, 20, SNAP_T)
        off = _tug(t, speed=speed, amp=26 + 20 * prog(t, 20, SNAP_T))
        _tug_world(ctx, t, off, lean_amp=0.1, pull=0.08 * prog(t, 21, SNAP_T),
                   show_board=False, cit_mode="tied")
        return

    # --- 끊어진 뒤
    k = prog(t, SNAP_T, SNAP_T + 1.0)
    e = ease_out_cubic(k)
    for P, sgn, x0 in ((A, 1, 190), (B, -1, 810)):
        x = x0 - sgn * 700 * e
        y = GROUND - math.sin(math.pi * min(k * 1.2, 1)) * 260
        P.draw(ctx, x, y, 1, sgn, -0.2 - 2.2 * e, mood="dizzy" if k > 0.2 else "shock", t=t,
               hands=((160, -300), (125, -290)))
    # 시민 낙하 → 앉아서 팻말
    kf = prog(t, SNAP_T, SNAP_T + 0.6)
    cy = lerp(865, GROUND, ease_out_bounce(kf))
    sitting = t > SNAP_T + 1.0
    if sitting:
        CIT.draw(ctx, 500, GROUND, s=0.95, mood="blank", t=t, arms="sign")
        ks = ease_out_back(prog(t, 23.9, 24.3), 2.0)
        ctx.save()
        ctx.translate(570, GROUND - 385)
        _scale(ctx, ks, ks)
        ctx.rotate(wobble(t, 4, 0.04, 2))
        thick_line(ctx, [(0, 0), (0, 240)], 16, "#B07A3E", 4)
        rrect(ctx, -230, -170, 460, 190, 18)
        fill_stroke(ctx, "#FFFFFF", 7)
        draw_text(ctx, "그래서\n제 월급은요?", 0, -75, 62, font="black", fill="#111111", spacing=0)
        ctx.restore()
        # 지친 표현 (한숨)
        kk = (t * 0.7) % 1.0
        draw_text(ctx, "휴...", 330 - kk * 40, GROUND - 330 - kk * 80, 56, font="black",
                  fill="#333333", alpha=1 - kk)
    else:
        CIT.draw(ctx, 500, cy, s=0.85, mood="worried", t=t, arms="up", rot=0.2 * math.sin(t * 9))
    # 끊어지는 이펙트
    kb = prog(t, SNAP_T, SNAP_T + 0.5)
    if kb < 1:
        star_burst(ctx, 500, 720, 190 * ease_out_back(kb), 90, n=12, seed=7)
        fill_stroke(ctx, "#FFFFFF", 7, alpha=1 - kb)
        draw_text(ctx, "툭!", 500, 720, 110, font="black", fill="#D7263D", stroke=6,
                  stroke_fill="#111111", scale=ease_out_back(kb), alpha=1 - kb * 0.8)


def outro(ctx, t):
    """26~31s: 엔딩 카드 (화면 전체)."""
    st = _static()
    ctx.rectangle(0, 0, W, 1920)
    set_rgb(ctx, "#FFD93D")
    ctx.fill()
    ctx.set_source_surface(st["dots_y"], 0, 0)
    ctx.paint()
    speed_lines(ctx, W / 2, 760, 420, 1600, 70, t, color="#FFFFFF", alpha=0.45, seed=1)

    k1 = ease_out_back(prog(t, 26.4, 26.8), 2.2)
    draw_text(ctx, "여러분의 생각은?", W / 2, 640, 110, font="black", fill="#FFFFFF",
              stroke=10, stroke_fill="#111111", scale=k1, rot=-0.04)
    k2 = ease_out_back(prog(t, 26.9, 27.3))
    if k2 > 0:
        ctx.save()
        ctx.translate(W / 2, 840)
        _scale(ctx, k2, k2)
        speech_bubble(ctx, 0, 0, 640, 170, (-180, 120), fill="#FFFFFF")
        draw_text(ctx, "댓글로 남겨주세요!", 0, 0, 64, font="jua", fill="#111111")
        ctx.restore()

    # 구독 버튼
    k3 = ease_out_back(prog(t, 27.6, 28.0), 2.0)
    clicked = t > 28.9
    press = 1 - 0.1 * math.sin(math.pi * prog(t, 28.85, 29.1))
    pulse = 1 + 0.04 * math.sin(t * 8) if not clicked else 1
    if k3 > 0:
        ctx.save()
        ctx.translate(W / 2, 1120)
        _scale(ctx, k3 * press * pulse, k3 * press * pulse)
        rrect(ctx, -230, -75, 460, 150, 75)
        fill_stroke(ctx, "#8A8A8A" if clicked else "#E62117", 8)
        draw_text(ctx, "구독중" if clicked else "구독", 30, 2, 76, font="black", fill="#FFFFFF")
        # 종 아이콘
        ring = math.sin(t * 30) * 0.4 * (1 - prog(t, 28.9, 29.8)) if clicked else 0
        ctx.save()
        ctx.translate(-120, 0)
        ctx.rotate(ring)
        ctx.new_path()
        ctx.move_to(-28, 25)
        ctx.curve_to(-28, -40, 28, -40, 28, 25)
        ctx.close_path()
        fill_stroke(ctx, "#FFFFFF", 5)
        ellipse(ctx, 0, 32, 9, 9)
        fill_stroke(ctx, "#FFFFFF", 4)
        ctx.restore()
        ctx.restore()
    # 커서 손
    if 28.1 < t < 30.0:
        kh = ease_in_out(prog(t, 28.1, 28.8))
        hx, hy = lerp(900, W / 2 + 110, kh), lerp(1500, 1150, kh)
        ctx.save()
        ctx.translate(hx, hy)
        ctx.rotate(-0.4)
        rrect(ctx, -22, -10, 44, 90, 20)
        fill_stroke(ctx, "#FFFFFF", 6)
        rrect(ctx, -10, -70, 22, 80, 11)
        fill_stroke(ctx, "#FFFFFF", 6)
        ctx.restore()
        if clicked and t < 29.6:
            kr = prog(t, 28.9, 29.6)
            ctx.new_path()
            ctx.arc(W / 2 + 110, 1080, 40 + 120 * kr, 0, 2 * math.pi)
            set_rgb(ctx, "#FFFFFF", 1 - kr)
            ctx.set_line_width(8)
            ctx.stroke()

    draw_text(ctx, "오늘의 만평", W / 2, 1380, 54, font="black", fill="#111111",
              alpha=prog(t, 28.0, 28.5))
    draw_text(ctx, "매일 한 컷으로 보는 세상", W / 2, 1450, 40, font="jua", fill="#333333",
              alpha=prog(t, 28.2, 28.7))
    # 시작 시 원형 아이리스 트랜지션
    if t < 26.4:
        r = 1300 * ease_in_out(prog(t, 26.0, 26.4))
        ctx.save()
        ctx.rectangle(0, 0, W, 1920)
        ctx.arc_negative(W / 2, 900, r, 2 * math.pi, 0)
        set_rgb(ctx, INK)
        ctx.fill()
        ctx.restore()


# ============================================================ frame
def _header(ctx, t):
    k = prog(t, 0.1, 0.4)
    sc = lerp(2.6, 1.0, ease_out_cubic(k))
    if k > 0:
        ctx.save()
        ctx.translate(W / 2, 150)
        ctx.rotate(-0.035)
        _scale(ctx, sc, sc)
        rrect(ctx, -330, -70, 660, 140, 10)
        fill_stroke(ctx, "#111111", 0, alpha=k)
        draw_text(ctx, "오늘의 만평", 0, 2, 92, font="black", fill="#FFD93D", alpha=k)
        ctx.restore()
        # 스탬프 태그
        ks = ease_out_back(prog(t, 0.35, 0.6), 2.4)
        ctx.save()
        ctx.translate(890, 95)
        ctx.rotate(0.25)
        _scale(ctx, ks, ks)
        ellipse(ctx, 0, 0, 62, 62)
        fill_stroke(ctx, "#D7263D", 6)
        draw_text(ctx, "#01", 0, 2, 46, font="black", fill="#FFFFFF")
        ctx.restore()
    kt = ease_out_back(prog(t, 0.7, 1.05), 2.0)
    draw_text(ctx, "'협치'는 어디에?", W / 2, 278, 70, font="black", fill="#FFFFFF",
              stroke=8, stroke_fill="#111111", scale=kt)


def _caption(ctx, t):
    cur = None
    for t0, t1, txt in CAPTIONS:
        if t0 <= t < t1:
            cur = (t0, t1, txt)
    if cur is None:
        return
    t0, t1, txt = cur
    kin = ease_out_back(prog(t, t0, t0 + 0.25), 1.6)
    kout = prog(t, t1 - 0.15, t1)
    n = int((t - t0) * 22) + 1
    shown = txt[:n]
    full_w, full_h = text_size(txt, 64, "jua", spacing=8)
    bw, bh = max(full_w + 90, 560), full_h + 60
    ctx.save()
    ctx.translate(W / 2, CAP_Y)
    _scale(ctx, kin, kin * (1 - kout))
    rrect(ctx, -bw / 2 + 10, -bh / 2 + 12, bw, bh, 26)
    set_rgb(ctx, INK)
    ctx.fill()
    rrect(ctx, -bw / 2, -bh / 2, bw, bh, 26)
    fill_stroke(ctx, "#FFFFFF", 7)
    # 부분 텍스트는 전체 텍스트 기준 왼쪽 위 정렬로 고정해서 흔들림 방지
    lines_full = txt.split("\n")
    lines_shown = shown.split("\n")
    lh = full_h / len(lines_full)
    for i, line in enumerate(lines_shown):
        lw, _ = text_size(lines_full[i], 64, "jua")
        y = -full_h / 2 + lh * (i + 0.5)
        draw_text(ctx, line, -lw / 2, y, 64, font="jua", fill="#111111", anchor=(0, 0.5))
    ctx.restore()


def _panel(ctx, t, scene_fn):
    reveal = ease_out_cubic(prog(t, 1.0, 1.6))
    if reveal <= 0:
        return
    ph = PH * reveal
    # 그림자
    rrect(ctx, PX + 14, PY + 16, PW, ph, 28)
    set_rgb(ctx, INK)
    ctx.fill()
    ctx.save()
    rrect(ctx, PX, PY, PW, ph, 28)
    ctx.clip()
    ctx.translate(PX, PY)
    scene_fn(ctx, t)
    ctx.restore()
    rrect(ctx, PX, PY, PW, ph, 28)
    fill_stroke(ctx, None, 10)


def render_frame(ctx, t):
    st = _static()
    ctx.set_source_surface(st["paper"], 0, 0)
    ctx.paint()
    ctx.set_source_surface(st["dots"], 0, 0)
    ctx.paint()

    if t >= 26.0:
        outro(ctx, t)
        return

    _header(ctx, t)
    if t < 14.0:
        fn = scene_tug
    elif t < 20.0:
        fn = scene_blame
    else:
        fn = scene_snap
    _panel(ctx, t, fn)

    # 씬 전환 플래시
    for tt in (14.0, 20.0):
        if tt - 0.05 < t < tt + 0.25:
            a = 1 - prog(t, tt, tt + 0.25)
            rrect(ctx, PX, PY, PW, PH, 28)
            set_rgb(ctx, "#FFFFFF", a)
            ctx.fill()

    _caption(ctx, t)
    draw_text(ctx, "* 특정 정당, 인물과 무관한 풍자 창작물입니다", W / 2, 1665, 30,
              font="jua", fill="#7A7366", alpha=prog(t, 1.0, 1.5))
