"""오늘의 만평 #05 — 금메달 따고 욕먹는 이유  (두둥실 캐릭터 + 단계 진행 바)

실제 사건 (2026년 10월 초 국내 보도 기준):
- 2026 아이치·나고야 아시안게임에서 축구·야구가 결승에서 일본을 꺾고 금메달
- 우승 직후 일부 축구 선수들이 '군대 안 간다'는 취지의 발언·SNS 게시 → 비판
- 국방부 장관: "신성한 국방의 의무를 폄하하는 것에 대해 심히 유감", 국감에서 "병역특례 궁극적 폐지"
- BTS 사례를 든 형평성 국민청원 (대중문화예술인은 특례 대상 아님)
- 2022 항저우: 축구 22명 중 20명, 야구 24명 중 19명 혜택
- 체육요원: 기초군사훈련 + 34개월 분야 복무 + 봉사활동 544시간 (면제가 아님)
- 아시안게임 1위 기준 삭제, 올림픽 3위 이상 기준 유지 병역법 개정안 발의
선수 발언은 실제 인용이 아니라 취지만 전한다. 개인 이름은 쓰지 않는다.
"""
import math

from .. import squire as S
from ..doodle import Doodle
from ..engine import W, draw_text, ease_out_back, ease_out_cubic, ellipse, prog, rrect, set_rgb
from ..explainer import Explainer, close_up, label

TITLE = "금메달 따고 욕먹는 이유 | 오늘의 만평"
DURATION = 48.0

ATH = Doodle(coat="#D9473B", hair="cap", hair_color="#2A2420", collar=False, pants="#F3EBD5")
ATH2 = Doodle(coat="#2F5E9C", hair="tuft", collar=False, pants="#F3EBD5")
MIN = Doodle(coat="#2F3A30", tie="#7A8C5E", hair="gray", hair_color="#CFCFCF", glasses=True, badge=True)
SINGER = Doodle(coat="#6B4F9C", hair="bob", hair_color="#1E1E28", collar=False)
CIT = Doodle(coat="#6F7F63", hair="beanie", hair_color="#C25B3F", collar=False)

VOICE = {
    "N": ("male", "+80%", "+20Hz", 1.18),
    "M": ("male", "+55%", "-10Hz", 0.88),  # 국방부 장관: 낮고 단호하게
}
CAP_COLOR = {"N": "#FFFFFF", "M": "#FFE38A"}

SCRIPT = [
    ("hook", [("N", "금메달 하나면 군 복무 대신 운동을 계속할 수 있어. "
                    "근데 이번엔 그 금메달 때문에 욕을 먹고 있대.", None)], {"tail": 0.6}),
    ("rule", [("N", "기준은 올림픽 동메달 이상, 아니면 아시안게임 금메달.", None)], {"tail": 0.8}),
    ("final", [("N", "이번 아이치 나고야 아시안게임에선 축구랑 야구가 둘 다 결승에서 일본을 꺾고 금메달을 땄어.",
                "이번 아이치·나고야 아시안게임에선 축구랑 야구가 둘 다 결승에서 일본을 꺾고 금메달을 땄어.")],
     {"tail": 0.6}),
    ("sns", [("N", "근데 우승 직후, 일부 축구 선수들이 이제 군대 안 간다는 식의 말을 하고 SNS에도 올렸어.",
              "근데 우승 직후, 일부 축구 선수들이 \"이제 군대 안 간다\"는 식의 말을 하고 SNS에도 올렸어."),
             ("N", "금메달보다 군 면제가 목표였냐는 비판이 쏟아졌지.", None)], {"tail": 0.6}),
    ("minister", [("M", "신성한 국방의 의무를 폄하하는 것에 대해, 심히 유감입니다.", None),
                  ("N", "장관은 국정감사에서 병역특례를 궁극적으로 폐지하겠다고까지 했어.", None)],
     {"tail": 0.8}),
    ("bts", [("N", "그러자 터져 나온 말. 비티에스는 세계 일 위를 해도 다 군대 갔는데?",
              "그러자 터져 나온 말. \"BTS는 세계 1위를 해도 다 군대 갔는데?\""),
             ("N", "대중문화예술인은 아무리 성과를 내도 특례 대상이 아니거든. 국민청원까지 올라왔어.", None)],
     {"tail": 0.6}),
    ("numbers", [("N", "지난 항저우 대회 때도 축구는 스물두 명 중 스무 명, 야구는 스물네 명 중 열아홉 명이 혜택을 받았어.",
                  "지난 항저우 대회 때도 축구는 22명 중 20명, 야구는 24명 중 19명이 혜택을 받았어.")],
     {"tail": 0.8}),
    ("factcheck", [("N", "다만 엄밀히 말하면 면제는 아니야.", "다만 엄밀히 말하면 '면제'는 아니야."),
                   ("N", "기초군사훈련 받고, 삼십사 개월 동안 선수로 뛰면서 봉사활동 오백사십사 시간을 채워야 해.",
                    "기초군사훈련 받고, 34개월 동안 선수로 뛰면서 봉사활동 544시간을 채워야 해.")],
     {"tail": 0.8}),
    ("bill", [("N", "국회에선 아시안게임 금메달 기준을 아예 없애는 법안이 나왔어. 올림픽 메달 기준은 그대로 두고.",
               None)], {"tail": 0.8}),
    ("outro", [("N", "금메달이면 군 복무를 대신해도 될까, 이제 바꿔야 할까?", None),
               ("N", "댓글로 알려줘!", None)], {"tail": 2.4}),
]

CHAPTERS = [("배경", "hook"), ("사건", "final"), ("반응", "minister"), ("결과", "factcheck")]


def _frac(sh, i, f):
    """i 번째 대사의 f 비율 지점 (로컬 시간)."""
    return sh.m(i) + (sh.me(i) - sh.m(i)) * f


def cues(ep):
    c = []
    starts = ep.chapter_starts()[1:-1]
    for st in starts:
        c.append((st + 0.05, "stamp"))
    for i, sh in enumerate(ep.shots):
        st = sh.start
        if i > 0:
            c.append((st, "whoosh"))
        if sh.name == "hook":
            c.append((st + 0.3, "ding"))
            c.append((st + _frac(sh, 0, 0.55), "thud"))
        if sh.name == "rule":
            c.append((st + 0.4, "pop"))
            c.append((st + 0.9, "pop"))
        if sh.name == "final":
            c.append((st + _frac(sh, 0, 0.5), "stamp"))
            c.append((st + _frac(sh, 0, 0.8), "stamp"))
        if sh.name == "sns":
            c.append((st + 0.6, "tick"))
            for k in range(4):
                c.append((st + sh.m(1) + k * 0.25, "pop"))
        if sh.name == "minister":
            c.append((st + 0.25, "slide"))
            c.append((st + sh.m(1) + 0.4, "stamp"))
        if sh.name == "bts":
            c.append((st + 0.4, "boing"))
            c.append((st + sh.m(1) + 0.5, "stamp"))
        if sh.name == "numbers":
            for k in range(2):
                c.append((st + 0.5 + k * 0.8, "pop"))
        if sh.name == "factcheck":
            c.append((st + 0.3, "stamp"))
            c.append((st + sh.me(0) - 0.3, "snap"))
            for k in range(3):
                c.append((st + _frac(sh, 1, 0.15 + k * 0.3), "pop"))
        if sh.name == "bill":
            c.append((st + _frac(sh, 0, 0.45), "snap"))
            c.append((st + _frac(sh, 0, 0.85), "ding"))
        if sh.name == "outro":
            c.append((st + sh.m(1), "pop"))
            c.append((st + sh.m(1) + 0.8, "ding"))
    return c


# ---------------------------------------------------------------- 소품
def medal(ctx, x, y, s, rot=0.0, text="1"):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    for sg, col in ((-1, "#C9473B"), (1, "#2F5E9C")):  # 리본
        ctx.new_path()
        ctx.move_to(sg * 20, -130)
        ctx.line_to(sg * 60, -130)
        ctx.line_to(sg * 18, -20)
        ctx.line_to(sg * -14, -20)
        ctx.close_path()
        S.fs(ctx, col, lw=6)
    ellipse(ctx, 0, 30, 70, 70)
    S.fs(ctx, "#E8B93E", lw=8)
    ellipse(ctx, 0, 30, 50, 50)
    S.fs(ctx, "#F2CE5C", lw=4)
    draw_text(ctx, text, 0, 32, 64, font="black", fill="#8C6A12")
    ctx.restore()


def bubble(ctx, text, x, y, k, size=56, fill="#FFFFFF", ink="#2E3A4A", tail=1):
    """말풍선 (k: 팝업 배율)."""
    if k <= 0.01:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(k, k)
    tw = len(text) * size * 0.95 + 70
    ctx.new_path()
    ctx.move_to(tail * 20, 40)
    ctx.line_to(tail * 60, 95)
    ctx.line_to(tail * 70, 40)
    ctx.close_path()
    S.fs(ctx, fill, lw=6)
    rrect(ctx, -tw / 2, -55, tw, 110, 40)
    S.fs(ctx, fill, lw=6)
    rrect(ctx, tail * 20 - 4, 30, 54, 16, 4)
    set_rgb(ctx, fill)
    ctx.fill()
    draw_text(ctx, text, 0, 2, size, font="black", fill=ink)
    ctx.restore()


def card(ctx, x, y, w, h, k, fill="#FBF7EC", rot=0.0):
    """팝업 카드 배경. 이후 그릴 내용을 위해 변환을 걸어 둔 채 ctx.save() 상태로 돌려준다."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(max(k, 0.01), max(k, 0.01))
    rrect(ctx, -w / 2, -h / 2, w, h, 30)
    S.fs(ctx, fill, lw=9)


# ---------------------------------------------------------------- 샷 그리기
def _stadium(ctx):
    S.sky(ctx, "#8EB4D6", "#DCEAF3", h=1100)
    for i in range(3):  # 관중석
        rrect(ctx, -50, 700 + i * 110, W + 100, 120, 20)
        S.fs(ctx, ("#5C6B7E", "#6B7A8C", "#7A8899")[i], lw=6)
        for j in range(18):
            ellipse(ctx, 30 + j * 60 + (i % 2) * 30, 715 + i * 110, 18, 18)
            set_rgb(ctx, ("#F3EBD5", "#E8B93E", "#C9473B", "#9FD3F0")[(i + j) % 4], 0.85)
            ctx.fill()
    ctx.rectangle(0, 1030, W, 1000)
    set_rgb(ctx, "#6E9B57")
    ctx.fill()
    for i in range(6):  # 잔디 줄무늬
        ctx.rectangle(0, 1030 + i * 160, W, 80)
        set_rgb(ctx, "#79A862")
        ctx.fill()


def shot_hook(ctx, lt, sh, ep):
    _stadium(ctx)
    boo = _frac(sh, 0, 0.55)
    booing = lt >= boo
    ATH.draw(ctx, 540, 1720, 1.35, 1, pose="cheer" if not booing else "shrug",
             expr="smug" if not booing else "shock", t=lt, sweat=booing)
    medal(ctx, 540 + 20, 1720 - 330 * 1.35, 0.8, rot=math.sin(lt * 5) * 0.15)
    k = ease_out_back(prog(lt, 0.1, 0.5), 2.0)
    if not booing:
        draw_text(ctx, "금메달!", 540, 420, 130, font="black", fill="#E8B93E", stroke=12,
                  stroke_fill="#2E2A28", scale=max(k, 0.01))
    for j, (txt, x, y) in enumerate((("우~~", 230, 420), ("면제가 목표?", 760, 330), ("실망이다", 300, 620))):
        bubble(ctx, txt, x, y, ease_out_back(prog(lt, boo + j * 0.2, boo + j * 0.2 + 0.3), 2.0),
               size=58, fill="#F7D9D4", tail=1 if x < 540 else -1)


def shot_rule(ctx, lt, sh, ep):
    S.desk(ctx)
    card(ctx, 540, 720, 900, 860, ease_out_back(prog(lt, 0.05, 0.4), 1.6), rot=-0.02)
    draw_text(ctx, "체육요원 편입 기준", 0, -340, 70, font="black", fill="#2E3A4A")
    rows = (("올림픽", "동메달 이상", "3"), ("아시안게임", "금메달", "1"))
    for i, (a, b, num) in enumerate(rows):
        kk = ease_out_back(prog(lt, 0.4 + i * 0.5, 0.75 + i * 0.5), 2.0)
        if kk <= 0.01:
            continue
        ctx.save()
        ctx.translate(0, -170 + i * 230)
        ctx.scale(kk, kk)
        medal(ctx, -300, -10, 0.75, text=num)
        draw_text(ctx, a, 80, -40, 66, font="black", fill="#2E3A4A")
        draw_text(ctx, b, 80, 40, 66, font="black", fill=S.RUST)
        ctx.restore()
    if lt > 1.3:
        draw_text(ctx, "→ 현역 대신 체육요원 복무", 0, 320, 54, font="black", fill="#4F7A9C",
                  alpha=prog(lt, 1.3, 1.6))
    ctx.restore()


def shot_final(ctx, lt, sh, ep):
    S.planks(ctx, base="#2A3240", dark="#222833")
    card(ctx, 540, 760, 920, 900, ease_out_back(prog(lt, 0.05, 0.4), 1.4), fill="#1E2430")
    draw_text(ctx, "아시안게임 결승", 0, -350, 72, font="black", fill="#E8B93E")
    for i, (sport, t_win) in enumerate((("축구", 0.5), ("야구", 0.8))):
        y = -120 + i * 280
        draw_text(ctx, sport, -320, y, 64, font="black", fill="#F3EBD5")
        draw_text(ctx, "한국", -80, y, 72, font="black", fill="#FFFFFF")
        draw_text(ctx, "vs", 90, y, 50, font="black", fill="#8C96A6")
        draw_text(ctx, "일본", 250, y, 72, font="black", fill="#FFFFFF")
        S.stamp(ctx, -80, y + 10, "우승", prog(lt, _frac(sh, 0, t_win), _frac(sh, 0, t_win) + 0.4),
                color="#E8B93E", size=110, rot=-0.15)
    ctx.restore()
    if lt > _frac(sh, 0, 0.85):  # 꽃가루
        S.confetti(ctx, lt, _frac(sh, 0, 0.85))


def _phone(ctx, x, y, lt, k):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(0.06)
    ctx.scale(max(k, 0.01), max(k, 0.01))
    rrect(ctx, -210, -360, 420, 720, 50)
    S.fs(ctx, "#2E2E33", lw=8)
    rrect(ctx, -185, -320, 370, 640, 26)
    S.fs(ctx, "#FFFFFF", lw=0)
    ellipse(ctx, -130, -250, 34, 34)
    S.fs(ctx, "#D9473B", lw=5)
    draw_text(ctx, "선수 SNS", 20, -250, 40, font="black", fill="#2E3A4A")
    rrect(ctx, -160, -190, 320, 230, 18)
    S.fs(ctx, "#F3EBD5", lw=0)
    medal(ctx, 0, -100, 0.6)
    draw_text(ctx, "이제 군대", 0, 110, 52, font="black", fill="#2E3A4A")
    draw_text(ctx, "안 간다~", 0, 175, 52, font="black", fill="#2E3A4A")
    heart = 1 + 0.15 * math.sin(lt * 8)
    draw_text(ctx, "♥ 12.4만", -60, 260, 38, font="jua", fill="#D9473B", scale=heart)
    ctx.restore()


def shot_sns(ctx, lt, sh, ep):
    S.planks(ctx, base="#B9A57A", dark="#9C8960", w=150)
    ATH.draw(ctx, 280, 1830, 1.5, 1, pose="wave" if lt < sh.m(1) else "down",
             expr="smug" if lt < sh.m(1) else "sad", t=lt, sweat=lt >= sh.m(1))
    medal(ctx, 300, 1830 - 330 * 1.5, 0.85, rot=math.sin(lt * 4) * 0.1)
    _phone(ctx, 740, 760, lt, ease_out_back(prog(lt, 0.3, 0.7), 1.6))
    draw_text(ctx, "※ 발언 취지 재구성", 740, 1170, 34, font="black", fill="#5C4E36")
    comments = (("면제가 목표?", 300, 380), ("국가대표 맞아?", 760, 260), ("군인들 생각은?", 330, 560),
                ("실망이야", 820, 1420))
    for j, (txt, x, y) in enumerate(comments):
        bubble(ctx, txt, x, y, ease_out_back(prog(lt, sh.m(1) + j * 0.25, sh.m(1) + j * 0.25 + 0.3), 2.0),
               size=50, fill="#F7D9D4", tail=1 if x < 540 else -1)


def shot_minister(ctx, lt, sh, ep):
    close_up(ctx, lt, sh, ep, MIN, "M", 1, 420, "#4E5A4A", "#3F4A3C", "국방부 장관", 0, calm=True)
    S.stamp(ctx, 760, 620, "궁극적 폐지", prog(lt, sh.m(1) + 0.4, sh.m(1) + 0.9), size=90, rot=0.1)


def shot_bts(ctx, lt, sh, ep):
    S.planks(ctx, base=S.SLATE, dark=S.SLATE_D, seed=4)
    tilt = 0.18 * ease_out_back(prog(lt, 0.3, 1.0), 1.8) * (1 + 0.1 * math.sin(lt * 3))
    cx, cy = 540, 760
    # 받침대
    ctx.new_path()
    ctx.move_to(cx - 30, cy)
    ctx.line_to(cx + 30, cy)
    ctx.line_to(cx + 90, 1180)
    ctx.line_to(cx - 90, 1180)
    ctx.close_path()
    S.fs(ctx, "#B9A57A", lw=8)
    ctx.save()
    ctx.translate(cx, cy)
    ctx.rotate(tilt)  # 체육 쪽(오른쪽)으로 기운 저울
    rrect(ctx, -420, -14, 840, 28, 14)
    S.fs(ctx, "#E8B93E", lw=7)
    ctx.restore()
    ends = []
    for sg in (-1, 1):
        ex = cx + sg * 400 * math.cos(tilt)
        ey = cy + sg * 400 * math.sin(tilt)
        ends.append((ex, ey))
        for dx in (-110, 110):
            ctx.move_to(ex, ey)
            ctx.line_to(ex + dx, ey + 180)
        set_rgb(ctx, S.OUT)
        ctx.set_line_width(6)
        ctx.stroke()
        ellipse(ctx, ex, ey + 190, 130, 30)
        S.fs(ctx, "#C8CDD4", lw=7)
    (lx, ly), (rx, ry) = ends
    SINGER.draw(ctx, lx, ly + 180, 0.42, 1, pose="cheer", expr="neutral", t=lt)
    S.tube(ctx, [(lx + 50, ly - 70), (lx + 70, ly - 10)], 10, "#3A3F4A", lw=5)  # 마이크
    ellipse(ctx, lx + 48, ly - 80, 16, 20)
    S.fs(ctx, "#2E2E33", lw=5)
    ATH2.draw(ctx, rx, ry + 180, 0.42, -1, pose="cheer", expr="smug", t=lt)
    medal(ctx, rx, ry + 180 - 330 * 0.42, 0.35)
    draw_text(ctx, "세계 1위 가수", lx, ly + 260, 46, font="black", fill="#F3EBD5")
    draw_text(ctx, "→ 현역 입대", lx, ly + 320, 44, font="black", fill="#FFC9A8")
    draw_text(ctx, "아시안게임 金", rx, ry + 260, 46, font="black", fill="#F3EBD5")
    draw_text(ctx, "→ 체육요원", rx, ry + 320, 44, font="black", fill="#9FE3DA")
    k = ease_out_back(prog(lt, sh.m(1) + 0.5, sh.m(1) + 0.9), 1.6)
    if k > 0.01:
        card(ctx, 540, 1620, 640, 300, k, rot=-0.03)
        draw_text(ctx, "국민청원", 0, -70, 70, font="black", fill="#2E3A4A")
        draw_text(ctx, "\"BTS도 군대 갔다\"", 0, 40, 52, font="black", fill=S.RUST)
        ctx.restore()


def _people(ctx, x, y, total, got, k, color):
    """사람 아이콘 격자: 혜택받은 수만큼 색칠."""
    cols = 6
    for i in range(total):
        r, c = divmod(i, cols)
        px, py = x + c * 62, y + r * 76
        on = i < got * k
        ellipse(ctx, px, py, 18, 18)
        S.fs(ctx, color if on else "#D5D0C2", lw=5)
        rrect(ctx, px - 22, py + 22, 44, 34, 14)
        S.fs(ctx, color if on else "#D5D0C2", lw=5)


def shot_numbers(ctx, lt, sh, ep):
    S.desk(ctx)
    S.graph_paper(ctx, 60, 120, 960, 1680)
    draw_text(ctx, "2022 항저우 아시안게임", 540, 270, 64, font="black", fill="#2E3A4A")
    draw_text(ctx, "병역 혜택 받은 인원", 540, 360, 50, font="black", fill="#7A8594")
    for i, (sport, total, got, col) in enumerate((("축구", 22, 20, S.RUST), ("야구", 24, 19, "#4F7A9C"))):
        y = 450 + i * 380
        k = ease_out_cubic(prog(lt, 0.5 + i * 0.8, 1.3 + i * 0.8))
        draw_text(ctx, sport, 180, y + 120, 72, font="black", fill="#2E3A4A")
        _people(ctx, 330, y + 20, total, got, k, col)
        draw_text(ctx, f"{round(got * k)} / {total}", 840, y + 150, 64, font="black", fill=col)


def shot_factcheck(ctx, lt, sh, ep):
    S.planks(ctx, base="#B9A57A", dark="#9C8960", w=150)
    S.stamp(ctx, 540, 420, "면제?", prog(lt, 0.3, 0.7), size=150, rot=-0.1)
    kx = ease_out_back(prog(lt, sh.me(0) - 0.3, sh.me(0)), 2.0)
    if kx > 0.01:  # 빨간 X
        ctx.save()
        ctx.translate(540, 420)
        ctx.scale(kx, kx)
        for a in (1, -1):
            ctx.move_to(-200, -120 * a)
            ctx.line_to(200, 120 * a)
        set_rgb(ctx, "#C9473B")
        ctx.set_line_width(30)
        ctx.stroke()
        ctx.restore()
    items = (("기초군사훈련", "입소"), ("34개월", "분야 복무"), ("544시간", "봉사활동"))
    for j, (big, small) in enumerate(items):
        t0 = _frac(sh, 1, 0.15 + j * 0.3)
        k = ease_out_back(prog(lt, t0, t0 + 0.3), 2.0)
        if k <= 0.01:
            continue
        x = 200 + j * 340
        card(ctx, x, 830, 310, 260, k, rot=(j - 1) * 0.04)
        draw_text(ctx, big, 0, -30, 60 if len(big) < 5 else 44, font="black", fill=S.RUST)
        draw_text(ctx, small, 0, 60, 42, font="black", fill="#2E3A4A")
        ctx.restore()


def shot_bill(ctx, lt, sh, ep):
    S.desk(ctx)
    S.paper(ctx, 540, 820, 1.6, "병역법 개정안", rot=-0.02, lines=0)
    rows = (("아시안게임 금메달", "삭제", 0.45, S.RUST), ("올림픽 메달", "유지", 0.85, "#4F7A9C"))
    for i, (name, verdict, f, col) in enumerate(rows):
        y = 700 + i * 220
        draw_text(ctx, name, 470, y, 62, font="black", fill="#2E3A4A")
        t0 = _frac(sh, 0, f)
        if i == 0:  # 취소선
            k = ease_out_cubic(prog(lt, t0 - 0.2, t0 + 0.1))
            if k > 0:
                ctx.move_to(200, y)
                ctx.line_to(200 + 540 * k, y)
                set_rgb(ctx, S.RUST)
                ctx.set_line_width(14)
                ctx.stroke()
        S.stamp(ctx, 830, y, verdict, prog(lt, t0, t0 + 0.4), color=col, size=80, rot=-0.1)


def shot_outro(ctx, lt, sh, ep):
    S.planks(ctx, base=S.SLATE, dark=S.SLATE_D, seed=9)
    waving = lt >= sh.m(1)
    CIT.draw(ctx, 540, 2120, 1.7, 1, pose="wave" if waving else "shrug",
             expr="smug" if waving else "deadpan", t=lt)
    if not waving:
        for j, (txt, x) in enumerate((("유지", 260), ("폐지", 820))):
            bubble(ctx, txt, x, 560, ease_out_back(prog(lt, 0.5 + j * 0.4, 0.8 + j * 0.4), 2.0), size=80,
                   fill="#F3EBD5" if j == 0 else "#F7D9D4", tail=1 if j == 0 else -1)
    label(ctx, "댓글로 알려줘!", 540, 330, ease_out_back(prog(lt, sh.m(1), sh.m(1) + 0.4), 2.0), size=80)
    label(ctx, "구독", 540, 560, ease_out_back(prog(lt, sh.m(1) + 0.8, sh.m(1) + 1.2), 2.0),
          fill=S.RUST, ink="#FFFFFF")


SHOT_FN = {k[5:]: v for k, v in globals().items() if k.startswith("shot_")}
CAMERA = {
    "hook": (540, 1100, 0.08), "rule": (540, 860, 0.05), "final": (540, 760, 0.06),
    "sns": (740, 760, 0.06), "minister": (420, 900, 0.06), "bts": (540, 900, 0.05),
    "numbers": (540, 800, 0.04), "factcheck": (540, 700, 0.06), "bill": (540, 820, 0.05),
    "outro": (540, 1000, 0.04),
}

EP = Explainer(SCRIPT, VOICE, CAP_COLOR, SHOT_FN, CAMERA, cues,
               notice="※ 언론 보도 기반 / 선수 발언은 취지만 재구성했습니다", chapters=CHAPTERS)
render_frame, mix = EP.render_frame, EP.mix


def prepare():
    global DURATION
    DURATION = EP.prepare().duration
