"""우리 집 아침 #01 — 말 잘하는 아기의 아침 대화

부모와 아기의 평범한 아침을 자연스러운 대화로 보여주는 육아·일상 쇼츠.
아기가 엄마를 깨우고 → 아침 메뉴로 '협상'하고 → 출근하는 아빠를 저금통으로 붙잡는 이야기.

- 화자 3명: 엄마(M), 아빠(D), 아기(K). 아기 목소리는 여성 음성을 피치 업 + 살짝 느리게 변조.
- 자막은 화자별 색상 (엄마 분홍 / 아빠 하늘 / 아기 노랑), 쇼츠 하단 UI 바로 위에 배치.
- 배경/캐릭터/소품은 cartoon_shorts/family.py.
"""
import math

from .. import family as F
from .. import squire as S
from ..engine import (clamp, draw_text, ease_in_out, ease_out_back, ease_out_cubic,
                      prog, rrect)
from ..explainer import Episode

TITLE = "우리 집 아침 #01 - 말 잘하는 아기의 아침 대화"
DURATION = 45.0

MOM = S.Person(coat="#F2A7A0", hair="bob", hair_color="#3A2A22", hood=True, pants="#8E7CA8")
DAD = S.Person(coat="#4E5A6B", tie="#E3826F", hair="part", hair_color="#2E2420")
BABY = F.Baby(onesie="#FFD978")

VOICES = {
    "M": ("ko-KR-SunHiNeural", "+4%", "+0Hz"),
    "D": ("ko-KR-InJoonNeural", "+6%", "-2Hz"),
    "K": ("ko-KR-SunHiNeural", "+0%", "+12Hz", (1.3, 0.97)),  # 아기: 피치 업 + 살짝 느리게
}
CAP_COLORS = {"M": "#FFC4D6", "D": "#BFD7FF", "K": "#FFF3A8"}

SCRIPT = [
    ("wake", [("K", "엄마, 엄마! 해님 일어났어!"),
              ("M", "으응... 해님은 일어났는데, 엄마는 조금만 더 잘래...")], {"tail": 0.3}),
    ("kiss", [("K", "그럼 내가 뽀뽀해 줄게. 쪽!"),
              ("M", "아이고, 눈이 [번쩍] 떠졌네!")], {"tail": 0.5}),
    ("breakfast", [("M", "우리 아가, 아침 뭐 먹을까?"),
                   ("K", "음... [아이스크림]!")], {"tail": 0.5}),
    ("deal", [("M", "아침부터 아이스크림? 밥 다 먹고 생각해 보자."),
              ("K", "그럼 밥 다 먹으면, 아이스크림 [두 개]야?"),
              ("M", "...그런 협상은 어디서 배웠어?")], {"tail": 0.7}),
    ("door", [("D", "아빠 회사 다녀올게!"),
              ("K", "아빠, 회사 가지 마. 나랑 놀자...")], {"tail": 0.4}),
    ("piggy", [("D", "아빠가 돈 벌어 와야, 장난감도 사 주지."),
               ("K", "그럼 내 돼지 저금통 줄게. 오늘은 같이 놀자.")], {"tail": 0.6}),
    ("melt", [("D", "...여보, 나 오늘 회사 못 가겠어."),
              ("M", "가.")], {"tail": 0.9}),
    ("bye", [("K", "아빠, 빨리 와! 사랑해!"),
             ("D", "아빠도 사랑해! 금방 올게!")], {"tail": 3.0}),
]


def _mo(spk, sh, lt):
    return EP.mouth(spk, sh.start + lt)


def _in(sh, lt, i):
    return sh.m(i) <= lt < sh.me(i) + 0.1


# ================================================================ 침실
def _bedroom(ctx, lt, sun_k=1.0):
    F.wall(ctx, "#FBE3D6", "#F6C7B4", floor_y=1250, seed=2)
    F.window(ctx, 610, 230, 360, 380, t=lt, sun_k=sun_k)
    F.frame_pic(ctx, 250, 400, 210, 180, kind=1, rot=-0.05)
    F.bed(ctx, 70, 860, 1070, 1420)
    F.pillow(ctx, 235, 1035, 270, 115)


def _mom_lying(ctx, lt, expr, mouth, lump=True):
    F.lying_head(ctx, MOM, 255, 995, 1.12, expr=expr, mouth=mouth, t=lt)
    F.blanket(ctx, 360, 960, 870, 1310, lump=8 * math.sin(lt * 1.6) if lump else 0)


def _zzz(ctx, lt, x, y, alpha=1.0):
    for i in range(3):
        k = (lt * 0.7 + i / 3) % 1.0
        draw_text(ctx, "Z", x + k * 70 + i * 6, y - k * 160, 40 + 30 * k, font="black",
                  fill="#7C8FB5", stroke=6, stroke_fill="#FFFFFF", alpha=alpha * math.sin(k * math.pi))


def shot_wake(ctx, lt, sh):
    _bedroom(ctx, lt, sun_k=ease_out_cubic(prog(lt, 0.1, 1.6)))
    _mom_lying(ctx, lt, "deadpan", _mo("M", sh, lt))
    if lt < sh.m(1):
        _zzz(ctx, lt, 300, 860)
    jump = _in(sh, lt, 0)
    hop = abs(math.sin(lt * 6.5)) * 70 if jump else 0
    BABY.draw(ctx, 650, 1060 - hop, 1.1, -1, pose="cheer" if jump else "down",
              expr="happy" if jump else "neutral", mouth=_mo("K", sh, lt), t=lt, bob=not jump)


def shot_kiss(ctx, lt, sh):
    _bedroom(ctx, lt)
    t_kiss = sh.word_t(0, 4)
    t_wow = sh.word_t(1, 2)
    if lt < t_kiss:
        mexpr = "deadpan"
    elif lt < t_kiss + 0.7 or (t_wow <= lt < t_wow + 0.6):
        mexpr = "shock"
    else:
        mexpr = "neutral"
    _mom_lying(ctx, lt, mexpr, _mo("M", sh, lt), lump=lt < t_kiss)
    lean = 0.28 * ease_in_out(prog(lt, t_kiss - 0.5, t_kiss))
    bexpr = "kiss" if t_kiss - 0.3 <= lt < t_kiss + 0.6 else "happy"
    BABY.draw(ctx, 520, 1060, 1.1, -1, pose="reach" if lt >= t_kiss - 0.5 else "down",
              expr=bexpr, mouth=_mo("K", sh, lt), t=lt, rot=-lean)
    F.pop_text(ctx, "쪽!", 220, 760, prog(lt, t_kiss, t_kiss + 1.2), size=120)
    F.hearts(ctx, 300, 900, lt, t_kiss, n=8, seed=4)
    F.pop_text(ctx, "번쩍!", 230, 770, prog(lt, t_wow, t_wow + 1.1), size=110, fill="#FFD54A", rot=0.1)
    if lt >= t_wow:
        F.sparkles(ctx, 270, 990, lt, n=6, r=190, seed=7)


# ================================================================ 부엌
def _kitchen(ctx, lt, sh, mom_pose="down", mom_expr="neutral", sweat=False,
             baby_pose="down", baby_expr="neutral"):
    F.kitchen(ctx, floor_y=1300, t=lt)
    MOM.draw(ctx, 790, 1660, 1.42, -1, pose=mom_pose, expr=mom_expr, mouth=_mo("M", sh, lt),
             t=lt, sweat=sweat)
    F.high_chair_back(ctx, 300, 1280)
    BABY.draw(ctx, 300, 1290, 1.25, 1, pose=baby_pose, expr=baby_expr,
              mouth=_mo("K", sh, lt), t=lt, legs=False)
    F.table(ctx, 1290)
    F.bowl(ctx, 320, 1300, 0.95)
    F.spoon(ctx, 470, 1260, 0.8, rot=0.5)
    F.bowl(ctx, 760, 1300, 0.8, color="#F7C9C2", food="#FFE3A3")


def shot_breakfast(ctx, lt, sh):
    want = sh.word_t(1, 1)
    hmm = _in(sh, lt, 1) and lt < want
    _kitchen(ctx, lt, sh, mom_pose="down",
             baby_pose="cheer" if lt >= want else "down",
             baby_expr="sparkle" if lt >= want else ("pout" if hmm else "neutral"))
    if hmm:
        draw_text(ctx, "?", 470, 780, 120, font="black", fill="#7C8FB5", stroke=10,
                  stroke_fill="#FFFFFF", rot=0.15 * math.sin(lt * 4))
    k = ease_out_back(prog(lt, want - 0.15, want + 0.35), 2.0)
    F.think_bubble(ctx, 360, 470, 440, 400, (320, 860), k)
    if k > 0.01:
        F.ice_cream(ctx, 360, 470 + 40 * k, 0.9 * k, rot=0.08 * math.sin(lt * 3))
        F.sparkles(ctx, 360, 450, lt, n=4, r=150, seed=3)


def shot_deal(ctx, lt, sh):
    two = sh.word_t(1, 4)
    talk2 = lt >= sh.m(2)
    _kitchen(ctx, lt, sh,
             mom_pose="hips" if not talk2 else "shrug",
             mom_expr="deadpan" if talk2 else "neutral", sweat=talk2,
             baby_pose="cheer" if _in(sh, lt, 1) else ("hold" if talk2 else "down"),
             baby_expr="sparkle" if lt >= sh.m(1) else "pout")
    k = ease_out_back(prog(lt, two - 0.2, two + 0.3), 2.0)
    if k > 0.01:
        F.think_bubble(ctx, 380, 470, 560, 400, (320, 860), k)
        for i, dx in enumerate((-110, 110)):
            ki = ease_out_back(prog(lt, two + i * 0.18, two + i * 0.18 + 0.35), 2.2)
            F.ice_cream(ctx, 380 + dx * k, 500, 0.75 * ki, rot=(-0.15 if i == 0 else 0.15),
                        scoops=(("#F6B9C4", "#FFF0C2") if i == 0 else ("#C9A26E", "#9AD88A")))
    if talk2:
        S.stamp(ctx, 540, 1440, "협상왕 등극", prog(lt, sh.m(2) + 0.4, sh.m(2) + 1.0),
                color="#E2504F", rot=-0.12, size=84)


# ================================================================ 현관
def _hall(ctx, lt, open_k=0.0):
    F.wall(ctx, "#E8E4F6", "#D2CCEA", floor_y=1350, floor="#D7B892", floor_d="#BE9D75", seed=6)
    F.door(ctx, 640, 300, 340, 1050, open_k=open_k, t=lt)
    F.frame_pic(ctx, 280, 470, 230, 190, kind=2, rot=0.04)
    F.frame_pic(ctx, 150, 760, 150, 150, kind=0, rot=-0.06)


def _dad(ctx, lt, sh, x, y, s, pose, expr, sweat=False, case=True):
    if case:
        F.briefcase(ctx, x + 112 * s, y - 175 * s, s * 0.95)
    DAD.draw(ctx, x, y, s, -1, pose=pose, expr=expr, mouth=_mo("D", sh, lt), t=lt,
             bob=False, sweat=sweat)


def shot_door(ctx, lt, sh):
    _hall(ctx, lt)
    _dad(ctx, lt, sh, 640, 1665, 1.62, "wave" if _in(sh, lt, 0) else "down",
         "neutral" if lt < sh.m(1) else "shock")
    pull = lt >= sh.m(1)
    run = ease_out_cubic(prog(lt, sh.m(1) - 0.4, sh.m(1) + 0.1))
    BABY.draw(ctx, 180 + 170 * run, 1665, 1.2, 1, pose="pull" if pull else "down",
              expr="sad" if pull else "neutral", mouth=_mo("K", sh, lt), t=lt)


def shot_piggy(ctx, lt, sh):
    _hall(ctx, lt)
    offer = lt >= sh.m(1)
    _dad(ctx, lt, sh, 640, 1665, 1.62, "shrug" if _in(sh, lt, 0) else "down",
         "neutral" if not offer else "shock")
    BABY.draw(ctx, 350, 1665, 1.2, 1, pose="offer" if offer else "pull",
              expr="sparkle" if offer else "sad", mouth=_mo("K", sh, lt), t=lt)
    if offer:
        k = ease_out_back(prog(lt, sh.m(1), sh.m(1) + 0.4), 2.2)
        F.piggy(ctx, 540, 1365, 0.72 * k, rot=-0.08, t=lt)
        F.sparkles(ctx, 540, 1345, lt, n=5, r=150, seed=5)


def shot_melt(ctx, lt, sh):
    _hall(ctx, lt)
    slide = ease_out_cubic(prog(lt, sh.m(1) - 0.5, sh.m(1) - 0.1))
    if slide > 0:
        MOM.draw(ctx, -260 + 400 * slide, 1665, 1.6, 1, pose="hips", expr="deadpan",
                 mouth=_mo("M", sh, lt), t=lt)
    _dad(ctx, lt, sh, 650, 1665, 1.62, "down",
         "sad" if lt < sh.m(1) + 0.2 else "shock", sweat=lt >= sh.m(1))
    if lt < sh.m(1):
        F.hearts(ctx, 650, 900, lt, 0.2, n=10, spread=320, seed=8, dur=2.4)
    BABY.draw(ctx, 350, 1665, 1.2, 1, pose="hold", expr="sparkle", mouth=_mo("K", sh, lt), t=lt)
    F.piggy(ctx, 360, 1465, 0.6, t=lt)
    S.stamp(ctx, 540, 420, "가.", prog(lt, sh.m(1), sh.m(1) + 0.6), color="#4E5A6B", rot=-0.08, size=160)


def shot_bye(ctx, lt, sh):
    _hall(ctx, lt, open_k=ease_in_out(prog(lt, 0.0, 0.8)))
    _dad(ctx, lt, sh, 830, 1640, 1.45, "wave" if lt >= sh.m(1) - 0.2 else "down", "neutral")
    MOM.draw(ctx, 120, 1665, 1.6, 1, pose="wave" if lt >= sh.me(1) else "down", expr="neutral", t=lt)
    BABY.draw(ctx, 380, 1665, 1.2, 1, pose="wave", expr="happy" if not _in(sh, lt, 0) else "neutral",
              mouth=_mo("K", sh, lt), t=lt)
    F.hearts(ctx, 380, 1245, lt, sh.word_t(0, 3), n=8, seed=11)
    F.hearts(ctx, 800, 900, lt, sh.word_t(1, 1), n=8, seed=12)
    # 엔딩 카드: 댓글 유도
    k = ease_out_back(prog(lt, sh.me(1) + 0.2, sh.me(1) + 0.6), 1.8)
    if k > 0.01:
        ctx.save()
        ctx.translate(540, 560)
        ctx.scale(k, k)
        rrect(ctx, -440, -170, 880, 340, 40)
        S.fs(ctx, "#FFFDF5")
        draw_text(ctx, "여러분 아이는 어떤 말로\n출근길을 막나요?", 0, -45, 66, font="black",
                  fill="#3A3F4A", spacing=18)
        rrect(ctx, -230, 70, 460, 80, 40)
        S.fs(ctx, "#F08A9B", lw=6)
        draw_text(ctx, "댓글로 알려주세요!", 0, 112, 46, font="black", fill="#FFFFFF")
        ctx.restore()


SHOT_FNS = {k[5:]: v for k, v in dict(globals()).items() if k.startswith("shot_")}
CAMERA = {
    "wake": (540, 1000, 0.04), "kiss": (330, 980, 0.12), "breakfast": (420, 900, 0.05),
    "deal": (540, 800, 0.06), "door": (480, 1250, 0.05), "piggy": (420, 1400, 0.1),
    "melt": (600, 1000, 0.06), "bye": (540, 1000, 0.03),
}

EP = Episode(TITLE, SCRIPT, SHOT_FNS, VOICES, CAP_COLORS, CAMERA,
             bgm_style="cute", bpm=96, bgm_gain=0.2, cap_y=1590)


def prepare():
    global DURATION
    EP.prepare()
    DURATION = EP.duration


def cues():
    c = []
    for i, sh in enumerate(EP.shots):
        st = sh.start
        if i > 0:
            c.append((st, "whoosh"))
        n = sh.name
        if n == "wake":
            t = sh.m(0)
            while t < sh.me(0):  # 침대 위 콩콩 점프
                c.append((st + t, "boing"))
                t += math.pi / 6.5
        if n == "kiss":
            c.append((st + sh.word_t(0, 4), "pop"))
            c.append((st + sh.word_t(1, 2), "ding"))
        if n == "breakfast":
            c.append((st + sh.word_t(1, 1) - 0.1, "pop"))
        if n == "deal":
            c.append((st + sh.word_t(1, 4), "pop"))
            c.append((st + sh.word_t(1, 4) + 0.18, "pop"))
            c.append((st + sh.m(2) + 0.4, "stamp"))
        if n == "door":
            c.append((st + sh.m(1) - 0.4, "slide"))
        if n == "piggy":
            c.append((st + sh.m(1), "ding"))
        if n == "melt":
            c.append((st + sh.m(1) - 0.5, "slide"))
            c.append((st + sh.m(1), "stamp"))
        if n == "bye":
            c.append((st + 0.1, "slide"))
            c.append((st + sh.me(1) + 0.2, "pop"))
    return sorted(c, key=lambda x: x[0])


def mix():
    return EP.mix(cues())


def _banner(ctx, t):
    """상단 고정 제목 띠."""
    a = clamp(t / 0.4)
    rrect(ctx, 150, 95, 780, 100, 50)
    S.fs(ctx, "#FFFDF5", lw=7, alpha=0.95 * a)
    draw_text(ctx, "말 잘하는 우리 아기의 아침", 540, 147, 54, font="black", fill="#E2504F", alpha=a)


def render_frame(ctx, t):
    if not EP.shots:
        prepare()
    EP.render_frame(ctx, t)
    _banner(ctx, t)
