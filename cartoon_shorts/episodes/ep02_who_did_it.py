"""오늘의 만평 #02 — 법안이랑 기업 문건이 토씨까지 똑같다고?  (해설 애니메이션 스타일 + TTS)

실제 사건: 2026년 10월 6일 산업통상부 국정감사에서 한 야당 의원이 RE100(재생에너지자립도시)
특별법이 한 기업의 내부 문건과 일정·조문이 일치한다며 입법로비 의혹을 제기한 건.
의혹은 '의원 주장'으로만 다루고, 장관 답변과 기업 반론을 함께 넣는다. 개인·기업 이름은 쓰지 않는다.

내레이션 한 줄 = 자막 한 덩어리, 샷(장면) 단위로 타임라인을 TTS 길이에 맞춰 자동 배치한다.
"""
import math
import random

import numpy as np

from .. import audio, tts
from .. import squire as S
from ..engine import (FPS, H, W, clamp, draw_text, ease_in_out, ease_out_back,
                      ease_out_cubic, ellipse, prog, rrect, set_rgb, wobble)

TITLE = "오늘의 만평 #02 - 법안이랑 기업 문건이 토씨까지 똑같다고?"
DURATION = 60.0

A = S.Person(coat="#4E5A6B", tie="#3E8E87", hair="part", hair_color="#4A3426", badge=True)
B = S.Person(coat="#3B3F48", tie="#5B6E8C", hair="part", hair_color="#8E8E8E", badge=True)  # 장관
CIT = S.Person(coat="#6F7F63", hair="beanie", hood=True, pants="#3D4656")

# 화자 → (edge 음성, 속도, 피치, 추가 피치 배율) — 빠르고 높은 만화 톤
VOICE = {
    "N": ("male", "+80%", "+20Hz", 1.18),
    "A": ("male2", "+85%", "+0Hz", 1.25),
    "B": ("male", "+60%", "-10Hz", 0.92),  # 장관: 혼자 낮고 덤덤하게 (대비 개그)
}
CAP_COLOR = {"N": "#FFFFFF", "A": "#9FE3DA", "B": "#FFC9A8", "AB": "#FFE38A"}


# ---------------------------------------------------------------- 대본
# (화자, TTS 문장, 자막 문장 or None)
SCRIPT = [
    ("exterior", [("N", "지금 국정감사에서 제대로 터진 사건, 하나 알려줄게!", None)], {}),
    ("bill", [("N", "주인공은 알이백 특별법! 재생에너지 자립도시를 만들자는 법이야.",
               "주인공은 RE100 특별법! 재생에너지 자립도시를 만들자는 법이야.")], {}),
    ("folder", [("N", "근데 한 야당 의원이, 어느 기업의 내부 문건을 짠! 하고 꺼냈어.", None)], {}),
    ("a_close", [("N", "의원 왈,", None),
                 ("A", "이 문건이랑 법안, 조문 토씨까지 똑같다니까?!", None)], {}),
    ("calendar", [("N", "문건 속 계획은, 이천이십오년 시월 법안 발의.",
                   "문건 속 계획: 2025년 10월 법안 발의."),
                  ("N", "의원 말로는,", None),
                  ("N", "실제로 그 무렵부터 관련 법안 발의가 줄줄이!", None)], {"tail": 1.2}),
    ("arrow", [("N", "게다가 법이 생기기도 전에, 예산 이백육억이 먼저 잡혔다는 지적까지!",
                "게다가 법이 생기기도 전에, 예산 206억이 먼저 잡혔다는 지적까지!")], {"tail": 0.6}),
    ("b_close", [("N", "장관의 대답은?", None),
                 ("B", "다른 법안을 보고 만든 것으로 추정됩니다.", None)], {"tail": 0.8}),
    ("tug", [("N", "의혹이냐, 우연이냐! 줄다리기 시작!", None)], {"tail": 1.2}),
    ("compare", [("N", "기업 문건이랑 발의된 법안, 진짜 토씨까지 같은 걸까?", None)],
     {"tail": 1.2}),
    ("outro", [("N", "기업은 불법도 특혜도 없었다는 입장, 야당은 특검까지 요구 중!", None),
               ("N", "너희 생각은 어때? 댓글로 알려줘!", None)], {"tail": 2.0}),
]

TRANS = 0.3  # 샷 전환 시간
LEAD = 0.25  # 샷 시작 후 첫 대사까지
GAP = 0.08
TAIL = 0.5  # 샷 끝 여운 배율 (숏폼 템포)


class Shot:
    def __init__(self, name, lines, opts):
        self.name, self.lines, self.opts = name, lines, opts
        self.start = self.dur = 0.0
        self.marks = []  # (local_start, local_end) per line

    def m(self, i):
        return self.marks[i][0]

    def me(self, i):
        return self.marks[i][1]


SHOTS = []
LINES = []  # (global_start, global_end, speaker, caption)
ENV = {}  # 화자별 입모양 엔벨로프 (프레임 단위)
VOICE_TRACK = None
CUES = []


def prepare():
    global DURATION, VOICE_TRACK
    SHOTS.clear()
    LINES.clear()
    segs = []  # (start, speaker, samples)
    cur = 0.0
    for name, lines, opts in SCRIPT:
        sh = Shot(name, lines, opts)
        sh.start = cur
        lt = LEAD
        for spk, text, cap in lines:
            parts = []
            for sp in (("A", "B") if spk == "AB" else (spk,)):
                v, r, p, k = VOICE[sp]
                x, _ = tts.synth(text, v, rate=r, pitch=p, shift=k)
                parts.append((sp, x))
            d = max(len(x) for _, x in parts) / audio.SR
            for sp, x in parts:
                segs.append((cur + lt, sp, x))
            sh.marks.append((lt, lt + d))
            LINES.append((cur + lt, cur + lt + d, spk, cap or text))
            lt += d + GAP
        sh.dur = lt - GAP + max(opts.get("tail", 0.45) * TAIL, opts.get("min_tail", 0))
        cur += sh.dur
        SHOTS.append(sh)
    DURATION = cur
    n = int(DURATION * audio.SR) + audio.SR
    VOICE_TRACK = np.zeros(n, np.float32)
    per = {k: np.zeros(n, np.float32) for k in ("N", "A", "B")}
    for st, sp, x in segs:
        p = int(st * audio.SR)
        VOICE_TRACK[p:p + len(x)] += x * 0.9
        per[sp][p:p + len(x)] += x
    hop = audio.SR // FPS
    for k, tr in per.items():
        frames = len(tr) // hop
        rms = np.sqrt(np.mean(tr[:frames * hop].reshape(frames, hop) ** 2, axis=1))
        rms = np.convolve(rms, np.ones(2) / 2, "same")
        peak = np.percentile(rms[rms > 1e-4], 95) if np.any(rms > 1e-4) else 1
        ENV[k] = np.clip(rms / peak, 0, 1)
    CUES[:] = _cues()


def mix():
    duck = [(s, e) for s, e, *_ in LINES]
    return audio.mix(DURATION, CUES, bgm_gain=0.3, duck=duck, voice=VOICE_TRACK,
                     style="explain", bpm=118)


def mouth(spk, t):
    e = ENV.get(spk)
    if e is None:
        return 0.0
    i = int(t * FPS)
    return float(e[i]) if 0 <= i < len(e) else 0.0


def shot_named(name):
    return next(s for s in SHOTS if s.name == name)


# ---------------------------------------------------------------- 사운드 큐
CAL_SEQ = ["25.6", "25.7", "25.8", "25.9", "25.10"]


def _calendar_flips(sh):
    """(local_time, 이전 라벨, 다음 라벨) — 첫 대사 동안 문건 속 일정이 넘어간다."""
    t0 = sh.m(0) + 0.15
    span = (sh.me(0) - sh.m(0)) * 0.8
    n = len(CAL_SEQ) - 1
    return [(t0 + span * j / n, CAL_SEQ[j], CAL_SEQ[j + 1]) for j in range(n)]


def _gavel_times(sh):
    t = sh.me(0) - 0.2
    return [t, t + 0.38, t + 0.76]


def _cues():
    c = []
    for i, sh in enumerate(SHOTS):
        st = sh.start
        if i > 0:
            c.append((st, "whoosh"))
        if sh.name == "bill":
            c.append((st + sh.me(0) - 0.4, "stamp"))
        if sh.name == "folder":
            c.append((st + 0.55, "thud"))
        if sh.name in ("a_close", "b_close"):
            c.append((st + 0.25, "slide"))
            c.append((st + sh.m(1), "pop"))
        if sh.name == "tug":
            c.append((st + 0.3, "boing"))
            c.append((st + sh.dur - 0.9, "boing"))
        if sh.name == "calendar":
            for ft, *_ in _calendar_flips(sh):
                c.append((st + ft, "rip"))
            c.append((st + sh.m(2), "stamp"))
        if sh.name == "arrow":
            c.append((st + 0.35, "fall"))
            for k in range(2):
                c.append((st + 0.9 + k * 0.35, "pop"))
        if sh.name == "rain":
            c.append((st, "rain", sh.dur + TRANS))
        if sh.name == "gavel":
            for gt in _gavel_times(sh):
                c.append((st + gt, "gavel"))
            c.append((st + _gavel_times(sh)[-1] + 0.3, "stamp"))
        if sh.name == "smug":
            c.append((st + sh.m(1), "cheer", 2.0))
        if sh.name == "compare":
            c.append((st + sh.me(0) - 0.6, "stamp"))
        if sh.name == "outro":
            c.append((st + sh.m(1), "pop"))
            c.append((st + sh.m(1) + 0.8, "ding"))
    return sorted(c, key=lambda x: x[0])


# ---------------------------------------------------------------- 샷 그리기
def shot_exterior(ctx, lt, sh):
    S.sky(ctx, "#8EA4BA", "#D9E0E2")
    for i, (x, y, s) in enumerate(((60, 300, 1.4), (620, 180, 1.1), (300, 620, 0.9))):
        S.cloud(ctx, (x + lt * 25 * (i + 1)) % 1500 - 300, y, s, "#B9C6D2")
    # 새
    set_rgb(ctx, S.OUT)
    ctx.set_line_width(5)
    for i in range(4):
        bx = 150 + i * 90 + lt * 60
        by = 520 + (i % 2) * 40 + math.sin(lt * 6 + i) * 8
        w = 22 + 6 * math.sin(lt * 12 + i)
        ctx.move_to(bx - w, by - 10)
        ctx.line_to(bx, by)
        ctx.line_to(bx + w, by - 10)
    ctx.stroke()
    ctx.rectangle(0, 1380, W, H)
    set_rgb(ctx, S.OLIVE)
    ctx.fill()
    S.assembly(ctx, 540, 1400, 1.0)
    # 잔디 덤불
    rnd = random.Random(2)
    for i in range(7):
        x = -40 + i * 175 + rnd.uniform(-20, 20)
        y = 1480 + rnd.uniform(0, 300)
        rrect(ctx, x, y, 210, 80, 30)
        S.fs(ctx, "#A6B57E")
    rrect(ctx, 400, 1400, 280, H, 0)
    S.fs(ctx, "#D9CDAE")


def shot_bill(ctx, lt, sh):
    S.desk(ctx)
    S.paper(ctx, 540, 900, 1.5, "RE100 특별법", rot=-0.04, lines=8)
    # 펜이 글을 씀
    k = prog(lt, 0.4, sh.me(0) - 0.6)
    px = 540 - 260 + 520 * ((k * 4) % 1.0)
    py = 760 + int(k * 4) * 85
    if k < 1:
        ctx.save()
        ctx.translate(px + 120, py - 150)
        ctx.rotate(0.5)
        rrect(ctx, -22, -200, 44, 260, 14)
        S.fs(ctx, "#2F3B4C")
        ctx.new_path()
        ctx.move_to(-22, 60)
        ctx.line_to(0, 110)
        ctx.line_to(22, 60)
        ctx.close_path()
        S.fs(ctx, "#E8B93E")
        ctx.restore()
    S.stamp(ctx, 640, 1180, "발의", prog(lt, sh.me(0) - 0.4, sh.me(0) + 0.2), size=100)


def shot_folder(ctx, lt, sh):
    S.planks(ctx, base="#3E4F63", dark="#31404F")
    S.spotlight(ctx, 540, -50, 300, 1100, 1500, alpha=0.3)
    ellipse(ctx, 540, 1200, 420, 70)
    set_rgb(ctx, (0, 0, 0, 0.25))
    ctx.fill()
    k = ease_out_back(prog(lt, 0.2, 0.7), 1.3)
    S.folder(ctx, -400 + 940 * k, 960, 1.5, "내부 문건", rot=-0.05 * (1 - k))
    rnd = random.Random(4)
    for _ in range(40):  # 먼지
        x = 540 + rnd.uniform(-450, 450)
        y = (rnd.uniform(0, 1500) - lt * rnd.uniform(10, 40)) % 1500
        ellipse(ctx, x + wobble(lt, x, 15), y, 4, 4)
        set_rgb(ctx, (1, 0.97, 0.85, 0.5))
        ctx.fill()


def _close(ctx, lt, sh, P, spk, facing, x, base, dark, label, calm=False):
    S.planks(ctx, base=base, dark=dark, seed=facing + 3)
    k = ease_out_cubic(prog(lt, 0.0, 0.5))
    talking = sh.m(1) <= lt
    mo = mouth(spk, sh.start + lt)
    P.draw(ctx, x - facing * 700 * (1 - k), 1830, 2.05, facing,
           pose="hips" if calm else ("point" if talking else "hips"),
           expr="deadpan" if calm else ("angry" if talking else "smug"),
           mouth=mo * 1.3, t=lt + facing)
    kl = ease_out_back(prog(lt, 0.4, 0.75))
    if kl > 0.01:
        ctx.save()
        ctx.translate(W / 2 + facing * -230, 250)
        ctx.scale(kl, kl)
        ctx.rotate(-0.05 * facing)
        rrect(ctx, -170, -60, 340, 120, 60)
        S.fs(ctx, "#F3EBD5")
        draw_text(ctx, label, 0, 4, 66, font="black", fill="#2E3A4A")
        ctx.restore()
    if talking and not calm:
        for i in range(3):  # 말하는 효과선
            a = -0.6 + i * 0.35
            r0 = 300 + 20 * math.sin(lt * 20 + i)
            cx, cy = x + facing * 140, 860
            ctx.move_to(cx + facing * math.cos(a) * r0, cy + math.sin(a) * r0)
            ctx.line_to(cx + facing * math.cos(a) * (r0 + 70), cy + math.sin(a) * (r0 + 70))
        set_rgb(ctx, "#F3EBD5")
        ctx.set_line_width(10)
        ctx.stroke()


def shot_a_close(ctx, lt, sh):
    _close(ctx, lt, sh, A, "A", 1, 420, S.SLATE, S.SLATE_D, "야당 의원")


def shot_b_close(ctx, lt, sh):
    _close(ctx, lt, sh, B, "B", -1, 660, "#B9A57A", "#9C8960", "장관", calm=True)


def _hand(x, y, s, facing, rot, p):
    lx, ly = p[0] * s * facing, p[1] * s
    c, sn = math.cos(rot), math.sin(rot)
    return x + lx * c - ly * sn, y + lx * sn + ly * c


def shot_tug(ctx, lt, sh):
    S.planks(ctx, base=S.SLATE, dark=S.SLATE_D)
    ctx.rectangle(0, 1450, W, H)
    set_rgb(ctx, "#8C7A5E")
    ctx.fill()
    ctx.move_to(0, 1450)
    ctx.line_to(W, 1450)
    set_rgb(ctx, S.OUT)
    ctx.set_line_width(8)
    ctx.stroke()
    off = 45 * math.sin(lt * 4.2) * prog(lt, 0.2, 0.6)
    s = 0.95
    pa = (230 + off, 1480)
    pb = (850 + off, 1480)
    ra, rb = -0.18, 0.18
    ha = _hand(*pa, s, 1, ra, (215, -285))
    hb = _hand(*pb, s, -1, rb, (215, -285))
    mid = ((ha[0] + hb[0]) / 2, (ha[1] + hb[1]) / 2 + 40)
    S.tube(ctx, [ha, mid, hb], 16, "#C89B5C", lw=5)
    S.folder(ctx, mid[0], mid[1] + 130, 0.6, "RE100법", rot=wobble(lt, 1, 0.12, 4))
    for P, p, f, r in ((A, pa, 1, ra), (B, pb, -1, rb)):
        P.draw(ctx, p[0], p[1], s, f, pose="pull", expr="angry", mouth=0.3 + 0.3 * abs(math.sin(lt * 9)),
               t=lt, rot=r, bob=False, sweat=True)
        for i in range(3):  # 흙먼지
            k = (lt * 1.5 + i / 3) % 1.0
            ellipse(ctx, p[0] - f * (40 + 120 * k), 1460 - 30 * k, 30 + 40 * k, 22 + 25 * k)
            S.fs(ctx, "#D8CBB0", lw=5, alpha=1 - k)


def shot_calendar(ctx, lt, sh):
    S.planks(ctx, base=S.SLATE, dark=S.SLATE_D, seed=7)
    flips = _calendar_flips(sh)
    cur = CAL_SEQ[0]
    for ft, a, b in flips:
        if lt >= ft:
            cur = b
    sub = "문건 속 일정"
    S.calendar(ctx, 560, 1000, 1.0, cur, sub, seed=len(cur))
    for i, (ft, a, b) in enumerate(flips):
        k = (lt - ft) / 0.9
        if 0 <= k < 1:
            S.flying_page(ctx, 560, 1000, 1.0, k, a, sub, seed=len(a),
                          direction=-1 if i % 3 else 1)
    S.stamp(ctx, 560, 1080, "발의!", prog(lt, sh.m(2), sh.m(2) + 0.5), size=150, rot=-0.15)


def shot_arrow(ctx, lt, sh):
    S.desk(ctx)
    S.graph_paper(ctx, 60, 120, 960, 1680)
    draw_text(ctx, "법 통과 전인데?", 540, 260, 92, font="black", fill="#2E3A4A", rot=-0.03)
    items = [("예산", 300, 620), ("206억", 760, 900)]
    for i, (name, x, y) in enumerate(items):
        k = ease_out_back(prog(lt, 0.9 + i * 0.35, 1.2 + i * 0.35), 2.2)
        if k < 0.01:
            continue
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(k, k)
        ctx.rotate(wobble(lt, i, 0.05, 2))
        tw = len(name) * 60 + 150
        rrect(ctx, -tw / 2, -55, tw, 110, 20)
        S.fs(ctx, "#FBF7EC")
        draw_text(ctx, name, -35, 2, 60, font="black", fill="#2E3A4A")
        ctx.new_path()
        ax = tw / 2 - 50
        ctx.move_to(ax, -35)
        ctx.line_to(ax + 30, 0)
        ctx.line_to(ax + 12, 0)
        ctx.line_to(ax + 12, 35)
        ctx.line_to(ax - 12, 35)
        ctx.line_to(ax - 12, 0)
        ctx.line_to(ax - 30, 0)
        ctx.close_path()
        S.fs(ctx, S.RUST, lw=4)
        ctx.restore()
    k = ease_out_cubic(prog(lt, 0.3, 1.3))
    S.big_arrow(ctx, 540, 2050, 1.0, 0.25 + 0.75 * k)


def shot_rain(ctx, lt, sh):
    S.sky(ctx, "#3E4654", "#5F6978")
    S.cloud(ctx, -100 + lt * 10, 250, 1.6, "#4B5462")
    S.cloud(ctx, 500 - lt * 8, 420, 1.3, "#555E6C")
    # 길
    ctx.new_path()
    ctx.move_to(0, 1300)
    ctx.line_to(W, 1220)
    ctx.line_to(W, H)
    ctx.line_to(0, H)
    ctx.close_path()
    S.fs(ctx, "#8E9097")
    for i in range(6):
        y = 1330 + i * 110
        ctx.move_to(0, y + 20)
        ctx.line_to(W, y - 60 + i * 10)
    set_rgb(ctx, S.OUT, 0.35)
    ctx.set_line_width(5)
    ctx.stroke()
    S.lamppost(ctx, 830, 1700, lt)
    ellipse(ctx, 430, 1700, 260, 45)
    set_rgb(ctx, "#6E8196", 0.7)
    ctx.fill()
    CIT.draw(ctx, 430, 1700, 1.25, 1, pose="down", expr="sad", t=lt, bob=False)
    S.sigh(ctx, 600, 920, lt, 0.6)
    S.rain(ctx, lt)


def shot_gavel(ctx, lt, sh):
    S.planks(ctx, base="#7A5236", dark="#5C3B25", w=170)
    S.spotlight(ctx, 540, -50, 300, 1200, 1700, alpha=0.25)
    times = _gavel_times(sh)
    ang, shake = -0.9, 0.0
    for j, gt in enumerate(times):
        if gt - 0.18 <= lt < gt:  # 내려치는 중
            ang = -0.9 * (1 - prog(lt, gt - 0.18, gt) ** 2)
        elif lt >= gt:
            last = j == len(times) - 1
            ang = 0.0 if last else -0.9 * prog(lt, gt + 0.05, gt + 0.2)
            shake = max(shake, 1 - prog(lt, gt, gt + 0.25))
    ctx.save()
    ctx.translate(wobble(lt, 3, 18 * shake, 40), wobble(lt, 5, 18 * shake, 37))
    S.gavel(ctx, 420, 1250, 1.3, ang)
    if shake > 0:
        for i in range(10):
            a = i / 10 * math.pi * 2
            r0, r1 = 180, 180 + 120 * shake
            ctx.move_to(420 + math.cos(a) * r0, 1290 + math.sin(a) * r0 * 0.5)
            ctx.line_to(420 + math.cos(a) * r1, 1290 + math.sin(a) * r1 * 0.5)
        set_rgb(ctx, "#F3EBD5", shake)
        ctx.set_line_width(10)
        ctx.stroke()
    ctx.restore()
    S.stamp(ctx, 540, 560, "가결", prog(lt, times[-1] + 0.3, times[-1] + 0.9), size=180, rot=-0.12)


def shot_smug(ctx, lt, sh):
    S.planks(ctx, base="#B9A57A", dark="#9C8960", w=150)
    # 후광
    ctx.save()
    ctx.translate(540, 900)
    for i in range(16):
        ctx.rotate(math.pi / 8)
        ctx.move_to(0, 0)
        ctx.line_to(-90, -1400)
        ctx.line_to(90, -1400)
        ctx.close_path()
    set_rgb(ctx, "#FFF3C4", 0.35)
    ctx.fill()
    ctx.restore()
    shouting = lt >= sh.m(1)
    ma = mouth("A", sh.start + lt) * 1.3
    mb = mouth("B", sh.start + lt) * 1.3
    A.draw(ctx, 300, 1620, 1.25, 1, pose="cheer" if shouting else "hips",
           expr="smug", mouth=ma, t=lt)
    B.draw(ctx, 780, 1620, 1.25, -1, pose="cheer" if shouting else "hips",
           expr="smug", mouth=mb, t=lt + 0.5)
    S.confetti(ctx, lt, sh.m(1))


def shot_compare(ctx, lt, sh):
    S.desk(ctx)
    k1 = ease_out_back(prog(lt, 0.1, 0.5))
    k2 = ease_out_back(prog(lt, 0.4, 0.8))
    S.paper(ctx, 285 - 600 * (1 - k1), 950, 0.95, "기업 문건", rot=-0.05)
    S.paper(ctx, 795 + 600 * (1 - k2), 950, 0.95, "발의 법안", rot=0.04)
    ke = ease_out_back(prog(lt, 1.6, 2.0), 2.4)
    if ke > 0.01:
        ellipse(ctx, 540, 950, 70 * ke, 70 * ke)
        S.fs(ctx, "#E8B93E")
        draw_text(ctx, "?", 540, 945, 110, font="black", fill="#2E3A4A", scale=ke)
    S.stamp(ctx, 540, 1430, "의혹", prog(lt, sh.me(0) - 0.6, sh.me(0)), size=140, rot=-0.08)


def shot_outro(ctx, lt, sh):
    S.planks(ctx, base=S.SLATE, dark=S.SLATE_D, seed=9)
    waving = lt >= sh.m(1)
    CIT.draw(ctx, 540, 2060, 2.0, 1, pose="wave" if waving else "down",
             expr="neutral" if waving else "deadpan", t=lt)
    k = ease_out_back(prog(lt, sh.m(1), sh.m(1) + 0.4), 2.0)
    if k > 0.01:
        ctx.save()
        ctx.translate(540, 330)
        ctx.scale(k, k)
        rrect(ctx, -330, -95, 660, 190, 40)
        S.fs(ctx, "#F3EBD5")
        ctx.new_path()
        ctx.move_to(-60, 90)
        ctx.line_to(-110, 170)
        ctx.line_to(20, 90)
        ctx.close_path()
        S.fs(ctx, "#F3EBD5")
        rrect(ctx, -322, -88, 644, 170, 36)
        set_rgb(ctx, "#F3EBD5")
        ctx.fill()
        draw_text(ctx, "댓글로 알려줘!", 0, 0, 80, font="black", fill="#2E3A4A")
        ctx.restore()
    k2 = ease_out_back(prog(lt, sh.m(1) + 0.8, sh.m(1) + 1.2), 2.0)
    if k2 > 0.01:
        ctx.save()
        ctx.translate(540, 560)
        ctx.scale(k2, k2)
        rrect(ctx, -170, -60, 340, 120, 60)
        S.fs(ctx, S.RUST)
        draw_text(ctx, "구독", 0, 4, 66, font="black", fill="#FFFFFF")
        ctx.restore()


SHOT_FN = {k[5:]: v for k, v in globals().items() if k.startswith("shot_")}
CAMERA = {  # 샷별 켄 번스 (초점 x, y, 줌 증가량)
    "exterior": (540, 1000, 0.12), "bill": (540, 950, 0.08), "folder": (540, 1200, 0.1),
    "a_close": (420, 900, 0.06), "b_close": (660, 900, 0.06), "tug": (540, 1200, 0.05),
    "calendar": (560, 1000, 0.08), "arrow": (540, 1100, 0.06), "rain": (430, 1200, 0.1),
    "gavel": (420, 1100, 0.05), "smug": (540, 1000, 0.06), "compare": (540, 1000, 0.07),
    "outro": (540, 1000, 0.04),
}


# ---------------------------------------------------------------- 자막
def _chunks(text):
    words = text.split()
    out, cur = [], ""
    for w in words:
        cand = (cur + " " + w).strip()
        if cur and (len(cand) > 9 or cur.endswith((",", ".", "?", "!"))):
            out.append(cur)
            cur = w
        else:
            cur = cand
    if cur:
        out.append(cur)
    return out


def _caption(ctx, t):
    for st, en, spk, text in LINES:
        if st <= t < en + 0.15:
            chunks = _chunks(text)
            weights = [len(c.replace(" ", "")) + 1.5 for c in chunks]
            tot = sum(weights)
            acc = st
            for c, w in zip(chunks, weights):
                d = (en - st) * w / tot
                if acc <= t < acc + d or (c is chunks[-1] and t >= acc):
                    k = prog(t, acc, acc + 0.09)
                    sc = 1.18 - 0.18 * ease_out_cubic(k)
                    col = CAP_COLOR.get(spk, "#FFFFFF")
                    draw_text(ctx, c, W / 2 + 6, 1268 + 8, 100, font="black", fill="#1E1E22",
                              stroke=12, stroke_fill="#1E1E22", scale=sc, alpha=0.6 * k)
                    draw_text(ctx, c, W / 2, 1268, 100, font="black", fill=col,
                              stroke=12, stroke_fill="#1E1E22", scale=sc, alpha=min(1, k * 2))
                    return
                acc += d
            return


# ---------------------------------------------------------------- frame
def _draw_shot(ctx, i, t):
    sh = SHOTS[i]
    lt = t - sh.start
    fx, fy, z = CAMERA.get(sh.name, (540, 960, 0.05))
    zoom = 1 + z * ease_in_out(clamp(lt / max(sh.dur, 0.1)))
    ctx.save()
    ctx.translate(fx, fy)
    ctx.scale(zoom, zoom)
    ctx.translate(-fx, -fy)
    SHOT_FN[sh.name](ctx, lt, sh)
    ctx.restore()


def render_frame(ctx, t):
    if not SHOTS:
        prepare()
    i = 0
    for j, sh in enumerate(SHOTS):
        if sh.start <= t:
            i = j
    sh = SHOTS[i]
    lt = t - sh.start
    if i > 0 and lt < TRANS:
        e = ease_in_out(lt / TRANS)
        if i % 2 == 0:  # 휙 넘기기
            ctx.save()
            ctx.translate(-W * e, 0)
            _draw_shot(ctx, i - 1, t)
            ctx.restore()
            ctx.save()
            ctx.translate(W * (1 - e), 0)
            _draw_shot(ctx, i, t)
            ctx.restore()
            set_rgb(ctx, S.OUT)
            ctx.rectangle(W * (1 - e) - 14, 0, 14, H)
            ctx.fill()
        else:  # 펀치 컷
            ctx.save()
            p = 1 + 0.08 * (1 - e)
            ctx.translate(W / 2, H / 2)
            ctx.scale(p, p)
            ctx.translate(-W / 2, -H / 2)
            _draw_shot(ctx, i, t)
            ctx.restore()
            if lt < 0.08:
                ctx.rectangle(0, 0, W, H)
                set_rgb(ctx, "#FFFFFF", 0.5 * (1 - lt / 0.08))
                ctx.fill()
    else:
        _draw_shot(ctx, i, t)
    S.vignette(ctx, 0.35)
    S.grain(ctx, t, 0.05)
    draw_text(ctx, "※ 국정감사 발언·언론 보도 기반 / 의혹은 확인되지 않은 주장입니다", W / 2, 70, 30,
              font="black", fill="#FFFFFF", alpha=0.75, stroke=6, stroke_fill="#1E1E22")
    _caption(ctx, t)
