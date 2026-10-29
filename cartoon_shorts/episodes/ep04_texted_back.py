"""Two Different Universes #01 — Why Hasn't He Texted Back?

영어권 파일럿 쇼츠. 대사 없이 무표정한 영국식 다큐 내레이터 한 명이 상황을 중계하는 포맷.
구조: REALITY(문자 전송) → HER VERSION(추리) → HIS VERSION(게임) → THE TRUTH(폰 방전) → 엔딩.

타임라인 설정: 폰 방전 8:26 PM → 그녀의 문자 8:27 PM → 충전 9:14 PM (47분 경과).
화면 구도: 위쪽 = 상황(폰·증거판·TV), 가운데 = 자막, 아래쪽 = 캐릭터 상반신.
"""
import math

from .. import squire as S
from ..engine import (H, W, clamp, draw_text, ease_in_out, ease_out_back,
                      ease_out_cubic, ellipse, lerp, prog, rrect, set_rgb, wobble)
from ..explainer import Episode

TITLE = "Why Hasn't He Texted Back? | Two Different Universes #01"
DURATION = 30.0

HER = S.Person(coat="#C46D86", hair="bob", hair_color="#4A2E24", hood=True, pants="#3F4560")
HIM = S.Person(coat="#3F6E9A", hair="part", hair_color="#2F241E", hood=True, pants="#4A4A52")

VOICES = {"N": ("en-GB-RyanNeural", "-2%", "-2Hz")}
CAP_COLORS = {"N": "#FFFFFF"}

SCRIPT = [
    ("hook", [("N", "She sent him a text."),
              ("N", "[47 minutes] ago.")], {"tail": 0.5}),
    ("her", [("N", "Since then, she has checked her phone [23 times]."),
             ("N", "She has reviewed their entire relationship,"),
             ("N", "including a [suspicious] thumbs-up from Tuesday.")], {"tail": 0.5}),
    ("verdict", [("N", "Her conclusion? He is [losing interest].")], {"tail": 0.7}),
    ("him", [("N", "Meanwhile, he is having the [best night] of his life.")], {"tail": 0.6}),
    ("twist", [("N", "There was only one problem."),
               ("N", "His phone died [48 minutes ago].")], {"tail": 0.7}),
    ("split", [("N", "Her text never even arrived.")], {"tail": 0.6}),
    ("charge", [("N", "At 9:14, he finally plugs it in."),
                ("N", "And sees [two] new messages.")], {"tail": 1.1}),
    ("outro", [("N", "Same moment. [Two worlds]."),
               ("N", "So, who was right? Tell us in the comments.")], {"tail": 2.0}),
]

PINK, PINK_D = "#B9788C", "#A86A7E"
BLUE, BLUE_D = "#56718F", "#46607C"
BUBBLE_ME = "#4C8DF6"
BUBBLE_THEM = "#E6E6EB"
BUST = dict(y=2230, s=1.35)  # 캐릭터 상반신 구도


# ================================================================ rooms & props
def her_room(ctx, dark=0.0):
    S.planks(ctx, base=PINK, dark=PINK_D, seed=4)
    rrect(ctx, 0, 1700, W, 220, 0)
    S.fs(ctx, "#6E4B57", lw=0)
    if dark > 0:
        ctx.rectangle(0, 0, W, H)
        set_rgb(ctx, "#1F2433", 0.55 * dark)
        ctx.fill()


def his_room(ctx):
    S.planks(ctx, base=BLUE, dark=BLUE_D, seed=6)
    rrect(ctx, 0, 1700, W, 220, 0)
    S.fs(ctx, "#3A3F4A", lw=0)


def phone(ctx, x, y, s, screen=None, rot=0.0):
    """정면 휴대폰. screen(ctx) 는 폰 로컬 좌표 (-160,-330)~(160,310) 화면 안에 그린다."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    rrect(ctx, -185, -370, 370, 740, 54)
    S.fs(ctx, "#2B2D35")
    ctx.save()
    rrect(ctx, -160, -330, 320, 640, 30)
    ctx.clip()
    if screen:
        screen(ctx)
    else:
        ctx.rectangle(-170, -340, 340, 660)
        set_rgb(ctx, "#0D0E12")
        ctx.fill()
    ctx.restore()
    rrect(ctx, -40, -352, 80, 12, 6)
    set_rgb(ctx, "#111216")
    ctx.fill()
    ctx.restore()


def bubble(ctx, text, y, me, k):
    """채팅 말풍선 (k: 0→1 팝)."""
    if k <= 0:
        return
    sc = ease_out_back(clamp(k), 2.2)
    w = max(130, len(text) * 30 + 60)
    x = 140 - w if me else -140
    ctx.save()
    ctx.translate(x + (w if me else 0), y)
    ctx.scale(sc, sc)
    ctx.translate(-(w if me else 0), 0)
    rrect(ctx, 0, -38, w, 76, 36)
    set_rgb(ctx, BUBBLE_ME if me else BUBBLE_THEM)
    ctx.fill()
    draw_text(ctx, text, w / 2, 2, 40, font="black", fill="#FFFFFF" if me else "#22242A")
    ctx.restore()


def chat(ctx, bubbles, status=None, clock="9:14"):
    ctx.rectangle(-170, -340, 340, 660)
    set_rgb(ctx, "#FFFFFF")
    ctx.fill()
    draw_text(ctx, clock, -110, -300, 26, font="black", fill="#22242A")
    rrect(ctx, -170, -270, 340, 110, 0)
    set_rgb(ctx, "#F3F3F6")
    ctx.fill()
    ellipse(ctx, 0, -235, 26, 26)
    set_rgb(ctx, "#8FA3B8")
    ctx.fill()
    draw_text(ctx, "Jake", 0, -188, 26, font="black", fill="#22242A")
    for text, y, me, k in bubbles:
        bubble(ctx, text, y, me, k)
    if status:  # (텍스트, y)
        draw_text(ctx, status[0], 130, status[1], 24, font="black", fill="#8A8D96",
                  anchor=(1, 0.5))


def battery(ctx, x, y, s, level, color):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rrect(ctx, -60, -30, 120, 60, 10)
    set_rgb(ctx, color)
    ctx.set_line_width(7)
    ctx.stroke()
    rrect(ctx, 62, -12, 10, 24, 3)
    ctx.fill()
    if level > 0:
        rrect(ctx, -50, -20, 100 * level, 40, 5)
        ctx.fill()
    ctx.restore()


def dead_screen(ctx, t):
    ctx.rectangle(-170, -340, 340, 660)
    set_rgb(ctx, "#0D0E12")
    ctx.fill()
    a = 0.45 + 0.55 * (0.5 + 0.5 * math.cos(t * 7))
    ctx.push_group()
    battery(ctx, 0, -20, 1.2, 0.06, "#E0483C")
    draw_text(ctx, "0%", 0, 70, 44, font="black", fill="#E0483C")
    ctx.pop_group_to_source()
    ctx.paint_with_alpha(a)


def phone_back(ctx, t):
    """여자가 든 휴대폰 (뒷면)."""
    rrect(ctx, -60, -400, 125, 220, 20)
    S.fs(ctx, "#2B2D35", lw=5)
    ellipse(ctx, -25, -370, 13, 13)
    set_rgb(ctx, "#4A4D58")
    ctx.fill()


def controller(ctx, t):
    rrect(ctx, -100, -262, 210, 90, 44)
    S.fs(ctx, "#33363F", lw=5)
    for bx, col in ((60, "#E0483C"), (82, "#5FA8D3")):
        ellipse(ctx, bx, -222, 11, 11)
        set_rgb(ctx, col)
        ctx.fill()
    rrect(ctx, -70, -230, 40, 14, 4)
    set_rgb(ctx, "#8A8D96")
    ctx.fill()
    rrect(ctx, -57, -243, 14, 40, 4)
    ctx.fill()


def sticky(ctx, x, y, text, color, rot, k=1.0):
    if k <= 0:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(ease_out_back(clamp(k)), ease_out_back(clamp(k)))
    rrect(ctx, -105, -90, 210, 180, 6)
    S.fs(ctx, color, lw=5)
    draw_text(ctx, text, 0, 4, 38, font="black", fill="#2E2A28", spacing=4)
    ellipse(ctx, 0, -74, 12, 12)
    set_rgb(ctx, "#C9473B")
    ctx.fill()
    ctx.restore()


def thumbs_up(ctx, x, y, s):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rrect(ctx, -34, -10, 70, 60, 14)
    S.fs(ctx, "#F2C46B", lw=5)
    rrect(ctx, -22, -62, 28, 62, 12)
    S.fs(ctx, "#F2C46B", lw=5)
    ctx.restore()


NOTES = [  # (x, y, 텍스트, 색, 회전)
    (215, 420, "MON\n'haha'", "#FFE58A", -0.08),
    (865, 430, "SAT\n'k.'", "#BDE6C1", 0.07),
    (250, 830, "TUE\n ", "#FFC9A8", 0.05),
    (850, 840, "11 MIN\nREPLY?", "#C9DDFF", -0.06),
]


def board(ctx, lt, sh):
    """코르크 증거판. 대사 1 시작에 내려오고, 대사 2의 'suspicious' 에 TUE 메모에 빨간 동그라미."""
    k = ease_out_cubic(prog(lt, sh.m(1) - 0.2, sh.m(1) + 0.4))
    if k <= 0:
        return
    ctx.save()
    ctx.translate(0, -900 * (1 - k))
    rrect(ctx, 80, 270, 920, 760, 18)
    S.fs(ctx, "#8C5D3D")
    rrect(ctx, 110, 300, 860, 700, 8)
    S.fs(ctx, "#C99A6B", lw=4)
    # 가운데 사진
    ctx.save()
    ctx.translate(540, 630)
    ctx.rotate(0.03)
    rrect(ctx, -120, -140, 240, 280, 6)
    S.fs(ctx, "#FBF8EF", lw=5)
    rrect(ctx, -100, -120, 200, 190, 4)
    set_rgb(ctx, "#8FA3B8")
    ctx.fill()
    ellipse(ctx, 0, -30, 55, 55)
    S.fs(ctx, S.FACE, lw=4)
    draw_text(ctx, "JAKE", 0, 105, 34, font="black", fill="#2E2A28")
    ctx.restore()
    # 빨간 실: 메모가 하나씩 붙으며 연결
    t_notes = [sh.m(1) + 0.4 + i * 0.35 for i in range(len(NOTES))]
    for (nx, ny, *_), tn in zip(NOTES, t_notes):
        kk = prog(lt, tn + 0.15, tn + 0.5)
        if kk > 0:
            ctx.move_to(540, 630)
            ctx.line_to(lerp(540, nx, kk), lerp(630, ny - 74, kk))
            set_rgb(ctx, "#C9473B")
            ctx.set_line_width(6)
            ctx.stroke()
    for (nx, ny, txt, col, rot), tn in zip(NOTES, t_notes):
        sticky(ctx, nx, ny, txt, col, rot, prog(lt, tn, tn + 0.3))
        if txt.startswith("TUE") and lt > tn:
            thumbs_up(ctx, nx + 5, ny + 40, 0.75 * ease_out_back(prog(lt, tn, tn + 0.3)))
    # 'suspicious' 빨간 동그라미 + ?!
    ts = sh.word_t(2, 2)
    kc = prog(lt, ts, ts + 0.45)
    if kc > 0:
        nx, ny = NOTES[2][0], NOTES[2][1]
        ctx.new_path()
        ctx.arc(nx, ny, 150, -math.pi / 2, -math.pi / 2 + 2 * math.pi * kc)
        set_rgb(ctx, "#E0251B")
        ctx.set_line_width(14)
        ctx.stroke()
        draw_text(ctx, "?!", nx + 190, ny - 120, 120, font="black", fill="#E0251B", stroke=8,
                  stroke_fill="#FFFFFF", scale=ease_out_back(prog(lt, ts + 0.2, ts + 0.5), 2.4))
    ctx.restore()


def couch(ctx):
    rrect(ctx, 60, 1450, 960, 300, 50)
    S.fs(ctx, "#7F8C5C")
    rrect(ctx, 20, 1520, 140, 260, 40)
    S.fs(ctx, "#6E7A4E")
    rrect(ctx, 920, 1520, 140, 260, 40)
    S.fs(ctx, "#6E7A4E")


def tv(ctx, lt, t_win):
    rrect(ctx, 130, 230, 820, 520, 24)
    S.fs(ctx, "#1E1F25")
    ctx.save()
    rrect(ctx, 160, 260, 760, 460, 10)
    ctx.clip()
    ctx.rectangle(160, 260, 760, 460)
    set_rgb(ctx, "#78C6F0")
    ctx.fill()
    ctx.rectangle(160, 640, 760, 80)
    set_rgb(ctx, "#6FB04F")
    ctx.fill()
    for i in range(6):  # 흘러가는 블록
        bx = 920 - ((lt * 220 + i * 160) % 920)
        rrect(ctx, bx, 560 - (i % 3) * 60, 60, 60, 6)
        S.fs(ctx, "#E8A33E", lw=4)
    jy = abs(math.sin(lt * 4)) * 120
    rrect(ctx, 330, 580 - jy, 60, 60, 10)
    S.fs(ctx, "#E0483C", lw=4)
    if lt >= t_win:
        k = ease_out_back(prog(lt, t_win, t_win + 0.35), 2.6)
        draw_text(ctx, "VICTORY!", 540, 420, 120, font="black", fill="#FFD54A", stroke=10,
                  stroke_fill="#2B2D35", scale=k, rot=wobble(lt, 3, 0.04))
    ctx.restore()
    rrect(ctx, 470, 750, 140, 30, 6)
    S.fs(ctx, "#1E1F25", lw=4)


def label(ctx, x, y, text, color, k=1.0, size=48):
    if k <= 0:
        return
    w = len(text) * size * 0.62 + 70
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(ease_out_back(clamp(k)), ease_out_back(clamp(k)))
    rrect(ctx, -w / 2, -size * 0.8, w, size * 1.6, size * 0.8)
    S.fs(ctx, color, lw=5)
    draw_text(ctx, text, 0, 3, size, font="black", fill="#FFFFFF")
    ctx.restore()


def her_bust(ctx, lt, expr="deadpan", pose="hold", y=None, s=None, sweat=False):
    HER.draw(ctx, 540, y or BUST["y"], s or BUST["s"], 1, pose=pose, expr=expr, t=lt,
             prop=phone_back if pose == "hold" else None, sweat=sweat)


def him_bust(ctx, lt, expr="smug", pose="game", y=None, s=None, sweat=False, x=540):
    HIM.draw(ctx, x, y or BUST["y"], s or BUST["s"], -1, pose=pose, expr=expr, t=lt,
             prop=controller if pose == "game" else (phone_back if pose == "hold" else None),
             sweat=sweat)


# ================================================================ shots
def shot_hook(ctx, lt, sh):
    her_room(ctx)
    kb = prog(lt, 0.25, 0.55)
    # 시계: 대사 2 동안 8:27 → 9:14
    kc = ease_in_out(prog(lt, sh.m(1), sh.me(1)))
    mins = int(47 * kc)
    clock = f"{8 + (27 + mins) // 60}:{(27 + mins) % 60:02d}"

    def scr(c):
        chat(c, [("hey :)", 40, True, kb)], status=("Sent 8:27 PM", 100) if kb >= 1 else None,
             clock=clock)
    phone(ctx, 540, 760, 1.25, scr)
    if lt >= sh.m(1):
        label(ctx, 540, 1650, f"+{mins} min", S.RUST, prog(lt, sh.m(1), sh.m(1) + 0.3), size=64)
    draw_text(ctx, "REALITY", 540, 170, 54, font="black", fill="#FFFFFF", stroke=8,
              stroke_fill=S.OUT, alpha=prog(lt, 0.0, 0.3))


def shot_her(ctx, lt, sh):
    her_room(ctx)
    draw_text(ctx, "HER VERSION", 540, 170, 54, font="black", fill="#FFFFFF", stroke=8,
              stroke_fill=S.OUT)
    # 확인 횟수 카운터 (대사 0)
    kc = prog(lt, sh.m(0) + 0.6, sh.me(0))
    n = int(23 * ease_out_cubic(kc))
    a = 1 - prog(lt, sh.m(1) - 0.3, sh.m(1))
    if a > 0:
        label(ctx, 540, 640, f"PHONE CHECKS: {n}", S.RUST, prog(lt, sh.m(0), sh.m(0) + 0.3) * a,
              size=72)
    board(ctx, lt, sh)
    ts = sh.word_t(2, 2)
    her_bust(ctx, lt, expr="angry" if lt > ts else "deadpan")


def shot_verdict(ctx, lt, sh):
    her_room(ctx, dark=prog(lt, 0.0, 0.6))
    S.rain(ctx, lt, n=120, alpha=0.5 * prog(lt, 0.0, 0.6))
    tw = sh.word_t(0, 4)
    k = prog(lt, tw, tw + 0.5)
    S.stamp(ctx, 540, 620, "LOSING", k, rot=-0.12, size=120)
    S.stamp(ctx, 540, 830, "INTEREST", prog(lt, tw + 0.25, tw + 0.75), rot=-0.12, size=120)
    her_bust(ctx, lt, expr="sad")
    S.sigh(ctx, 720, 1420, lt, tw + 0.6)


def shot_him(ctx, lt, sh):
    his_room(ctx)
    tw = sh.word_t(0, 5)
    tv(ctx, lt, tw)
    couch(ctx)
    draw_text(ctx, "HIS VERSION", 540, 150, 54, font="black", fill="#FFFFFF", stroke=8,
              stroke_fill=S.OUT)
    him_bust(ctx, lt, expr="smug" if lt > tw else "neutral")
    S.confetti(ctx, lt, tw, n=70)


def shot_twist(ctx, lt, sh):
    his_room(ctx)
    ctx.rectangle(0, 0, W, H)
    set_rgb(ctx, "#101218", 0.35 * prog(lt, 0, 0.5))
    ctx.fill()
    # 옆 탁자 위 휴대폰 클로즈업
    rrect(ctx, -40, 1180, W + 80, 900, 30)
    S.fs(ctx, S.WOOD)
    phone(ctx, 540, 720, 1.25, lambda c: dead_screen(c, lt))
    td = sh.m(1)
    if lt >= td:
        k = prog(lt, td + 0.3, td + 0.8)
        S.stamp(ctx, 540, 1560, "DIED 8:26 PM", k, color="#FFF3E0", rot=-0.08, size=84)


def shot_split(ctx, lt, sh):
    # 위: 그녀 (비 내리는 방), 아래: 그 (게임 중)
    ctx.save()
    ctx.rectangle(0, 0, W, 960)
    ctx.clip()
    her_room(ctx, dark=0.7)
    S.rain(ctx, lt, n=70, alpha=0.4)
    her_bust(ctx, lt, expr="sad", y=1250, s=1.0)
    label(ctx, 540, 110, "SHE THINKS: HE'S IGNORING ME", PINK_D, 1.0, size=40)
    ctx.restore()
    ctx.save()
    ctx.rectangle(0, 960, W, 960)
    ctx.clip()
    ctx.translate(0, 960)
    his_room(ctx)
    ctx.restore()
    ctx.save()
    ctx.rectangle(0, 960, W, 960)
    ctx.clip()
    him_bust(ctx, lt, expr="smug", y=2290, s=1.2)
    label(ctx, 540, 1060, "HE THINKS: WHAT TEXT?", BLUE_D, prog(lt, 0.6, 0.9), size=40)
    ctx.restore()
    rrect(ctx, -10, 950, W + 20, 20, 0)
    set_rgb(ctx, S.OUT)
    ctx.fill()


def shot_charge(ctx, lt, sh):
    his_room(ctx)
    t_on = sh.m(0) + 1.2
    t1 = sh.word_t(1, 2)
    t2 = sh.word_t(1, 4) + 0.15
    on = lt >= t_on

    def scr(c):
        if not on:
            dead_screen(c, lt)
            return
        chat(c, [("hey :)", -60, False, prog(lt, t1, t1 + 0.3)),
                 ("nvm.", 50, False, prog(lt, t2, t2 + 0.3))], clock="9:14")
    phone(ctx, 540, 700, 1.1, scr)
    # 충전 케이블
    ctx.move_to(540, 1110)
    ctx.curve_to(540, 1250, 900, 1200, 1000, 1380)
    set_rgb(ctx, "#F2F0EA")
    ctx.set_line_width(14)
    ctx.stroke()
    if on:
        k = ease_out_back(prog(lt, t_on, t_on + 0.3))
        if k > 0.01:
            battery(ctx, 870, 260, 1.3 * k, 0.15, "#5FBF5A")
    shock = lt > t2 + 0.3
    him_bust(ctx, lt, expr="shock" if shock else "neutral", pose="shrug" if shock else "down",
             sweat=shock)


def shot_outro(ctx, lt, sh):
    ctx.rectangle(0, 0, W, H)
    set_rgb(ctx, PINK)
    ctx.fill()
    ctx.move_to(W, 0)
    ctx.line_to(W, H)
    ctx.line_to(0, H)
    ctx.line_to(0, 1150)
    ctx.close_path()
    set_rgb(ctx, BLUE)
    ctx.fill()
    k1 = ease_out_back(prog(lt, sh.m(0), sh.m(0) + 0.4), 2.0)
    k2 = ease_out_back(prog(lt, sh.word_t(0, 2), sh.word_t(0, 2) + 0.4), 2.0)
    draw_text(ctx, "SAME MOMENT.", 540, 420, 104, font="black", fill="#FFFFFF", stroke=10,
              stroke_fill=S.OUT, scale=k1)
    draw_text(ctx, "TWO WORLDS.", 540, 590, 104, font="black", fill="#FFD54A", stroke=10,
              stroke_fill=S.OUT, scale=k2)
    draw_text(ctx, "TWO DIFFERENT UNIVERSES", 540, 160, 46, font="black", fill="#FFFFFF",
              alpha=0.85)
    HER.draw(ctx, 270, 2150, 1.0, 1, pose="wave" if lt > sh.m(1) else "down", expr="neutral", t=lt)
    HIM.draw(ctx, 810, 2150, 1.0, -1, pose="wave" if lt > sh.m(1) else "down", expr="neutral",
             t=lt + 0.5)
    kc = ease_out_back(prog(lt, sh.me(1) - 0.2, sh.me(1) + 0.2), 2.0)
    if kc > 0.01:
        label(ctx, 540, 960, "WHO'S RIGHT? COMMENT BELOW", S.RUST, kc, size=50)


SHOT_FNS = {k[5:]: v for k, v in dict(globals()).items() if k.startswith("shot_")}
CAMERA = {
    "hook": (540, 760, 0.10), "her": (540, 700, 0.05), "verdict": (540, 720, 0.08),
    "him": (540, 500, 0.05), "twist": (540, 720, 0.14), "split": (540, 960, 0.03),
    "charge": (540, 700, 0.06), "outro": (540, 600, 0.03),
}

EP = Episode(TITLE, SCRIPT, SHOT_FNS, VOICES, CAP_COLORS, CAMERA, bgm_style="explain",
             bpm=96, bgm_gain=0.22, cap_chars=14)


def prepare():
    global DURATION
    EP.prepare()
    DURATION = EP.duration


def cues():
    c = []
    for i, sh in enumerate(EP.shots):
        st = sh.start
        if i > 0:
            c.append((st, "whoosh"))
        n = sh.name
        if n == "hook":
            c.append((st + 0.3, "pop"))
            for j in range(12):
                c.append((st + sh.m(1) + (sh.me(1) - sh.m(1)) * j / 12, "tick"))
        if n == "her":
            for j in range(23):
                tt = sh.m(0) + 0.6 + (sh.me(0) - sh.m(0) - 0.6) * (j / 23) ** 0.5
                c.append((st + tt, "tick"))
            for j in range(4):
                c.append((st + sh.m(1) + 0.4 + j * 0.35, "thud"))
            c.append((st + sh.word_t(2, 2), "stamp"))
        if n == "verdict":
            c.append((st + 0.1, "rain", sh.dur))
            tw = sh.word_t(0, 4)
            c.append((st + tw + 0.15, "stamp"))
            c.append((st + tw + 0.4, "stamp"))
        if n == "him":
            c.append((st + sh.word_t(0, 5), "cheer", 1.6))
            c.append((st + sh.word_t(0, 5), "ding"))
        if n == "twist":
            c.append((st + sh.m(1) + 0.1, "fall"))
            c.append((st + sh.m(1) + 0.55, "stamp"))
        if n == "split":
            c.append((st + 0.1, "rain", sh.dur))
            c.append((st + 0.7, "pop"))
        if n == "charge":
            c.append((st + sh.m(0) + 1.2, "ding"))
            c.append((st + sh.word_t(1, 2), "pop"))
            c.append((st + sh.word_t(1, 4) + 0.15, "pop"))
            c.append((st + sh.word_t(1, 4) + 0.45, "boing"))
        if n == "outro":
            c.append((st + sh.m(0), "pop"))
            c.append((st + sh.word_t(0, 2), "pop"))
            c.append((st + sh.me(1), "ding"))
    return sorted(c, key=lambda x: x[0])


def mix():
    return EP.mix(cues())


def render_frame(ctx, t):
    if not EP.shots:
        prepare()
    EP.render_frame(ctx, t)
