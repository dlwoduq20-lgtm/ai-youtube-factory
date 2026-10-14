"""오늘의 만평 #12 — 12월부터 기름값 미친듯이 오른다는데?  (소문 훅 → 팩트체크)

실제 사실 (보도·정부 발표 기준):
- 2.27(중동 전쟁 직전) 휘발유 1,692.58원 → 4.21 전국 평균 2,003.81원 (+18.4%) (연합·네이트)
- 석유 최고가격제: 정유사가 주유소·대리점에 공급하는 가격 상한. 10차 휘발유 1,784원, 3연속 동결(9.19부터 4주),
  브렌트유 9.16 105.8달러 (머니투데이·SBS Biz)
- 유류세 휘발유 15% 인하(리터당 122원) 11.30까지 연장 (아주경제·파이낸셜뉴스)
- 21주 연속 하락, 10월 첫째 주 1,857.6원 (MTN)
- 정유사 손실 보전 예비비 4조 2천억 원 편성 (핀포인트뉴스)
- 제도 중단 시 가격 급등 우려 (헤럴드경제·뉴시스) — 확정 아님, 유류세 인하는 그동안 여러 번 연장됨
'미친듯이 오른다'는 소문으로만 던지고 영상 안에서 팩트체크한다. 개인 이름은 쓰지 않는다.
"""
import math

from .. import squire as S
from ..doodle import Doodle
from ..engine import H, W, draw_text, ease_out_back, ease_out_cubic, ellipse, prog, rrect, set_rgb
from ..explainer import Explainer, bubble, card, label

TITLE = "12월부터 기름값 미친듯이 오른다는데? | 오늘의 만평"
DURATION = 48.0

DRIVER = Doodle(coat="#5B8BC9", hair="cap", hair_color="#2A2420", collar=False)
OWNER = Doodle(coat="#E58A3A", hair="beanie", hair_color="#C9473B", collar=False, pants="#3A3F4A")
OFFICIAL = Doodle(coat="#2F3440", tie="#4F7A9C", hair="cap", hair_color="#2A2420", glasses=True, badge=True)
REFINER = Doodle(coat="#7F8C5C", hair="beanie", hair_color="#E8B93E", collar=False)

VOICE = {
    "N": ("male", "+80%", "+20Hz", 1.18),
    "D": ("male2", "+75%", "+0Hz", 1.15),  # 운전자
    "O": ("male", "+70%", "+0Hz", 0.98),  # 주유소 사장
    "G": ("female", "+75%", "+20Hz", 1.12),  # 공무원
    "R": ("male2", "+70%", "+0Hz", 0.95),  # 정유사 직원
}
CAP_COLOR = {"N": "#FFFFFF", "D": "#9FD3F0", "O": "#FFC48A", "G": "#FFE38A", "R": "#C9E3A8"}
HOOK = ("12월부터 기름값", "미친듯이 오른다는데?")

SCRIPT = [
    ("hook", [("D", "십이월부터 기름값 미친듯이 오른다는데?", "12월부터 기름값 미친듯이 오른다는데?"),
              ("O", "손님, 그거 반은 맞아요.", None)], {"tail": 0.25}),
    ("pump", [("D", "지금은 지난주보다 더 싼데?", None),
              ("O", "그게 다 눌러 놓은 가격이거든요.", None)], {"tail": 0.3}),
    ("war", [("N", "올해 이월 말, 중동 전쟁 직전 휘발유는 천육백구십이 원.", "올해 2월 말, 중동 전쟁 직전 휘발유는 1,692원."),
             ("N", "사월엔 전국 평균 이천삼 원. 두 달 새 십팔 점 사 퍼센트 뛰었어.",
              "4월엔 전국 평균 2,003원. 두 달 새 18.4% 뛰었어.")], {"tail": 0.3}),
    ("cap", [("N", "그러자 정부가 정유사 공급가에 상한선을 그었어. 석유 최고가격제야.", None),
             ("G", "휘발유, 리터당 천칠백팔십사 원 넘게 받지 마세요!", "휘발유, 리터당 1,784원 넘게 받지 마세요!"),
             ("N", "유류세도 십오 퍼센트 깎아서, 리터당 백이십이 원 내려 줬고.", "유류세도 15% 깎아서, 리터당 122원 내려 줬고.")],
     {"tail": 0.3}),
    ("drop", [("N", "덕분에 기름값은 이십일 주 연속 내려서, 지금 천팔백오십칠 원이야.",
               "덕분에 기름값은 21주 연속 내려서, 지금 1,857원이야.")], {"tail": 0.3}),
    ("twist", [("R", "근데 그 손해, 누가 메꿔 줘요?", None),
               ("N", "정부가 정유사 손실 보전용으로 잡아 둔 예비비만 사조 이천억 원. 결국 세금이야.",
                "정부가 정유사 손실 보전용으로 잡아 둔 예비비만 4조 2천억 원. 결국 세금이야."),
               ("N", "국제유가는 구월에 배럴당 백오 달러를 넘었는데, 정부는 최고가격을 세 번 연속 동결했어.",
                "국제유가는 9월에 배럴당 105달러를 넘었는데, 정부는 최고가격을 세 번 연속 동결했어.")], {"tail": 0.3}),
    ("dec", [("N", "그런데 유류세 인하는 십일월 삼십일까지. 연장이 안 되면, 휘발유는 리터당 최대 백이십이 원 오를 수 있어.",
              "그런데 유류세 인하는 11월 30일까지. 연장이 안 되면, 휘발유는 리터당 최대 122원 오를 수 있어."),
             ("N", "최고가격제까지 끝나면, 눌러 둔 가격이 한꺼번에 튈 수 있다는 우려도 나와.", None),
             ("N", "다만 정부는 그동안 인하를 계속 연장해 왔어. 아직 확정된 건 없어.", None)], {"tail": 0.3}),
    ("us", [("N", "너라면, 세금으로 기름값 계속 누를래, 아니면 지금 제값 낼래?", None)], {"tail": 0.2}),
    ("loop", [], {"tail": 0, "min_tail": 0.45, "cut": True}),
]

CHAPTERS = [("의문", "hook"), ("배경", "war"), ("반전", "twist"), ("결론", "dec")]


def cues(ep):
    c = [(st + 0.05, "stamp") for st in ep.chapter_starts()[1:-1]]
    for i, sh in enumerate(ep.shots):
        st = sh.start
        if i > 0 and sh.name != "loop":
            c.append((st, "whoosh"))
        if sh.name == "hook":
            c.append((st + sh.m(1), "boing"))
        if sh.name == "pump":
            c.append((st + sh.at(1, "눌러"), "stamp"))
        if sh.name == "war":
            c.append((st + sh.at(0, "천육백"), "pop"))
            c.append((st + sh.at(1, "이천삼"), "pop"))
            c.append((st + sh.at(1, "십팔"), "stamp"))
        if sh.name == "cap":
            c.append((st + sh.at(0, "상한선"), "snap"))
            c.append((st + sh.m(1), "boing"))
            c.append((st + sh.at(2, "백이십이"), "ding"))
        if sh.name == "drop":
            c.append((st + sh.at(0, "이십일"), "fall"))
            c.append((st + sh.at(0, "천팔백"), "stamp"))
        if sh.name == "twist":
            c.append((st + sh.m(0), "boing"))
            c.append((st + sh.at(1, "사조"), "stamp"))
            c.append((st + sh.at(1, "세금"), "stamp"))
            c.append((st + sh.at(2, "동결"), "snap"))
        if sh.name == "dec":
            c.append((st + sh.at(0, "십일월"), "tick"))
            c.append((st + sh.at(0, "백이십이"), "stamp"))
            c.append((st + sh.at(1, "튈"), "boing"))
            c.append((st + sh.at(2, "확정"), "stamp"))
        if sh.name == "us":
            c.append((st + sh.m(0), "pop"))
    return c


# ---------------------------------------------------------------- 소품
def station_bg(ctx):
    S.sky(ctx, "#CFE6F5", "#F4EEE2")
    rrect(ctx, -40, 1300, W + 80, 300, 0)  # 바닥
    S.fs(ctx, "#B9B2A0", lw=0)
    rrect(ctx, 40, 230, W - 80, 70, 20)  # 캐노피
    S.fs(ctx, "#E58A3A", lw=8)


def price_board(ctx, x, y, s, price, k=1.0, arrow=0):
    """주유소 가격판. arrow: -1 내림, +1 오름."""
    if k <= 0.01:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s * k, s * k)
    rrect(ctx, -170, -150, 340, 300, 24)
    S.fs(ctx, "#2E3440", lw=8)
    draw_text(ctx, "휘발유", 0, -85, 46, font="black", fill="#F3EBD5")
    rrect(ctx, -140, -40, 280, 110, 14)
    S.fs(ctx, "#1A1D24", lw=5)
    draw_text(ctx, price, 0, 16, 76, font="black", fill="#FFC24A")
    if arrow:
        draw_text(ctx, "▼" if arrow < 0 else "▲", 0, 115, 50, font="black",
                  fill="#7FC8F0" if arrow < 0 else "#FF7A6A")
    ctx.restore()


def pump(ctx, x, y, s):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rrect(ctx, -90, -420, 180, 420, 22)
    S.fs(ctx, "#D9473B", lw=8)
    rrect(ctx, -60, -380, 120, 90, 10)
    S.fs(ctx, "#FBF7EC", lw=5)
    ctx.move_to(90, -300)
    ctx.curve_to(170, -300, 170, -150, 140, -120)
    set_rgb(ctx, S.OUT)
    ctx.set_line_width(14)
    ctx.stroke()
    ctx.restore()


def coin_bag(ctx, x, y, s, k, text):
    if k <= 0.01:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s * k, s * k)
    ctx.new_path()
    ctx.move_to(-60, -150)
    ctx.curve_to(-230, -40, -200, 170, 0, 170)
    ctx.curve_to(200, 170, 230, -40, 60, -150)
    ctx.close_path()
    S.fs(ctx, "#E8C46A", lw=8)
    rrect(ctx, -70, -180, 140, 40, 16)
    S.fs(ctx, "#C9A23E", lw=7)
    draw_text(ctx, text, 0, 40, 74, font="black", fill="#5A4318")
    ctx.restore()


# ---------------------------------------------------------------- 샷 그리기
def _hook_frame(ctx, lt, sh, ep, frozen=False):
    station_bg(ctx)
    t = 0.0 if frozen else lt
    o_on = (not frozen) and lt >= sh.m(1)
    m = 0 if frozen else ep.mouth("D", sh.start + lt) * 1.3
    DRIVER.draw(ctx, 520, 2300, 2.4, 1, pose="flail" if not frozen and lt > 0.4 and not o_on else "shrug",
                expr="shock", mouth=m, t=t, bob=False, sweat=True)
    if o_on:  # 사장님 등장
        k = ease_out_back(prog(lt, sh.m(1) - 0.15, sh.m(1) + 0.2), 1.4)
        OWNER.draw(ctx, 140 - 300 * (1 - k), 1700, 1.15, 1, pose="hips", expr="smug",
                   mouth=ep.mouth("O", sh.start + lt) * 1.3, t=lt)
    # 첫 프레임부터 떠 있는 훅 말풍선
    ctx.save()
    ctx.translate(500, 320)
    rrect(ctx, -440, -120, 880, 240, 60)
    S.fs(ctx, "#FFFFFF", lw=9)
    ctx.new_path()
    ctx.move_to(-20, 115)
    ctx.line_to(30, 210)
    ctx.line_to(70, 115)
    ctx.close_path()
    S.fs(ctx, "#FFFFFF", lw=9)
    rrect(ctx, -30, 100, 110, 24, 4)
    set_rgb(ctx, "#FFFFFF")
    ctx.fill()
    for j, ln in enumerate(HOOK):
        draw_text(ctx, ln, 0, -48 + j * 100, 80, font="black", fill="#2E3A4A" if j == 0 else S.RUST)
    ctx.restore()


def shot_hook(ctx, lt, sh, ep):
    _hook_frame(ctx, lt, sh, ep)


def shot_loop(ctx, lt, sh, ep):
    _hook_frame(ctx, 0.0, ep.shots[0], ep, frozen=True)


def shot_pump(ctx, lt, sh, ep):
    station_bg(ctx)
    pump(ctx, 840, 1360, 1.1)
    tp = sh.at(1, "눌러")
    press = ease_out_back(prog(lt, tp - 0.1, tp + 0.25), 1.5)
    bx, by = 540, 620 + 40 * press
    price_board(ctx, bx, by, 1.15, "1,857", arrow=-1)
    if press > 0.01:  # 위에서 꾹 누르는 손바닥(누름판)
        rrect(ctx, bx - 220, by - 360 - 200 * (1 - press), 440, 150, 30)
        S.fs(ctx, "#F2D2B6", lw=8)
        draw_text(ctx, "꾹", bx, by - 285 - 200 * (1 - press), 70, font="black", fill=S.RUST)
    o_on = lt >= sh.m(1)
    DRIVER.draw(ctx, 260, 1480, 1.0, 1, pose="point" if not o_on else "down", expr="smug" if not o_on else "shock",
                mouth=ep.mouth("D", sh.start + lt) * 1.3, t=lt)
    OWNER.draw(ctx, 620, 1480, 0.95, -1, pose="shrug" if o_on else "down", expr="deadpan",
               mouth=ep.mouth("O", sh.start + lt) * 1.3, t=lt + 1)


def shot_war(ctx, lt, sh, ep):
    S.sky(ctx, "#F4C78A", "#F8E8D0")
    for i in range(3):  # 멀리 연기
        S.cloud(ctx, 200 + i * 330, 1250 - (i % 2) * 60, 1.2, "#8C8478", alpha=0.35)
    ta, tb = sh.at(0, "천육백"), sh.at(1, "이천삼")
    base = 1080
    ka = ease_out_cubic(prog(lt, ta - 0.2, ta + 0.3))
    kb = ease_out_cubic(prog(lt, tb - 0.2, tb + 0.5))
    for x, h, k, lab, val, col in ((340, 380, ka, "2월 말", "1,692원", "#7FA8C9"),
                                   (740, 540, kb, "4월", "2,003원", S.RUST)):
        if k > 0.01:
            rrect(ctx, x - 110, base - h * k, 220, h * k, 16)
            S.fs(ctx, col, lw=8)
            draw_text(ctx, val, x, base - h * k - 60, 66, font="black", fill="#2E3A4A")
            draw_text(ctx, lab, x, base - 45, 46, font="black", fill="#FFFFFF")
    draw_text(ctx, "전국 평균 휘발유 (리터당)", 540, 250, 52, font="black", fill="#5A4A3A")
    t8 = sh.at(1, "십팔")
    S.stamp(ctx, 540, 375, "두 달 새 +18.4%", prog(lt, t8, t8 + 0.45), size=72, rot=-0.05)


def shot_cap(ctx, lt, sh, ep):
    S.planks(ctx, base=S.SLATE, dark=S.SLATE_D, seed=3)
    tl = sh.at(0, "상한선")
    kl = ease_out_cubic(prog(lt, tl - 0.1, tl + 0.4))
    if kl > 0.01:  # 빨간 상한선
        ctx.rectangle(80, 560, 920 * kl, 22)
        set_rgb(ctx, S.RUST)
        ctx.fill()
        if kl > 0.9:
            label(ctx, "최고가격 1,784원", 540, 470, ease_out_back(prog(lt, tl + 0.3, tl + 0.6), 1.6),
                  fill="#FFD6D0", size=56)
    g_on = lt >= sh.m(1)
    OFFICIAL.draw(ctx, 250, 1450, 1.15, 1, pose="point" if g_on else "hips", expr="angry" if g_on else "neutral",
                  mouth=ep.mouth("G", sh.start + lt) * 1.3, t=lt)
    if g_on and lt < sh.m(2):
        bubble(ctx, "넘게 받지 마세요!", 560, 720, ease_out_back(prog(lt, sh.m(1), sh.m(1) + 0.3), 1.6), size=56, tail=-1)
    t2 = sh.at(2, "십오")
    k2 = ease_out_back(prog(lt, t2 - 0.1, t2 + 0.3), 1.6)
    if k2 > 0.01:
        card(ctx, 670, 900, 460, 300, k2, fill="#FFF7C9", rot=0.03)
        draw_text(ctx, "유류세 -15%", 0, -60, 70, font="black", fill="#2E3A4A")
        draw_text(ctx, "리터당 -122원", 0, 50, 62, font="black", fill=S.RUST)
        ctx.restore()


def shot_drop(ctx, lt, sh, ep):
    station_bg(ctx)
    tw = sh.at(0, "이십일")
    kw = ease_out_cubic(prog(lt, tw - 0.3, tw + 0.8))
    for i in range(7):  # 내려가는 계단 화살표
        if kw * 7 > i:
            x, y = 150 + i * 110, 420 + i * 70
            draw_text(ctx, "▼", x, y, 64, font="black", fill="#4F7A9C")
    label(ctx, "21주 연속 ↓", 540, 400, ease_out_back(prog(lt, tw, tw + 0.3), 1.6), fill="#D6EAF8", size=60)
    tp = sh.at(0, "천팔백")
    price_board(ctx, 620, 900, 1.25, "1,857", k=ease_out_back(prog(lt, tp - 0.15, tp + 0.25), 1.6), arrow=-1)
    DRIVER.draw(ctx, 200, 1500, 0.9, 1, pose="cheer", expr="smug", t=lt)


def shot_twist(ctx, lt, sh, ep):
    S.planks(ctx, base="#E9DCC6", dark="#D9C9AE", w=150)
    REFINER.draw(ctx, 250, 1480, 1.05, 1, pose="shrug", expr="sad" if lt < sh.m(1) else "smug",
                 mouth=ep.mouth("R", sh.start + lt) * 1.3, t=lt)
    if lt < sh.m(1):
        bubble(ctx, "손해는 누가?", 420, 620, ease_out_back(prog(lt, 0.05, 0.35), 1.6), size=60, tail=-1)
    tb = sh.at(1, "사조")
    coin_bag(ctx, 700, 800, 1.0, ease_out_back(prog(lt, tb - 0.15, tb + 0.25), 1.6), "4.2조")
    if lt >= tb:
        label(ctx, "손실 보전 예비비", 700, 560, ease_out_back(prog(lt, tb, tb + 0.3), 1.6), fill="#FFF7C9", size=46)
    ts = sh.at(1, "세금")
    S.stamp(ctx, 700, 1080, "결국 세금", prog(lt, ts, ts + 0.45), size=80, rot=-0.07)
    if lt >= sh.m(2):
        k = ease_out_back(prog(lt, sh.m(2), sh.m(2) + 0.3), 1.6)
        card(ctx, 540, 400, 820, 240, k, rot=-0.02)
        draw_text(ctx, "국제유가 105달러↑", 0, -45, 58, font="black", fill="#2E3A4A")
        td = sh.at(2, "동결")
        if lt >= td:
            draw_text(ctx, "최고가격 3연속 동결", 0, 50, 58, font="black", fill=S.RUST)
        ctx.restore()


def shot_dec(ctx, lt, sh, ep):
    S.sky(ctx, "#D9E4EE", "#F2EEE4")
    t11 = sh.at(0, "십일월")
    k11 = ease_out_back(prog(lt, t11 - 0.1, t11 + 0.3), 1.6)
    if k11 > 0.01:
        card(ctx, 330, 470, 440, 340, k11, fill="#FBF7EC", rot=-0.04)
        draw_text(ctx, "11월 30일", 0, -60, 70, font="black", fill=S.RUST)
        draw_text(ctx, "유류세 인하 끝", 0, 40, 50, font="black", fill="#2E3A4A")
        ctx.restore()
    t1 = sh.at(0, "백이십이")
    k1 = ease_out_back(prog(lt, t1 - 0.1, t1 + 0.3), 1.6)
    if k1 > 0.01:
        card(ctx, 720, 520, 400, 280, k1, fill="#FFE1DC", rot=0.04)
        draw_text(ctx, "최대", 0, -60, 46, font="black", fill="#7A8594")
        draw_text(ctx, "+122원", 0, 30, 78, font="black", fill=S.RUST)
        ctx.restore()
    # 스프링에 눌린 가격판: '튈' 순간 튀어오름
    tj = sh.at(1, "튈")
    jump = ease_out_back(prog(lt, tj - 0.1, tj + 0.4), 2.2)
    bx, by = 540, 980 - 240 * jump
    ctx.move_to(540, 1360)
    for i in range(8):
        yy = 1360 - (i + 1) * (1360 - by - 150) / 8
        ctx.line_to(540 + (40 if i % 2 == 0 else -40), yy)
    set_rgb(ctx, "#7A8594")
    ctx.set_line_width(12)
    ctx.stroke()
    price_board(ctx, bx, by, 0.9, "????", arrow=1 if jump > 0.2 else 0)
    tc = sh.at(2, "확정")
    S.stamp(ctx, 540, 1040, "아직 확정 아님", prog(lt, tc, tc + 0.45), size=72, rot=-0.06)


def shot_us(ctx, lt, sh, ep):
    S.planks(ctx, base="#E9DCC6", dark="#D9C9AE", w=150)
    OFFICIAL.draw(ctx, 220, 1480, 0.95, 1, pose="hips", expr="smug", t=lt)
    coin_bag(ctx, 220, 700, 0.55, 1.0, "세금")
    price_board(ctx, 780, 700, 0.75, "제값?", arrow=1)
    DRIVER.draw(ctx, 560, 1520, 1.05, 1, pose="shrug", expr="shock", sweat=True,
                mouth=0, t=lt)
    label(ctx, "계속 누르기", 260, 470, ease_out_back(prog(lt, 0.2, 0.5), 1.6), fill="#D6EAF8", size=46)
    label(ctx, "지금 제값", 760, 470, ease_out_back(prog(lt, 0.6, 0.9), 1.6), fill="#FFD6D0", size=46)


SHOT_FN = {k[5:]: v for k, v in globals().items() if k.startswith("shot_")}
CAMERA = {
    "hook": (540, 900, 0.0), "loop": (540, 900, 0.0), "pump": (540, 860, 0.04), "war": (540, 800, 0.04),
    "cap": (540, 800, 0.05), "drop": (540, 800, 0.04), "twist": (540, 800, 0.05), "dec": (540, 800, 0.04),
    "us": (540, 900, 0.04),
}

EP = Explainer(SCRIPT, VOICE, CAP_COLOR, SHOT_FN, CAMERA, cues,
               notice="※ 상황극 / 언론 보도·정부 발표 기반", chapters=CHAPTERS, overlay_delay=2.0)
render_frame, mix = EP.render_frame, EP.mix


def prepare():
    global DURATION
    DURATION = EP.prepare().duration
