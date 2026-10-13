"""오늘의 만평 #11 — 요즘 중국·일본이 한국 쟁탈전 하는 이유  (나라 의인화 상황극)

실제 사실 (보도 기준):
- 2026.1.5 베이징 한중 정상회담(약 90분) → 1.13 일본 총리 고향 나라현에서 한일 정상회담 (정책브리핑·이코노미데일리)
  일본 언론: "중국 분열 공세 차단" 취지 평가 (에포크타임스 인용)
- 발단: 2025.11 일본 총리 국회 발언(대만 유사시 일본 개입 가능성 취지) → 중국 철회 요구, 일본 거부
- 중국: 11.14 일본 여행 자제 권고, 일본 해산물 수입 중단 (파이낸셜뉴스·여행신문)
- 올 상반기 방일 중국인 56.4% 감소, 일본 측 "우리 인기 여전" (헤럴드경제)
- 4월 방한 중국인 약 57만 4천 명, 국가별 1위 (한국관광공사 집계 보도)
- 2026.5.19 두 정상 안동 하회마을 선유줄불놀이 관람 (YTN)
- 미국 대통령의 대화 권유를 중국 주석이 거절, 11월 선전 APEC 중일 정상회담 불투명 (경향신문·뉴스핌)
- 반사이익 vs 반중 여론·중국 의존도 위험 지적 (코리아포스트)
나라를 반 친구로 의인화한 상황극이다. 정치인 실명은 쓰지 않고, 일본 총리 발언은 '취지'로만 전한다.
"""
import math

from .. import squire as S
from ..doodle import Doodle
from ..engine import H, W, draw_text, ease_out_back, ease_out_cubic, ellipse, prog, rrect, set_rgb
from ..explainer import Explainer, bubble, card, label

TITLE = "요즘 중국·일본이 한국 쟁탈전 하는 이유 | 오늘의 만평"
DURATION = 47.0

KOREA = Doodle(coat="#3F6FB5", hair="cap", hair_color="#2A2420")
CHINA = Doodle(coat="#C8382E", hair="tuft", hair_color="#2A2420", collar=False, pants="#3A3F4A")
JAPAN = Doodle(coat="#F2EEE6", tie="#C8382E", hair="bob", hair_color="#2A2420", pants="#2F3440")

VOICE = {
    "N": ("male", "+80%", "+20Hz", 1.18),
    "K": ("male2", "+75%", "+0Hz", 1.15),  # 한국이
    "C": ("male", "+70%", "+0Hz", 0.95),  # 중국이
    "J": ("female", "+75%", "+20Hz", 1.12),  # 일본이
}
CAP_COLOR = {"N": "#FFFFFF", "K": "#9FD3F0", "C": "#FFB3A8", "J": "#FFE38A"}
HOOK = ("요즘 중국·일본이", "한국 쟁탈전 하는 이유")

SCRIPT = [
    ("hook", [("N", "요즘 중국이랑 일본이, 한국 쟁탈전 하는 이유.", None),
              ("K", "아 둘 다 좀 놔 봐!", None)], {"tail": 0.25}),
    ("invite", [("C", "한국아, 우리 집 먼저 와! 밥 살게!", None),
                ("J", "아니지, 우리 집 먼저 와야지!", None)], {"tail": 0.3}),
    ("summit", [("N", "올해 일월, 우리 대통령이 베이징에서 정상회담을 하자,", "올해 1월, 우리 대통령이 베이징에서 정상회담을 하자,"),
                ("N", "딱 팔 일 뒤 일본 총리는 자기 고향 나라현으로 불렀어.", "딱 8일 뒤 일본 총리는 자기 고향 나라현으로 불렀어.")],
     {"tail": 0.35}),
    ("remark", [("N", "둘이 틀어진 건 작년 십일월. 일본 총리가 대만에 무슨 일 나면 일본도 나설 수 있다는 취지로 말했거든.",
                 "둘이 틀어진 건 작년 11월. 일본 총리가 대만에 무슨 일 나면 일본도 나설 수 있다는 취지로 말했거든.")],
     {"tail": 0.3}),
    ("clash", [("C", "그 말 취소해!", None),
               ("J", "못 해!", None)], {"tail": 0.3}),
    ("ban", [("N", "중국은 일본 여행 자제령을 내리고, 일본 해산물 수입까지 막았어.", None),
             ("N", "올 상반기 일본 간 중국인은 오십육 점 사 퍼센트 줄었대.", "올 상반기 일본 간 중국인은 56.4% 줄었대.")],
     {"tail": 0.35}),
    ("tourists", [("N", "그 관광객들이 어디로 갔냐면… 한국. 사월 한국 찾은 외국인 일 위가 중국인, 오십칠만 명이야.",
                   "그 관광객들이 어디로 갔냐면… 한국. 4월 한국 찾은 외국인 1위가 중국인, 57만 명이야."),
                  ("J", "흥, 우리 인기는 여전하거든?", None)], {"tail": 0.3}),
    ("fireworks", [("J", "한국아, 불꽃놀이 보러 갈래?", None),
                   ("N", "오월엔 일본 총리가 안동까지 와서 하회마을 불꽃놀이를 같이 봤어.",
                    "5월엔 일본 총리가 안동까지 와서 하회마을 불꽃놀이를 같이 봤어."),
                   ("N", "일본 언론은 한일 회담이 중국의 갈라치기를 막았다고 평가했고.", None)], {"tail": 0.3}),
    ("freeze", [("N", "근데 정작 둘 사이는 아직 꽁꽁 얼어 있어.", None),
                ("N", "미국 대통령이 일본이랑 대화해 보라고 권했는데도, 중국 주석이 거절했대.", None),
                ("N", "그래서 십일월 중국 선전 에이펙에서 중일 정상회담도 불투명해.",
                 "그래서 11월 중국 선전 APEC에서 중일 정상회담도 불투명해.")], {"tail": 0.3}),
    ("us", [("N", "우리한텐 관광객이 느는 기회지만, 한쪽만 편들면 다른 쪽 보복이 올 수도 있어.", None),
            ("N", "너라면, 중국이랑 일본 중에 누구 손 잡을래?", None)], {"tail": 0.2}),
    ("loop", [], {"tail": 0, "min_tail": 0.45, "cut": True}),
]

CHAPTERS = [("쟁탈전", "hook"), ("이유", "remark"), ("반응", "tourists"), ("결론", "freeze")]


def cues(ep):
    c = [(st + 0.05, "stamp") for st in ep.chapter_starts()[1:-1]]
    for i, sh in enumerate(ep.shots):
        st = sh.start
        if i > 0 and sh.name != "loop":
            c.append((st, "whoosh"))
        if sh.name == "hook":
            c.append((st + sh.m(1), "boing"))
        if sh.name == "invite":
            c.append((st + sh.m(0), "pop"))
            c.append((st + sh.m(1), "pop"))
        if sh.name == "summit":
            c.append((st + sh.at(0, "베이징"), "ding"))
            c.append((st + sh.at(1, "팔 일"), "ding"))
            c.append((st + sh.at(1, "나라현"), "stamp"))
        if sh.name == "remark":
            c.append((st + sh.at(0, "대만"), "pop"))
            c.append((st + sh.at(0, "취지"), "tick"))
        if sh.name == "clash":
            c.append((st + sh.m(0), "boing"))
            c.append((st + sh.m(1), "stamp"))
        if sh.name == "ban":
            c.append((st + sh.at(0, "여행"), "stamp"))
            c.append((st + sh.at(0, "해산물"), "stamp"))
            c.append((st + sh.at(1, "오십육"), "fall"))
        if sh.name == "tourists":
            c.append((st + sh.at(0, "한국."), "ding"))
            c.append((st + sh.at(0, "오십칠만"), "stamp"))
            c.append((st + sh.m(1), "boing"))
        if sh.name == "fireworks":
            c.append((st + sh.at(1, "불꽃놀이"), "pop"))
            c.append((st + sh.at(2, "갈라치기"), "stamp"))
        if sh.name == "freeze":
            c.append((st + sh.at(0, "꽁꽁"), "snap"))
            c.append((st + sh.at(1, "거절"), "stamp"))
            c.append((st + sh.at(2, "불투명"), "stamp"))
        if sh.name == "us":
            c.append((st + sh.at(0, "기회"), "ding"))
            c.append((st + sh.at(0, "보복"), "fall"))
            c.append((st + sh.m(1), "pop"))
    return c


# ---------------------------------------------------------------- 소품
def classroom(ctx):
    S.planks(ctx, base="#E9DCC6", dark="#D9C9AE", w=150)
    rrect(ctx, 90, 250, 900, 330, 18)  # 칠판
    S.fs(ctx, "#3E5A4A", lw=10)
    rrect(ctx, 70, 560, 940, 34, 10)
    S.fs(ctx, "#8C5D3D", lw=6)


def name_tag(ctx, text, x, y, k=1.0, fill="#F3EBD5"):
    label(ctx, text, x, y, k, fill=fill, size=44)


def kid(ctx, P, spk, x, y, s, facing, lt, sh, ep, pose="down", expr="neutral", bob=True, tag=None, tag_fill="#F3EBD5"):
    m = ep.mouth(spk, sh.start + lt) * 1.3 if ep else 0
    P.draw(ctx, x, y, s, facing, pose=pose, expr=expr, mouth=m, t=lt + x * 0.01, bob=bob)
    if tag:
        name_tag(ctx, tag, x, y - 760 * s, 1.0, fill=tag_fill)


def bolt(ctx, x, y, s, t):
    ctx.save()
    ctx.translate(x, y + math.sin(t * 30) * 6)
    ctx.scale(s, s)
    ctx.new_path()
    for px, py in ((-20, -110), (30, -110), (5, -20), (45, -20), (-30, 120), (-5, 20), (-45, 20)):
        ctx.line_to(px, py)
    ctx.close_path()
    S.fs(ctx, "#FFD93D", lw=7)
    ctx.restore()


def suitcase(ctx, x, y, s, color):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rrect(ctx, -20, -70, 40, 24, 8)
    S.fs(ctx, "#2E2A28", lw=5)
    rrect(ctx, -55, -52, 110, 90, 14)
    S.fs(ctx, color, lw=6)
    ctx.restore()


# ---------------------------------------------------------------- 샷 그리기
def _hook_frame(ctx, lt, sh, ep, frozen=False):
    S.sky(ctx, "#DCE8F5", "#F6F0E4")
    t = 0.0 if frozen else lt
    yell = (not frozen) and lt >= sh.m(1)
    tug = math.sin(t * 7) * 18
    # 양쪽에서 팔을 잡아당기는 중국이·일본이 (화면 가장자리)
    CHINA.draw(ctx, 30 + tug, 2050, 1.55, 1, pose="pull", expr="angry", t=t, bob=False)
    JAPAN.draw(ctx, 1050 + tug, 2050, 1.55, -1, pose="pull", expr="angry", t=t + 1, bob=False)
    m = ep.mouth("K", sh.start + lt) * 1.3 if (ep and yell) else 0
    KOREA.draw(ctx, 540 + tug * 0.5, 2280, 2.4, 1, pose="flail" if yell else "shrug",
               expr="angry" if yell else "shock", mouth=m, t=t, bob=False, sweat=True)
    name_tag(ctx, "중국이", 170, 590, fill="#FFB3A8")
    name_tag(ctx, "일본이", 860, 470, fill="#FFF0B3")
    for j, ln in enumerate(HOOK):  # 첫 프레임부터 떠 있는 훅 문장
        draw_text(ctx, ln, 540, 250 + j * 120, 92 if j == 0 else 100, font="black",
                  fill="#FFFFFF" if j == 0 else "#FFE38A", stroke=14, stroke_fill="#2E2A28")


def shot_hook(ctx, lt, sh, ep):
    _hook_frame(ctx, lt, sh, ep)


def shot_loop(ctx, lt, sh, ep):
    _hook_frame(ctx, 0.0, ep.shots[0], ep, frozen=True)


def shot_invite(ctx, lt, sh, ep):
    classroom(ctx)
    j_on = lt >= sh.m(1)
    kid(ctx, KOREA, "K", 540, 1420, 0.85, 1, lt, sh, None, pose="shrug", expr="shock", tag="한국이", tag_fill="#BFE0F5")
    kid(ctx, CHINA, "C", 220, 1500, 1.05, 1, lt, sh, ep, pose="wave" if not j_on else "hips",
        expr="smug" if not j_on else "angry", tag="중국이", tag_fill="#FFB3A8")
    kid(ctx, JAPAN, "J", 820, 1500, 1.05, -1, lt, sh, ep, pose="wave" if j_on else "down",
        expr="smug" if j_on else "neutral", tag="일본이", tag_fill="#FFF0B3")
    bubble(ctx, "밥 살게!", 300, 420, ease_out_back(prog(lt, sh.m(0), sh.m(0) + 0.3), 1.6), size=64, tail=1)
    bubble(ctx, "우리 집 먼저!", 720, 420, ease_out_back(prog(lt, sh.m(1), sh.m(1) + 0.3), 1.6), size=60, tail=-1)


def shot_summit(ctx, lt, sh, ep):
    S.planks(ctx, base="#F0E4CC", dark="#E2D3B6", w=150)
    tb = sh.at(0, "베이징")
    kb = ease_out_back(prog(lt, tb - 0.15, tb + 0.25), 1.6)
    if kb > 0.01:
        card(ctx, 540, 450, 760, 300, kb, fill="#FFE1DC", rot=-0.03)
        draw_text(ctx, "1월 5일", 0, -75, 64, font="black", fill=S.RUST)
        draw_text(ctx, "베이징 한중 정상회담", 0, 30, 58, font="black", fill="#2E3A4A")
        ctx.restore()
    t8 = sh.at(1, "팔 일")
    k8 = ease_out_back(prog(lt, t8 - 0.1, t8 + 0.3), 1.6)
    if k8 > 0.01:
        card(ctx, 540, 790, 760, 300, k8, fill="#FFF7C9", rot=0.03)
        draw_text(ctx, "8일 뒤 · 1월 13일", 0, -75, 60, font="black", fill=S.RUST)
        draw_text(ctx, "나라현 한일 정상회담", 0, 30, 58, font="black", fill="#2E3A4A")
        ctx.restore()
    tn = sh.at(1, "나라현")
    S.stamp(ctx, 540, 1010, "일본 총리 고향", prog(lt, tn, tn + 0.45), size=70, rot=-0.06)


def shot_remark(ctx, lt, sh, ep):
    S.planks(ctx, base=S.SLATE, dark=S.SLATE_D, seed=2)
    rrect(ctx, 300, 1180, 480, 300, 16)  # 연단
    S.fs(ctx, "#8C5D3D", lw=8)
    talking = lt >= sh.at(0, "일본 총리")
    JAPAN.draw(ctx, 540, 1250, 1.05, 1, pose="point" if talking else "down", expr="smug" if talking else "neutral",
               t=lt, bob=False)
    draw_text(ctx, "작년 11월 · 국회", 540, 1330, 46, font="black", fill="#F3EBD5")
    ta = sh.at(0, "대만")
    ka = ease_out_back(prog(lt, ta - 0.1, ta + 0.3), 1.6)
    if ka > 0.01:
        card(ctx, 540, 400, 820, 260, ka, rot=-0.02)
        draw_text(ctx, "대만에 무슨 일 나면", 0, -50, 60, font="black", fill="#2E3A4A")
        draw_text(ctx, "일본도 나설 수 있다", 0, 45, 64, font="black", fill=S.RUST)
        ctx.restore()
    tc = sh.at(0, "취지")
    label(ctx, "(발언 취지)", 760, 590, ease_out_back(prog(lt, tc, tc + 0.3), 1.6), fill="#FFF7C9", size=42)


def shot_clash(ctx, lt, sh, ep):
    S.planks(ctx, base="#3A3F52", dark="#30354A", seed=5)
    j_on = lt >= sh.m(1)
    kid(ctx, CHINA, "C", 270, 1500, 1.2, 1, lt, sh, ep, pose="point", expr="angry", tag="중국이", tag_fill="#FFB3A8")
    kid(ctx, JAPAN, "J", 790, 1500, 1.2, -1, lt, sh, ep, pose="hips" if not j_on else "point",
        expr="smug" if not j_on else "angry", tag="일본이", tag_fill="#FFF0B3")
    bolt(ctx, 540, 820, 1.4, lt)
    bubble(ctx, "취소해!", 300, 330, ease_out_back(prog(lt, sh.m(0), sh.m(0) + 0.3), 1.6), size=70, tail=1)
    bubble(ctx, "못 해!", 780, 330, ease_out_back(prog(lt, sh.m(1), sh.m(1) + 0.3), 1.6), size=70, tail=-1)


def shot_ban(ctx, lt, sh, ep):
    S.planks(ctx, base="#F3E3D3", dark="#E6D2BE", w=150)
    CHINA.draw(ctx, 250, 1480, 1.05, 1, pose="point", expr="angry", t=lt)
    tt, ts = sh.at(0, "여행"), sh.at(0, "해산물")
    S.stamp(ctx, 640, 420, "일본 여행 자제령", prog(lt, tt, tt + 0.45), size=68, rot=-0.05)
    S.stamp(ctx, 640, 600, "해산물 수입 중단", prog(lt, ts, ts + 0.45), size=68, rot=0.04)
    t5 = sh.at(1, "오십육")
    k5 = ease_out_back(prog(lt, t5 - 0.1, t5 + 0.3), 1.8)
    if k5 > 0.01:
        card(ctx, 640, 960, 520, 360, k5, fill="#FBF7EC", rot=0.02)
        draw_text(ctx, "올 상반기 일본 간 중국인", 0, -110, 36, font="black", fill="#7A8594")
        draw_text(ctx, "-56.4%", 0, 20, 120, font="black", fill=S.RUST)
        ctx.restore()


def shot_tourists(ctx, lt, sh, ep):
    S.sky(ctx, "#CFE3F2", "#F2EEE4")
    rrect(ctx, 80, 1180, 920, 40, 12)  # 바닥선
    S.fs(ctx, "#B9B2A0", lw=6)
    tk = sh.at(0, "한국.")
    k = ease_out_cubic(prog(lt, 0.2, tk + 0.3))
    for j in range(6):  # 캐리어 줄줄이 한국 쪽으로
        x = -150 + j * 120 + 450 * k
        suitcase(ctx, x, 1150 - (j % 2) * 30, 1.0, ("#C8382E", "#E8B93E", "#5BA37A")[j % 3])
    kid(ctx, KOREA, "K", 800, 1180, 0.9, -1, lt, sh, None, pose="cheer" if lt >= tk else "down",
        expr="smug" if lt >= tk else "neutral", tag="한국이", tag_fill="#BFE0F5")
    t57 = sh.at(0, "오십칠만")
    k57 = ease_out_back(prog(lt, t57 - 0.1, t57 + 0.3), 1.8)
    if k57 > 0.01:
        card(ctx, 390, 470, 580, 340, k57, rot=-0.02)
        draw_text(ctx, "4월 방한 외국인 1위", 0, -95, 42, font="black", fill="#7A8594")
        draw_text(ctx, "중국인 57만 명", 0, 25, 70, font="black", fill=S.RUST)
        ctx.restore()
    if lt >= sh.m(1):  # 일본이 툭 끼어듦
        kj = ease_out_back(prog(lt, sh.m(1) - 0.1, sh.m(1) + 0.3), 1.4)
        JAPAN.draw(ctx, 260, 1500 + 500 * (1 - kj), 1.0, 1, pose="hips", expr="smug",
                   mouth=ep.mouth("J", sh.start + lt) * 1.3, t=lt)
        bubble(ctx, "인기 여전하거든?", 400, 820, kj, size=54, tail=-1)


def shot_fireworks(ctx, lt, sh, ep):
    S.sky(ctx, "#1E2340", "#3A3458")
    ctx.rectangle(0, 1200, W, 300)  # 강
    set_rgb(ctx, "#27304F")
    ctx.fill()
    tf = sh.at(1, "불꽃놀이")
    if lt >= tf - 0.3:  # 줄불: 줄에 매달린 불꽃이 비처럼 떨어짐
        ctx.move_to(0, 300)
        ctx.curve_to(300, 380, 700, 380, W, 300)
        set_rgb(ctx, "#8C7A5A")
        ctx.set_line_width(4)
        ctx.stroke()
        for i in range(26):
            x = 40 + i * 40
            ph = (lt * 1.3 + i * 0.37) % 1.0
            y = 360 + ph * 760
            ellipse(ctx, x, y, 7, 7)
            set_rgb(ctx, "#FFC24A", 1 - ph * 0.7)
            ctx.fill()
    KOREA.draw(ctx, 380, 1520, 0.95, 1, pose="down", expr="smug" if lt >= tf else "neutral", t=lt)
    JAPAN.draw(ctx, 700, 1520, 0.95, -1, pose="wave" if lt < sh.m(1) else "down", expr="smug",
               mouth=ep.mouth("J", sh.start + lt) * 1.3, t=lt + 1)
    label(ctx, "5월 · 안동 하회마을", 540, 300, ease_out_back(prog(lt, tf - 0.2, tf + 0.2), 1.6), fill="#FFF7C9", size=52)
    tg = sh.at(2, "갈라치기")
    kg = ease_out_back(prog(lt, sh.m(2), sh.m(2) + 0.3), 1.6)
    if kg > 0.01:
        card(ctx, 540, 640, 720, 240, kg, rot=0.02)
        draw_text(ctx, "일본 언론", 0, -60, 42, font="black", fill="#7A8594")
        draw_text(ctx, "“중국 분열 공세 차단”", 0, 30, 54, font="black", fill="#2E3A4A")
        ctx.restore()
    S.stamp(ctx, 540, 880, "갈라치기 차단?", prog(lt, tg, tg + 0.45), size=58, rot=-0.06)


def shot_freeze(ctx, lt, sh, ep):
    S.sky(ctx, "#BFD9EC", "#E6F1F8")
    tf = sh.at(0, "꽁꽁")
    fr = prog(lt, tf, tf + 0.5)
    CHINA.draw(ctx, 330, 1480, 1.05, -1, pose="hips", expr="angry", t=0 if fr >= 1 else lt, bob=fr < 1)
    JAPAN.draw(ctx, 750, 1480, 1.05, 1, pose="hips", expr="angry", t=0 if fr >= 1 else lt, bob=fr < 1)
    if fr > 0:  # 얼음 덩어리
        rrect(ctx, 130, 700, 820, 820, 60)
        set_rgb(ctx, "#DDF1FF", 0.45 * fr)
        ctx.fill_preserve()
        set_rgb(ctx, "#7FB6D9", fr)
        ctx.set_line_width(10)
        ctx.stroke()
    tr = sh.at(1, "거절")
    kr = ease_out_back(prog(lt, sh.m(1), sh.m(1) + 0.3), 1.6)
    if kr > 0.01:
        card(ctx, 540, 420, 780, 260, kr, rot=-0.02)
        draw_text(ctx, "미국: “대화해 봐”", 0, -50, 56, font="black", fill="#2E3A4A")
        if lt >= tr:
            draw_text(ctx, "중국: 거절", 0, 50, 64, font="black", fill=S.RUST)
        ctx.restore()
    tb = sh.at(2, "불투명")
    if lt >= sh.m(2):
        label(ctx, "11월 선전 APEC 중일 회담", 540, 640, ease_out_back(prog(lt, sh.m(2), sh.m(2) + 0.3), 1.6),
              fill="#FFF7C9", size=46)
    S.stamp(ctx, 540, 1100, "불투명", prog(lt, tb, tb + 0.45), size=100, rot=-0.07)


def shot_us(ctx, lt, sh, ep):
    S.planks(ctx, base="#E9DCC6", dark="#D9C9AE", w=150)
    q = lt >= sh.m(1)
    CHINA.draw(ctx, 170, 1480, 0.95, 1, pose="pull", expr="smug", t=lt)
    JAPAN.draw(ctx, 910, 1480, 0.95, -1, pose="pull", expr="smug", t=lt + 1)
    KOREA.draw(ctx, 540, 1500, 1.1, 1, pose="shrug", expr="shock" if q else "neutral", t=lt, sweat=True)
    to, tr = sh.at(0, "기회"), sh.at(0, "보복")
    label(ctx, "관광객 ↑ 기회", 540, 380, ease_out_back(prog(lt, to - 0.1, to + 0.25), 1.6), fill="#D6F0D8", size=56)
    label(ctx, "한쪽 편들면 보복?", 540, 540, ease_out_back(prog(lt, tr - 0.1, tr + 0.25), 1.6), fill="#FFD6D0", size=56)
    if q:
        bubble(ctx, "누구 손 잡지?", 540, 700, ease_out_back(prog(lt, sh.m(1), sh.m(1) + 0.3), 1.6), size=60)


SHOT_FN = {k[5:]: v for k, v in globals().items() if k.startswith("shot_")}
CAMERA = {
    "hook": (540, 900, 0.0), "loop": (540, 900, 0.0), "invite": (540, 900, 0.04), "summit": (540, 760, 0.04),
    "remark": (540, 800, 0.05), "clash": (540, 900, 0.06), "ban": (560, 800, 0.04), "tourists": (540, 800, 0.04),
    "fireworks": (540, 800, 0.05), "freeze": (540, 800, 0.04), "us": (540, 900, 0.04),
}

EP = Explainer(SCRIPT, VOICE, CAP_COLOR, SHOT_FN, CAMERA, cues,
               notice="※ 나라를 의인화한 상황극 / 언론 보도 기반", chapters=CHAPTERS, overlay_delay=2.0)
render_frame, mix = EP.render_frame, EP.mix


def prepare():
    global DURATION
    DURATION = EP.prepare().duration
