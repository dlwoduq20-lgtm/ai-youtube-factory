"""오늘의 만평 #09 — 내 연봉을 어떻게 알아?  (상황극 오프닝 + 실용 팁 + 한 줄 질문 + 이음매 없는 루프)

실제 사실 (2026년 9월 말~10월 초 보도·금융당국 발표):
- 신한은행: 고객 약 2만5천 명 이름·전화번호·연소득·대출 산출한도 등 유출, 9/30 당국 신고, 행장 "손해 전액 보상"
- 6개 은행 웹 로그에서 AI 침투 테스트 도구(ARTEX) 흔적 — 금융보안원: AI 자율 공격이 아니라 공격자가 도구를 이용
- 국민은행 공격 9/27 23:19부터 약 43시간
- 한전 직원 2만4천여 명 정보 외부 노출(긴급 삭제), 초대형 교회 2곳 교인 정보 최대 100만 건 유출 가능성(보안업체 분석)
- 비밀번호·OTP 유출 없음, 고객 자금 피해 확인 안 됨(10/6 기준). 금융당국 소비자경보 '주의', 1개월 특별대응
- 행동요령: 내 정보를 알아도 믿지 말 것 / 선입금·앱 설치 요구는 사기 / 확인은 공식 앱·대표번호
첫 장면의 금액은 상황극용 가상 숫자다. 개인 이름은 쓰지 않는다.
"""
import math

from .. import squire as S
from ..doodle import Doodle
from ..engine import H, W, draw_text, ease_out_back, ease_out_cubic, ellipse, prog, rrect, set_rgb
from ..explainer import Explainer, card, label

TITLE = "내 연봉을 어떻게 알아? | 오늘의 만평"
DURATION = 47.0

ME = Doodle(coat="#7A8FB0", hair="cap", hair_color="#2A2420", collar=False, pants="#5C6B7E")
CROOK = Doodle(coat="#2A2A30", tie="#55585F", hair="cap", hair_color="#111114", glasses=True)
HACKER = Doodle(coat="#23262D", hair="beanie", hair_color="#3A3F4A", collar=False)

VOICE = {
    "N": ("male", "+80%", "+20Hz", 1.18),
    "S": ("male2", "+65%", "+0Hz", 1.02),  # 사기범: 능글맞게
    "P": ("female", "+75%", "+20Hz", 1.12),  # 주인공
}
CAP_COLOR = {"N": "#FFFFFF", "S": "#F7A8A0", "P": "#9FE3DA"}
HOOK_TEXT = "내 연봉을 어떻게 알아?"

SCRIPT = [
    ("hook", [("S", "고객님, 연 소득 사천이백만 원에, 대출 한도 오천까지 나오시네요?",
               "고객님, 연 소득 4,200만 원에, 대출 한도 5천까지 나오시네요?"),
              ("P", "…제 연봉을 어떻게 아세요?", None),
              ("S", "저희가 다 알고 있죠. 일단 기존 대출부터 갚으시고요.", None)], {"tail": 0.5}),
    ("domino", [("N", "요즘 이런 전화, 진짜 조심해야 돼. 구월 말부터 은행들이 줄줄이 해킹당했거든.",
                 "요즘 이런 전화, 진짜 조심해야 돼. 9월 말부터 은행들이 줄줄이 해킹당했거든.")], {"tail": 0.5}),
    ("leak", [("N", "신한은행에선 이만 오천 명의 이름, 전화번호에 연 소득, 대출 한도까지 빠져나갔어.",
               "신한은행에선 2만 5천 명의 이름, 전화번호에 연 소득, 대출 한도까지 빠져나갔어.")], {"tail": 0.6}),
    ("hacker", [("N", "해커는 에이아이 해킹 도구를 썼고, 국민은행엔 사십삼 시간 동안 공격이 이어졌대.",
                 "해커는 AI 해킹 도구를 썼고, 국민은행엔 43시간 동안 공격이 이어졌대.")], {"tail": 0.6}),
    ("fire", [("N", "불똥은 은행 밖으로 번졌어. 한전에선 직원 이만 사천 명 정보가 노출됐고,",
               "불똥은 은행 밖으로 번졌어. 한전에선 직원 2만 4천 명 정보가 노출됐고,"),
              ("N", "초대형 교회 두 곳은 교인 정보 최대 백만 건 유출 가능성까지 나왔어.",
               "초대형 교회 두 곳은 교인 정보 최대 100만 건 유출 가능성까지 나왔어.")], {"tail": 0.6}),
    ("check", [("N", "다행히 비밀번호랑 오티피는 안 털렸고, 아직 돈이 빠져나간 피해는 확인되지 않았어.",
                "다행히 비밀번호랑 OTP는 안 털렸고, 아직 돈이 빠져나간 피해는 확인되지 않았어.")], {"tail": 0.5}),
    ("tips", [("N", "그래서 딱 세 가지만 기억해.", None),
              ("N", "내 정보를 줄줄 읊어도 믿지 마. 선입금이나 앱 설치 요구는 무조건 사기야.", None),
              ("N", "확인은 문자 링크 말고, 은행 공식 앱이나 대표번호로.", None),
              ("N", "근데 털린 건 은행인데, 왜 조심은 우리가 해야 하지?", None)], {"tail": 0.2}),
    ("loop", [], {"tail": 0, "min_tail": 0.45, "cut": True}),
]

CHAPTERS = [("상황", "hook"), ("사건", "domino"), ("확산", "fire"), ("대처", "check")]


def cues(ep):
    c = [(st + 0.05, "stamp") for st in ep.chapter_starts()[1:-1]]
    for i, sh in enumerate(ep.shots):
        st = sh.start
        if i > 0 and sh.name != "loop":
            c.append((st, "whoosh"))
        if sh.name == "hook":
            for k in range(3):
                c.append((st + 0.05 + k * 0.25, "tick"))
            c.append((st + sh.m(1), "boing"))
        if sh.name == "domino":
            for k in range(4):
                c.append((st + sh.at(0, "줄줄이") + k * 0.18, "thud"))
        if sh.name == "leak":
            for w in ("이름", "전화번호", "연 소득", "대출 한도"):
                c.append((st + sh.at(0, w), "stamp"))
        if sh.name == "hacker":
            c.append((st + sh.at(0, "에이아이"), "ding"))
            c.append((st + sh.at(0, "사십삼"), "tick"))
        if sh.name == "fire":
            c.append((st + sh.at(0, "한전"), "fall"))
            c.append((st + sh.at(1, "교회"), "fall"))
        if sh.name == "check":
            c.append((st + sh.at(0, "비밀번호"), "pop"))
            c.append((st + sh.at(0, "오티피"), "pop"))
        if sh.name == "tips":
            for w, j in (("믿지", 1), ("선입금", 1), ("문자", 2)):
                c.append((st + sh.at(j, w), "pop"))
    return c


# ---------------------------------------------------------------- 소품
def phone(ctx, x, y, s, lt, shake=1.0, red=0.0):
    """진동하는 폰: 발신 화면 '○○은행 대출상담'."""
    ctx.save()
    ctx.translate(x + math.sin(lt * 60) * 6 * shake, y)
    ctx.rotate(0.08 + math.sin(lt * 45) * 0.02 * shake)
    ctx.scale(s, s)
    rrect(ctx, -170, -320, 340, 640, 44)
    S.fs(ctx, "#2E2E33", lw=8)
    rrect(ctx, -150, -290, 300, 580, 26)
    S.fs(ctx, "#1E2A3A" if red < 0.5 else "#4A1E22", lw=0)
    draw_text(ctx, "○○은행", 0, -200, 54, font="black", fill="#FFFFFF")
    draw_text(ctx, "대출상담", 0, -130, 54, font="black", fill="#FFFFFF")
    CROOK.draw(ctx, 0, 140, 0.32, 1, pose="hips", expr="smug", t=lt, bob=False)
    for sg, col in ((-1, "#5FB36A"), (1, "#D9473B")):
        ellipse(ctx, sg * 80, 230, 36, 36)
        S.fs(ctx, col, lw=5)
    ctx.restore()
    if shake > 0:  # 진동선
        for sg in (-1, 1):
            for j in range(2):
                ctx.move_to(x + sg * (s * 200 + j * 30), y - 60)
                ctx.line_to(x + sg * (s * 200 + j * 30), y + 60)
        set_rgb(ctx, "#F3EBD5", 0.7)
        ctx.set_line_width(8)
        ctx.stroke()


def bedroom(ctx, lt, sh, ep, frozen=False):
    S.sky(ctx, "#1A2236", "#2C3650")
    ctx.rectangle(0, 0, W, H)
    set_rgb(ctx, "#000000", 0.0)
    ctx.fill()
    ellipse(ctx, 820, 330, 70, 70)  # 창밖 달
    set_rgb(ctx, "#F2E6B8", 0.9)
    ctx.fill()
    rrect(ctx, 40, 1180, 720, 260, 30)  # 침대
    S.fs(ctx, "#6B5A8C", lw=8)
    rrect(ctx, 60, 1120, 230, 110, 40)  # 베개
    S.fs(ctx, "#E8E2F0", lw=7)
    talking_me = (not frozen) and sh.m(1) <= lt < sh.m(2)
    shocked = (not frozen) and lt >= sh.m(1)
    ME.draw(ctx, 330, 1430, 1.0, 1, pose="shrug" if shocked else "down",
            expr="shock" if shocked else "neutral",
            mouth=(ep.mouth("P", sh.start + lt) * 1.3) if talking_me else 0, t=0 if frozen else lt,
            sweat=shocked, bob=False)
    red = 0.0 if frozen else prog(lt, sh.m(2), sh.m(2) + 0.4)
    if red > 0:
        ctx.rectangle(0, 0, W, H)
        set_rgb(ctx, "#C9473B", 0.12 * red)
        ctx.fill()
    phone(ctx, 720, 860, 0.95, 0.0 if frozen else lt, shake=1.0, red=red)
    draw_text(ctx, HOOK_TEXT, 540, 230, 96, font="black", fill="#FFFFFF", stroke=14, stroke_fill="#1E1E22")
    draw_text(ctx, "※ 상황극", 160, 1470 - 60, 34, font="black", fill="#C9D3DE")


def bank(ctx, x, y, s, rot=0.0, name="은행", color="#DDD8CB"):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    ctx.new_path()  # 지붕 삼각형
    ctx.move_to(-130, -300)
    ctx.line_to(0, -380)
    ctx.line_to(130, -300)
    ctx.close_path()
    S.fs(ctx, "#C6C2B6", lw=7)
    rrect(ctx, -120, -300, 240, 300, 6)
    S.fs(ctx, color, lw=7)
    for i in range(4):
        rrect(ctx, -95 + i * 58, -270, 24, 230, 6)
        S.fs(ctx, "#F1EEE5", lw=4)
    draw_text(ctx, name, 0, -330, 34, font="black", fill="#2E3A4A")
    ctx.restore()


# ---------------------------------------------------------------- 샷 그리기
def shot_hook(ctx, lt, sh, ep):
    bedroom(ctx, lt, sh, ep)


def shot_loop(ctx, lt, sh, ep):
    bedroom(ctx, 0.0, ep.shots[0], ep, frozen=True)


def shot_domino(ctx, lt, sh, ep):
    S.planks(ctx, base=S.SLATE, dark=S.SLATE_D, seed=2)
    ctx.rectangle(0, 1150, W, 500)
    set_rgb(ctx, "#8C7A5E")
    ctx.fill()
    t0 = sh.at(0, "줄줄이")
    for i in range(4):
        k = ease_out_cubic(prog(lt, t0 + i * 0.18, t0 + i * 0.18 + 0.4))
        bank(ctx, 200 + i * 210, 1150, 0.85, rot=1.2 * k, name=("A은행", "B은행", "C은행", "D은행")[i])
    k2 = ease_out_back(prog(lt, t0 + 0.8, t0 + 1.2), 2.0)
    if k2 > 0.01:
        label(ctx, "9월 말부터 연쇄 해킹", 540, 420, k2, fill="#FBF7EC", ink=S.RUST, size=64)


def shot_leak(ctx, lt, sh, ep):
    S.desk(ctx)
    k = ease_out_back(prog(lt, 0.05, 0.4), 1.4)
    card(ctx, 520, 700, 820, 900, k, rot=-0.01)
    draw_text(ctx, "유출된 정보", 0, -360, 64, font="black", fill="#2E3A4A")
    draw_text(ctx, "신한은행 고객 약 2만5천 명", 0, -280, 42, font="black", fill="#7A8594")
    rows = ("이름", "전화번호", "연 소득", "대출 한도")
    for j, w in enumerate(rows):
        y = -150 + j * 130
        t0 = sh.at(0, w)
        kk = ease_out_back(prog(lt, t0, t0 + 0.3), 2.0)
        draw_text(ctx, w, -150, y, 60, font="black", fill="#2E3A4A" if j < 2 else S.RUST)
        if kk > 0.01:
            ctx.save()
            ctx.translate(200, y)
            ctx.rotate(-0.12)
            ctx.scale(kk, kk)
            rrect(ctx, -90, -40, 180, 80, 14)
            set_rgb(ctx, S.RUST)
            ctx.set_line_width(8)
            ctx.stroke()
            draw_text(ctx, "유출", 0, 2, 50, font="black", fill=S.RUST)
            ctx.restore()
    ctx.restore()


def shot_hacker(ctx, lt, sh, ep):
    S.sky(ctx, "#101820", "#1C2A36")
    for i in range(16):  # 흘러내리는 코드
        x = 60 + i * 64
        y = (lt * 300 + i * 137) % 1500
        draw_text(ctx, "01", x, y, 34, font="jua", fill="#3FA06A", alpha=0.35)
    HACKER.draw(ctx, 330, 1440, 0.95, 1, pose="point", expr="smug", t=lt)
    rrect(ctx, 470, 980, 380, 30, 10)  # 책상 위 노트북
    S.fs(ctx, "#B9BEC6", lw=6)
    rrect(ctx, 500, 760, 320, 220, 14)
    S.fs(ctx, "#2E3A4A", lw=7)
    ta = sh.at(0, "에이아이")
    ka = ease_out_back(prog(lt, ta, ta + 0.3), 2.0)
    if ka > 0.01:
        draw_text(ctx, "AI 해킹 도구", 660, 870, 46, font="black", fill="#9FE3DA", scale=ka)
    t43 = sh.at(0, "사십삼")
    n = int(43 * ease_out_cubic(prog(lt, t43 - 0.6, t43 + 0.4)))
    ellipse(ctx, 540, 360, 120, 120)  # 시계
    S.fs(ctx, "#F3EBD5", lw=9)
    a = lt * 8
    ctx.move_to(540, 360)
    ctx.line_to(540 + math.cos(a) * 90, 360 + math.sin(a) * 90)
    ctx.move_to(540, 360)
    ctx.line_to(540 + math.cos(a / 12) * 55, 360 + math.sin(a / 12) * 55)
    set_rgb(ctx, S.OUT)
    ctx.set_line_width(10)
    ctx.stroke()
    if n > 0:
        label(ctx, f"공격 {n}시간째", 540, 560, 1.0, fill="#FBF7EC", ink=S.RUST, size=60)


def shot_fire(ctx, lt, sh, ep):
    S.planks(ctx, base="#4A3B2E", dark="#3B2F24", w=150)
    nodes = (("은행", 230, 520, 0.0, None), ("한전", 760, 520, sh.at(0, "한전"), "직원 2만4천 명 노출"),
             ("교회 2곳", 500, 980, sh.at(1, "교회"), "교인 정보 최대 100만 건\n유출 가능성"))
    for j in range(2):  # 번지는 불길 선
        _, x0, y0, _, _ = nodes[j]
        _, x1, y1, t1, _ = nodes[j + 1]
        k = prog(lt, t1 - 0.4, t1)
        if k > 0:
            ctx.move_to(x0, y0)
            ctx.line_to(x0 + (x1 - x0) * k, y0 + (y1 - y0) * k)
            set_rgb(ctx, "#E8873E")
            ctx.set_line_width(16)
            ctx.set_dash([30, 20])
            ctx.stroke()
            ctx.set_dash([])
    for name, x, y, t0, note in nodes:
        k = ease_out_back(prog(lt, t0, t0 + 0.35), 2.0) if t0 else 1.0
        if k <= 0.01:
            continue
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(k, k)
        for f in range(5):  # 불꽃
            a = f * 1.25 + lt * 3
            r = 120 + 15 * math.sin(lt * 9 + f)
            ellipse(ctx, math.cos(a) * 30, -60 + math.sin(a) * 20, r * 0.5, r * 0.7)
            set_rgb(ctx, ("#E8873E", "#E8B93E")[f % 2], 0.55)
            ctx.fill()
        ellipse(ctx, 0, 0, 110, 110)
        S.fs(ctx, "#F3EBD5", lw=9)
        draw_text(ctx, name, 0, 4, 52 if len(name) < 4 else 44, font="black", fill="#2E3A4A")
        ctx.restore()
        if note and k > 0.5:
            draw_text(ctx, note, x, y + 170, 42, font="black", fill="#FFE38A", stroke=8, stroke_fill="#2E2A28")


def shot_check(ctx, lt, sh, ep):
    S.desk(ctx)
    k = ease_out_back(prog(lt, 0.05, 0.4), 1.4)
    card(ctx, 520, 700, 820, 760, k, rot=0.01)
    draw_text(ctx, "지금까지 확인된 것", 0, -300, 58, font="black", fill="#2E3A4A")
    items = (("비밀번호", "안전", "비밀번호", "#4F7A9C"), ("OTP", "안전", "오티피", "#4F7A9C"),
             ("돈 빠져나간 피해", "확인 안 됨", "피해", S.RUST))
    for j, (name, st, w, col) in enumerate(items):
        y = -150 + j * 150
        t0 = sh.at(0, w)
        kk = ease_out_back(prog(lt, t0, t0 + 0.3), 2.0)
        draw_text(ctx, name, -330, y, 54, font="black", fill="#2E3A4A", anchor=(0, 0.5))
        if kk > 0.01:
            draw_text(ctx, st, 250, y, 54, font="black", fill=col, scale=kk)
    ctx.restore()


def shot_tips(ctx, lt, sh, ep):
    S.planks(ctx, base=S.SLATE, dark=S.SLATE_D, seed=5)
    k = ease_out_back(prog(lt, 0.05, 0.4), 1.4)
    card(ctx, 520, 700, 840, 920, k, rot=-0.01)
    draw_text(ctx, "딱 3가지만 기억해", 0, -370, 64, font="black", fill="#2E3A4A")
    tips = (("내 정보를 알아도", "믿지 마", 1, "믿지"), ("선입금·앱 설치 요구", "= 사기", 1, "선입금"),
            ("확인은 문자 링크 ✕", "공식 앱·대표번호", 2, "문자"))
    for j, (a, b, li, w) in enumerate(tips):
        y = -200 + j * 200
        t0 = sh.at(li, w)
        kk = ease_out_back(prog(lt, t0, t0 + 0.3), 1.8)
        if kk <= 0.01:
            continue
        ctx.save()
        ctx.translate(0, y)
        ctx.scale(kk, kk)
        ellipse(ctx, -330, 10, 46, 46)
        S.fs(ctx, S.RUST, lw=6)
        draw_text(ctx, str(j + 1), -330, 12, 54, font="black", fill="#FFFFFF")
        draw_text(ctx, a, 40, -26, 48, font="black", fill="#2E3A4A")
        draw_text(ctx, b, 40, 44, 54, font="black", fill=S.RUST)
        ctx.restore()
    ctx.restore()


SHOT_FN = {k[5:]: v for k, v in globals().items() if k.startswith("shot_")}
CAMERA = {
    "hook": (540, 1000, 0.0), "loop": (540, 1000, 0.0), "domino": (540, 1000, 0.05), "leak": (520, 700, 0.04),
    "hacker": (540, 800, 0.05), "fire": (500, 760, 0.05), "check": (520, 700, 0.04), "tips": (520, 700, 0.03),
}

EP = Explainer(SCRIPT, VOICE, CAP_COLOR, SHOT_FN, CAMERA, cues,
               notice="※ 언론 보도·금융당국 발표 기반 / 첫 장면은 상황극", chapters=CHAPTERS)
render_frame, mix = EP.render_frame, EP.mix


def prepare():
    global DURATION
    DURATION = EP.prepare().duration
