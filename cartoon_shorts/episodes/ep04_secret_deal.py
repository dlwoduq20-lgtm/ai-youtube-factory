"""오늘의 만평 #04 — 비밀로 하자며?!  (두둥실 캐릭터 + TTS)

실제 사건 (2026년 9~10월, 국내외 보도 기준):
- 9/23 우크라이나 대통령이 유엔총회 연설에서 북한군 포로 2명을 한국에 넘겼다고 공개
- 한국 정부: 비공개로 하기로 사전 합의했다며 반발 / 우크라이나 대통령실: 그런 합의는 없었다
- 9/28 외교부, 주한 우크라이나 대사대리 불러 해명·사과 요구 / 10/2 대통령, 공개 사과 요구
- 10/8 주우크라이나 대사 본국 소환 결정 (대사관 운영은 계속, 협의 지속)
- 우크라이나 외무부: 건설적 대화 재개에 열려 있다
합의 여부는 양측 주장이 엇갈리므로 어느 한쪽 말을 사실로 단정하지 않는다. 개인 이름은 쓰지 않는다.
"""
import math

from .. import squire as S
from ..doodle import Doodle
from ..engine import H, W, draw_text, ease_out_back, ease_out_cubic, ellipse, prog, rrect, set_rgb
from ..explainer import Explainer, close_up, label

TITLE = "오늘의 만평 #04 - 비밀로 하자며?!"
DURATION = 37.0

KR = Doodle(coat="#2F3E5C", tie="#C9473B", hair="cap", hair_color="#2A2420", badge=True)
UA = Doodle(coat="#5E6B45", hair="cap", hair_color="#4A3A2A", collar=False)
CIT = Doodle(coat="#6F7F63", hair="beanie", hair_color="#C25B3F", collar=False)

# 화자 → (edge 음성, 속도, 피치, 추가 피치 배율)
VOICE = {
    "N": ("male", "+80%", "+20Hz", 1.18),
    "K": ("female", "+75%", "+30Hz", 1.12),
    "U": ("male2", "+50%", "+0Hz", 0.95),  # 우크라이나 측: 혼자 덤덤하게
}
CAP_COLOR = {"N": "#FFFFFF", "K": "#9FD3F0", "U": "#FFE38A"}

SCRIPT = [
    ("hook", [("N", "비밀로 해달라며? 근데 그걸 유엔에서 말해버렸다고?", None)],
     {"tail": 1.0, "min_tail": 0.9}),
    ("podium", [("N", "지난달 유엔총회. 우크라이나 대통령이 연설하다가 이렇게 말했대.", None),
                ("U", "북한군 포로 두 명, 한국에 넘겼습니다!",
                 "북한군 포로 2명, 한국에 넘겼습니다!")], {"tail": 0.6}),
    ("risk", [("N", "문제는 이게 원래 비밀이었다는 거야.", None),
              ("N", "북한에 남은 포로 가족들이 위험해질 수 있거든.", None)], {"tail": 0.6}),
    ("kr", [("K", "공개 안 하기로 약속했잖아요!", None)], {"tail": 0.4}),
    ("ua", [("U", "그런 약속, 한 적 없는데요?", None)], {"tail": 0.8}),
    ("tug", [("N", "한국은 거짓말이라고 하고, 우크라이나는 오해래.", None),
             ("N", "말이 완전히 엇갈리는 거지.", None)], {"tail": 0.8}),
    ("calendar", [("N", "한국은 항의하고, 사과를 요구하다가,", None),
                  ("N", "결국 우크라이나 주재 대사를 불러들였어.", None)], {"tail": 1.8}),
    ("plane", [("N", "대사관 문을 닫은 건 아니야.", None),
               ("N", "대신, 우리 화났다는 신호를 확실히 보낸 거지.",
                "대신, \"우리 화났다\"는 신호를 확실히 보낸 거지.")], {"tail": 0.8}),
    ("door", [("N", "우크라이나는 대화하겠다고는 하는데, 아직 사과는 없어.", None)], {"tail": 1.4}),
    ("outro", [("N", "비밀 약속, 누구 말이 맞는 것 같아?", None),
               ("N", "댓글로 알려줘!", None)], {"tail": 2.4}),
]

CAL = ["9.23", "9.28", "10.2", "10.8"]


def _cal_flips(sh):
    """(local_time, 이전, 다음) — 항의(9.28)·사과 요구(10.2)는 첫 대사, 대사 소환(10.8)은 둘째 대사."""
    a, b = sh.m(0) + 0.1, sh.m(0) + (sh.me(0) - sh.m(0)) * 0.55
    return [(a, CAL[0], CAL[1]), (b, CAL[1], CAL[2]), (sh.m(1) + 0.2, CAL[2], CAL[3])]


def cues(ep):
    c = []
    for i, sh in enumerate(ep.shots):
        st = sh.start
        if i > 0:
            c.append((st, "whoosh"))
        if sh.name == "hook":
            c.append((st + 0.3, "thud"))
            c.append((st + sh.me(0) - 0.1, "snap"))
            c.append((st + sh.me(0), "stamp"))
        if sh.name == "podium":
            c.append((st + sh.m(1), "ding"))
        if sh.name in ("kr", "ua"):
            c.append((st + 0.25, "slide"))
            c.append((st + sh.m(len(sh.lines) - 1), "pop"))
        if sh.name == "tug":
            c.append((st + 0.3, "boing"))
            c.append((st + sh.dur - 0.9, "boing"))
        if sh.name == "calendar":
            for ft, *_ in _cal_flips(sh):
                c.append((st + ft, "rip"))
            c.append((st + sh.me(1) - 0.2, "stamp"))
        if sh.name == "risk":
            c.append((st + 0.3, "thud"))
            c.append((st + sh.m(1), "boing"))
        if sh.name == "plane":
            c.append((st + 0.2, "whoosh"))
        if sh.name == "door":
            c.append((st + 0.6, "slide"))
            c.append((st + sh.me(0) - 0.4, "stamp"))
        if sh.name == "outro":
            c.append((st + sh.m(1), "pop"))
            c.append((st + sh.m(1) + 0.8, "ding"))
    return c


# ---------------------------------------------------------------- 샷 그리기
def _padlock(ctx, x, y, s, open_k):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.save()  # 고리: open_k 만큼 위로 빠지며 돌아감
    ctx.translate(40, -40 * open_k)
    ctx.rotate(-0.5 * open_k)
    ctx.new_path()
    ctx.arc(-40, -60, 55, math.pi, 0)
    ctx.line_to(15, 0)
    ctx.move_to(-95, 0)
    ctx.line_to(-95, -60)
    set_rgb(ctx, S.OUT)
    ctx.set_line_width(36)
    ctx.stroke_preserve()
    set_rgb(ctx, "#B9BEC6")
    ctx.set_line_width(22)
    ctx.stroke()
    ctx.restore()
    rrect(ctx, -110, -20, 220, 170, 26)
    S.fs(ctx, "#E8B93E", lw=9)
    ellipse(ctx, 0, 50, 20, 20)
    set_rgb(ctx, S.OUT)
    ctx.fill()
    rrect(ctx, -8, 55, 16, 50, 6)
    ctx.fill()
    ctx.restore()


def shot_hook(ctx, lt, sh, ep):
    S.planks(ctx, base="#3E4F63", dark="#31404F")
    S.spotlight(ctx, 540, -50, 300, 1100, 1500, alpha=0.3)
    k = ease_out_back(prog(lt, 0.1, 0.5), 1.4)
    S.folder(ctx, -400 + 940 * k, 980, 1.6, "비공개 합의", rot=-0.05 * (1 - k))
    open_k = ease_out_back(prog(lt, sh.me(0) - 0.1, sh.me(0) + 0.25), 2.0)
    shake = math.sin(lt * 40) * 6 * prog(lt, sh.me(0) - 0.6, sh.me(0) - 0.1) * (1 - prog(lt, sh.me(0), sh.me(0) + 0.1))
    _padlock(ctx, 540 + shake, 1260, 0.9, open_k)
    S.stamp(ctx, 560, 640, "공개?!", prog(lt, sh.me(0), sh.me(0) + 0.45), size=150, rot=-0.12)


def _globe(ctx, x, y, r, alpha):
    set_rgb(ctx, "#DCE6F2", alpha)
    ctx.set_line_width(10)
    ellipse(ctx, x, y, r, r)
    ctx.stroke()
    for k in (0.35, 0.75):
        ellipse(ctx, x, y, r * k, r)
        ctx.stroke()
    for dy in (-0.5, 0.0, 0.5):
        w = r * math.sqrt(1 - dy * dy)
        ctx.move_to(x - w, y + dy * r)
        ctx.line_to(x + w, y + dy * r)
    ctx.stroke()


def shot_podium(ctx, lt, sh, ep):
    S.sky(ctx, "#24354F", "#3D5476")
    for i in range(9):  # 커튼 주름
        ctx.rectangle(i * 130 - 20, 0, 60, H)
        set_rgb(ctx, "#000000", 0.08)
        ctx.fill()
    _globe(ctx, 540, 520, 230, 0.55)
    draw_text(ctx, "유엔총회", 540, 860, 70, font="black", fill="#DCE6F2", alpha=0.8)
    talking = lt >= sh.m(1)
    UA.draw(ctx, 520, 1960, 1.8, 1, pose="point" if talking else "down",
            expr="smug" if not talking else "neutral", mouth=ep.mouth("U", sh.start + lt) * 1.3, t=lt)
    # 연단
    ctx.new_path()
    ctx.move_to(250, 1300)
    ctx.line_to(830, 1300)
    ctx.line_to(780, H)
    ctx.line_to(300, H)
    ctx.close_path()
    S.fs(ctx, "#6B4E35", lw=9)
    rrect(ctx, 230, 1270, 620, 60, 14)
    S.fs(ctx, "#856246", lw=9)
    _globe(ctx, 540, 1560, 110, 0.7)
    # 마이크
    S.tube(ctx, [(640, 1280), (700, 1190)], 12, "#3A3F4A", lw=6)
    ellipse(ctx, 705, 1170, 26, 34)
    S.fs(ctx, "#2E2E33", lw=6)
    if talking:  # 퍼져나가는 음파
        for j in range(3):
            k = ((lt - sh.m(1)) * 1.4 + j / 3) % 1.0
            ctx.new_path()
            ctx.arc(705, 1170, 60 + 260 * k, -0.9, 0.3)
            set_rgb(ctx, "#F3EBD5", 1 - k)
            ctx.set_line_width(10)
            ctx.stroke()
        # 카메라 플래시
        if int(lt * 5) % 3 == 0:
            ctx.rectangle(0, 0, W, H)
            set_rgb(ctx, "#FFFFFF", 0.06)
            ctx.fill()


FAMILY = [Doodle(coat="#7D7468", hair="gray", hair_color="#CFCFCF", collar=False),
          Doodle(coat="#8A6F7A", hair="bob", hair_color="#2F2724", collar=False),
          Doodle(coat="#6B7E8C", hair="tuft", collar=False)]


def shot_risk(ctx, lt, sh, ep):
    S.planks(ctx, base="#3E4F63", dark="#31404F")
    danger = lt >= sh.m(1)
    for i, (P, x, sc) in enumerate(zip(FAMILY, (300, 780, 540), (0.9, 0.9, 0.7))):
        P.draw(ctx, x, 1180, sc, 1 if x < 540 else -1, pose="down",
               expr="shock" if danger else "neutral", t=lt + i, sweat=danger)
    draw_text(ctx, "북한에 남은 포로 가족", 540, 1460, 64, font="black", fill="#F3EBD5")
    # 비밀 방패: 위험해지면 금이 가며 흔들린다
    k = max(0.01, ease_out_back(prog(lt, 0.1, 0.5), 1.4))
    shake = math.sin(lt * 38) * 10 * prog(lt, sh.m(1), sh.m(1) + 0.2)
    ctx.save()
    ctx.translate(540 + shake, 400)
    ctx.scale(k * 0.75, k * 0.75)
    ctx.new_path()
    ctx.move_to(-230, -200)
    ctx.line_to(230, -200)
    ctx.curve_to(230, 60, 120, 200, 0, 260)
    ctx.curve_to(-120, 200, -230, 60, -230, -200)
    ctx.close_path()
    S.fs(ctx, "#8FAFC9", lw=10)
    draw_text(ctx, "비밀", 0, 0, 120, font="black", fill="#2E3A4A")
    if danger:
        ctx.move_to(-40, -200)
        ctx.line_to(10, -90)
        ctx.line_to(-30, -20)
        ctx.line_to(40, 90)
        set_rgb(ctx, S.OUT)
        ctx.set_line_width(10)
        ctx.stroke()
    ctx.restore()
    if danger:
        kw = max(0.01, ease_out_back(prog(lt, sh.m(1), sh.m(1) + 0.35), 2.0))
        ctx.save()
        ctx.translate(820, 260)
        ctx.scale(kw, kw)
        ctx.new_path()
        ctx.move_to(0, -95)
        ctx.line_to(105, 85)
        ctx.line_to(-105, 85)
        ctx.close_path()
        S.fs(ctx, "#E8B93E", lw=9)
        draw_text(ctx, "!", 0, 20, 110, font="black", fill="#2E3A4A")
        ctx.restore()


def shot_kr(ctx, lt, sh, ep):
    close_up(ctx, lt, sh, ep, KR, "K", 1, 420, S.SLATE, S.SLATE_D, "한국 정부", 0)


def shot_ua(ctx, lt, sh, ep):
    close_up(ctx, lt, sh, ep, UA, "U", -1, 660, "#8C8A62", "#737150", "우크라이나 측", 0, calm=True)


def shot_tug(ctx, lt, sh, ep):
    S.planks(ctx, base=S.SLATE, dark=S.SLATE_D)
    ctx.rectangle(0, 1450, W, H)
    set_rgb(ctx, "#8C7A5E")
    ctx.fill()
    off = 45 * math.sin(lt * 4.2) * prog(lt, 0.2, 0.6)
    s = 0.95
    pa, pb = (220 + off, 1480), (860 + off, 1480)
    ha, hb = (pa[0] + 175 * s, pa[1] - 255 * s), (pb[0] - 175 * s, pb[1] - 255 * s)
    mid = ((ha[0] + hb[0]) / 2, (ha[1] + hb[1]) / 2 + 40)
    S.tube(ctx, [ha, mid, hb], 16, "#C89B5C", lw=5)
    S.folder(ctx, mid[0], mid[1] + 130, 0.6, "비공개 합의", rot=math.sin(lt * 4) * 0.12)
    for P, p, f, word in ((KR, pa, 1, "거짓말!"), (UA, pb, -1, "오해!")):
        P.draw(ctx, p[0], p[1], s, f, pose="pull", expr="angry", mouth=0.3 + 0.3 * abs(math.sin(lt * 9)),
               t=lt, rot=-0.15 * f, bob=False, sweat=True)
        label(ctx, word, p[0] + f * 60, 600, ease_out_back(prog(lt, 0.3 + (f < 0) * 0.4, 0.7 + (f < 0) * 0.4)))


def shot_calendar(ctx, lt, sh, ep):
    S.planks(ctx, base=S.SLATE, dark=S.SLATE_D, seed=7)
    flips = _cal_flips(sh)
    cur = CAL[0]
    for ft, a, b in flips:
        if lt >= ft:
            cur = b
    sub = "외교 갈등 일지"
    S.calendar(ctx, 560, 1000, 1.0, cur, sub, seed=len(cur))
    for j, (ft, a, b) in enumerate(flips):
        k = (lt - ft) / 0.9
        if 0 <= k < 1:
            S.flying_page(ctx, 560, 1000, 1.0, k, a, sub, seed=j, direction=-1 if j % 2 else 1)
    S.stamp(ctx, 560, 1060, "대사 소환!", prog(lt, sh.me(1) - 0.2, sh.me(1) + 0.3), size=105, rot=-0.15)


def _plane(ctx, x, y, s):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(-s, s)  # 왼쪽(서울 방향)으로 비행
    ctx.new_path()  # 꼬리 날개
    ctx.move_to(-300, -20)
    ctx.line_to(-360, -150)
    ctx.line_to(-290, -150)
    ctx.line_to(-210, -20)
    ctx.close_path()
    S.fs(ctx, "#C9473B", lw=8)
    rrect(ctx, -340, -50, 680, 110, 55)
    S.fs(ctx, "#F6F3EC", lw=9)
    ctx.new_path()  # 날개
    ctx.move_to(-40, 20)
    ctx.line_to(-170, 190)
    ctx.line_to(-90, 190)
    ctx.line_to(90, 20)
    ctx.close_path()
    S.fs(ctx, "#D8DDE4", lw=8)
    for i in range(7):
        ellipse(ctx, -180 + i * 60, -8, 14, 16)
        S.fs(ctx, "#7FA6C9", lw=4)
    ctx.restore()


def shot_plane(ctx, lt, sh, ep):
    S.sky(ctx, "#8EB4D6", "#DCEAF3")
    for i, (cx, cy, cs) in enumerate(((100, 380, 1.3), (700, 260, 1.0), (400, 1100, 1.5), (850, 1500, 1.1))):
        S.cloud(ctx, (cx + lt * 120 * (i % 2 + 1)) % 1500 - 250, cy, cs, "#FFFFFF", alpha=0.9)
    x = 1250 - 1000 * prog(lt, 0.0, sh.dur)
    y = 900 + math.sin(lt * 3) * 25
    ctx.move_to(x + 360, y)  # 비행운
    ctx.line_to(x + 1400, y + 60)
    set_rgb(ctx, "#FFFFFF", 0.7)
    ctx.set_line_width(16)
    ctx.set_dash([40, 30])
    ctx.stroke()
    ctx.set_dash([])
    _plane(ctx, x, y, 1.0)
    draw_text(ctx, "대사 귀국", x, y + 250, 70, font="black", fill="#2E3A4A", stroke=10, stroke_fill="#FFFFFF")
    label(ctx, "주우크라이나 대사관: 운영 중", 540, 1560, ease_out_back(prog(lt, sh.m(0) + 0.3, sh.m(0) + 0.7)),
          size=56)


def shot_door(ctx, lt, sh, ep):
    S.planks(ctx, base="#B9A57A", dark="#9C8960", w=150)
    draw_text(ctx, "대화의 문", 540, 330, 110, font="black", fill="#2E3A4A")
    ctx.rectangle(240, 520, 600, 1000)  # 문 안쪽 빛
    set_rgb(ctx, "#FFF3C4")
    ctx.fill()
    k = ease_out_cubic(prog(lt, 0.4, 1.2))
    ctx.new_path()  # 바닥으로 새어 나오는 빛
    ctx.move_to(260, 1520)
    ctx.line_to(820, 1520)
    ctx.line_to(820 + 200 * k, 1900)
    ctx.line_to(160 - 100 * k, 1900)
    ctx.close_path()
    set_rgb(ctx, "#FFF3C4", 0.45 * k)
    ctx.fill()
    dw = 600 - 380 * k  # 문짝이 반쯤 열린다 (원근감용으로 가로 폭만 줄임)
    ctx.new_path()
    ctx.move_to(240, 520)
    ctx.line_to(240 + dw, 520 + 50 * k)
    ctx.line_to(240 + dw, 1520 - 50 * k)
    ctx.line_to(240, 1520)
    ctx.close_path()
    S.fs(ctx, "#6B4E35", lw=9)
    ellipse(ctx, 240 + dw - 40, 1030, 18, 18)
    S.fs(ctx, "#E8B93E", lw=5)
    rrect(ctx, 220, 500, 640, 1040, 10)
    S.fs(ctx, None, lw=14)
    UA.draw(ctx, 690, 1530, 0.9, -1, pose="wave", expr="smug", t=lt)
    S.stamp(ctx, 540, 1700, "사과: 아직", prog(lt, sh.me(0) - 0.4, sh.me(0) + 0.1), size=110, rot=-0.08)


def shot_outro(ctx, lt, sh, ep):
    S.planks(ctx, base=S.SLATE, dark=S.SLATE_D, seed=9)
    waving = lt >= sh.m(1)
    CIT.draw(ctx, 540, 2120, 1.7, 1, pose="wave" if waving else "shrug",
             expr="smug" if waving else "deadpan", t=lt)
    label(ctx, "댓글로 알려줘!", 540, 330, ease_out_back(prog(lt, sh.m(1), sh.m(1) + 0.4), 2.0), size=80)
    label(ctx, "구독", 540, 560, ease_out_back(prog(lt, sh.m(1) + 0.8, sh.m(1) + 1.2), 2.0),
          fill=S.RUST, ink="#FFFFFF")


SHOT_FN = {k[5:]: v for k, v in globals().items() if k.startswith("shot_")}
CAMERA = {
    "hook": (540, 1000, 0.1), "podium": (540, 1100, 0.07), "kr": (420, 900, 0.06),
    "ua": (660, 900, 0.06), "tug": (540, 1200, 0.05), "calendar": (560, 1000, 0.08),
    "plane": (540, 900, 0.04), "door": (540, 1000, 0.06), "outro": (540, 1000, 0.04),
    "risk": (540, 1000, 0.08),
}

EP = Explainer(SCRIPT, VOICE, CAP_COLOR, SHOT_FN, CAMERA, cues,
               notice="※ 국내외 언론 보도 기반 / 비공개 합의 여부는 양측 주장이 엇갈립니다")
render_frame, mix = EP.render_frame, EP.mix


def prepare():
    global DURATION
    DURATION = EP.prepare().duration
