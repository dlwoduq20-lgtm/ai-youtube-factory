"""오늘의 만평 #07 — 딸은 상주 하면 안 된다고?  (상황극 오프닝 + 양자택일 CTA + 루프 엔딩)

실제 화제 (2026년 10월 10일 전후 보도, 온라인 사연 = 작성자 주장):
- 모친상을 치른 세 자매 중 장녀가 상주 완장을 찼다가 장례지도사에게
  "원래 상주는 여자가 맡는 것이 아니다"는 말을 여러 번 들었다는 SNS 사연
- 장녀: "2026년인 지금 여자 상주가 왜 문제인지 모르겠다", "그런 낡은 말씀은 내게 하실 필요가 없다"
- 경험담: 외동딸 대신 군 휴가 나온 사촌 남동생이 상주 / 남자가 없다고 먼 당숙 장례에 불려 간 남성
- 장사법 연고자 순위: 배우자 → 자녀 → 부모 … (자녀에 성별 구분 없음)
- 2023.5.11 대법원 전원합의체: 제사주재자 '장남 우선' → 협의 없으면 성별 무관 최근친 연장자
장례지도사 측 입장은 보도되지 않았다. 고인·슬픔을 웃음거리로 쓰지 않고, 개인 이름은 쓰지 않는다.
"""
import math

from .. import squire as S
from ..doodle import Doodle
from ..engine import W, draw_text, ease_out_back, ellipse, prog, rrect, set_rgb
from ..explainer import Explainer, bubble, card, close_up, label

TITLE = "딸은 상주 하면 안 된다고? | 오늘의 만평"
DURATION = 47.0

DIR = Doodle(coat="#26282E", tie="#55585F", hair="gray", hair_color="#BDBDBD", glasses=True)
SIS = Doodle(coat="#1E1E22", hair="bob", hair_color="#2A2420", collar=True)
COUSIN = Doodle(coat="#5E6B45", hair="cap", hair_color="#2A2420", collar=False)
ONLY = Doodle(coat="#2A2A30", hair="bob", hair_color="#3A2A24")
FARMAN = Doodle(coat="#33363D", tie="#55585F", hair="tuft")
CIT = Doodle(coat="#6F7F63", hair="beanie", hair_color="#C25B3F", collar=False)

VOICE = {
    "N": ("male", "+80%", "+20Hz", 1.18),
    "D": ("male", "+55%", "-10Hz", 0.92),  # 장례지도사: 낮고 덤덤하게
    "E": ("female", "+70%", "+20Hz", 1.08),  # 장녀: 또렷하고 단호하게
}
CAP_COLOR = {"N": "#FFFFFF", "D": "#C9D3DE", "E": "#FFC9A8"}

SCRIPT = [
    ("hook", [("D", "잠깐만요, 상주는 원래 여자가 하는 게 아니에요.", None),
              ("E", "저희 엄마 장례식인데요?", None),
              ("D", "혹시… 남자 친척은 없으세요?", None)], {"tail": 0.5}),
    ("post", [("N", "이번 주 에스엔에스를 달군 실제 사연이야. 세 자매 중 장녀가 어머니 장례에서 상주 완장을 찼다가, "
                    "이런 말을 여러 번 들었대.",
               "이번 주 SNS를 달군 실제 사연이야. 세 자매 중 장녀가 어머니 장례에서 상주 완장을 찼다가, "
               "이런 말을 여러 번 들었대.")], {"tail": 0.5}),
    ("eldest", [("E", "이천이십육 년에 여자 상주가 왜 문제예요? 그런 낡은 말씀은 안 하셔도 돼요.",
                 "2026년에 여자 상주가 왜 문제예요? 그런 낡은 말씀은 안 하셔도 돼요.")], {"tail": 0.6}),
    ("stories", [("N", "비슷한 경험담이 줄줄이 달렸어.", None),
                 ("N", "외동딸인데 완장도 못 차보고, 군 휴가 나온 사촌 남동생이 상주를 했다는 사람.", None),
                 ("N", "반대로, 집안에 남자가 없다고 왕래도 없던 먼 친척 장례에 불려 가 상주를 선 남자도 있었어.", None)],
     {"tail": 0.6}),
    ("law", [("N", "그럼 법은? 장사법은 배우자 다음 순위를 그냥 자녀로 정해. 아들, 딸 구분이 없어.",
              "그럼 법은? 장사법은 배우자 다음 순위를 그냥 '자녀'로 정해. 아들, 딸 구분이 없어."),
             ("N", "대법원도 이천이십삼 년에, 제사를 이끌 사람은 장남이 아니라 성별 상관없이 나이순이라고 판례를 바꿨어.",
              "대법원도 2023년에, 제사를 이끌 사람은 장남이 아니라 성별 상관없이 나이순이라고 판례를 바꿨어.")],
     {"tail": 0.6}),
    ("scale", [("N", "그래도 장례만큼은 오래된 관습을 지켜야 한다는 의견도 여전히 있어.", None)], {"tail": 0.6}),
    ("vote", [("N", "너는 어때? 일 번, 상주는 성별 상관없이 가족이 정하면 된다. 이 번, 장례만큼은 전통 관습을 따르는 게 맞다.",
               "너는 어때? 1번, 상주는 성별 상관없이 가족이 정하면 된다. 2번, 장례만큼은 전통 관습을 따르는 게 맞다."),
              ("N", "번호로 댓글 남겨줘.", None),
              ("D", "…혹시, 남자 친척은 없으세요?", None)], {"tail": 0.6}),
]

CHAPTERS = [("사연", "hook"), ("반응", "stories"), ("팩트", "law"), ("결론", "scale")]
HOOK_TEXT = "딸은 상주 안 돼?"


def cues(ep):
    c = [(st + 0.05, "stamp") for st in ep.chapter_starts()[1:-1]]
    for i, sh in enumerate(ep.shots):
        st = sh.start
        if i > 0:
            c.append((st, "whoosh"))
        if sh.name == "hook":
            c.append((st + sh.m(2), "boing"))
        if sh.name == "post":
            c.append((st + 0.4, "tick"))
        if sh.name == "eldest":
            c.append((st + 0.25, "slide"))
        if sh.name == "stories":
            for j in range(3):
                c.append((st + sh.m(j) + 0.1, "pop"))
        if sh.name == "law":
            c.append((st + sh.at(0, "구분"), "stamp"))
            c.append((st + sh.m(1), "gavel"))
            c.append((st + sh.at(1, "나이순"), "stamp"))
        if sh.name == "vote":
            c.append((st + sh.at(0, "일 번"), "pop"))
            c.append((st + sh.at(0, "이 번"), "pop"))
            c.append((st + sh.m(1), "ding"))
            c.append((st + sh.m(2), "slide"))
    return c


# ---------------------------------------------------------------- 소품
def armband(ctx, x, y, s, rot=0.0):
    """상주 완장 (검은 띠에 흰 줄 두 개)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    rrect(ctx, -34, -22, 68, 44, 8)
    S.fs(ctx, "#111114", lw=5)
    for dy in (-8, 8):
        ctx.rectangle(-34, dy - 3, 68, 6)
        set_rgb(ctx, "#F2F2F2")
        ctx.fill()
    ctx.restore()


def wear_armband(x, y, s, facing):
    """Doodle 앞팔 윗부분 위치 (pose='down'/'hips' 기준 근사)."""
    return x + facing * 82 * s, y - 285 * s


def hall(ctx):
    """빈소: 어두운 벽, 흰 천 제단, 리본 액자(얼굴 없음), 국화."""
    S.planks(ctx, base="#3A3D44", dark="#30333A", w=150)
    rrect(ctx, 150, 860, 780, 140, 12)  # 제단
    S.fs(ctx, "#F2F0EA", lw=8)
    rrect(ctx, 420, 500, 240, 300, 10)  # 액자
    S.fs(ctx, "#1E1E22", lw=8)
    rrect(ctx, 445, 525, 190, 250, 6)
    S.fs(ctx, "#D9D6CE", lw=0)
    ctx.new_path()  # 검은 리본
    ctx.move_to(420, 545)
    ctx.line_to(465, 500)
    ctx.line_to(495, 500)
    ctx.line_to(420, 575)
    ctx.close_path()
    ctx.move_to(660, 545)
    ctx.line_to(615, 500)
    ctx.line_to(585, 500)
    ctx.line_to(660, 575)
    ctx.close_path()
    set_rgb(ctx, "#111114")
    ctx.fill()
    for i in range(14):  # 국화
        x = 190 + i * 54
        y = 850 + (i % 2) * 18
        for dx, dy in ((-12, 0), (12, 0), (0, -12), (0, 12)):
            ellipse(ctx, x + dx, y + dy, 16, 16)
            set_rgb(ctx, "#FAFAF5")
            ctx.fill()
        ellipse(ctx, x, y, 9, 9)
        set_rgb(ctx, "#E8D27A")
        ctx.fill()


# ---------------------------------------------------------------- 샷 그리기
def shot_hook(ctx, lt, sh, ep):
    hall(ctx)
    q = lt >= sh.m(2)
    s = 1.15
    SIS.draw(ctx, 300, 1520, s, 1, pose="down" if lt < sh.m(1) else "point",
             expr="shock" if q else ("neutral" if lt < sh.m(1) else "angry"),
             mouth=ep.mouth("E", sh.start + lt) * 1.3, t=lt, sweat=q)
    armband(ctx, *wear_armband(300, 1520, s, 1), s, rot=-0.2)
    DIR.draw(ctx, 790, 1520, s, -1, pose="point" if lt < sh.m(1) else "hips", expr="deadpan",
             mouth=ep.mouth("D", sh.start + lt) * 1.3, t=lt, bob=False)
    if q:  # 엉뚱한 질문에 물음표
        for j, (x, y) in enumerate(((200, 700), (420, 640))):
            k = ease_out_back(prog(lt, sh.m(2) + 0.3 + j * 0.15, sh.m(2) + 0.6 + j * 0.15), 2.0)
            draw_text(ctx, "?", x, y, 120, font="black", fill="#E8B93E", stroke=10, stroke_fill="#1E1E22",
                      scale=max(k, 0.01))
    # 첫 프레임부터 떠 있는 훅 문구
    draw_text(ctx, HOOK_TEXT, 540, 330, 104, font="black", fill="#FFFFFF", stroke=14, stroke_fill="#1E1E22")


def shot_post(ctx, lt, sh, ep):
    S.planks(ctx, base="#B9A57A", dark="#9C8960", w=150)
    k = ease_out_back(prog(lt, 0.05, 0.4), 1.5)
    card(ctx, 520, 650, 800, 820, k, rot=-0.02)
    ellipse(ctx, -300, -320, 36, 36)
    S.fs(ctx, "#9AA3AE", lw=5)
    draw_text(ctx, "익명 · SNS", -150, -320, 40, font="black", fill="#7A8594")
    lines = ("엄마 장례식에서", "장녀인 제가 상주 완장을", "찼더니…", "\"원래 여자는 상주", "하는 거 아니에요\"")
    for j, txt in enumerate(lines):
        draw_text(ctx, txt, 0, -200 + j * 90, 56, font="black", fill=S.RUST if j >= 3 else "#2E3A4A")
    n = int(9999 * prog(lt, 0.5, sh.dur * 0.8))
    draw_text(ctx, f"♥ {n:,}   댓글 폭주", 0, 300, 40, font="jua", fill="#C9473B")
    ctx.restore()
    for j in range(3):  # 세 자매
        x = 330 + j * 190
        ONLY.draw(ctx, x, 1440, 0.42 - j * 0.04, 1, pose="down", expr="sad", t=lt + j, bob=False)
    armband(ctx, *wear_armband(330, 1440, 0.42, 1), 0.42, rot=-0.2)


def shot_eldest(ctx, lt, sh, ep):
    close_up(ctx, lt, sh, ep, SIS, "E", 1, 420, "#3A3D44", "#30333A", "장녀", 0)
    armband(ctx, *wear_armband(420, 1830, 2.05, 1), 2.05, rot=-0.2)


def shot_stories(ctx, lt, sh, ep):
    S.planks(ctx, base=S.SLATE, dark=S.SLATE_D, seed=6)
    t1, t2 = sh.m(1), sh.m(2)
    k1 = ease_out_back(prog(lt, t1, t1 + 0.35), 1.8)
    if k1 > 0.01:
        bubble(ctx, "외동딸인데 완장도 못 차봄", 540, 300, k1, size=50, fill="#F3EBD5")
        ONLY.draw(ctx, 300, 900, 0.62, 1, pose="down", expr="sad", t=lt, bob=False)
        tc = sh.at(1, "사촌")
        kc = ease_out_back(prog(lt, tc, tc + 0.35), 1.8)
        if kc > 0.01:
            COUSIN.draw(ctx, 760, 900, 0.62, -1, pose="shrug", expr="shock", t=lt)
            armband(ctx, *wear_armband(760, 900, 0.62, -1), 0.62, rot=0.2)
            label(ctx, "군 휴가 중 사촌 동생", 640, 960, kc, size=38)
    k2 = ease_out_back(prog(lt, t2, t2 + 0.35), 1.8)
    if k2 > 0.01:
        tf = sh.at(2, "먼 친척")
        kf = ease_out_back(prog(lt, tf, tf + 0.35), 1.8)
        if kf > 0.01:
            FARMAN.draw(ctx, 170, 1430, 0.62, 1, pose="shrug", expr="sad", t=lt, sweat=True)
            armband(ctx, *wear_armband(170, 1430, 0.62, 1), 0.62, rot=-0.2)
        bubble(ctx, "남자 없다고 먼 친척 상주로", 610, 1090, k2, size=44, fill="#DCE6F2", tail=-1)


def shot_law(ctx, lt, sh, ep):
    S.desk(ctx)
    if lt < sh.m(1):
        k = ease_out_back(prog(lt, 0.05, 0.4), 1.4)
        card(ctx, 520, 640, 800, 760, k, rot=-0.02)
        draw_text(ctx, "장사법 · 연고자 순위", 0, -290, 58, font="black", fill="#2E3A4A")
        rows = ("① 배우자", "② 자녀", "③ 부모", "④ 그 밖의 직계비속…")
        for j, txt in enumerate(rows):
            y = -160 + j * 115
            if j == 1:
                kh = prog(lt, sh.at(0, "자녀"), sh.at(0, "자녀") + 0.3)
                rrect(ctx, -330, y - 45, 660 * kh, 90, 20)
                set_rgb(ctx, "#E8B93E", 0.6)
                ctx.fill()
            draw_text(ctx, txt, -300, y, 58, font="black", fill="#2E3A4A", anchor=(0, 0.5))
        ctx.restore()
        tg = sh.at(0, "구분")
        S.stamp(ctx, 540, 1080, "아들·딸 구분 없음", prog(lt, tg, tg + 0.45), size=74, rot=-0.06)
        return
    k = ease_out_back(prog(lt, sh.m(1), sh.m(1) + 0.4), 1.4)
    card(ctx, 520, 640, 800, 760, k, rot=0.02)
    draw_text(ctx, "2023 대법원 전원합의체", 0, -290, 54, font="black", fill="#2E3A4A")
    draw_text(ctx, "제사 이끌 사람(제사주재자)", 0, -190, 46, font="black", fill="#7A8594")
    draw_text(ctx, "장남 우선", 0, -40, 84, font="black", fill="#9AA3AE")
    ks = prog(lt, sh.at(1, "장남"), sh.at(1, "장남") + 0.4)
    if ks > 0:
        ctx.move_to(-190, -40)
        ctx.line_to(-190 + 380 * ks, -40)
        set_rgb(ctx, S.RUST)
        ctx.set_line_width(14)
        ctx.stroke()
    tn = sh.at(1, "나이순")
    kn = ease_out_back(prog(lt, tn, tn + 0.35), 2.0)
    draw_text(ctx, "→ 성별 무관, 나이순", 0, 130, 70, font="black", fill=S.RUST, scale=max(kn, 0.01))
    ctx.restore()


def shot_scale(ctx, lt, sh, ep):
    S.planks(ctx, base="#3A3D44", dark="#30333A", w=150)
    tilt = 0.12 * math.sin(lt * 2.2)
    cx, cy = 520, 620
    ctx.new_path()
    ctx.move_to(cx - 30, cy)
    ctx.line_to(cx + 30, cy)
    ctx.line_to(cx + 90, 1100)
    ctx.line_to(cx - 90, 1100)
    ctx.close_path()
    S.fs(ctx, "#B9A57A", lw=8)
    ctx.save()
    ctx.translate(cx, cy)
    ctx.rotate(tilt)
    rrect(ctx, -380, -14, 760, 28, 14)
    S.fs(ctx, "#E8B93E", lw=7)
    ctx.restore()
    for sg, name, sub in ((-1, "전통 관습", "아들·장손 우선"), (1, "가족의 선택", "성별 무관")):
        ex = cx + sg * 360 * math.cos(tilt)
        ey = cy + sg * 360 * math.sin(tilt)
        for dx in (-100, 100):
            ctx.move_to(ex, ey)
            ctx.line_to(ex + dx, ey + 170)
        set_rgb(ctx, S.OUT)
        ctx.set_line_width(6)
        ctx.stroke()
        ellipse(ctx, ex, ey + 180, 120, 28)
        S.fs(ctx, "#C8CDD4", lw=7)
        draw_text(ctx, name, ex, ey + 280, 54, font="black", fill="#F3EBD5")
        draw_text(ctx, sub, ex, ey + 345, 40, font="black", fill="#C9D3DE")
    rrect(ctx, cx - 360 * math.cos(tilt) - 50, cy - 360 * math.sin(tilt) + 100, 100, 70, 8)  # 족보 책
    S.fs(ctx, "#8C3B3B", lw=6)
    for j in range(3):  # 가족 셋
        ellipse(ctx, cx + 360 * math.cos(tilt) - 50 + j * 50, cy + 360 * math.sin(tilt) + 130, 22, 22)
        S.fs(ctx, "#FFF4E0", lw=5)


def shot_vote(ctx, lt, sh, ep):
    ctx.rectangle(0, 0, W / 2, 1920)
    set_rgb(ctx, "#5E6B45")
    ctx.fill()
    ctx.rectangle(W / 2, 0, W / 2, 1920)
    set_rgb(ctx, "#3A3D44")
    ctx.fill()
    t1, t2 = sh.at(0, "일 번"), sh.at(0, "이 번")
    for x, num, a, b, t0 in ((260, "1", "성별 상관없이", "가족이 정하기", t1), (790, "2", "장례는", "전통 관습대로", t2)):
        k = ease_out_back(prog(lt, t0, t0 + 0.35), 1.6)
        if k <= 0.01:
            continue
        ctx.save()
        ctx.translate(x, 700)
        ctx.scale(k, k)
        ellipse(ctx, 0, -220, 110, 110)
        S.fs(ctx, "#F3EBD5", lw=10)
        draw_text(ctx, num, 0, -216, 150, font="black", fill="#2E3A4A")
        draw_text(ctx, a, 0, 0, 62, font="black", fill="#FFFFFF")
        draw_text(ctx, b, 0, 90, 62, font="black", fill="#FFFFFF")
        ctx.restore()
    if lt < t1:
        draw_text(ctx, "너는 어때?", 540, 700, 110, font="black", fill="#FFFFFF", stroke=12, stroke_fill="#1E1E22",
                  scale=max(0.01, ease_out_back(prog(lt, 0.05, 0.35), 2.0)))
    if lt >= sh.m(1):
        bubble(ctx, "번호로 댓글!", 540, 1080, ease_out_back(prog(lt, sh.m(1), sh.m(1) + 0.35), 2.0), size=70)
    if lt >= sh.m(2):  # 루프: 장례지도사가 다시 쓱 등장
        k = ease_out_back(prog(lt, sh.m(2), sh.m(2) + 0.4), 1.4)
        DIR.draw(ctx, 1200 - 300 * k, 1560, 1.0, -1, pose="point", expr="deadpan",
                 mouth=ep.mouth("D", sh.start + lt) * 1.3, t=lt, bob=False)
    kq = prog(lt, sh.dur - 0.5, sh.dur)
    if kq > 0:
        draw_text(ctx, HOOK_TEXT, 540, 330, 104, font="black", fill="#FFFFFF", stroke=14, stroke_fill="#1E1E22",
                  alpha=kq)


SHOT_FN = {k[5:]: v for k, v in globals().items() if k.startswith("shot_")}
CAMERA = {
    "hook": (540, 1000, 0.05), "post": (520, 700, 0.05), "eldest": (420, 900, 0.06),
    "stories": (540, 800, 0.04), "law": (520, 700, 0.05), "scale": (520, 800, 0.04),
    "vote": (540, 800, 0.03),
}

EP = Explainer(SCRIPT, VOICE, CAP_COLOR, SHOT_FN, CAMERA, cues,
               notice="※ 온라인 사연(작성자 주장)·언론 보도 기반", chapters=CHAPTERS)
render_frame, mix = EP.render_frame, EP.mix


def prepare():
    global DURATION
    DURATION = EP.prepare().duration
