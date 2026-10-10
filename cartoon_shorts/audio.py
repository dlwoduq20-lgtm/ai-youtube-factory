"""BGM / 효과음 절차적 합성 (외부 음원 없이 저작권 걱정 없는 사운드)."""
import math
import wave

import numpy as np

SR = 44100


def _env(n, a=0.005, r=0.1):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / max(r, 1e-4))
    return e


def _sweep(f0, f1, dur):
    n = int(dur * SR)
    f = np.geomspace(f0, f1, n)
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


def _lowpass(x, k):
    """단순 1-pole 저역 통과 (k: 0~1, 클수록 밝음)."""
    y = np.empty_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc += k * (v - acc)
        y[i] = acc
    return y


def _noise(dur, seed=0):
    return np.random.default_rng(seed).uniform(-1, 1, int(dur * SR))


def sfx(kind, seed=0, dur=None):
    if kind == "rain":
        d = dur or 3.0
        n = _noise(d, seed)
        n = n - np.convolve(n, np.ones(3) / 3, "same")
        e = np.minimum(1, np.minimum(np.arange(len(n)), len(n) - np.arange(len(n))) / (0.5 * SR))
        return 0.18 * n * e
    if kind == "gavel":
        d = 0.4
        return 1.0 * _sweep(380, 160, d) * _env(int(d * SR), 0.001, 0.05) + \
            0.5 * _noise(d, seed) * _env(int(d * SR), 0.0005, 0.01)
    if kind == "rip":
        d = 0.35
        n = _noise(d, seed) * (0.5 + 0.5 * np.sign(np.sin(np.arange(int(d * SR)) / SR * 2 * np.pi * 60)))
        return 0.4 * n * _env(int(d * SR), 0.005, 0.12)
    if kind == "cheer":
        d = dur or 1.5
        out = np.zeros(int(d * SR))
        rng = np.random.default_rng(seed)
        for _ in range(14):
            st = int(rng.uniform(0, d * 0.5) * SR)
            f = rng.uniform(500, 900)
            seg = 0.08 * _sweep(f, f * 1.3, 0.4) * _env(int(0.4 * SR), 0.05, 0.2)
            out[st:st + len(seg)] += seg[:len(out) - st]
        return out + 0.1 * _noise(d, seed) * np.linspace(1, 0, len(out))
    if kind == "pop":
        return 0.6 * _sweep(500, 1400, 0.09) * _env(int(0.09 * SR), 0.002, 0.03)
    if kind == "whoosh":
        n = _noise(0.45, seed)
        e = np.sin(np.linspace(0, math.pi, len(n))) ** 2
        return 0.5 * np.convolve(n, np.ones(18) / 18, "same") * e * 2.2
    if kind == "thud":
        d = 0.3
        return 0.9 * _sweep(140, 45, d) * _env(int(d * SR), 0.002, 0.09) + \
            0.2 * _noise(d, seed) * _env(int(d * SR), 0.001, 0.015)
    if kind == "snap":
        d = 0.25
        n = _noise(d, seed)
        hp = n - np.convolve(n, np.ones(6) / 6, "same")
        return 1.1 * hp * _env(int(d * SR), 0.001, 0.04) + 0.5 * _sweep(900, 200, d) * _env(int(d * SR), 0.001, 0.05)
    if kind == "boing":
        d = 0.6
        t = np.arange(int(d * SR)) / SR
        f = 220 + 140 * np.sin(2 * np.pi * 9 * t) * np.exp(-t * 4)
        return 0.5 * np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(len(t), 0.003, 0.25)
    if kind == "stamp":
        d = 0.35
        return 0.9 * _sweep(220, 60, d) * _env(int(d * SR), 0.001, 0.08) + \
            0.5 * _noise(d, seed) * _env(int(d * SR), 0.001, 0.03)
    if kind == "tick":
        d = 0.03
        return 0.25 * _noise(d, seed) * _env(int(d * SR), 0.0005, 0.006)
    if kind == "ding":
        d = 0.9
        t = np.arange(int(d * SR)) / SR
        return 0.35 * (np.sin(2 * np.pi * 1318 * t) + 0.5 * np.sin(2 * np.pi * 1976 * t)) * _env(len(t), 0.002, 0.3)
    if kind == "flip":
        d = 0.08
        return 0.35 * _noise(d, seed) * _env(int(d * SR), 0.001, 0.02)
    if kind == "slide":
        return 0.45 * _sweep(300, 1200, 0.35) * _env(int(0.35 * SR), 0.02, 0.2)
    if kind == "fall":
        return 0.4 * _sweep(1400, 180, 0.9) * _env(int(0.9 * SR), 0.01, 0.6)
    raise ValueError(kind)


def _note(freq, dur, kind="pluck"):
    n = int(dur * SR)
    t = np.arange(n) / SR
    if kind == "bass":
        w = np.sign(np.sin(2 * np.pi * freq * t)) * 0.5 + np.sin(2 * np.pi * freq * t) * 0.5
        return 0.35 * _lowpass(w, 0.08) * _env(n, 0.005, 0.12)
    if kind == "kick":
        return 0.8 * _sweep(120, 40, dur) * _env(n, 0.001, 0.07)
    if kind == "hat":
        return 0.08 * _noise(dur, int(freq)) * _env(n, 0.0005, 0.015)
    # pluck (마림바 느낌)
    w = np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(2 * np.pi * freq * 4 * t) * np.exp(-t * 30)
    return 0.22 * w * _env(n, 0.002, 0.18)


def bgm(duration, bpm=112, seed=4, style="comic"):
    """style=comic: 통통 튀는 C 메이저 / explain: 잔잔한 피치카토 A 마이너 (해설용)
    / cute: 오르골 느낌의 높은 C 메이저, 킥 없음 (육아·일상용)."""
    rng = np.random.default_rng(seed)
    out = np.zeros(int(duration * SR) + SR)
    beat = 60 / bpm
    step = beat / 2
    bass_line = [130.81, 196.0, 174.61, 196.0]  # C G F G
    scale = [523.25, 587.33, 659.25, 783.99, 880.0, 1046.5]
    if style == "explain":
        bass_line = [110.0, 87.31, 130.81, 98.0]  # Am F C G
        scale = [440.0, 523.25, 587.33, 659.25, 783.99, 880.0]
    if style == "cute":
        bass_line = [130.81, 174.61, 110.0, 196.0]  # C F Am G
        scale = [1046.5, 1174.66, 1318.51, 1567.98, 1760.0, 2093.0]
    motif = [rng.integers(0, len(scale)) if rng.random() > 0.25 else -1 for _ in range(16)]
    i = 0
    t = 0.0
    while t < duration:
        pos = int(t * SR)
        bar = int(t / (beat * 4))
        if i % 2 == 0:
            root = bass_line[bar % 4]
            seg = _note(root if (i // 2) % 2 == 0 else root * 1.5, step * 0.9, "bass")
            if style == "cute":
                seg = seg * 0.45
            out[pos:pos + len(seg)] += seg
            if (i // 2) % 2 == 0 and style == "comic":
                k = _note(0, 0.2, "kick")
                out[pos:pos + len(k)] += k
        h = _note(i, 0.05, "hat") * {"comic": 1, "cute": 0.25}.get(style, 0.5)
        out[pos:pos + len(h)] += h
        m = motif[i % 16]
        if m >= 0 and bar % 4 != 3:
            seg = _note(scale[m], step * 1.5)
            out[pos:pos + len(seg)] += seg
        i += 1
        t += step
    return out[:int(duration * SR)]


def mix(duration, cues, bgm_gain=0.55, duck=None, voice=None, style="comic", bpm=112):
    """cues: [(time_sec, kind[, dur])], duck: [(t0, t1)] 구간 BGM 감쇄, voice: 내레이션 트랙."""
    track = bgm(duration, bpm=bpm, style=style) * bgm_gain
    if duck:
        g = np.ones_like(track)
        for t0, t1 in duck:
            g[int(t0 * SR):int(t1 * SR)] = 0.35
        g = np.convolve(g, np.ones(2000) / 2000, "same")
        track *= g
    for i, cue in enumerate(cues):
        t, kind = cue[0], cue[1]
        s = sfx(kind, seed=i, dur=cue[2] if len(cue) > 2 else None)
        p = int(t * SR)
        if p >= len(track):
            continue
        e = min(len(track), p + len(s))
        track[p:e] += s[:e - p]
    if voice is not None:
        n = min(len(voice), len(track))
        track[:n] += voice[:n]
    # 페이드 아웃 + 소프트 리미터
    fo = int(0.8 * SR)
    track[-fo:] *= np.linspace(1, 0, fo)
    track = np.tanh(track * 1.1) * 0.85
    return track


def write_wav(path, data):
    pcm = (np.clip(data, -1, 1) * 32767).astype(np.int16)
    stereo = np.repeat(pcm[:, None], 2, axis=1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(stereo.tobytes())
