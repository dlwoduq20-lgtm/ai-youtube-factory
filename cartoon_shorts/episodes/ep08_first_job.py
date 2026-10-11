"""오늘의 만평 #08 — 신입인데 경력 있냐고요?  (상황극 오프닝 + 한 줄 질문 + 이음매 없는 루프)

실제 사실 (보도 기준):
- 8월 고용동향(9/9 발표): 청년(15~29세) 고용률 44.1%, 28개월 연속 하락 / 청년 취업자 14만3천 명 감소, 46개월 연속
- 원티드랩 '2026 채용 트렌드 서베이'(인사담당자 153곳): 채용 수요 4~7년 차 49.7%, 1~3년 차 19.6%,
  8~11년 차 17.6%, 신입 12.4%
- 진학사 캐치: 신입 채용공고 2024 상반기 5,753건 → 2026 상반기 2,500건 (56% 감소)
- IT 업계 관계자(서울신문): 테스트 코드·데이터 정리를 AI가 맡아 신입 여러 명보다 숙련자 + AI 도구가 효율적
- 한국은행: 신규 채용 중 청년 비중 36.9%(2014~2019) → 29.3%(2024~2026), 단 청년 고용 부진을 AI 탓으로만 돌리긴 어렵다
엔딩은 투표 카드 없이 한 줄 질문 뒤 첫 장면과 같은 화면으로 끊어 루프시킨다. 개인 이름은 쓰지 않는다.
"""
import math

from .. import squire as S
from ..doodle import Doodle
from ..engine import draw_text, ease_out_back, ease_out_cubic, ellipse, prog, rrect, set_rgb
from ..explainer import Explainer, card, label

TITLE = "신입인데 경력 있냐고요? | 오늘의 만평"
DURATION = 47.0

BOSS = Doodle(coat="#2F3E5C", tie="#7A8594", hair="gray", hair_color="#BDBDBD", glasses=True)
JOB = Doodle(coat="#3A4250", tie="#C9473B", hair="cap", hair_color="#2A2420")
DEV = Doodle(coat="#5C6B7E", hair="tuft", glasses=True, collar=False)

VOICE = {
    "N": ("male", "+80%", "+20Hz", 1.18),
    "I": ("male", "+55%", "-10Hz", 0.92),  # 면접관: 낮고 덤덤하게
    "A": ("male2", "+75%", "+0Hz", 1.2),  # 지원자
    "R": ("male", "+65%", "+0Hz", 1.0),  # IT 업계 관계자
}
CAP_COLOR = {"N": "#FFFFFF", "I": "#C9D3DE", "A": "#9FE3DA", "R": "#FFE38A"}
HOOK_TEXT = "신입인데 경력 있어요?"

SCRIPT = [
    ("hook", [("I", "경력 있으세요?", None),
              ("A", "신입 지원인데요…?", None),
              ("I", "아, 그럼… 혹시 에이아이보다 잘하는 거 있어요?", "아, 그럼… 혹시 AI보다 잘하는 거 있어요?")],
     {"tail": 0.6}),
    ("rate", [("N", "웃기지? 근데 요즘 구직자한텐 꽤 현실이야.", None),
              ("N", "팔 월 청년 고용률 사십사 점 일 퍼센트, 이십팔 개월째 떨어지는 중이야.",
               "8월 청년 고용률 44.1%, 28개월째 떨어지는 중이야.")], {"tail": 0.6}),
    ("jobs", [("N", "청년 취업자는 일 년 새 십사만 명 넘게 줄었어. 사십육 개월 연속 감소야.",
               "청년 취업자는 1년 새 14만 명 넘게 줄었어. 46개월 연속 감소야.")], {"tail": 0.6}),
    ("demand", [("N", "기업이 제일 뽑고 싶은 연차? 사 년에서 칠 년 차가 절반이고, 신입은 십이 점 사 퍼센트뿐이래.",
                 "기업이 제일 뽑고 싶은 연차? 4~7년 차가 절반이고, 신입은 12.4%뿐이래."),
                ("N", "신입 채용공고도 이 년 새 반 넘게 줄었어. 오천칠백오십삼 건에서 이천오백 건으로.",
                 "신입 채용공고도 2년 새 반 넘게 줄었어. 5,753건에서 2,500건으로.")], {"tail": 0.6}),
    ("ai", [("N", "여기에 에이아이까지 왔어. 테스트 코드, 데이터 정리 같은 신입 일을 에이아이가 하니까,",
             "여기에 AI까지 왔어. 테스트 코드, 데이터 정리 같은 신입 일을 AI가 하니까,"),
            ("R", "신입 여러 명보다, 숙련자 한 명에 에이아이 쓰는 게 효율적이죠.",
             "신입 여러 명보다, 숙련자 한 명에 AI 쓰는 게 효율적이죠.")], {"tail": 0.6}),
    ("fact", [("N", "실제로 신규 채용에서 청년 비중은 팬데믹 전 삼십육 점 구 퍼센트에서 이십구 점 삼 퍼센트로 떨어졌어.",
               "실제로 신규 채용에서 청년 비중은 팬데믹 전 36.9%에서 29.3%로 떨어졌어."),
              ("N", "다만 한국은행은, 청년 취업난을 전부 에이아이 탓으로 돌리긴 어렵다고 선을 그었어.",
               "다만 한국은행은, 청년 취업난을 전부 AI 탓으로 돌리긴 어렵다고 선을 그었어.")], {"tail": 0.6}),
    ("wheel", [("N", "경력을 쌓으려면 일을 해야 하는데, 일을 하려면 경력이 있어야 하는 거지.", None),
               ("N", "이거, 에이아이 탓일까, 기업 탓일까?", "이거, AI 탓일까, 기업 탓일까?")], {"tail": 0.2}),
    ("loop", [], {"tail": 0, "min_tail": 0.45, "cut": True}),  # 첫 프레임과 같은 화면 → 자동 재생 시 이음매 없이 처음으로
]

CHAPTERS = [("상황", "hook"), ("현실", "rate"), ("원인", "ai"), ("결론", "fact")]


def cues(ep):
    c = [(st + 0.05, "stamp") for st in ep.chapter_starts()[1:-1]]
    for i, sh in enumerate(ep.shots):
        st = sh.start
        if i > 0 and sh.name != "loop":
            c.append((st, "whoosh"))
        if sh.name == "hook":
            c.append((st + sh.at(2, "에이아이"), "ding"))
        if sh.name == "rate":
            c.append((st + sh.at(1, "사십사"), "stamp"))
        if sh.name == "jobs":
            c.append((st + sh.at(0, "십사만"), "fall"))
            c.append((st + sh.at(0, "사십육"), "stamp"))
        if sh.name == "demand":
            c.append((st + sh.at(0, "사 년"), "pop"))
            c.append((st + sh.at(0, "신입은"), "pop"))
            c.append((st + sh.at(1, "오천"), "pop"))
            c.append((st + sh.at(1, "이천오백"), "fall"))
        if sh.name == "ai":
            c.append((st + sh.at(0, "테스트"), "slide"))
            c.append((st + sh.at(0, "데이터"), "slide"))
            c.append((st + sh.m(1), "pop"))
        if sh.name == "fact":
            c.append((st + sh.at(0, "이십구"), "fall"))
            c.append((st + sh.at(1, "선을"), "stamp"))
        if sh.name == "wheel":
            c.append((st + 0.3, "boing"))
            c.append((st + sh.at(1, "에이아이"), "pop"))
            c.append((st + sh.at(1, "기업"), "pop"))
    return c


# ---------------------------------------------------------------- 소품
def robot(ctx, x, y, s, t, glow=0.0):
    """AI 로봇 (네모 화면 얼굴 + 안테나)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.move_to(0, -150)
    ctx.line_to(0, -200)
    set_rgb(ctx, S.OUT)
    ctx.set_line_width(8)
    ctx.stroke()
    ellipse(ctx, 0, -210, 16, 16)
    S.fs(ctx, "#E8B93E" if glow > 0.5 else "#C9473B", lw=5)
    rrect(ctx, -110, -150, 220, 170, 40)
    S.fs(ctx, "#D8DDE4", lw=8)
    rrect(ctx, -85, -125, 170, 120, 26)
    S.fs(ctx, "#2E3A4A", lw=5)
    blink = (t * 0.7) % 1 > 0.92
    for ex in (-35, 35):
        if blink:
            ctx.move_to(ex - 14, -65)
            ctx.line_to(ex + 14, -65)
            set_rgb(ctx, "#9FE3DA")
            ctx.set_line_width(6)
            ctx.stroke()
        else:
            ellipse(ctx, ex, -65, 14, 18)
            set_rgb(ctx, "#9FE3DA")
            ctx.fill()
    rrect(ctx, -80, 30, 160, 130, 30)  # 몸통
    S.fs(ctx, "#C6CCD4", lw=8)
    if glow > 0:
        ellipse(ctx, 0, -40, 200 * (1 + glow * 0.2), 160 * (1 + glow * 0.2))
        set_rgb(ctx, "#9FE3DA", 0.25 * glow)
        ctx.fill()
    ctx.restore()


def laptop(ctx, x, y, s, t, glow):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rrect(ctx, -130, -170, 260, 170, 14)
    S.fs(ctx, "#3A3F4A", lw=7)
    rrect(ctx, -115, -155, 230, 140, 8)
    S.fs(ctx, "#2E3A4A" if glow < 0.5 else "#3E5A6E", lw=0)
    draw_text(ctx, "AI", 0, -85, 70, font="black", fill="#9FE3DA" if (t * 2) % 1 > 0.3 or glow else "#5E8A90")
    rrect(ctx, -160, -6, 320, 22, 8)
    S.fs(ctx, "#B9BEC6", lw=6)
    ctx.restore()


def room(ctx, lt, sh, ep, frozen=False):
    """면접장: 면접관(오른쪽, 책상 뒤) + 노트북 AI, 지원자(왼쪽)."""
    S.planks(ctx, base="#C9C2B0", dark="#B5AD99", w=150)
    rrect(ctx, 300, 300, 480, 260, 12)  # 창문
    S.fs(ctx, "#BFD7EA", lw=8)
    ctx.move_to(540, 300)
    ctx.line_to(540, 560)
    set_rgb(ctx, S.OUT)
    ctx.set_line_width(8)
    ctx.stroke()
    q = (not frozen) and lt >= sh.m(2)
    shocked = (not frozen) and lt >= sh.at(2, "에이아이") + 0.2
    mi = 0 if frozen else ep.mouth("I", sh.start + lt)
    ma = 0 if frozen else ep.mouth("A", sh.start + lt)
    JOB.draw(ctx, 280, 1460, 1.05, 1, pose="shrug" if shocked else "down",
             expr="shock" if shocked else ("smug" if (not frozen and sh.m(1) <= lt < sh.m(2)) else "neutral"),
             mouth=ma * 1.3, t=0 if frozen else lt, sweat=shocked, bob=not frozen)
    BOSS.draw(ctx, 790, 1460, 1.05, -1, pose="hips", expr="deadpan", mouth=mi * 1.3,
              t=0 if frozen else lt, bob=False)
    rrect(ctx, 560, 1080, 480, 70, 10)  # 면접관 책상
    S.fs(ctx, "#8C6A4A", lw=8)
    rrect(ctx, 590, 1150, 420, 300, 0)
    S.fs(ctx, "#7A5C40", lw=8)
    glow = prog(lt, sh.at(2, "에이아이"), sh.at(2, "에이아이") + 0.3) if q else 0.0
    laptop(ctx, 690, 1080, 0.8, 0 if frozen else lt, glow)
    draw_text(ctx, HOOK_TEXT, 540, 230, 96, font="black", fill="#FFFFFF", stroke=14, stroke_fill="#1E1E22")


# ---------------------------------------------------------------- 샷 그리기
def shot_hook(ctx, lt, sh, ep):
    room(ctx, lt, sh, ep)


def shot_loop(ctx, lt, sh, ep):
    room(ctx, 0.0, ep.shots[0], ep, frozen=True)  # 영상 첫 프레임과 같은 화면


def shot_rate(ctx, lt, sh, ep):
    S.desk(ctx)
    S.graph_paper(ctx, 60, 200, 960, 1000)
    draw_text(ctx, "청년(15~29세) 고용률", 540, 290, 58, font="black", fill="#2E3A4A")
    k = prog(lt, 0.3, sh.at(1, "이십팔") + 0.3)
    n = 29
    pts = []
    for i in range(n):
        x = 130 + i * (820 / (n - 1))
        y = 460 + i * 15 + 22 * math.sin(i * 1.7)
        pts.append((x, y))
    m = max(2, int(n * k))
    ctx.move_to(*pts[0])
    for p in pts[1:m]:
        ctx.line_to(*p)
    set_rgb(ctx, S.RUST)
    ctx.set_line_width(12)
    ctx.stroke()
    if m > 1:
        ellipse(ctx, *pts[m - 1], 16, 16)
        S.fs(ctx, S.RUST, lw=5)
    t44 = sh.at(1, "사십사")
    k1 = ease_out_back(prog(lt, t44, t44 + 0.35), 2.0)
    if k1 > 0.01:
        label(ctx, "8월 44.1%", 420, 990, k1, fill="#FBF7EC", ink=S.RUST, size=70)
    S.stamp(ctx, 620, 1120, "28개월 연속 ↓", prog(lt, sh.at(1, "이십팔"), sh.at(1, "이십팔") + 0.45), size=72,
            rot=-0.05)


def shot_jobs(ctx, lt, sh, ep):
    S.planks(ctx, base=S.SLATE, dark=S.SLATE_D, seed=3)
    t14 = sh.at(0, "십사만")
    gone = prog(lt, t14, t14 + 1.2)
    for i in range(24):  # 사람 아이콘이 뒤에서부터 사라짐
        r, c = divmod(i, 6)
        x, y = 210 + c * 132, 380 + r * 150
        a = 1.0 if i < 24 - int(10 * gone) else 0.18
        ellipse(ctx, x, y, 30, 30)
        S.fs(ctx, "#F3EBD5", lw=6, alpha=a)
        rrect(ctx, x - 38, y + 36, 76, 60, 24)
        S.fs(ctx, "#F3EBD5", lw=6, alpha=a)
    k = ease_out_back(prog(lt, t14, t14 + 0.35), 1.8)
    if k > 0.01:
        label(ctx, "청년 취업자 -14만3천 명", 520, 1000, k, fill="#FBF7EC", ink=S.RUST, size=60)
    t46 = sh.at(0, "사십육")
    S.stamp(ctx, 520, 1140, "46개월 연속 감소", prog(lt, t46, t46 + 0.45), size=74, rot=-0.05)


def shot_demand(ctx, lt, sh, ep):
    S.desk(ctx)
    if lt < sh.m(1):
        k = ease_out_back(prog(lt, 0.05, 0.4), 1.4)
        card(ctx, 520, 680, 820, 900, k, rot=-0.01)
        draw_text(ctx, "기업이 뽑고 싶은 연차", 0, -360, 58, font="black", fill="#2E3A4A")
        draw_text(ctx, "(인사담당자 153곳 조사)", 0, -290, 36, font="jua", fill="#7A8594")
        bars = (("신입", 12.4, "신입은"), ("1~3년", 19.6, "사 년"), ("4~7년", 49.7, "사 년"), ("8~11년", 17.6, "사 년"))
        for j, (name, v, word) in enumerate(bars):
            y = -170 + j * 140
            t0 = sh.at(0, word)
            kb = ease_out_cubic(prog(lt, t0, t0 + 0.45))
            hi = name in ("신입", "4~7년")
            draw_text(ctx, name, -300, y, 46, font="black", fill="#2E3A4A")
            w = 480 * v / 50 * kb
            rrect(ctx, -210, y - 32, max(w, 1), 64, 14)
            S.fs(ctx, (S.RUST if name == "신입" else "#4F7A9C") if hi else "#9AA3AE", lw=6)
            if kb > 0.05:
                draw_text(ctx, f"{v * kb:.1f}%", -190 + w + 70, y, 44, font="black", fill="#2E3A4A")
        ctx.restore()
        return
    k = ease_out_back(prog(lt, sh.m(1), sh.m(1) + 0.4), 1.4)
    card(ctx, 520, 680, 820, 700, k, rot=0.01)
    draw_text(ctx, "신입 채용공고 (상반기)", 0, -260, 56, font="black", fill="#2E3A4A")
    t1, t2 = sh.at(1, "오천"), sh.at(1, "이천오백")
    draw_text(ctx, "2024년  5,753건", 0, -100, 64, font="black", fill="#4F7A9C",
              scale=max(0.01, ease_out_back(prog(lt, t1, t1 + 0.3), 2.0)))
    draw_text(ctx, "↓", 0, 20, 80, font="black", fill="#2E3A4A", alpha=prog(lt, t2 - 0.2, t2))
    draw_text(ctx, "2026년  2,500건", 0, 140, 64, font="black", fill=S.RUST,
              scale=max(0.01, ease_out_back(prog(lt, t2, t2 + 0.3), 2.0)))
    ctx.restore()
    S.stamp(ctx, 540, 1180, "-56%", prog(lt, t2 + 0.4, t2 + 0.8), size=110, rot=-0.08)


def shot_ai(ctx, lt, sh, ep):
    S.planks(ctx, base="#C9C2B0", dark="#B5AD99", w=150)
    rrect(ctx, 80, 900, 900, 60, 10)  # 신입 책상
    S.fs(ctx, "#8C6A4A", lw=8)
    tasks = (("테스트 코드", "테스트"), ("데이터 정리", "데이터"))
    for j, (name, word) in enumerate(tasks):
        t0 = sh.at(0, word)
        k = ease_out_cubic(prog(lt, t0, t0 + 0.6))
        x = 260 + j * 200 + 300 * k  # 서류가 로봇 쪽으로 쓱
        rrect(ctx, x - 110, 760 - j * 40, 220, 140, 10)
        S.fs(ctx, "#FBF7EC", lw=6)
        draw_text(ctx, name, x, 830 - j * 40, 38, font="black", fill="#2E3A4A")
    robot(ctx, 790, 700, 0.95, lt, glow=prog(lt, sh.at(0, "에이아이가"), sh.at(0, "에이아이가") + 0.3))
    JOB.draw(ctx, 230, 1440, 0.9, 1, pose="shrug", expr="sad" if lt > sh.at(0, "데이터") else "neutral", t=lt)
    if lt >= sh.m(1):
        k = ease_out_back(prog(lt, sh.m(1), sh.m(1) + 0.35), 1.6)
        DEV.draw(ctx, 700, 1440, 0.85, -1, pose="hips", expr="smug", mouth=ep.mouth("R", sh.start + lt) * 1.3, t=lt)
        label(ctx, "IT 업계 관계자", 560, 330, k, size=56)
        draw_text(ctx, "※ 보도된 업계 발언 취지", 560, 420, 34, font="black", fill="#5C4E36", alpha=min(1, k))


def shot_fact(ctx, lt, sh, ep):
    S.desk(ctx)
    k = ease_out_back(prog(lt, 0.05, 0.4), 1.4)
    card(ctx, 520, 650, 820, 760, k, rot=-0.01)
    draw_text(ctx, "신규 채용 중 청년 비중", 0, -290, 56, font="black", fill="#2E3A4A")
    t2 = sh.at(0, "이십구")
    for j, (name, v, t0, col) in enumerate((("팬데믹 전", 36.9, 0.3, "#4F7A9C"), ("2024~2026", 29.3, t2, S.RUST))):
        x = -170 + j * 340
        kb = ease_out_cubic(prog(lt, t0, t0 + 0.5))
        h = 420 * v / 40 * kb
        rrect(ctx, x - 90, 240 - h, 180, h, 12)
        S.fs(ctx, col, lw=7)
        draw_text(ctx, f"{v * kb:.1f}%", x, 240 - h - 50, 52, font="black", fill=col)
        draw_text(ctx, name, x, 290, 40, font="black", fill="#2E3A4A")
    ctx.restore()
    ts = sh.at(1, "선을")
    S.stamp(ctx, 540, 1150, "한국은행: AI 탓만은 아님", prog(lt, ts, ts + 0.45), size=60, rot=-0.05)


def shot_wheel(ctx, lt, sh, ep):
    S.planks(ctx, base=S.SLATE, dark=S.SLATE_D, seed=8)
    cx, cy, r = 520, 820, 330
    spin = lt * 2.4
    ellipse(ctx, cx, cy, r, r)  # 쳇바퀴
    S.fs(ctx, None, lw=0)
    set_rgb(ctx, S.OUT)
    ctx.set_line_width(26)
    ctx.stroke()
    ellipse(ctx, cx, cy, r, r)
    set_rgb(ctx, "#E8B93E")
    ctx.set_line_width(14)
    ctx.stroke()
    for i in range(12):
        a = spin + i * math.pi / 6
        ctx.move_to(cx + math.cos(a) * (r - 20), cy + math.sin(a) * (r - 20))
        ctx.line_to(cx + math.cos(a) * (r + 20), cy + math.sin(a) * (r + 20))
    set_rgb(ctx, S.OUT)
    ctx.set_line_width(8)
    ctx.stroke()
    for name, a0 in (("경력", 0.0), ("일", math.pi)):  # 바퀴를 따라 도는 글자
        a = spin + a0
        draw_text(ctx, name, cx + math.cos(a) * (r + 90), cy + math.sin(a) * (r + 90), 64, font="black",
                  fill="#F3EBD5", stroke=10, stroke_fill="#1E1E22")
    JOB.draw(ctx, cx, cy + r - 16, 0.62, 1, pose="flail", expr="shock", t=lt * 2, sweat=True)
    if lt >= sh.m(1):
        ta, tb = sh.at(1, "에이아이"), sh.at(1, "기업")
        label(ctx, "AI 탓?", 290, 330, ease_out_back(prog(lt, ta, ta + 0.3), 2.0), fill="#DCE6F2", size=70)
        label(ctx, "기업 탓?", 740, 330, ease_out_back(prog(lt, tb, tb + 0.3), 2.0), fill="#F7D9D4", size=70)


SHOT_FN = {k[5:]: v for k, v in globals().items() if k.startswith("shot_")}
CAMERA = {
    "hook": (540, 1000, 0.0), "loop": (540, 1000, 0.0), "rate": (540, 700, 0.05), "jobs": (520, 700, 0.05),
    "demand": (520, 700, 0.04), "ai": (540, 900, 0.05), "fact": (520, 650, 0.05), "wheel": (520, 820, 0.06),
}

EP = Explainer(SCRIPT, VOICE, CAP_COLOR, SHOT_FN, CAMERA, cues,
               notice="※ 통계청·한국은행·채용 조사·언론 보도 기반", chapters=CHAPTERS)
render_frame, mix = EP.render_frame, EP.mix


def prepare():
    global DURATION
    DURATION = EP.prepare().duration
