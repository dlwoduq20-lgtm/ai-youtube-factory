"""오늘의 만평 #03 — 결혼에도 자격증이 필요해?  (해설 애니메이션 스타일 + TTS)

실제 화제: 중국 푸단대의 72세 교수가 3년 전 인터뷰에서 "적어도 3분의 1은 결혼에 적합하지 않다"
(결혼엔 경제력뿐 아니라 돌봄·희생 능력이 필요, 연애 시작 적정 나이 40세)고 한 영상이 2026년 9월 말
중국 SNS에서 재확산되며 논쟁 (SCMP 등 보도). 중국 상반기 혼인신고 7.5% 감소.
한국 수치: PMI '2026 웨딩 인식 조사' 미혼 500명 중 스몰웨딩 선호 55.2%, 노웨딩 13.4%.
개인 이름은 쓰지 않는다.
"""
import math

from .. import squire as S
from ..engine import draw_text, ease_out_back, ease_out_cubic, prog, rrect, set_rgb
from ..explainer import Explainer, close_up, label

TITLE = "오늘의 만평 #03 - 결혼에도 자격증이 필요해?"
DURATION = 37.0

PROF = S.Person(coat="#7A6248", tie="#8C3B3B", hair="part", hair_color="#DADADA", glasses=True)
GUY = S.Person(coat="#5C7A8C", hair="part", hair_color="#3A2A20", hood=True, pants="#34404F")
GIRL = S.Person(coat="#7A5C8C", hair="bob", hair_color="#3A2A24", hood=True, pants="#4A4250")
CIT = S.Person(coat="#6F7F63", hair="beanie", hood=True, pants="#3D4656")

# 화자 → (edge 음성, 속도, 피치, 추가 피치 배율)
VOICE = {
    "N": ("male", "+80%", "+20Hz", 1.18),
    "P": ("male2", "+40%", "-10Hz", 0.86),  # 교수: 혼자 느리고 낮게 (대비 개그)
    "Y": ("male2", "+85%", "+0Hz", 1.25),
    "W": ("female", "+80%", "+30Hz", 1.15),
}
CAP_COLOR = {"N": "#FFFFFF", "P": "#FFE38A", "Y": "#9FE3DA", "W": "#FFC9A8"}

# (샷 이름, [(화자, TTS 문장, 자막 문장 or None)], 옵션)
SCRIPT = [
    ("hook", [("N", "결혼에도 자격증이 필요하다고?!", None)], {"tail": 0.8}),
    ("prof", [("N", "중국의 일흔두 살 교수 왈,", "중국의 72살 교수 왈,"),
              ("P", "적어도 삼분의 일은, 결혼에 적합하지 않습니다.",
               "적어도 3분의 1은, 결혼에 적합하지 않습니다.")], {"tail": 0.6}),
    ("reqs", [("N", "결혼엔 돈뿐 아니라, 상대를 돌보고 희생하는 능력이 필요하다는 거야.", None)],
     {"tail": 0.8}),
    ("age", [("N", "그럼 연애 시작하기 좋은 나이는?", None), ("N", "무려,", None),
             ("N", "마흔 살!", None)], {"tail": 1.6}),
    ("pro", [("N", "삼 년 전 인터뷰가 다시 퍼지면서, 반응은 둘로 갈렸어.",
              "3년 전 인터뷰가 다시 퍼지면서, 반응은 둘로 갈렸어."),
             ("Y", "이기적인 사람은 결혼 안 하는 게 맞지!", None)], {"tail": 0.4}),
    ("con", [("W", "결혼이 희생이라니, 너무 구시대적이야!", None)], {"tail": 0.6}),
    ("drop", [("N", "실제로 중국은 올해 상반기 혼인신고가 칠 점 오 퍼센트 줄었대.",
               "실제로 중국은 올해 상반기 혼인신고가 7.5% 줄었대.")], {"tail": 0.8}),
    ("korea", [("N", "한국은? 미혼 절반 넘게 스몰웨딩, 열 명 중 한 명 넘게는 아예 노웨딩!", None)],
     {"tail": 1.2}),
    ("outro", [("N", "결혼 자격, 진짜 따로 있는 걸까?", None),
               ("N", "너희 생각은? 댓글로 알려줘!", None)], {"tail": 2.0}),
]

AGES = ["20세", "25세", "30세", "35세", "40세"]
REQS = ["경제력", "돌봄 능력", "희생 능력"]
BARS = [("스몰웨딩", 55.2), ("대규모 예식", 18.8), ("노웨딩", 13.4), ("이색 예식", 11.6)]


def _age_flips(sh):
    t0 = sh.m(0) + 0.15
    span = (sh.me(1) - sh.m(0)) * 0.95
    n = len(AGES) - 1
    return [(t0 + span * j / n, AGES[j], AGES[j + 1]) for j in range(n)]


def _req_times(sh):
    a, b = sh.m(0) + 0.3, sh.me(0) - 0.2
    return [a + (b - a) * (i + 1) / len(REQS) for i in range(len(REQS))]


def cues(ep):
    c = []
    for i, sh in enumerate(ep.shots):
        st = sh.start
        if i > 0:
            c.append((st, "whoosh"))
        if sh.name == "hook":
            c.append((st + 0.3, "thud"))
            c.append((st + sh.me(0) - 0.1, "stamp"))
        if sh.name == "prof":
            c.append((st + 0.25, "slide"))
            c.append((st + sh.m(1), "pop"))
        if sh.name == "reqs":
            for t in _req_times(sh):
                c.append((st + t, "pop"))
        if sh.name == "age":
            for ft, *_ in _age_flips(sh):
                c.append((st + ft, "rip"))
            c.append((st + sh.m(2), "stamp"))
        if sh.name in ("pro", "con"):
            c.append((st + 0.25, "slide"))
            c.append((st + sh.m(len(sh.lines) - 1), "pop"))
        if sh.name == "drop":
            c.append((st + 0.35, "fall"))
            c.append((st + sh.me(0) - 0.4, "stamp"))
        if sh.name == "korea":
            for k in range(len(BARS)):
                c.append((st + 0.5 + k * 0.3, "pop"))
        if sh.name == "outro":
            c.append((st + sh.m(1), "pop"))
            c.append((st + sh.m(1) + 0.8, "ding"))
    return c


# ---------------------------------------------------------------- 샷 그리기
def shot_hook(ctx, lt, sh, ep):
    S.planks(ctx, base="#B9A57A", dark="#9C8960", w=150)
    S.spotlight(ctx, 540, -50, 300, 1150, 1600, alpha=0.25)
    k = max(0.01, ease_out_back(prog(lt, 0.05, 0.45), 1.6))
    ctx.save()
    ctx.translate(540, 900)
    ctx.rotate(-0.06 + 0.04 * math.sin(lt * 3))
    ctx.scale(k, k)
    rrect(ctx, -380, -250, 760, 500, 30)
    S.fs(ctx, "#FBF7EC", lw=10)
    rrect(ctx, -380, -250, 760, 120, 30)
    S.fs(ctx, "#C9473B", lw=10)
    draw_text(ctx, "결혼 자격증", 0, -190, 80, font="black", fill="#FFFFFF")
    rrect(ctx, -330, -90, 220, 280, 14)  # 사진 칸
    S.fs(ctx, "#E3DCC8", lw=6)
    draw_text(ctx, "?", -220, 50, 160, font="black", fill="#9C8960")
    for i, (a, b) in enumerate((("이름", "○○○"), ("경제력", "?"), ("희생력", "?"))):
        draw_text(ctx, f"{a}: {b}", 130, -40 + i * 85, 54, font="jua", fill="#2E3A4A")
    ctx.restore()
    S.stamp(ctx, 620, 1010, "자격 미달?", prog(lt, sh.me(0) - 0.1, sh.me(0) + 0.4), size=110, rot=-0.12)


def shot_prof(ctx, lt, sh, ep):
    close_up(ctx, lt, sh, ep, PROF, "P", 1, 420, "#6B5A48", "#56483A", "중국 72세 교수", 1, calm=True)


def shot_pro(ctx, lt, sh, ep):
    close_up(ctx, lt, sh, ep, GUY, "Y", 1, 420, S.SLATE, S.SLATE_D, "공감파", 1)


def shot_con(ctx, lt, sh, ep):
    close_up(ctx, lt, sh, ep, GIRL, "W", -1, 660, "#B9A57A", "#9C8960", "반박파", 0)


def shot_reqs(ctx, lt, sh, ep):
    S.desk(ctx)
    S.paper(ctx, 540, 880, 1.55, "결혼 필수 능력", rot=-0.03, lines=0)
    for i, (name, t) in enumerate(zip(REQS, _req_times(sh))):
        y = 700 + i * 170
        rrect(ctx, 250, y - 50, 100, 100, 14)
        S.fs(ctx, "#FFFFFF", lw=7)
        draw_text(ctx, name, 600, y, 84, font="black", fill="#2E3A4A")
        k = ease_out_back(prog(lt, t, t + 0.25), 2.0)
        if k > 0.01:  # 체크 표시
            ctx.save()
            ctx.translate(300, y)
            ctx.scale(k, k)
            ctx.move_to(-35, 0)
            ctx.line_to(-8, 30)
            ctx.line_to(45, -40)
            set_rgb(ctx, S.RUST)
            ctx.set_line_width(18)
            ctx.stroke()
            ctx.restore()


def shot_age(ctx, lt, sh, ep):
    S.planks(ctx, base=S.SLATE, dark=S.SLATE_D, seed=7)
    flips = _age_flips(sh)
    cur = AGES[0]
    for ft, a, b in flips:
        if lt >= ft:
            cur = b
    sub = "연애 시작 적정 나이"
    S.calendar(ctx, 560, 1000, 1.0, cur, sub, seed=len(cur))
    for i, (ft, a, b) in enumerate(flips):
        k = (lt - ft) / 0.9
        if 0 <= k < 1:
            S.flying_page(ctx, 560, 1000, 1.0, k, a, sub, seed=i, direction=-1 if i % 3 else 1)
    S.stamp(ctx, 560, 1080, "40세?!", prog(lt, sh.m(2), sh.m(2) + 0.5), size=170, rot=-0.15)


def shot_drop(ctx, lt, sh, ep):
    S.desk(ctx)
    S.graph_paper(ctx, 60, 120, 960, 1680)
    draw_text(ctx, "중국 혼인신고", 540, 260, 96, font="black", fill="#2E3A4A", rot=-0.03)
    draw_text(ctx, "올해 상반기", 540, 380, 60, font="black", fill="#7A8594")
    k = ease_out_cubic(prog(lt, 0.3, 1.3))
    ctx.save()
    ctx.translate(540, 470)
    ctx.rotate(math.pi)  # 아래로 꽂히는 화살표
    S.big_arrow(ctx, 0, 0, 0.9, 0.2 + 0.8 * k, color="#4F7A9C", with_hand=False)
    ctx.restore()
    S.stamp(ctx, 540, 1050, "-7.5%", prog(lt, sh.me(0) - 0.4, sh.me(0) + 0.1), size=170, rot=-0.1)


def shot_korea(ctx, lt, sh, ep):
    S.desk(ctx)
    S.graph_paper(ctx, 60, 120, 960, 1680)
    draw_text(ctx, "한국 미혼이 원하는", 540, 250, 76, font="black", fill="#2E3A4A")
    draw_text(ctx, "결혼식은?", 540, 350, 76, font="black", fill="#2E3A4A")
    for i, (name, v) in enumerate(BARS):
        y = 560 + i * 170
        k = ease_out_cubic(prog(lt, 0.5 + i * 0.3, 1.2 + i * 0.3))
        draw_text(ctx, name, 120, y - 55, 52, font="black", fill="#2E3A4A", anchor=(0, 0.5))
        w = 760 * v / 60 * k
        rrect(ctx, 120, y - 20, max(w, 1), 70, 14)
        S.fs(ctx, S.RUST if i in (0, 2) else "#9AA3AE", lw=6)
        if k > 0.05:
            draw_text(ctx, f"{v * k:.1f}%", 140 + w, y + 15, 52, font="black", fill="#2E3A4A",
                      anchor=(0, 0.5))
    draw_text(ctx, "PMI '2026 웨딩 인식 조사' 미혼 500명", 540, 1700, 40, font="jua", fill="#7A8594")


def shot_outro(ctx, lt, sh, ep):
    S.planks(ctx, base=S.SLATE, dark=S.SLATE_D, seed=9)
    waving = lt >= sh.m(1)
    CIT.draw(ctx, 540, 2060, 2.0, 1, pose="wave" if waving else "shrug",
             expr="neutral" if waving else "deadpan", t=lt)
    label(ctx, "댓글로 알려줘!", 540, 330, ease_out_back(prog(lt, sh.m(1), sh.m(1) + 0.4), 2.0), size=80)
    label(ctx, "구독", 540, 560, ease_out_back(prog(lt, sh.m(1) + 0.8, sh.m(1) + 1.2), 2.0),
           fill=S.RUST, ink="#FFFFFF")


SHOT_FN = {k[5:]: v for k, v in globals().items() if k.startswith("shot_")}
CAMERA = {  # 샷별 켄 번스 (초점 x, y, 줌 증가량)
    "hook": (540, 950, 0.1), "prof": (420, 900, 0.06), "reqs": (540, 900, 0.06),
    "age": (560, 1000, 0.08), "pro": (420, 900, 0.06), "con": (660, 900, 0.06),
    "drop": (540, 900, 0.06), "korea": (540, 800, 0.05), "outro": (540, 1000, 0.04),
}

EP = Explainer(SCRIPT, VOICE, CAP_COLOR, SHOT_FN, CAMERA, cues,
               notice="※ 언론 보도(SCMP 등)·PMI 조사 기반 / 발언은 3년 전 인터뷰 재확산")
render_frame, mix = EP.render_frame, EP.mix


def prepare():
    global DURATION
    DURATION = EP.prepare().duration
