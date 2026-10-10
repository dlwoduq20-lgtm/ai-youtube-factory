"""오늘의 만평 #03 — 280조 원을 쓰고도 아이가 줄어든 이유

정보 밀도 높은 해설형 만평. 모든 수치는 공식 통계/보도 기준 (아래 SOURCES).
- 출생아: 1970년 약 100.7만 명 → 2025년 25만 4,300명 (국가데이터처 2025 출생통계)
- 합계출산율: 2005 1.08 → 2023 0.72(역대 최저) → 2024 0.75 → 2025 0.80
- 저출산 예산: 1~3차 기본계획 + 2021년 = 약 280조 원 (저출산고령사회위원회 자료, 경향신문 2023.2 보도)
- 예산 끼워넣기: SW 전문인력 양성, 어린이보호구역 교통환경 사업 등 (머니투데이 2018 전수조사),
  "기존의 다른 목적이나 취지를 가지고 추진되던 사업을 저출산 정책에 포함시킨 경우가 많다" (국회예산정책처 2016.12)
- 사교육비: 참여 학생 1인당 월 60만 4천 원, 역대 최고 (교육부·국가데이터처 2025 사교육비 조사)
- 혼인: 2025년 약 24만 건, 3년 연속 증가·7년 만에 최다. 요인: 30대 초반 인구 증가, 코로나19 기저효과 (국가데이터처)
"""
import math
import random

from .. import squire as S
from ..engine import (H, W, clamp, draw_text, ease_in_out, ease_out_back,
                      ease_out_bounce, ease_out_cubic, ellipse, prog, rrect,
                      set_rgb, wobble)
from ..explainer import Episode, counter, line_chart

TITLE = "오늘의 만평 #03 - 280조 원을 쓰고도 아이가 줄어든 이유"
DURATION = 90.0

A = S.Person(coat="#4E5A6B", tie="#3E8E87", hair="part", hair_color="#4A3426", badge=True)
B = S.Person(coat="#8A6F52", tie="#C9473B", hair="bob", hair_color="#2F2724", badge=True)
GOV = S.Person(coat="#6B6F78", tie="#2F3B4C", hair="part", hair_color="#2A2A2E", glasses=True)
PARENT = S.Person(coat="#7A5C7E", hair="bob", hair_color="#3A2A22")
CIT = S.Person(coat="#6F7F63", hair="beanie", hood=True, pants="#3D4656")

VOICES = {
    "N": ("ko-KR-InJoonNeural", "+16%", "+0Hz"),
    "G": ("ko-KR-HyunsuMultilingualNeural", "+14%", "+0Hz"),
    "P": ("ko-KR-SunHiNeural", "+4%", "-2Hz"),
    "A": ("ko-KR-HyunsuMultilingualNeural", "+12%", "-4Hz"),
    "B": ("ko-KR-SunHiNeural", "+12%", "+4Hz"),
}
CAP_COLORS = {"N": "#FFFFFF", "G": "#BFD7FF", "P": "#F7C6E6", "AB": "#9FE3DA"}

SRC_BIRTH = "국가데이터처 2025 출생통계"
SCRIPT = [
    ("hook", [("N", "[1970년], 이 나라에서 태어난 아기는 [100만 명]."),
              ("N", "그런데 작년엔? [25만 명]. 4분의 1로 줄었습니다.")],
     {"src": SRC_BIRTH, "tail": 0.5}),
    ("budget", [("N", "정부는 [2006년]부터 저출산 대책에 돈을 쏟아부었습니다."),
                ("N", "2021년까지만 따져도 [약 280조 원].")],
     {"src": "저출산고령사회위원회 기본계획 예산"}),
    ("tfr", [("N", "그런데 2005년 [1.08명]이던 합계출산율은, 2023년 [0.72명]까지 떨어졌죠."),
             ("N", "OECD 회원국 중 [유일하게] 1명도 안 되는 나라가 됐습니다.")],
     {"src": "국가데이터처 출생통계", "tail": 0.6}),
    ("jar", [("N", "이쯤 되면 궁금해집니다. 그 많은 돈, 다 어디로 갔을까?")], {"tail": 0.6}),
    ("stickers", [("N", "한 언론이 예산 목록을 전수조사해 보니,"),
                  ("G", "이것도 저출산 예산! 저것도 저출산 예산!"),
                  ("N", "[소프트웨어 인재 양성], [어린이 보호구역 교통 사업]까지 들어가 있었습니다.")],
     {"src": "머니투데이 저출산 예산 전수조사 (2018)", "tail": 0.5}),
    ("nabo", [("N", "국회예산정책처도 지적했죠. 원래 다른 목적이던 사업을 [끼워 넣은 경우가 많다]고요.")],
     {"src": "국회예산정책처 (2016.12)", "tail": 0.8}),
    ("academy", [("N", "그 사이 부모들의 지갑은 어땠을까요?"),
                 ("P", "학원비만 한 달에 [60만 원]이 넘어요..."),
                 ("N", "실제로 사교육 받는 학생 한 명당 월 [60만 4천 원]. 역대 최고입니다.")],
     {"src": "교육부, 국가데이터처 2025 사교육비 조사", "tail": 0.6}),
    ("rebound", [("N", "그런데 반전이 있습니다. 출산율이 [2년 연속] 올랐어요. [0.80명]."),
                 ("N", "결혼도 [3년 연속] 늘어서, [7년 만에 최다]입니다.")],
     {"src": "국가데이터처 2025 출생, 혼인 통계", "tail": 0.6}),
    ("cheer", [("N", "드디어 정책이 통한 걸까요?"), ("AB", "다 저희 정책 덕분입니다!")],
     {"tail": 0.8}),
    ("pyramid", [("N", "통계 당국의 설명은 조금 다릅니다."),
                 ("N", "[30대 초반 인구]가 늘었고, 코로나로 [미뤘던 결혼]이 몰렸다는 거죠.")],
     {"src": "국가데이터처 2025 혼인, 이혼 통계", "tail": 0.6}),
    ("aging", [("N", "이 세대가 지나가고 나면, 그때도 반등이 이어질까요?")], {"tail": 1.0}),
    ("outro", [("N", "[280조 원]보다 중요한 건, [어디에] 쓰느냐 아닐까요?"),
               ("N", "여러분 생각을 댓글로 남겨주세요.")], {"tail": 2.4}),
]

SOURCES = [
    "국가데이터처 2025년 출생통계, 혼인 이혼 통계",
    "교육부, 국가데이터처 2025년 초중고 사교육비 조사",
    "저출산고령사회위원회 기본계획 예산 (경향신문 2023.2.22)",
    "머니투데이 저출산 예산 전수조사 (2018.4)",
    "국회예산정책처 (2016.12)",
]

TFR = [(2005, 1.08), (2010, 1.23), (2015, 1.24), (2018, 0.98), (2020, 0.84),
       (2021, 0.81), (2022, 0.78), (2023, 0.72)]
TFR_UP = [(2023, 0.72), (2024, 0.75), (2025, 0.80)]


# ================================================================ props
def baby(ctx, x, y, r, t=0.0, seed=0):
    ellipse(ctx, x, y + r * 0.9, r * 0.95, r * 0.75)
    S.fs(ctx, "#E9D7B8", lw=4)
    ellipse(ctx, x, y, r, r)
    S.fs(ctx, S.FACE, lw=4)
    set_rgb(ctx, S.OUT)
    ctx.set_line_width(3)
    ctx.arc(x + 3, y - r + 4, 6, math.pi, math.pi * 2.2)
    ctx.stroke()
    blink = (t * 0.5 + seed * 0.37) % 1.0 > 0.95
    for ex in (-r * 0.35, r * 0.35):
        if blink:
            ctx.move_to(x + ex - 4, y)
            ctx.line_to(x + ex + 4, y)
            ctx.stroke()
        else:
            ellipse(ctx, x + ex, y, 3.5, 4.5)
            ctx.fill()


def money_bag(ctx, x, y, s, rot=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    ctx.new_path()
    ctx.move_to(-35, -70)
    ctx.curve_to(-120, -20, -110, 80, 0, 80)
    ctx.curve_to(110, 80, 120, -20, 35, -70)
    ctx.close_path()
    S.fs(ctx, "#D8C08A")
    rrect(ctx, -40, -95, 80, 30, 12)
    S.fs(ctx, "#B99E66")
    draw_text(ctx, "₩", 0, 15, 70, font="black", fill="#6B5427")
    ctx.restore()


def jar(ctx, x, y, s):
    """옹기 (밑 빠진 독)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.new_path()
    ctx.move_to(-150, -300)
    ctx.curve_to(-330, -220, -330, 150, -170, 250)
    ctx.line_to(170, 250)
    ctx.curve_to(330, 150, 330, -220, 150, -300)
    ctx.close_path()
    S.fs(ctx, "#7A4A2E")
    rrect(ctx, -170, -330, 340, 50, 20)
    S.fs(ctx, "#6A3F26")
    ctx.new_path()
    ctx.move_to(-250, -60)
    ctx.curve_to(-100, -20, 100, -20, 250, -60)
    set_rgb(ctx, "#C99A6B", 0.6)
    ctx.set_line_width(10)
    ctx.stroke()
    # 구멍 + 금
    ellipse(ctx, 0, 248, 90, 22)
    S.fs(ctx, "#1E1A18")
    set_rgb(ctx, S.OUT)
    ctx.set_line_width(6)
    ctx.move_to(-60, 230)
    ctx.line_to(-90, 160)
    ctx.line_to(-70, 120)
    ctx.move_to(50, 232)
    ctx.line_to(80, 180)
    ctx.stroke()
    ctx.restore()


def box(ctx, x, y, w, h, label, sticker_k=0.0, rot=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.new_path()
    ctx.move_to(-w / 2, -h)
    ctx.line_to(-w / 2 + 40, -h - 40)
    ctx.line_to(w / 2 + 40, -h - 40)
    ctx.line_to(w / 2, -h)
    ctx.close_path()
    S.fs(ctx, "#D8B47A")
    ctx.new_path()
    ctx.move_to(w / 2, -h)
    ctx.line_to(w / 2 + 40, -h - 40)
    ctx.line_to(w / 2 + 40, -40)
    ctx.line_to(w / 2, 0)
    ctx.close_path()
    S.fs(ctx, "#B88F55")
    rrect(ctx, -w / 2, -h, w, h, 4)
    S.fs(ctx, "#C9A066")
    rrect(ctx, -w / 2 + 25, -h + 25, w - 50, 120, 8)
    S.fs(ctx, "#FBF7EC", lw=4)
    draw_text(ctx, label, 0, -h + 85, 44, font="black", fill="#2E3A4A", spacing=2)
    if sticker_k > 0:
        sc = 2.2 - 1.2 * min(1, sticker_k / 0.3)
        ctx.save()
        ctx.translate(30, -h * 0.38)
        ctx.rotate(-0.2)
        ctx.scale(sc, sc)
        ellipse(ctx, 0, 0, 86, 86)
        S.fs(ctx, S.RUST, lw=6)
        ellipse(ctx, 0, 0, 70, 70)
        set_rgb(ctx, "#FFFFFF")
        ctx.set_line_width(4)
        ctx.stroke()
        draw_text(ctx, "저출산\n예산", 0, 2, 38, font="black", fill="#FFFFFF", spacing=0)
        ctx.restore()
    ctx.restore()


def building(ctx, x, y, w, h, sign, t, seed):
    rrect(ctx, x, y - h, w, h, 4)
    S.fs(ctx, "#3B4352")
    rnd = random.Random(seed)
    for r in range(int((h - 160) / 70)):
        for c in range(int((w - 40) / 60)):
            on = rnd.random() < 0.8
            flick = on and (t * 0.3 + rnd.random()) % 1.0 > 0.02
            rrect(ctx, x + 25 + c * 60, y - h + 150 + r * 70, 38, 46, 4)
            set_rgb(ctx, "#F6D68A" if flick else "#2C323D")
            ctx.fill()
    rrect(ctx, x + 15, y - h + 25, w - 30, 95, 10)
    S.fs(ctx, "#F3EBD5", lw=5)
    draw_text(ctx, sign, x + w / 2, y - h + 72, 54, font="black", fill=S.RUST)


def wallet(ctx, x, y, s, open_k):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rrect(ctx, -110, -70, 220, 140, 20)
    S.fs(ctx, "#6A4429")
    ctx.save()
    ctx.translate(0, -70)
    ctx.scale(1, 1 - 1.6 * open_k)
    rrect(ctx, -110, -60, 220, 60, 16)
    S.fs(ctx, "#7E5434")
    ctx.restore()
    ctx.restore()


def bill(ctx, x, y, rot):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    rrect(ctx, -60, -30, 120, 60, 6)
    S.fs(ctx, "#9CC08B", lw=4)
    draw_text(ctx, "₩", 0, 2, 40, font="black", fill="#3E5A33")
    ctx.restore()


def info_card(ctx, x, y, k, big, small, color=S.RUST, w=640):
    if k <= 0.01:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(k, k)
    rrect(ctx, -w / 2 + 10, -95 + 12, w, 190, 30)
    set_rgb(ctx, S.OUT)
    ctx.fill()
    rrect(ctx, -w / 2, -95, w, 190, 30)
    S.fs(ctx, "#FBF7EC")
    draw_text(ctx, big, 0, -18, 92, font="black", fill=color)
    draw_text(ctx, small, 0, 58, 42, font="black", fill="#5A6B7D")
    ctx.restore()


# ================================================================ shots
def shot_hook(ctx, lt, sh):
    S.planks(ctx)
    t1, t2 = sh.m(0), sh.m(1)
    for side, (x0, label, n, tstart, tlen, total) in enumerate((
            (70, "1970년", 100, t1 + 0.3, 1.6, 100.7), (590, "2025년", 25, sh.word_t(1, 2), 0.7, 25.4))):
        k_lab = ease_out_back(prog(lt, tstart - 0.3, tstart))
        draw_text(ctx, label, x0 + 210, 330, 76, font="black", fill="#F3EBD5", stroke=8,
                  stroke_fill=S.OUT, scale=k_lab)
        for i in range(n):
            ti = tstart + tlen * i / n
            kk = ease_out_back(prog(lt, ti, ti + 0.18), 2.5)
            if kk < 0.02:
                continue
            col, row = i % 10, i // 10
            bx, by = x0 + 22 + col * 42, 1010 - row * 56
            ctx.save()
            ctx.translate(bx, by)
            ctx.scale(kk, kk)
            baby(ctx, 0, 0, 17, lt, i)
            ctx.restore()
        kc = prog(lt, tstart, tstart + tlen)
        if kc > 0:
            draw_text(ctx, counter(total, kc, "{:.1f}만 명"),
                      x0 + 210, 1130, 66, font="black", fill="#FFD54A", stroke=8, stroke_fill=S.OUT)
    draw_text(ctx, "아기 1명 = 1만 명", W / 2, 1190, 40, font="jua", fill="#F3EBD5",
              alpha=prog(lt, t1 + 0.5, t1 + 1.0) * 0.9)
    S.stamp(ctx, 800, 560, "1/4", prog(lt, sh.me(1) - 0.8, sh.me(1) - 0.2), size=150, rot=0.12)


def shot_budget(ctx, lt, sh):
    S.planks(ctx, base="#4A5D73", dark="#3D4E61")
    S.spotlight(ctx, 540, -50, 260, 900, 1300, alpha=0.25)
    # 냄비(예산 항아리)
    rrect(ctx, 220, 860, 640, 330, 60)
    S.fs(ctx, "#5E6670")
    rrect(ctx, 190, 830, 700, 70, 30)
    S.fs(ctx, "#6E7782")
    draw_text(ctx, "저출산 예산", 540, 1040, 84, font="black", fill="#F3EBD5")
    rnd = random.Random(3)
    for i in range(26):
        t0 = 0.3 + i * 0.22
        k = (lt - t0) / 0.7
        if 0 <= k < 1:
            bx = 540 + rnd.uniform(-220, 220)
            money_bag(ctx, bx, -120 + 1000 * k * k, 0.8, rot=rnd.uniform(-0.4, 0.4))
        else:
            rnd.uniform(-220, 220), rnd.uniform(-0.4, 0.4)
    ky = prog(lt, 0.3, sh.me(0))
    yr = 2006 + int(15 * ky)
    draw_text(ctx, f"{yr}년", 540, 330, 120, font="black", fill="#F3EBD5", stroke=10, stroke_fill=S.OUT)
    kt = prog(lt, sh.m(1), sh.word_t(1, 2) + 0.4)
    if kt > 0:
        draw_text(ctx, counter(280, kt, "약 {:.0f}조 원"), 540, 560, 130, font="black",
                  fill="#FFD54A", stroke=12, stroke_fill=S.OUT, scale=ease_out_back(prog(lt, sh.m(1), sh.m(1) + 0.3)))


def _chart_base(ctx, title):
    S.desk(ctx)
    S.graph_paper(ctx, 50, 150, 980, 1050)
    draw_text(ctx, title, 540, 240, 72, font="black", fill="#2E3A4A")


def shot_tfr(ctx, lt, sh):
    _chart_base(ctx, "합계출산율 (명)")
    k = prog(lt, sh.m(0) + 0.2, sh.me(0) - 0.2)
    line_chart(ctx, 130, 380, 820, 640, TFR, 0.5, 1.4, k, xr=(2005, 2025), ref=(1.0, "1명"),
               label_every={0, 2, 7})
    ks = prog(lt, sh.m(1) + 0.3, sh.m(1) + 0.9)
    S.stamp(ctx, 540, 1145, "OECD 유일 1명 미만", ks, size=72, rot=-0.04)


def shot_jar(ctx, lt, sh):
    S.planks(ctx, base="#5B4A3F", dark="#4A3B31", w=160)
    ctx.rectangle(0, 1250, W, H)
    set_rgb(ctx, "#6E5C4E")
    ctx.fill()
    jar(ctx, 540, 1000, 1.25)
    rnd = random.Random(8)
    for i in range(30):  # 위로 들어가는 돈
        t0 = i * 0.13
        k = ((lt - t0) * 0.9) % 1.6
        if lt < t0 or k > 1:
            continue
        x = 540 + rnd.uniform(-140, 140)
        bill(ctx, x + math.sin(k * 6 + i) * 30, -80 + 620 * k, k * 4 + i)
    for i in range(30):  # 아래로 새는 돈
        t0 = 0.4 + i * 0.13
        k = ((lt - t0) * 0.9) % 1.6
        if lt < t0 or k > 1:
            continue
        x = 540 + rnd.uniform(-60, 60)
        bill(ctx, x + k * rnd.uniform(-400, 400), 1310 + 600 * k * k, k * 6 + i)
    kq = ease_out_back(prog(lt, sh.me(0) - 1.2, sh.me(0) - 0.8), 2.4)
    draw_text(ctx, "?", 860, 420, 260, font="black", fill="#FFD54A", stroke=12, stroke_fill=S.OUT,
              scale=kq, rot=0.2 + wobble(lt, 1, 0.08, 3))


def shot_stickers(ctx, lt, sh):
    S.planks(ctx, base="#4F6378", dark="#405265", seed=11)
    ctx.rectangle(0, 1120, W, H)
    set_rgb(ctx, "#8C7A5E")
    ctx.fill()
    ks = ease_out_back(prog(lt, 0.1, 0.5))
    if ks > 0.01:
        ctx.save()
        ctx.translate(540, 420)
        ctx.scale(ks, ks)
        ctx.rotate(-0.03)
        rrect(ctx, -380, -110, 760, 220, 18)
        S.fs(ctx, "#F3EBD5")
        draw_text(ctx, "'저출산 예산' 목록", 0, -20, 80, font="black", fill="#2E3A4A")
        draw_text(ctx, "2006~2017년 전수조사 중 일부", 0, 62, 40, font="jua", fill="#5A6B7D")
        ctx.restore()
    labels = ["SW 인재\n양성", "어린이보호구역\n교통 사업", "청소년\n범죄 예방"]
    # 스티커 붙는 시각: G 대사의 각 단어 + 마지막 내레이션
    slap = [sh.word_t(1, 0), sh.word_t(1, 2), sh.m(2) + 0.2]
    for i, (lb, bx) in enumerate(zip(labels, (210, 540, 870))):
        kb = ease_out_bounce(prog(lt, 0.1 + i * 0.15, 0.6 + i * 0.15))
        box(ctx, bx, lerp_(-300, 1130, kb), 290 if i != 1 else 310, 330, lb,
            sticker_k=prog(lt, slap[i], slap[i] + 0.5))
    talking = sh.m(1) <= lt < sh.me(1)
    GOV.draw(ctx, 540, 2200, 1.35, 1, pose="point" if talking else "hips",
             expr="smug", mouth=1.3 * S_mouth("G", sh.start + lt), t=lt)


def S_mouth(spk, t):
    return EP.mouth(spk, t)


def lerp_(a, b, k):
    return a + (b - a) * k


NABO_QUOTE = "기존의 다른 목적이나\n취지를 가지고 추진되던\n사업을 저출산 정책에\n포함시킨 경우가 많다"


def shot_nabo(ctx, lt, sh):
    S.desk(ctx)
    ctx.save()
    ctx.translate(540, 820)
    ctx.rotate(-0.03)
    rrect(ctx, -440, -470, 880, 940, 10)
    S.fs(ctx, "#FBF8EF")
    rrect(ctx, -440, -470, 880, 140, 10)
    S.fs(ctx, "#2E3A4A")
    draw_text(ctx, "국회예산정책처", 0, -400, 66, font="black", fill="#F3EBD5")
    n = int(len(NABO_QUOTE) * prog(lt, 0.3, sh.me(0) - 0.6))
    draw_text(ctx, "“", -360, -250, 160, font="black", fill=S.RUST)
    lines = NABO_QUOTE[:n].split("\n")
    for i, line in enumerate(lines):
        draw_text(ctx, line, -340, -170 + i * 110, 70, font="jua", fill="#2E2E33", anchor=(0, 0.5))
    ku = prog(lt, sh.me(0) - 0.6, sh.me(0))
    if ku > 0:  # 마지막 줄 형광펜
        ctx.rectangle(-345, 140, 600 * ku, 46)
        set_rgb(ctx, "#FFD54A", 0.55)
        ctx.fill()
    draw_text(ctx, "2016.12", 300, 360, 46, font="black", fill="#5A6B7D")
    ctx.restore()


def shot_academy(ctx, lt, sh):
    S.sky(ctx, "#1F2737", "#3A4458")
    for i in range(30):
        rnd = random.Random(i)
        ellipse(ctx, rnd.uniform(0, W), rnd.uniform(0, 600), 3, 3)
        set_rgb(ctx, "#F3EBD5", 0.5 + 0.5 * math.sin(lt * 3 + i))
        ctx.fill()
    for i, (x, w, h, sign) in enumerate(((-20, 300, 1050, "수학"), (300, 260, 1250, "영어"),
                                         (580, 240, 980, "논술"), (840, 280, 1150, "코딩"))):
        building(ctx, x, 1500, w, h, sign, lt, i)
    ctx.rectangle(0, 1500, W, H)
    set_rgb(ctx, "#4A4F5A")
    ctx.fill()
    talking = sh.m(1) <= lt < sh.me(1)
    PARENT.draw(ctx, 330, 2090, 1.3, 1, pose="shrug" if talking else "down",
                expr="sad", mouth=1.3 * S_mouth("P", sh.start + lt), t=lt, sweat=talking)
    ko = prog(lt, sh.m(1), sh.m(1) + 0.4)
    wallet(ctx, 760, 1680, 1.0, ko)
    if lt > sh.m(1):
        rnd = random.Random(2)
        for i in range(14):
            t0 = sh.m(1) + i * 0.15
            k = (lt - t0) / 1.2
            if 0 <= k < 1:
                bill(ctx, 760 + rnd.uniform(-300, 300) * k, 1600 - 900 * k + 500 * k * k,
                     k * rnd.uniform(-6, 6))
            else:
                rnd.uniform(0, 1), rnd.uniform(0, 1)
    kc = ease_out_back(prog(lt, sh.m(2) + 0.2, sh.m(2) + 0.6), 1.8)
    info_card(ctx, 540, 330, kc, "월 60.4만 원", "사교육 참여 학생 1인당 (역대 최고)")


def shot_rebound(ctx, lt, sh):
    _chart_base(ctx, "합계출산율 (명)")
    P = line_chart(ctx, 130, 380, 820, 640, TFR, 0.5, 1.4, 1.0, xr=(2005, 2025),
                   ref=(1.0, "1명"), label_every={0, 2})
    k = prog(lt, sh.m(0) + 0.6, sh.m(0) + 2.6)
    line_chart(ctx, 130, 380, 820, 640, TFR_UP, 0.5, 1.4, k, color="#4E9A6A",
               xr=(2005, 2025), label_every={2})
    if k >= 1:
        x, y = P(2025, 0.80)
        for i in range(8):
            a = i * math.pi / 4 + lt * 2
            r = 40 + 10 * math.sin(lt * 10)
            ctx.move_to(x + math.cos(a) * r, y + math.sin(a) * r)
            ctx.line_to(x + math.cos(a) * (r + 30), y + math.sin(a) * (r + 30))
        set_rgb(ctx, "#E8B93E")
        ctx.set_line_width(7)
        ctx.stroke()
    kc = ease_out_back(prog(lt, sh.m(1) + 0.2, sh.m(1) + 0.6), 1.8)
    info_card(ctx, 540, 1110, kc, "혼인 약 24만 건", "3년 연속 증가, 7년 만에 최다", color="#4E9A6A")


def shot_cheer(ctx, lt, sh):
    S.planks(ctx, base="#B9A57A", dark="#9C8960", w=150)
    ctx.save()
    ctx.translate(540, 900)
    for i in range(16):
        ctx.rotate(math.pi / 8)
        ctx.move_to(0, 0)
        ctx.line_to(-90, -1400)
        ctx.line_to(90, -1400)
        ctx.close_path()
    set_rgb(ctx, "#FFF3C4", 0.35)
    ctx.fill()
    ctx.restore()
    shouting = lt >= sh.m(1)
    for P, x, f, spk in ((A, 300, 1, "A"), (B, 780, -1, "B")):
        P.draw(ctx, x, 1640, 1.25, f, pose="cheer" if shouting else "hips", expr="smug",
               mouth=1.3 * S_mouth(spk, sh.start + lt), t=lt + (0 if f > 0 else 0.5))
    kb = ease_out_back(prog(lt, 0.3, 0.7))
    if kb > 0.01:
        ctx.save()
        ctx.translate(540, 330)
        ctx.scale(kb, kb)
        ctx.rotate(-0.04)
        rrect(ctx, -330, -80, 660, 160, 20)
        S.fs(ctx, S.RUST)
        draw_text(ctx, "출산율 반등!", 0, 4, 90, font="black", fill="#FFFFFF")
        ctx.restore()
    S.confetti(ctx, lt, sh.m(1))


AGES = list(range(0, 85, 5))


def _pyramid_val(age, shift):
    """인구 피라미드 모양 (설명용 도식): 30대 초반 + 50대에 볼록."""
    a = age - shift
    v = 0.55 + 0.25 * math.exp(-((a - 32) / 6) ** 2) + 0.35 * math.exp(-((a - 52) / 9) ** 2)
    v -= 0.25 * clamp((15 - age) / 15)  # 아래(어린 세대)는 좁음
    v -= 0.35 * clamp((age - 65) / 20)
    return max(0.08, v)


def _pyramid(ctx, lt, shift, hl_band):
    top, bot = 330, 1150
    bh = (bot - top) / len(AGES)
    for i, age in enumerate(AGES):
        y = bot - (i + 1) * bh
        v = _pyramid_val(age, shift)
        w = 400 * v
        hl = hl_band[0] <= age < hl_band[1]
        for sg, col in ((-1, "#6F8FB0"), (1, "#C98B7A")):
            x = 540 if sg > 0 else 540 - w
            rrect(ctx, x + (6 if sg > 0 else -6), y + 4, w, bh - 8, 6)
            S.fs(ctx, ("#FFD54A" if hl else col), lw=4)
        if age % 10 == 0:
            draw_text(ctx, f"{age}", 540, y + bh / 2, 30, font="black", fill="#2E3A4A",
                      stroke=4, stroke_fill="#FBF7EC")
    draw_text(ctx, "남", 230, bot + 50, 46, font="black", fill="#4E6E90")
    draw_text(ctx, "여", 850, bot + 50, 46, font="black", fill="#A86A5A")
    draw_text(ctx, "※ 모양은 설명을 위한 도식", W / 2, bot + 110, 32, font="jua", fill="#5A6B7D")


def shot_pyramid(ctx, lt, sh):
    S.desk(ctx)
    S.graph_paper(ctx, 50, 150, 980, 1150)
    draw_text(ctx, "인구 구조", 540, 240, 72, font="black", fill="#2E3A4A")
    on = lt >= sh.word_t(1, 0)
    _pyramid(ctx, lt, 0, (30, 35) if on else (-1, -1))
    k1 = ease_out_back(prog(lt, sh.word_t(1, 0), sh.word_t(1, 0) + 0.35), 2.0)
    if k1 > 0.01:
        ctx.save()
        ctx.translate(880, 1150 - 6.5 * (820 / len(AGES)))
        ctx.scale(k1, k1)
        rrect(ctx, -150, -55, 300, 110, 20)
        S.fs(ctx, "#FFD54A")
        draw_text(ctx, "30대 초반", 0, 2, 50, font="black", fill="#2E3A4A")
        ctx.restore()
    k2 = ease_out_back(prog(lt, sh.word_t(1, 4), sh.word_t(1, 4) + 0.35), 2.0)
    if k2 > 0.01:  # 결혼 반지
        ctx.save()
        ctx.translate(200, 520)
        ctx.scale(k2, k2)
        for dx, col in ((-35, "#E8B93E"), (35, "#D9DDE3")):
            ctx.new_path()
            ctx.arc(dx, 0, 55, 0, 2 * math.pi)
            set_rgb(ctx, S.OUT)
            ctx.set_line_width(26)
            ctx.stroke()
            ctx.arc(dx, 0, 55, 0, 2 * math.pi)
            set_rgb(ctx, col)
            ctx.set_line_width(14)
            ctx.stroke()
        draw_text(ctx, "미룬 결혼", 0, 110, 46, font="black", fill="#2E3A4A", stroke=6,
                  stroke_fill="#FBF7EC")
        ctx.restore()


def shot_aging(ctx, lt, sh):
    S.desk(ctx)
    S.graph_paper(ctx, 50, 150, 980, 1150)
    draw_text(ctx, "10년 뒤라면?", 540, 240, 72, font="black", fill="#2E3A4A")
    shift = 10 * ease_in_out(prog(lt, 0.3, sh.me(0) - 0.3))
    _pyramid(ctx, lt, shift, (30, 35))
    kq = ease_out_back(prog(lt, sh.me(0) - 0.8, sh.me(0) - 0.4), 2.4)
    draw_text(ctx, "?", 860, 1000, 240, font="black", fill=S.RUST, stroke=12, stroke_fill=S.OUT,
              scale=kq, rot=0.15)


def shot_outro(ctx, lt, sh):
    S.planks(ctx, seed=9)
    waving = lt >= sh.m(1)
    CIT.draw(ctx, 300, 2000, 1.7, 1, pose="wave" if waving else "down",
             expr="neutral" if waving else "deadpan", t=lt)
    k = ease_out_back(prog(lt, 0.2, 0.6))
    if k > 0.01:
        ctx.save()
        ctx.translate(560, 560)
        ctx.scale(k, k)
        rrect(ctx, -420, -360, 840, 720, 26)
        S.fs(ctx, "#F3EBD5")
        draw_text(ctx, "이번 영상 출처", 0, -295, 54, font="black", fill="#2E3A4A")
        for i, s in enumerate(SOURCES):
            draw_text(ctx, s, -380, -200 + i * 105, 34, font="jua", fill="#3A3F4A", anchor=(0, 0.5))
        ctx.restore()
    k2 = ease_out_back(prog(lt, sh.m(1), sh.m(1) + 0.4), 2.0)
    if k2 > 0.01:
        ctx.save()
        ctx.translate(760, 1560)
        ctx.scale(k2, k2)
        rrect(ctx, -230, -70, 460, 140, 70)
        S.fs(ctx, S.RUST)
        draw_text(ctx, "댓글 남기기", 0, 4, 60, font="black", fill="#FFFFFF")
        ctx.restore()


SHOT_FNS = {k[5:]: v for k, v in dict(globals()).items() if k.startswith("shot_")}
CAMERA = {
    "hook": (540, 800, 0.05), "budget": (540, 900, 0.08), "tfr": (540, 700, 0.06),
    "jar": (540, 1000, 0.1), "stickers": (540, 1200, 0.05), "nabo": (540, 820, 0.08),
    "academy": (540, 1100, 0.07), "rebound": (700, 700, 0.08), "cheer": (540, 1000, 0.06),
    "pyramid": (540, 700, 0.05), "aging": (540, 700, 0.05), "outro": (540, 900, 0.03),
}

EP = Episode(TITLE, SCRIPT, SHOT_FNS, VOICES, CAP_COLORS, CAMERA)


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
        if n == "hook":
            for j in range(0, 100, 4):
                c.append((st + sh.m(0) + 0.3 + 1.6 * j / 100, "tick"))
            for j in range(0, 25, 2):
                c.append((st + sh.word_t(1, 2) + 0.7 * j / 25, "tick"))
            c.append((st + sh.me(1) - 0.8, "stamp"))
        if n == "budget":
            for j in range(26):
                c.append((st + 0.3 + j * 0.22 + 0.6, "thud"))
            c.append((st + sh.m(1), "ding"))
        if n == "tfr":
            c.append((st + sh.m(0) + 0.2, "fall"))
            c.append((st + sh.m(1) + 0.3, "stamp"))
        if n == "jar":
            c.append((st + sh.me(0) - 1.2, "boing"))
        if n == "stickers":
            for j in range(3):
                c.append((st + 0.3 + j * 0.15, "thud"))
            for tt in (sh.word_t(1, 0), sh.word_t(1, 2), sh.m(2) + 0.2):
                c.append((st + tt + 0.1, "stamp"))
        if n == "nabo":
            for j in range(0, 30):
                tt = 0.3 + (sh.me(0) - 0.9) * j / 30
                c.append((st + tt, "tick"))
        if n == "academy":
            c.append((st + sh.m(1), "rip"))
            c.append((st + sh.m(2) + 0.2, "pop"))
        if n == "rebound":
            c.append((st + sh.m(0) + 0.6, "slide"))
            c.append((st + sh.m(0) + 2.6, "ding"))
            c.append((st + sh.m(1) + 0.2, "pop"))
        if n == "cheer":
            c.append((st + 0.3, "pop"))
            c.append((st + sh.m(1), "cheer", 2.0))
        if n == "pyramid":
            c.append((st + sh.word_t(1, 0), "pop"))
            c.append((st + sh.word_t(1, 4), "pop"))
        if n == "aging":
            c.append((st + sh.me(0) - 0.8, "boing"))
        if n == "outro":
            c.append((st + 0.2, "pop"))
            c.append((st + sh.m(1), "ding"))
    return sorted(c, key=lambda x: x[0])


def mix():
    return EP.mix(cues())


def render_frame(ctx, t):
    if not EP.shots:
        prepare()
    EP.render_frame(ctx, t)
