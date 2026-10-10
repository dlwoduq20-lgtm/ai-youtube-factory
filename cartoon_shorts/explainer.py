"""해설형(정보 밀도 높은) 쇼츠 공통 엔진.

에피소드는 SCRIPT(샷 목록) + 샷 그리기 함수만 정의하면 되고,
TTS 합성 → 타임라인 배치 → 단어 단위 자막 → 립싱크 → 믹싱은 여기서 처리한다.

자막 문법: "[280조 원]" 처럼 대괄호로 감싼 단어는 노란색 강조 (TTS 에는 괄호 없이 전달).
"""
import math
import re

import numpy as np

from . import audio, tts
from . import squire as S
from .engine import (FPS, H, W, clamp, draw_text, ease_in_out, ease_out_cubic,
                     prog, rrect, set_rgb, text_size)

TRANS = 0.3
LEAD = 0.4
GAP = 0.16
CAP_Y = 1300
CAP_SIZE = 92
HL = "#FFD54A"


class Shot:
    def __init__(self, name, lines, opts):
        self.name, self.lines, self.opts = name, lines, opts
        self.start = self.dur = 0.0
        self.marks = []  # 대사별 (local_start, local_end)
        self.words = []  # 대사별 [(local_start, local_end, 단어)] or None

    def m(self, i):
        return self.marks[i][0]

    def me(self, i):
        return self.marks[i][1]

    def word_t(self, i, k):
        """i번째 대사의 k번째 단어 시작 시각(로컬). 단어 정보가 없으면 비례 추정."""
        w = self.words[i]
        if w and k < len(w):
            return w[k][0]
        n = max(1, len(_plain(self.lines[i][1]).split()))
        return self.m(i) + (self.me(i) - self.m(i)) * k / n


def _plain(text):
    return text.replace("[", "").replace("]", "")


class Episode:
    def __init__(self, title, script, shot_fns, voices, cap_colors=None, camera=None,
                 bgm_style="explain", bpm=92, bgm_gain=0.26, cap_y=CAP_Y):
        self.title, self.script, self.shot_fns = title, script, shot_fns
        self.voices = voices
        self.cap_colors = cap_colors or {}
        self.camera = camera or {}
        self.bgm_style, self.bpm, self.bgm_gain = bgm_style, bpm, bgm_gain
        self.cap_y = cap_y
        self.shots, self.lines, self.env = [], [], {}
        self.voice_track = None
        self.duration = 0.0

    # ------------------------------------------------------------ build
    def prepare(self):
        self.shots, self.lines = [], []
        segs = []
        cur = 0.0
        for name, lines, opts in self.script:
            sh = Shot(name, lines, opts)
            sh.start = cur
            lt = opts.get("lead", LEAD)
            for spk, text in lines:
                parts, words = [], None
                for sp in (("A", "B") if spk == "AB" else (spk,)):
                    v, r, p, *shift = self.voices[sp]  # 4번째 값: (피치 배율, 템포 배율) 음색 변조
                    x, _, w = tts.synth_ex(_plain(text), v, rate=r, pitch=p,
                                           shift=shift[0] if shift else None)
                    parts.append((sp, x))
                    words = words or w
                d = max(len(x) for _, x in parts) / audio.SR
                for sp, x in parts:
                    segs.append((cur + lt, sp, x))
                sh.marks.append((lt, lt + d))
                sh.words.append([(lt + a, lt + b, t) for a, b, t in words] if words else None)
                self.lines.append(dict(start=cur + lt, end=cur + lt + d, spk=spk, text=text,
                                       chunks=self._chunks(text, cur + lt, d, words)))
                lt += d + GAP
            sh.dur = lt - GAP + opts.get("tail", 0.45)
            cur += sh.dur
            self.shots.append(sh)
        self.duration = cur
        n = int(cur * audio.SR) + audio.SR
        self.voice_track = np.zeros(n, np.float32)
        per = {}
        for st, sp, x in segs:
            p = int(st * audio.SR)
            self.voice_track[p:p + len(x)] += x * (0.75 if sp in ("A", "B") else 0.95)
            per.setdefault(sp, np.zeros(n, np.float32))[p:p + len(x)] += x
        hop = audio.SR // FPS
        for k, tr in per.items():
            frames = len(tr) // hop
            rms = np.sqrt(np.mean(tr[:frames * hop].reshape(frames, hop) ** 2, axis=1))
            rms = np.convolve(rms, np.ones(2) / 2, "same")
            peak = np.percentile(rms[rms > 1e-4], 95) if np.any(rms > 1e-4) else 1
            self.env[k] = np.clip(rms / peak, 0, 1)

    @staticmethod
    def _chunks(text, start, dur, words):
        """자막 덩어리 [(시작, 끝, [(단어, 강조여부)])]. edge 단어 타이밍이 있으면 그대로 사용."""
        toks = []
        hl = False
        for raw in text.split():
            open_ = raw.startswith("[")
            word = raw
            if open_:
                hl = True
            close = word.endswith("]") or re.search(r"\][.,?!…]*$", word)
            toks.append((word.replace("[", "").replace("]", ""), hl))
            if close:
                hl = False
        if words and len(words) == len(toks):
            times = [(start + a, start + b) for a, b, _ in words]
        else:
            lens = [len(t[0]) + 1 for t in toks]
            tot = sum(lens)
            acc, times = 0, []
            for ln in lens:
                times.append((start + dur * acc / tot, start + dur * (acc + ln) / tot))
                acc += ln
        chunks, cur, cur_len = [], [], 0
        for (w, h), (a, b) in zip(toks, times):
            if cur and (cur_len + len(w) > 9 or cur[-1][0].endswith((",", ".", "?", "!"))):
                chunks.append(cur)
                cur, cur_len = [], 0
            cur.append((w, h, a, b))
            cur_len += len(w) + 1
        if cur:
            chunks.append(cur)
        out = []
        for i, c in enumerate(chunks):
            st = c[0][2]
            en = chunks[i + 1][0][2] if i + 1 < len(chunks) else start + dur + 0.2
            out.append((st, en, [(w, h) for w, h, _, _ in c]))
        return out

    def mix(self, cues):
        duck = [(ln["start"], ln["end"]) for ln in self.lines]
        return audio.mix(self.duration, cues, bgm_gain=self.bgm_gain, duck=duck,
                         voice=self.voice_track, style=self.bgm_style, bpm=self.bpm)

    def mouth(self, spk, t):
        e = self.env.get(spk)
        if e is None:
            return 0.0
        i = int(t * FPS)
        return float(e[i]) if 0 <= i < len(e) else 0.0

    def speaking(self, spk, t):
        return any(ln["start"] <= t < ln["end"] and spk in ln["spk"] for ln in self.lines)

    # ------------------------------------------------------------ draw
    def caption(self, ctx, t):
        for ln in self.lines:
            for st, en, words in ln["chunks"]:
                if st <= t < en:
                    self._draw_chunk(ctx, t, st, words, ln["spk"])
                    return

    def _draw_chunk(self, ctx, t, st, words, spk):
        k = prog(t, st, st + 0.09)
        sc = 1.16 - 0.16 * ease_out_cubic(k)
        base = self.cap_colors.get(spk, "#FFFFFF")
        sizes = [text_size(w, CAP_SIZE, "black", stroke=12)[0] for w, _ in words]
        gap = 22
        total = sum(sizes) + gap * (len(words) - 1)
        fit = min(1.0, 1000 / max(total, 1))
        ctx.save()
        ctx.translate(W / 2, self.cap_y)
        ctx.scale(sc * fit, sc * fit)
        x = -total / 2
        for (w, hl), wd in zip(words, sizes):
            col = HL if hl else base
            draw_text(ctx, w, x + 7, 9, CAP_SIZE, font="black", fill="#1E1E22", stroke=12,
                      stroke_fill="#1E1E22", anchor=(0, 0.5), alpha=0.55 * k)
            draw_text(ctx, w, x, 0, CAP_SIZE, font="black", fill=col, stroke=12,
                      stroke_fill="#1E1E22", anchor=(0, 0.5), alpha=min(1, k * 2))
            x += wd + gap
        ctx.restore()

    def _draw_shot(self, ctx, i, t):
        sh = self.shots[i]
        lt = t - sh.start
        fx, fy, z = self.camera.get(sh.name, (540, 960, 0.05))
        zoom = 1 + z * ease_in_out(clamp(lt / max(sh.dur, 0.1)))
        ctx.save()
        ctx.translate(fx, fy)
        ctx.scale(zoom, zoom)
        ctx.translate(-fx, -fy)
        self.shot_fns[sh.name](ctx, lt, sh)
        ctx.restore()
        src = sh.opts.get("src")
        if src:
            a = prog(lt, 0.3, 0.8)
            draw_text(ctx, "출처: " + src, W / 2, 1745, 32, font="jua", fill="#F3EBD5",
                      stroke=5, stroke_fill="#1E1E22", alpha=0.9 * a)

    def render_frame(self, ctx, t):
        i = 0
        for j, sh in enumerate(self.shots):
            if sh.start <= t:
                i = j
        sh = self.shots[i]
        lt = t - sh.start
        if i > 0 and lt < TRANS:
            e = ease_in_out(lt / TRANS)
            if i % 2 == 0:
                ctx.save()
                ctx.translate(-W * e, 0)
                self._draw_shot(ctx, i - 1, t)
                ctx.restore()
                ctx.save()
                ctx.translate(W * (1 - e), 0)
                self._draw_shot(ctx, i, t)
                ctx.restore()
                set_rgb(ctx, S.OUT)
                ctx.rectangle(W * (1 - e) - 14, 0, 14, H)
                ctx.fill()
            else:
                ctx.save()
                p = 1 + 0.08 * (1 - e)
                ctx.translate(W / 2, H / 2)
                ctx.scale(p, p)
                ctx.translate(-W / 2, -H / 2)
                self._draw_shot(ctx, i, t)
                ctx.restore()
                if lt < 0.08:
                    ctx.rectangle(0, 0, W, H)
                    set_rgb(ctx, "#FFFFFF", 0.5 * (1 - lt / 0.08))
                    ctx.fill()
        else:
            self._draw_shot(ctx, i, t)
        S.vignette(ctx, 0.35)
        S.grain(ctx, t, 0.05)
        self.caption(ctx, t)


# ---------------------------------------------------------------- 데이터 시각화 헬퍼
def counter(value, k, fmt="{:,.0f}"):
    """0 → value 카운트업 문자열."""
    return fmt.format(value * ease_out_cubic(clamp(k)))


def line_chart(ctx, x, y, w, h, pts, ymin, ymax, k, color=S.RUST, xr=None, label_every=None,
               ref=None, lw=12, dot_last=True, t=0.0, fmt="{:.2f}"):
    """손그림 느낌의 꺾은선 그래프. pts=[(x값, y값)], k=그려진 비율(0~1)."""
    xs = [p[0] for p in pts]
    x0, x1 = xr or (min(xs), max(xs))

    def P(px, py):
        return (x + (px - x0) / (x1 - x0) * w, y + h - (py - ymin) / (ymax - ymin) * h)

    if ref is not None:
        rx0, ry = P(x0, ref[0])
        set_rgb(ctx, "#5A6B7D", 0.8)
        ctx.set_line_width(5)
        ctx.set_dash([18, 14])
        ctx.move_to(x, ry)
        ctx.line_to(x + w, ry)
        ctx.stroke()
        ctx.set_dash([])
        draw_text(ctx, ref[1], x + 8, ry - 34, 40, font="black", fill="#5A6B7D", anchor=(0, 0.5))
    n = len(pts) - 1
    seg = k * n
    full = int(seg)
    path = [P(*pts[0])]
    for i in range(1, min(full, n) + 1):
        path.append(P(*pts[i]))
    if full < n:
        a, b = P(*pts[full]), P(*pts[full + 1])
        f = seg - full
        path.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f))
    if len(path) > 1:
        S.tube(ctx, path, lw, color, lw=5)
    shown = pts[:full + 1]
    for i, (px, py) in enumerate(shown):
        cx, cy = P(px, py)
        from .engine import ellipse
        ellipse(ctx, cx, cy, 13, 13)
        S.fs(ctx, "#FBF7EC", lw=5)
        if label_every is None or i in label_every or i == len(shown) - 1:
            draw_text(ctx, fmt.format(py), cx, cy - 52, 44, font="black", fill="#2E3A4A",
                      stroke=6, stroke_fill="#FBF7EC")
            draw_text(ctx, str(px), cx, y + h + 40, 36, font="black", fill="#5A6B7D")
    return P
