"""오늘의 만평 #10 — 요즘 결혼식에 모르는 사람이 오는 이유  (훅 공식 + 얼굴 첫 프레임 + 상황극 유지)

실제 사실 (보도 기준):
- JTBC 〈사건반장〉(10/1): 서울 결혼식장에서 신랑·신부 모두 모르는 남녀가 축의금 봉투(5만 원)를 내고 식권 2장을
  받아감. 식대 1인 11만 원 → 22만 원어치. 하객 명단의 모르는 이름 → CCTV 확인. 암행투어 목적인지는 확인 안 됨
- '암행투어': 예비부부가 계약 전 실제 예식 시간대에 하객처럼 방문해 주차·로비 혼잡도·식사 확인. 배경은 대관료·식대 상승
- 피해 사례: 본식 사진에 외부인이 찍혀 삭제 비용, 식권 없이 식사하다 적발 / 에티켓: 촬영·신부대기실·식권 없는 식사 금지
그 커플을 암행투어족으로 단정하지 않는다. 대사는 보도를 재구성한 상황극이다. 개인 이름은 쓰지 않는다.
"""
import math

from .. import squire as S
from ..doodle import Doodle
from ..engine import H, W, draw_text, ease_out_back, ease_out_cubic, ellipse, prog, rrect, set_rgb
from ..explainer import Explainer, card, label

TITLE = "요즘 결혼식에 모르는 사람이 오는 이유 | 오늘의 만평"
DURATION = 47.0

BRIDE = Doodle(coat="#FBFAF6", hair="bob", hair_color="#3A2A24", collar=False, pants="#FBFAF6")
GROOM = Doodle(coat="#2F3440", tie="#C9A23E", hair="cap", hair_color="#2A2420")
SPY_M = Doodle(coat="#6B5A48", hair="cap", hair_color="#2A2420", glasses=True, collar=False)
SPY_F = Doodle(coat="#B98A9C", hair="bob", hair_color="#4A3426", glasses=True, collar=False)

VOICE = {
    "N": ("male", "+80%", "+20Hz", 1.18),
    "B": ("female", "+75%", "+20Hz", 1.12),  # 신부
    "G": ("male2", "+75%", "+0Hz", 1.15),  # 신랑
    "Y": ("male", "+70%", "+0Hz", 1.0),  # 예비신랑 (암행투어)
}
CAP_COLOR = {"N": "#FFFFFF", "B": "#FFC9D9", "G": "#9FD3F0", "Y": "#FFE38A"}
HOOK = ("요즘 결혼식에", "모르는 사람이 오는 이유")

SCRIPT = [
    ("hook", [("N", "요즘 결혼식에, 모르는 사람이 온다?", None),
              ("B", "이 이름… 누구야?", None)], {"tail": 0.3}),
    ("cctv", [("N", "지난달 서울의 한 결혼식. 신랑도 신부도 모르는 남녀가 축의금을 내고, 식권 두 장을 받아 갔어.", None)],
     {"tail": 0.4}),
    ("envelope", [("G", "봉투엔 오만 원인데… 식대가 한 명당 십일만 원이거든?", "봉투엔 5만 원인데… 식대가 한 명당 11만 원이거든?"),
                  ("N", "둘이 이십이만 원어치를 먹고 간 거지.", "둘이 22만 원어치를 먹고 간 거지.")], {"tail": 0.5}),
    ("spy", [("N", "그래서 의심받는 게, 요즘 예비부부들 사이에 퍼진 암행투어야.", "그래서 의심받는 게, 요즘 예비부부들 사이에 퍼진 '암행투어'야."),
             ("Y", "주차 되나, 로비 붐비나, 밥 맛있나… 하객인 척 미리 보는 거죠.", None)], {"tail": 0.4}),
    ("bill", [("N", "대관료랑 식대가 너무 올라서, 계약하기 전에 직접 확인하겠다는 거야.", None)], {"tail": 0.4}),
    ("photo", [("B", "내 본식 사진에… 이 사람은 또 누구야?", None),
               ("N", "실제로 모르는 사람이 사진에 찍혀서 지우는 데 돈이 들거나, 식권 없이 밥 먹다 걸린 일도 있었대.", None)],
     {"tail": 0.4}),
    ("rules", [("N", "다만 그 커플이 진짜 암행투어였는지는 확인되지 않았어.", None),
               ("N", "그래서 요즘은 사진 찍지 말기, 신부대기실 가지 말기, 식권 없이 밥 먹지 말기 같은 암행투어 에티켓까지 돌아.", None),
               ("N", "너라면, 내 결혼식에 암행투어 오는 거 괜찮아?", None)], {"tail": 0.2}),
    ("loop", [], {"tail": 0, "min_tail": 0.45, "cut": True}),
]

CHAPTERS = [("의문", "hook"), ("사건", "cctv"), ("이유", "spy"), ("결론", "rules")]


def cues(ep):
    c = [(st + 0.05, "stamp") for st in ep.chapter_starts()[1:-1]]
    for i, sh in enumerate(ep.shots):
        st = sh.start
        if i > 0 and sh.name != "loop":
            c.append((st, "whoosh"))
        if sh.name == "hook":
            c.append((st + sh.m(1), "boing"))
        if sh.name == "cctv":
            c.append((st + sh.at(0, "축의금"), "pop"))
            c.append((st + sh.at(0, "식권"), "ding"))
        if sh.name == "envelope":
            c.append((st + sh.at(0, "오만"), "pop"))
            c.append((st + sh.at(0, "십일만"), "pop"))
            c.append((st + sh.at(1, "이십이만"), "stamp"))
        if sh.name == "spy":
            c.append((st + sh.at(0, "암행투어"), "stamp"))
            for w in ("주차", "로비", "밥"):
                c.append((st + sh.at(1, w), "tick"))
        if sh.name == "bill":
            c.append((st + sh.at(0, "대관료"), "fall"))
            c.append((st + sh.at(0, "식대"), "fall"))
        if sh.name == "photo":
            c.append((st + sh.at(0, "이 사람"), "boing"))
            c.append((st + sh.at(1, "지우는"), "stamp"))
            c.append((st + sh.at(1, "식권"), "stamp"))
        if sh.name == "rules":
            c.append((st + sh.at(0, "확인되지"), "stamp"))
            for w in ("사진", "신부대기실", "식권"):
                c.append((st + sh.at(1, w), "snap"))
    return c


# ---------------------------------------------------------------- 소품
def hall_bg(ctx):
    S.sky(ctx, "#F8D9DF", "#FCEFE6")
    for i in range(7):  # 꽃 장식 아치
        a = math.pi * (0.1 + 0.8 * i / 6)
        x, y = 540 - math.cos(a) * 470, 760 - math.sin(a) * 520
        for dx, dy in ((-18, 0), (18, 0), (0, -18), (0, 18)):
            ellipse(ctx, x + dx, y + dy, 22, 22)
            set_rgb(ctx, ("#F7A8B8", "#FFFFFF")[i % 2])
            ctx.fill()


def veil(ctx, x, y, s, t):
    """신부 머리 뒤로 늘어진 면사포 + 작은 티아라 (Doodle 머리 위치 기준)."""
    hy = y - 540 * s
    ctx.new_path()
    ctx.move_to(x - 120 * s, hy - 110 * s)
    ctx.curve_to(x - 260 * s, hy + 80 * s, x - 240 * s, hy + 420 * s, x - 200 * s + math.sin(t * 2) * 8, hy + 560 * s)
    ctx.line_to(x + 200 * s + math.sin(t * 2 + 1) * 8, hy + 560 * s)
    ctx.curve_to(x + 240 * s, hy + 420 * s, x + 260 * s, hy + 80 * s, x + 120 * s, hy - 110 * s)
    ctx.close_path()
    set_rgb(ctx, "#FFFFFF", 0.55)
    ctx.fill_preserve()
    set_rgb(ctx, S.OUT, 0.5)
    ctx.set_line_width(5 * s)
    ctx.stroke()


def tiara(ctx, x, y, s):
    hy = y - 540 * s
    for i in range(5):
        ellipse(ctx, x + (i - 2) * 34 * s, hy - 135 * s - (12 if i == 2 else 0) * s, 12 * s, 12 * s)
        S.fs(ctx, "#F2CE5C", lw=4 * s)


def bride(ctx, x, y, s, lt, ep, sh, expr, spk_on=True, pose="down"):
    veil(ctx, x, y, s, lt)
    m = ep.mouth("B", sh.start + lt) * 1.3 if (ep and spk_on) else 0
    BRIDE.draw(ctx, x, y, s, 1, pose=pose, expr=expr, mouth=m, t=lt, bob=False)
    tiara(ctx, x, y, s)


def guestbook(ctx, x, y, s, k, highlight=0.0):
    if k <= 0.01:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(-0.08)
    ctx.scale(s * k, s * k)
    rrect(ctx, -200, -150, 400, 300, 16)
    S.fs(ctx, "#FBF7EC", lw=8)
    draw_text(ctx, "방명록", 0, -100, 46, font="black", fill="#8C6A4A")
    for j, name in enumerate(("김○○", "이○○", "??? ???")):
        y = -20 + j * 60
        if j == 2 and highlight > 0:
            rrect(ctx, -160, y - 26, 320, 52, 12)
            set_rgb(ctx, "#F7A8A0", 0.6 * highlight)
            ctx.fill()
        draw_text(ctx, name, 0, y, 42, font="jua", fill="#2E3A4A")
    ctx.restore()


# ---------------------------------------------------------------- 샷 그리기
def _hook_frame(ctx, lt, sh, ep, frozen=False):
    hall_bg(ctx)
    q = (not frozen) and lt >= sh.m(1)
    bride(ctx, 540, 2260, 2.45, 0.0 if frozen else lt, None if frozen else ep, sh,
          expr="shock" if q else "neutral", spk_on=q)
    kb = 1.0 if q else 0.0
    if q:
        kb = ease_out_back(prog(lt, sh.m(1) - 0.2, sh.m(1) + 0.15), 1.8)
    guestbook(ctx, 790, 1180, 1.0, kb, highlight=kb)
    for j, ln in enumerate(HOOK):  # 첫 프레임부터 떠 있는 훅 문장
        draw_text(ctx, ln, 540, 250 + j * 120, 92 if j == 0 else 100, font="black",
                  fill="#FFFFFF" if j == 0 else "#FFE38A", stroke=14, stroke_fill="#2E2A28")


def shot_hook(ctx, lt, sh, ep):
    _hook_frame(ctx, lt, sh, ep)


def shot_loop(ctx, lt, sh, ep):
    _hook_frame(ctx, 0.0, ep.shots[0], ep, frozen=True)


def shot_cctv(ctx, lt, sh, ep):
    S.sky(ctx, "#C9CCD2", "#E2E4E8")
    rrect(ctx, 120, 1000, 520, 120, 10)  # 접수대
    S.fs(ctx, "#B9B2A0", lw=8)
    draw_text(ctx, "축의금 접수", 380, 1060, 46, font="black", fill="#4A4A4A")
    tw = sh.at(0, "모르는")
    k = ease_out_cubic(prog(lt, 0.0, tw + 0.4))
    for P, dx in ((SPY_M, 0), (SPY_F, 150)):
        P.draw(ctx, 1100 - 420 * k + dx, 1300, 0.8, -1, pose="down", expr="neutral", t=lt, bob=k < 1)
    te = sh.at(0, "축의금")
    ke = prog(lt, te, te + 0.4)
    if ke > 0:  # 봉투가 접수대로
        x = 680 - 200 * ke
        rrect(ctx, x - 50, 960 - 30, 100, 60, 8)
        S.fs(ctx, "#FBF7EC", lw=5)
    tt = sh.at(0, "식권")
    kt = prog(lt, tt, tt + 0.5)
    for j in range(2):  # 식권 두 장이 커플 쪽으로
        if kt > 0:
            x = 400 + 300 * kt + j * 40
            rrect(ctx, x - 45, 900 - j * 50 - 60 * kt, 90, 50, 6)
            S.fs(ctx, "#FFE38A", lw=5)
            draw_text(ctx, "식권", x, 925 - j * 50 - 60 * kt, 26, font="black", fill="#2E3A4A")
    # 흑백 CCTV 느낌: 회색 덮개 + 테두리 + REC
    ctx.rectangle(0, 0, W, H)
    set_rgb(ctx, "#6A7078", 0.28)
    ctx.fill()
    for i in range(0, H, 8):
        ctx.rectangle(0, i, W, 2)
    set_rgb(ctx, "#000000", 0.06)
    ctx.fill()
    rrect(ctx, 50, 230, W - 100, 1140, 20)
    set_rgb(ctx, "#2E2E33")
    ctx.set_line_width(14)
    ctx.stroke()
    if int(lt * 2) % 2 == 0:
        ellipse(ctx, 120, 300, 18, 18)
        set_rgb(ctx, "#D9473B")
        ctx.fill()
    draw_text(ctx, "REC  CAM 02", 260, 300, 40, font="black", fill="#F2F2F2")


def shot_envelope(ctx, lt, sh, ep):
    S.planks(ctx, base="#C9B79C", dark="#B5A386", w=150)
    GROOM.draw(ctx, 250, 1450, 1.15, 1, pose="shrug" if lt >= sh.at(0, "십일만") else "down",
               expr="shock" if lt >= sh.at(0, "십일만") else "neutral",
               mouth=ep.mouth("G", sh.start + lt) * 1.3, t=lt)
    t5 = sh.at(0, "오만")
    k5 = ease_out_back(prog(lt, t5, t5 + 0.35), 1.8)
    if k5 > 0.01:
        card(ctx, 700, 500, 520, 280, k5, rot=-0.03)
        draw_text(ctx, "축의금", 0, -70, 46, font="black", fill="#7A8594")
        draw_text(ctx, "5만 원", 0, 30, 96, font="black", fill="#4F7A9C")
        ctx.restore()
    t11 = sh.at(0, "십일만")
    k11 = ease_out_back(prog(lt, t11, t11 + 0.35), 1.8)
    if k11 > 0.01:
        card(ctx, 700, 870, 520, 300, k11, rot=0.03)
        draw_text(ctx, "식권 2장", 0, -80, 46, font="black", fill="#7A8594")
        draw_text(ctx, "11만 원 × 2", 0, 25, 80, font="black", fill=S.RUST)
        ctx.restore()
    t22 = sh.at(1, "이십이만")
    S.stamp(ctx, 700, 1180, "22만 원어치", prog(lt, t22, t22 + 0.45), size=88, rot=-0.08)


def shot_spy(ctx, lt, sh, ep):
    S.planks(ctx, base="#E9DCC6", dark="#D9C9AE", w=150)
    rrect(ctx, 80, 300, 920, 120, 20)  # 웨딩홀 간판
    S.fs(ctx, "#FBF7EC", lw=8)
    draw_text(ctx, "○○ 웨딩홀 로비", 540, 362, 54, font="black", fill="#8C6A4A")
    sway = math.sin(lt * 3) * 30  # 두리번
    SPY_M.draw(ctx, 330 + sway, 1440, 1.0, 1, pose="point", expr="smug",
               mouth=ep.mouth("Y", sh.start + lt) * 1.3, t=lt)
    SPY_F.draw(ctx, 620 - sway, 1440, 0.9, -1, pose="hips", expr="smug", t=lt + 1)
    ta = sh.at(0, "암행투어")
    S.stamp(ctx, 540, 560, "암행투어", prog(lt, ta, ta + 0.45), size=110, rot=-0.06)
    if lt >= sh.m(1):  # 체크리스트
        card(ctx, 790, 820, 300, 360, ease_out_back(prog(lt, sh.m(1), sh.m(1) + 0.3), 1.6), rot=0.06)
        draw_text(ctx, "체크리스트", 0, -130, 40, font="black", fill="#2E3A4A")
        for j, w in enumerate(("주차", "로비", "밥")):
            y = -50 + j * 80
            draw_text(ctx, w if w != "밥" else "밥맛", -40, y, 44, font="black", fill="#2E3A4A")
            if lt >= sh.at(1, w):
                ctx.move_to(60, y)
                ctx.line_to(80, y + 22)
                ctx.line_to(115, y - 25)
                set_rgb(ctx, S.RUST)
                ctx.set_line_width(10)
                ctx.stroke()
        ctx.restore()


def shot_bill(ctx, lt, sh, ep):
    S.desk(ctx)
    ta, ts = sh.at(0, "대관료"), sh.at(0, "식대")
    k = ease_out_cubic(prog(lt, ta - 0.2, ts + 0.8))
    h = 420 + 700 * k  # 영수증이 쭉 늘어남
    rrect(ctx, 290, 240, 500, h, 10)
    S.fs(ctx, "#FBFAF6", lw=7)
    draw_text(ctx, "예식 견적서", 540, 310, 54, font="black", fill="#2E3A4A")
    rows = (("대관료", ta), ("식대", ts), ("꽃장식", ts + 0.3), ("음향·조명", ts + 0.5))
    for j, (name, t0) in enumerate(rows):
        if lt >= t0:
            y = 420 + j * 120
            draw_text(ctx, name, 420, y, 48, font="black", fill="#2E3A4A")
            draw_text(ctx, "↑↑", 680, y, 54, font="black", fill=S.RUST)
    kt = ease_out_back(prog(lt, sh.me(0) - 0.6, sh.me(0) - 0.2), 1.8)
    if kt > 0.01:
        label(ctx, "계약 전에 직접 확인?", 540, 1180, kt, fill="#FFE38A", size=60)


def shot_photo(ctx, lt, sh, ep):
    hall_bg(ctx)
    bride(ctx, 260, 1480, 1.05, lt, ep, sh, expr="shock" if lt >= sh.at(0, "이 사람") else "neutral")
    k = ease_out_back(prog(lt, 0.05, 0.4), 1.4)
    card(ctx, 690, 700, 520, 620, k, rot=0.04)
    rrect(ctx, -220, -260, 440, 380, 10)  # 사진
    S.fs(ctx, "#DCE6F2", lw=6)
    BRIDE.draw(ctx, -60, 110, 0.38, 1, pose="down", expr="smug", t=0, bob=False)
    GROOM.draw(ctx, 60, 110, 0.38, -1, pose="down", expr="smug", t=0, bob=False)
    SPY_M.draw(ctx, 170, 80, 0.26, -1, pose="down", expr="neutral", t=0, bob=False)  # 뒤에 낀 모르는 사람
    if lt >= sh.at(0, "이 사람"):
        ellipse(ctx, 170, -60, 70, 70)
        set_rgb(ctx, S.RUST)
        ctx.set_line_width(10)
        ctx.stroke()
        draw_text(ctx, "??", 170, -170, 56, font="black", fill=S.RUST)
    draw_text(ctx, "본식 사진", 0, 210, 46, font="black", fill="#2E3A4A")
    ctx.restore()
    td, tf = sh.at(1, "지우는"), sh.at(1, "식권")
    S.stamp(ctx, 690, 1130, "삭제 비용 발생", prog(lt, td, td + 0.4), size=62, rot=-0.06)
    S.stamp(ctx, 690, 1260 - 30, "식권 없이 식사 적발", prog(lt, tf, tf + 0.4), size=50, rot=0.05)


def shot_rules(ctx, lt, sh, ep):
    S.planks(ctx, base=S.SLATE, dark=S.SLATE_D, seed=4)
    tq = sh.at(0, "확인되지")
    S.stamp(ctx, 540, 360, "정체: 확인 안 됨", prog(lt, tq, tq + 0.45), size=80, rot=-0.05)
    if lt >= sh.m(1):
        k = ease_out_back(prog(lt, sh.m(1), sh.m(1) + 0.35), 1.5)
        card(ctx, 520, 820, 760, 620, k, fill="#FFF7C9", rot=-0.02)
        draw_text(ctx, "암행투어 에티켓", 0, -220, 58, font="black", fill="#2E3A4A")
        for j, (txt, w) in enumerate((("사진 찍지 말기", "사진"), ("신부대기실 가지 말기", "신부대기실"),
                                      ("식권 없이 밥 먹지 말기", "식권"))):
            y = -90 + j * 120
            draw_text(ctx, txt, 40, y, 50, font="black", fill="#2E3A4A")
            if lt >= sh.at(1, w):
                for a in (1, -1):
                    ctx.move_to(-300, y - 25 * a)
                    ctx.line_to(-250, y + 25 * a)
                set_rgb(ctx, S.RUST)
                ctx.set_line_width(10)
                ctx.stroke()
        ctx.restore()


SHOT_FN = {k[5:]: v for k, v in globals().items() if k.startswith("shot_")}
CAMERA = {
    "hook": (540, 900, 0.0), "loop": (540, 900, 0.0), "cctv": (540, 800, 0.04), "envelope": (600, 800, 0.05),
    "spy": (540, 900, 0.05), "bill": (540, 700, 0.04), "photo": (600, 800, 0.05), "rules": (520, 700, 0.03),
}

EP = Explainer(SCRIPT, VOICE, CAP_COLOR, SHOT_FN, CAMERA, cues,
               notice="※ 상황극(보도 재구성) / 언론 보도 기반", chapters=CHAPTERS, overlay_delay=2.0)
render_frame, mix = EP.render_frame, EP.mix


def prepare():
    global DURATION
    DURATION = EP.prepare().duration
