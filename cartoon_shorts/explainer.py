"""해설 애니메이션 쇼츠 공용 틀 (ep03~).

에피소드는 대본(SCRIPT), 화자별 음성(VOICE), 샷 그리기 함수, 효과음 큐만 정의하고
TTS 합성·타임라인 배치·립싱크·자막·전환·믹싱은 이 모듈이 맡는다.

    EP = Explainer(script, voice, cap_color, shot_fns, camera, cues_fn, notice="...")
    prepare, render_frame, mix = EP.prepare, EP.render_frame, EP.mix
"""
import math

import numpy as np

from . import audio, tts
from . import squire as S
from .engine import (FPS, H, W, clamp, draw_text, ease_in_out, ease_out_back, ease_out_cubic,
                     prog, rrect, set_rgb)

TRANS = 0.3  # 샷 전환 시간
LEAD = 0.25  # 샷 시작 후 첫 대사까지
GAP = 0.08  # 대사 사이
TAIL = 0.5  # 샷 끝 여운 배율 (숏폼 템포)


class Shot:
    def __init__(self, name, lines, opts):
        self.name, self.lines, self.opts = name, lines, opts
        self.start = self.dur = 0.0
        self.marks = []  # (local_start, local_end) per line

    def m(self, i):
        return self.marks[i][0]

    def me(self, i):
        return self.marks[i][1]


class Explainer:
    def __init__(self, script, voice, cap_color, shot_fns, camera, cues_fn, notice="",
                 bpm=118):
        """script: [(샷 이름, [(화자, TTS 문장, 자막 or None)], 옵션)]
        voice: 화자 → (edge 음성, 속도, 피치, 추가 피치 배율). 동시 발화는 화자 문자를 이어 쓴다 ("AB").
        shot_fns: 샷 이름 → fn(ctx, lt, sh, ep).  cues_fn(ep) → [(t, kind[, dur])]."""
        self.script, self.voice, self.cap_color = script, voice, cap_color
        self.shot_fns, self.camera, self.cues_fn = shot_fns, camera, cues_fn
        self.notice, self.bpm = notice, bpm
        self.shots, self.lines, self.env, self.cues = [], [], {}, []
        self.duration, self.voice_track = 0.0, None

    # ------------------------------------------------------------ 타임라인
    def prepare(self):
        self.shots.clear()
        self.lines.clear()
        segs = []  # (start, speaker, samples)
        cur = 0.0
        for name, lines, opts in self.script:
            sh = Shot(name, lines, opts)
            sh.start = cur
            lt = LEAD
            for spk, text, cap in lines:
                parts = []
                for sp in spk:
                    v, r, p, k = self.voice[sp]
                    x, _ = tts.synth(text, v, rate=r, pitch=p, shift=k)
                    parts.append((sp, x))
                d = max(len(x) for _, x in parts) / audio.SR
                for sp, x in parts:
                    segs.append((cur + lt, sp, x))
                sh.marks.append((lt, lt + d))
                self.lines.append((cur + lt, cur + lt + d, spk, cap or text))
                lt += d + GAP
            sh.dur = lt - GAP + max(opts.get("tail", 0.45) * TAIL, opts.get("min_tail", 0))
            cur += sh.dur
            self.shots.append(sh)
        self.duration = cur
        n = int(cur * audio.SR) + audio.SR
        self.voice_track = np.zeros(n, np.float32)
        per = {k: np.zeros(n, np.float32) for k in self.voice}
        for st, sp, x in segs:
            p = int(st * audio.SR)
            self.voice_track[p:p + len(x)] += x * 0.9
            per[sp][p:p + len(x)] += x
        hop = audio.SR // FPS
        for k, tr in per.items():  # 립싱크용 음량 엔벨로프 (프레임 단위)
            frames = len(tr) // hop
            rms = np.sqrt(np.mean(tr[:frames * hop].reshape(frames, hop) ** 2, axis=1))
            rms = np.convolve(rms, np.ones(2) / 2, "same")
            peak = np.percentile(rms[rms > 1e-4], 95) if np.any(rms > 1e-4) else 1
            self.env[k] = np.clip(rms / peak, 0, 1)
        self.cues = sorted(self.cues_fn(self), key=lambda c: c[0])
        return self

    def mix(self):
        duck = [(s, e) for s, e, *_ in self.lines]
        return audio.mix(self.duration, self.cues, bgm_gain=0.3, duck=duck,
                         voice=self.voice_track, style="explain", bpm=self.bpm)

    def mouth(self, spk, t):
        e = self.env.get(spk)
        if e is None:
            return 0.0
        i = int(t * FPS)
        return float(e[i]) if 0 <= i < len(e) else 0.0

    # ------------------------------------------------------------ 자막
    @staticmethod
    def _chunks(text):
        out, cur = [], ""
        for w in text.split():
            cand = (cur + " " + w).strip()
            if cur and (len(cand) > 9 or cur.endswith((",", ".", "?", "!"))):
                out.append(cur)
                cur = w
            else:
                cur = cand
        if cur:
            out.append(cur)
        return out

    def _caption(self, ctx, t):
        for st, en, spk, text in self.lines:
            if not st <= t < en + 0.15:
                continue
            chunks = self._chunks(text)
            weights = [len(c.replace(" ", "")) + 1.5 for c in chunks]
            tot = sum(weights)
            acc = st
            for c, w in zip(chunks, weights):
                d = (en - st) * w / tot
                if acc <= t < acc + d or (c is chunks[-1] and t >= acc):
                    k = prog(t, acc, acc + 0.09)
                    sc = 1.18 - 0.18 * ease_out_cubic(k)
                    col = self.cap_color.get(spk, "#FFFFFF")
                    draw_text(ctx, c, W / 2 + 6, 1276, 100, font="black", fill="#1E1E22",
                              stroke=12, stroke_fill="#1E1E22", scale=sc, alpha=0.6 * k)
                    draw_text(ctx, c, W / 2, 1268, 100, font="black", fill=col,
                              stroke=12, stroke_fill="#1E1E22", scale=sc, alpha=min(1, k * 2))
                    return
                acc += d
            return

    # ------------------------------------------------------------ 프레임
    def _draw_shot(self, ctx, i, t):
        sh = self.shots[i]
        lt = t - sh.start
        fx, fy, z = self.camera.get(sh.name, (540, 960, 0.05))
        zoom = 1 + z * ease_in_out(clamp(lt / max(sh.dur, 0.1)))
        ctx.save()
        ctx.translate(fx, fy)
        ctx.scale(zoom, zoom)
        ctx.translate(-fx, -fy)
        self.shot_fns[sh.name](ctx, lt, sh, self)
        ctx.restore()

    def render_frame(self, ctx, t):
        if not self.shots:
            self.prepare()
        i = max(j for j, sh in enumerate(self.shots) if sh.start <= t or j == 0)
        lt = t - self.shots[i].start
        if i > 0 and lt < TRANS:
            e = ease_in_out(lt / TRANS)
            if i % 2 == 0:  # 휙 넘기기
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
            else:  # 펀치 컷
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
        if self.notice:
            draw_text(ctx, self.notice, W / 2, 70, 30, font="black", fill="#FFFFFF", alpha=0.75,
                      stroke=6, stroke_fill="#1E1E22")
        self._caption(ctx, t)


# ---------------------------------------------------------------- 공용 샷 부품
def label(ctx, text, x, y, k, fill="#F3EBD5", ink="#2E3A4A", size=66):
    """둥근 이름표 (k: 0→1 팝업 배율)."""
    if k <= 0.01:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(k, k)
    tw = len(text) * size * 0.95 + 90
    rrect(ctx, -tw / 2, -60, tw, 120, 60)
    S.fs(ctx, fill)
    draw_text(ctx, text, 0, 4, size, font="black", fill=ink)
    ctx.restore()


def close_up(ctx, lt, sh, ep, P, spk, facing, x, base, dark, name, talk_line, calm=False):
    """인물 클로즈업: 옆에서 미끄러져 들어오고, talk_line 번째 대사부터 삿대질 + 효과선.
    calm=True 면 손 허리에 무표정으로 덤덤하게."""
    S.planks(ctx, base=base, dark=dark, seed=facing + 3)
    k = ease_out_cubic(prog(lt, 0.0, 0.5))
    talking = sh.m(talk_line) <= lt
    P.draw(ctx, x - facing * 700 * (1 - k), 1830, 2.05, facing,
           pose="hips" if calm else ("point" if talking else "hips"),
           expr="deadpan" if calm else ("angry" if talking else "smug"),
           mouth=ep.mouth(spk, sh.start + lt) * 1.3, t=lt + facing, bob=not calm)
    label(ctx, name, W / 2 - facing * 230, 250, ease_out_back(prog(lt, 0.4, 0.75)))
    if talking and not calm:
        for i in range(3):  # 말하는 효과선
            a = -0.6 + i * 0.35
            r0 = 300 + 20 * math.sin(lt * 20 + i)
            cx, cy = x + facing * 140, 860
            ctx.move_to(cx + facing * math.cos(a) * r0, cy + math.sin(a) * r0)
            ctx.line_to(cx + facing * math.cos(a) * (r0 + 70), cy + math.sin(a) * (r0 + 70))
        set_rgb(ctx, "#F3EBD5")
        ctx.set_line_width(10)
        ctx.stroke()
