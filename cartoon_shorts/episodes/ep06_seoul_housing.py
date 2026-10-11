"""오늘의 만평 #06 — 강남은 떨어지는데 서울은 오른다?  (역설형 훅 + 양자택일 CTA + 루프 엔딩)

실제 사실 (2026년 10월 8~9일 보도 기준):
- 한국부동산원: 서울 아파트값 87주 연속 상승(종전 최장 85주), 10월 첫째 주 +0.12%
  강남3구 5주째 하락(강남 -0.34%, 서초 -0.27%, 송파 -0.19%),
  서대문 0.36%·강북 0.35%·금천 0.34%·관악 0.33%·도봉 0.32% 상승
- 2025년 6·27 대책: 수도권 주담대 최대 6억 / 10·15 대책: 15억 초과 4억, 25억 초과 2억
- 10/8 정무위 국감: 야당 의원 "현금 부자만 집을 살 수 있게 해놨다" 취지 비판,
  금융위원장 "6억 제한 안 했으면 집값 상승 더 심했을 것", "공급을 더 빠르게 확대해야"
- 30대 직장인: 4억3천만 원 대출 계획 → 한도 축소로 1억3천만 원 추가 마련 (보도 사례)
- KB 아파트담보대출 PIR 서울 약 10배 (2026년 2분기)
대출 규제와 강남 하락의 인과관계는 단정하지 않고 사실만 나란히 보여준다. 개인 이름은 쓰지 않는다.
"""
import math

from .. import squire as S
from ..doodle import Doodle
from ..engine import W, draw_text, ease_out_back, ease_out_cubic, ellipse, prog, rrect, set_rgb
from ..explainer import Explainer, bubble, card, label

TITLE = "강남은 떨어지는데 서울은 오른다? | 오늘의 만평"
DURATION = 48.0

MP = Doodle(coat="#2F3E5C", tie="#C9473B", hair="cap", hair_color="#2A2420", badge=True)
FSC = Doodle(coat="#3A3F48", tie="#5B6E8C", hair="gray", hair_color="#CFCFCF", glasses=True, badge=True)
CIT = Doodle(coat="#6F7F63", hair="beanie", hair_color="#C25B3F", collar=False)

VOICE = {
    "N": ("male", "+80%", "+20Hz", 1.18),
    "P": ("male2", "+75%", "+0Hz", 1.2),  # 야당 의원: 따지듯 높고 빠르게
    "F": ("male", "+55%", "-10Hz", 0.9),  # 금융위원장: 낮고 덤덤하게
}
CAP_COLOR = {"N": "#FFFFFF", "P": "#9FD3F0", "F": "#FFE38A"}

SCRIPT = [
    ("hook", [("N", "강남은 떨어지는데, 서울은 팔십칠 주째 오른다?", "강남은 떨어지는데, 서울은 87주째 오른다?"),
              ("N", "이게 무슨 일인지, 지금부터 풀어줄게.", None)], {"tail": 0.4}),
    ("loan", [("N", "정부는 작년 유월부터 수도권 주택담보대출을 최대 육억으로 묶었어.",
               "정부는 작년 6월부터 수도권 주택담보대출을 최대 6억으로 묶었어."),
              ("N", "시월엔 더 조였지. 십오억 넘는 집은 사억, 이십오억 넘으면 이억까지만.",
               "10월엔 더 조였지. 15억 넘는 집은 4억, 25억 넘으면 2억까지만.")], {"tail": 0.6}),
    ("map", [("N", "비싼 집일수록 대출이 확 줄어든 셈이야. 그리고 지금, 강남 삼 구는 오 주째 하락 중.",
              "비싼 집일수록 대출이 확 줄어든 셈이야. 그리고 지금, 강남 3구는 5주째 하락 중."),
             ("N", "대신 서대문, 강북, 금천, 관악, 도봉 같은 외곽이 크게 오르면서 서울 전체는 팔십칠 주 연속 상승, 역대 최장이야.",
              "대신 서대문, 강북, 금천, 관악, 도봉 같은 외곽이 크게 오르면서 서울 전체는 87주 연속 상승, 역대 최장이야.")],
     {"tail": 0.8}),
    ("audit", [("P", "결국 현금 부자만 집 살 수 있게 만든 거 아닙니까?", None),
               ("F", "육억 제한을 안 했으면, 집값은 더 올랐을 겁니다.", "6억 제한을 안 했으면, 집값은 더 올랐을 겁니다.")],
     {"tail": 0.6}),
    ("income", [("N", "서울 아파트는 지금 연 소득의 약 열 배야. 한 푼도 안 쓰고 십 년을 모아야 하는 수준이지.",
                 "서울 아파트는 지금 연 소득의 약 10배야. 한 푼도 안 쓰고 10년을 모아야 하는 수준이지."),
                ("N", "사억 넘게 빌리려다 한도가 줄어서, 일억 넘는 돈을 갑자기 더 구해야 했던 삼십 대 사례도 나왔어.",
                 "4억 넘게 빌리려다 한도가 줄어서, 1억 넘는 돈을 갑자기 더 구해야 했던 30대 사례도 나왔어.")],
     {"tail": 0.6}),
    ("supply", [("N", "정부도 대출만으론 부족하대. 결국 공급을 더 빨리 늘려야 한다는 거야.", None)], {"tail": 0.8}),
    ("vote", [("N", "그래서 너는 어느 쪽이야?", None),
              ("N", "일 번, 대출을 더 조여야 한다. 이 번, 실수요자 대출은 풀어줘야 한다.",
               "1번, 대출을 더 조여야 한다. 2번, 실수요자 대출은 풀어줘야 한다."),
              ("N", "번호로 댓글 남겨줘. 근데 진짜 이상하지 않아?", None)], {"tail": 0.6}),
]

CHAPTERS = [("의문", "hook"), ("배경", "loan"), ("반응", "audit"), ("결과", "supply")]

# 서울 지도 위 구 위치(대략)와 10월 첫째 주 변동률(%)
DISTRICTS = [("도봉", 640, 330, 0.32), ("강북", 560, 440, 0.35), ("서대문", 400, 620, 0.36),
             ("관악", 430, 1010, 0.33), ("금천", 260, 1060, 0.34),
             ("서초", 610, 970, -0.27), ("강남", 730, 900, -0.34), ("송파", 830, 790, -0.19)]
BLUE, RED = "#4F7A9C", "#C9473B"


def _frac(sh, i, f):
    return sh.m(i) + (sh.me(i) - sh.m(i)) * f


def _loan_times(sh):
    """6억·4억·2억 막대가 각각 그 금액을 말하는 순간 등장."""
    return [sh.at(0, "육억"), sh.at(1, "사억"), sh.at(1, "이억")]


def _district_time(sh, name):
    """하락 3구는 '강남 삼 구' 에서 함께, 상승 구는 내레이션이 그 이름을 부르는 순간."""
    return sh.at(0, "강남") if dict((d[0], d[3]) for d in DISTRICTS)[name] < 0 else sh.at(1, name)


def cues(ep):
    c = [(st + 0.05, "stamp") for st in ep.chapter_starts()[1:-1]]
    for i, sh in enumerate(ep.shots):
        st = sh.start
        if i > 0:
            c.append((st, "whoosh"))
        if sh.name == "hook":
            c.append((st, "thud"))
            c.append((st + sh.m(1), "boing"))
        if sh.name == "loan":
            for t in _loan_times(sh):
                c.append((st + t, "fall"))
        if sh.name == "map":
            for name, *_ in DISTRICTS:
                c.append((st + _district_time(sh, name), "pop"))
            c.append((st + sh.at(1, "팔십칠"), "stamp"))
        if sh.name == "audit":
            c.append((st + sh.m(0), "slide"))
            c.append((st + sh.m(1), "slide"))
        if sh.name == "income":
            a, b = sh.at(0, "열"), sh.at(0, "십 년")
            for k in range(10):
                c.append((st + a + (b - a) * k / 10, "tick"))
            c.append((st + sh.at(1, "일억"), "thud"))
        if sh.name == "supply":
            c.append((st + 0.3, "stamp"))
            for k in range(4):
                c.append((st + sh.at(0, "공급") + k * 0.15, "pop"))
        if sh.name == "vote":
            c.append((st + sh.at(1, "일 번"), "pop"))
            c.append((st + sh.at(1, "이 번"), "pop"))
            c.append((st + sh.m(2), "ding"))
    return c


# ---------------------------------------------------------------- 소품
def arrow(ctx, x, y, s, up, color, k=1.0):
    """굵은 상승/하락 화살표 (k: 길이 진행)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s if up else -s)
    length = 380 * max(k, 0.05)
    ctx.new_path()
    ctx.move_to(-55, 160)
    ctx.line_to(-55, 160 - length)
    ctx.line_to(-140, 160 - length)
    ctx.line_to(0, 160 - length - 170)
    ctx.line_to(140, 160 - length)
    ctx.line_to(55, 160 - length)
    ctx.line_to(55, 160)
    ctx.close_path()
    S.fs(ctx, color, lw=9)
    ctx.restore()


def coin_stack(ctx, x, y, n, color="#E8B93E"):
    for i in range(n):
        ellipse(ctx, x, y - i * 26, 70, 24)
        S.fs(ctx, color, lw=6)


# ---------------------------------------------------------------- 샷 그리기
def shot_hook(ctx, lt, sh, ep):
    # 첫 프레임부터 큰 훅 문구가 떠 있어야 한다 (팝인 지연 없음)
    ctx.rectangle(0, 0, W / 2, 1920)
    set_rgb(ctx, "#2F4A66")
    ctx.fill()
    ctx.rectangle(W / 2, 0, W / 2, 1920)
    set_rgb(ctx, "#6B2E2A")
    ctx.fill()
    wob = math.sin(lt * 6) * 10
    draw_text(ctx, "강남", 270, 360, 150, font="black", fill="#DCEAF3")
    draw_text(ctx, "서울", 790, 360, 150, font="black", fill="#F7D9D4")
    arrow(ctx, 270, 760 + wob, 0.85, False, BLUE)
    arrow(ctx, 790, 760 - wob, 0.85, True, RED)
    draw_text(ctx, "5주째 하락", 270, 1120, 62, font="black", fill="#DCEAF3")
    draw_text(ctx, "87주째 상승", 780, 1120, 62, font="black", fill="#FFFFFF")
    sc = 1 + 0.12 * math.sin(lt * 8)
    draw_text(ctx, "???", 540, 720, 130, font="black", fill="#E8B93E", stroke=14, stroke_fill="#1E1E22", scale=sc)


def shot_loan(ctx, lt, sh, ep):
    S.desk(ctx)
    draw_text(ctx, "수도권 주택담보대출 한도", 540, 250, 64, font="black", fill="#F3EBD5",
              stroke=10, stroke_fill="#2E2A28")
    tiers = tuple(zip(("15억 이하", "15~25억", "25억 초과"), (6, 4, 2), _loan_times(sh)))
    for i, (name, amt, t0) in enumerate(tiers):
        k = ease_out_back(prog(lt, t0, t0 + 0.35), 1.6)
        if k <= 0.01:
            continue
        x = 200 + i * 290
        h = 110 * amt * ease_out_cubic(prog(lt, t0, t0 + 0.5))
        rrect(ctx, x - 110, 1130 - h, 220, h, 18)
        S.fs(ctx, (RED, "#D9874A", "#9AA3AE")[i], lw=8)
        draw_text(ctx, f"{amt}억", x, 1130 - h - 70, 84, font="black", fill="#F3EBD5", stroke=10,
                  stroke_fill="#2E2A28", scale=k)
        draw_text(ctx, name, x, 1190, 50, font="black", fill="#2E2A28", scale=k)
    if lt >= sh.m(1):
        draw_text(ctx, "비쌀수록 대출 ↓", 540, 1380, 70, font="black", fill=RED, stroke=10, stroke_fill="#FFFFFF",
                  alpha=prog(lt, sh.at(1, "이억"), sh.at(1, "이억") + 0.3))


def _seoul(ctx):
    S.sky(ctx, "#D9E4EC", "#C6D6E2")
    ctx.new_path()  # 서울 윤곽 (대충 둥근 다각형)
    pts = [(170, 520), (330, 300), (560, 210), (760, 280), (930, 470), (990, 760), (940, 1000),
           (780, 1150), (520, 1190), (300, 1160), (150, 980), (110, 760)]
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    ctx.close_path()
    S.fs(ctx, "#EDE6D3", lw=10)
    ctx.new_path()  # 한강
    ctx.move_to(120, 800)
    ctx.curve_to(360, 700, 560, 880, 760, 760)
    ctx.curve_to(860, 700, 940, 720, 995, 690)
    set_rgb(ctx, "#8FB4D6")
    ctx.set_line_width(46)
    ctx.stroke()
    draw_text(ctx, "한강", 360, 760, 40, font="black", fill="#4F7A9C")


def shot_map(ctx, lt, sh, ep):
    _seoul(ctx)
    for name, x, y, v in DISTRICTS:
        up = v > 0
        t0 = _district_time(sh, name)
        k = ease_out_back(prog(lt, t0, t0 + 0.35), 2.0)
        if k <= 0.01:
            continue
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(k, k)
        ellipse(ctx, 0, 0, 92, 92)
        S.fs(ctx, RED if up else BLUE, lw=8)
        draw_text(ctx, name, 0, -22, 44, font="black", fill="#FFFFFF")
        draw_text(ctx, f"{'↑' if up else '↓'}{abs(v):.2f}%", 0, 30, 34, font="black", fill="#FFFFFF")
        ctx.restore()
    t87 = sh.at(1, "팔십칠")
    S.stamp(ctx, 540, 1390, "87주 연속 · 역대 최장", prog(lt, t87, t87 + 0.45), size=72, rot=-0.04)


def shot_audit(ctx, lt, sh, ep):
    S.planks(ctx, base="#4A3B2E", dark="#3B2F24", w=150)
    rrect(ctx, -40, 1350, W + 80, 600, 0)
    S.fs(ctx, "#6B4E35", lw=0)
    talking = 0 if lt < sh.m(1) else 1
    for j, (P, x, f, spk, name) in enumerate(((MP, 280, 1, "P", "야당 의원"), (FSC, 800, -1, "F", "금융위원장"))):
        active = j == talking
        s = 1.35 if active else 1.1
        P.draw(ctx, x, 1560, s, f, pose=("point" if spk == "P" else "hips") if active else "down",
               expr=("angry" if spk == "P" else "deadpan") if active else "neutral",
               mouth=ep.mouth(spk, sh.start + lt) * 1.3, t=lt + j, bob=spk == "P")
        label(ctx, name, x, 280, 1.0 if active else 0.75, fill="#F3EBD5" if active else "#B9B2A0", size=56)
    rrect(ctx, 80, 1420, 920, 90, 20)  # 국감 책상
    S.fs(ctx, "#856246", lw=8)
    draw_text(ctx, "국정감사", 540, 420, 50, font="black", fill="#F3EBD5", stroke=8, stroke_fill="#2E2A28")


def shot_income(ctx, lt, sh, ep):
    S.desk(ctx)
    if lt < sh.m(1):  # 연 소득 × 10: 연봉 봉투 10개가 차례로 채워짐
        k = ease_out_back(prog(lt, 0.05, 0.4), 1.4)
        card(ctx, 520, 640, 820, 640, k, rot=-0.02)
        draw_text(ctx, "서울 아파트 = 연 소득 × 10", 0, -240, 56, font="black", fill="#2E3A4A")
        n = int(10 * prog(lt, sh.at(0, "열"), sh.at(0, "십 년")) + 0.999)
        for i in range(10):
            x, y = -310 + (i % 5) * 155, -60 + (i // 5) * 180
            on = i < n
            rrect(ctx, x - 62, y - 50, 124, 100, 12)
            S.fs(ctx, "#F3EBD5" if on else "#E3DCC8", lw=6 if on else 3, alpha=1 if on else 0.5)
            if on:
                draw_text(ctx, f"{i + 1}년", x, y, 40, font="black", fill=RED)
        ctx.restore()
        return
    # 30대 사례 카드 (같은 자리로 교체 — 하단 UI 영역을 피함)
    k2 = ease_out_back(prog(lt, sh.m(1), sh.m(1) + 0.4), 1.6)
    card(ctx, 520, 640, 820, 640, k2, fill="#FBF7EC", rot=0.02)
    draw_text(ctx, "30대 직장인 사례", 0, -230, 54, font="black", fill="#7A8594")
    draw_text(ctx, "대출 계획 4.3억", 0, -110, 66, font="black", fill="#2E3A4A")
    t_cut = sh.at(1, "한도")
    kc = ease_out_back(prog(lt, t_cut, t_cut + 0.3), 2.0)
    draw_text(ctx, "↓ 한도 축소", 0, 0, 62, font="black", fill=BLUE, scale=max(kc, 0.01))
    t_add = sh.at(1, "일억")
    kk = ease_out_back(prog(lt, t_add, t_add + 0.35), 2.0)
    draw_text(ctx, "+1.3억 더 구해야", 0, 140, 84, font="black", fill=RED, scale=max(kk, 0.01))
    ctx.restore()


def shot_supply(ctx, lt, sh, ep):
    S.sky(ctx, "#B9D3E6", "#E4EEF4")
    ctx.rectangle(0, 1450, W, 500)
    set_rgb(ctx, "#8C7A5E")
    ctx.fill()
    S.stamp(ctx, 540, 380, "대출 규제 = 해답?", prog(lt, 0.3, 0.7), size=80, rot=-0.06)
    for j in range(4):  # 아파트가 쑥쑥 올라감
        t0 = sh.at(0, "공급") + j * 0.15
        h = 700 * ease_out_back(prog(lt, t0, t0 + 0.5), 1.4) * (0.75 + 0.1 * (j % 3))
        if h < 2:
            continue
        x = 140 + j * 230
        rrect(ctx, x, 1450 - h, 180, h, 10)
        S.fs(ctx, ("#D8CBB0", "#C6B9A0", "#E3D8C0", "#CDBF9F")[j], lw=8)
        for r in range(int(h // 90)):
            for c in range(2):
                rrect(ctx, x + 30 + c * 70, 1450 - h + 30 + r * 90, 48, 50, 6)
                S.fs(ctx, "#7FA6C9", lw=4)
    kb = ease_out_back(prog(lt, sh.at(0, "공급"), sh.at(0, "공급") + 0.4), 2.0)
    label(ctx, "결국 답은 공급?", 540, 620, kb, size=70)


def shot_vote(ctx, lt, sh, ep):
    t1, t2 = sh.at(1, "일 번"), sh.at(1, "이 번")
    k1 = ease_out_back(prog(lt, t1, t1 + 0.35), 1.6)
    k2 = ease_out_back(prog(lt, t2, t2 + 0.35), 1.6)
    ctx.rectangle(0, 0, W / 2, 1920)
    set_rgb(ctx, "#2F4A66")
    ctx.fill()
    ctx.rectangle(W / 2, 0, W / 2, 1920)
    set_rgb(ctx, "#5E6B45")
    ctx.fill()
    for x, num, a, b, k in ((260, "1", "대출", "더 조이기", k1), (790, "2", "실수요자", "대출 풀기", k2)):
        if k <= 0.01:
            continue
        ctx.save()
        ctx.translate(x, 700)
        ctx.scale(k, k)
        ellipse(ctx, 0, -220, 110, 110)
        S.fs(ctx, "#F3EBD5", lw=10)
        draw_text(ctx, num, 0, -216, 150, font="black", fill="#2E3A4A")
        draw_text(ctx, a, 0, 0, 72, font="black", fill="#FFFFFF")
        draw_text(ctx, b, 0, 100, 72, font="black", fill="#FFFFFF")
        ctx.restore()
    if lt < sh.m(1):
        draw_text(ctx, "너는 어느 쪽?", 540, 700, 110, font="black", fill="#FFFFFF", stroke=12,
                  stroke_fill="#1E1E22", scale=max(0.01, ease_out_back(prog(lt, 0.05, 0.35), 2.0)))
    CIT.draw(ctx, 540, 2050, 1.2, 1, pose="wave" if lt >= sh.m(2) else "shrug",
             expr="smug" if lt >= sh.m(2) else "neutral", t=lt)
    if lt >= sh.m(2):
        bubble(ctx, "번호로 댓글!", 540, 330, ease_out_back(prog(lt, sh.m(2), sh.m(2) + 0.35), 2.0), size=70)
    # 루프: 끝에서 첫 장면의 "???" 가 미리 떠오른다
    kq = prog(lt, sh.dur - 0.5, sh.dur)
    if kq > 0:
        draw_text(ctx, "???", 540, 720, 130, font="black", fill="#E8B93E", stroke=14, stroke_fill="#1E1E22",
                  alpha=kq)


SHOT_FN = {k[5:]: v for k, v in globals().items() if k.startswith("shot_")}
CAMERA = {
    "hook": (540, 700, 0.04), "loan": (540, 900, 0.05), "map": (540, 760, 0.06),
    "audit": (540, 1000, 0.05), "income": (540, 900, 0.04), "supply": (540, 1000, 0.05),
    "vote": (540, 800, 0.03),
}

EP = Explainer(SCRIPT, VOICE, CAP_COLOR, SHOT_FN, CAMERA, cues,
               notice="※ 한국부동산원·KB·언론 보도 기반 / 의원 발언은 취지를 줄였습니다", chapters=CHAPTERS)
render_frame, mix = EP.render_frame, EP.mix


def prepare():
    global DURATION
    DURATION = EP.prepare().duration
