"""TTS 내레이션.

백엔드 우선순위:
  1. edge-tts  : 무료 고품질 한국어 신경망 음성 남/녀 (speech.platform.bing.com 접속 필요)
  2. google    : 구글 번역 TTS (translate.googleapis.com) — 자연스러운 한국어 여성 음성 1종.
                 캐릭터 구분은 피치 시프트로 처리. 비공식 엔드포인트라 상업 배포 전 교체 권장.
  3. espeak-ng : 오프라인 대체 (기계음) — espeakng-loader 패키지에 라이브러리/데이터 포함

결과는 .cache/tts/ 에 캐시되며 (SR=44100 mono float32 배열, 길이초) 를 돌려준다.
환경변수 TTS_BACKEND=edge|espeak 로 강제할 수 있다.
"""
import asyncio
import ctypes
import hashlib
import os
import subprocess

import numpy as np

from .audio import SR

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, ".cache", "tts")

VOICES = {
    "female": "ko-KR-SunHiNeural",
    "male": "ko-KR-InJoonNeural",
    "male2": "ko-KR-HyunsuMultilingualNeural",
}


def _decode(path):
    """ffmpeg 로 임의 오디오 → 44.1kHz mono float32."""
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
        check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def _edge(text, voice, rate, pitch, out):
    import edge_tts

    async def run():
        await edge_tts.Communicate(text, voice, rate=rate, pitch=pitch).save(out)

    asyncio.run(run())


# google 백엔드에서 음성별 (피치 배율, 속도 배율) — 원본은 여성 음성 1종
GOOGLE_STYLE = {
    "ko-KR-InJoonNeural": (1.0, 1.18),            # 내레이터: 원음 그대로
    "ko-KR-HyunsuMultilingualNeural": (0.82, 1.22),  # 남자 캐릭터: 낮게
    "ko-KR-SunHiNeural": (1.08, 1.22),            # 여자 캐릭터: 살짝 높게
}


def _google(text, voice, rate, pitch, out):
    import urllib.parse
    import urllib.request
    url = ("https://translate.googleapis.com/translate_tts?client=gtx&ie=UTF-8&tl=ko&q="
           + urllib.parse.quote(text))
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    raw = out + ".raw.mp3"
    with urllib.request.urlopen(req, timeout=20) as r, open(raw, "wb") as f:
        f.write(r.read())
    p, tempo = GOOGLE_STYLE.get(voice, (1.0, 1.15))
    af = f"rubberband=pitch={p}:tempo={tempo}:formant=preserved" if p != 1.0 else f"atempo={tempo}"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", af, "-ar", str(SR), out],
                   check=True)
    os.remove(raw)


def _espeak(text, voice, rate, pitch, out):
    import espeakng_loader
    lib = ctypes.cdll.LoadLibrary(espeakng_loader.get_library_path())
    data = espeakng_loader.get_data_path().encode()
    sr = lib.espeak_Initialize(0x02, 0, data, 0)  # AUDIO_OUTPUT_SYNCHRONOUS
    chunks = []
    CB = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_short), ctypes.c_int, ctypes.c_void_p)

    def cb(wav, n, _ev):
        if wav and n > 0:
            chunks.append(np.ctypeslib.as_array(wav, shape=(n,)).copy())
        return 0

    keep = CB(cb)
    lib.espeak_SetSynthCallback(keep)
    variant = {"ko-KR-SunHiNeural": b"ko+f3", "ko-KR-InJoonNeural": b"ko+m3"}.get(voice, b"ko+m1")
    lib.espeak_SetVoiceByName(variant)
    speed = int(175 * (1 + int(rate.rstrip("%") or 0) / 100))
    lib.espeak_SetParameter(1, speed, 0)  # espeakRATE
    lib.espeak_SetParameter(3, 50 + int(pitch.replace("Hz", "") or 0), 0)  # espeakPITCH
    buf = text.encode("utf-8") + b"\0"
    lib.espeak_Synth(buf, len(buf), 0, 0, 0, 0x01, None, None)  # espeakCHARS_UTF8
    lib.espeak_Synchronize()
    pcm = np.concatenate(chunks) if chunks else np.zeros(1, np.int16)
    import wave
    with wave.open(out, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.astype(np.int16).tobytes())


def synth(text, voice="female", rate="+10%", pitch="+0Hz"):
    """텍스트 → (samples, seconds). voice 는 VOICES 키 또는 edge 음성 이름."""
    voice = VOICES.get(voice, voice)
    backend = os.environ.get("TTS_BACKEND")
    os.makedirs(CACHE, exist_ok=True)
    order = [backend] if backend else ["edge", "google", "espeak"]
    last = None
    for b in order:
        key = hashlib.sha1(f"{b}|{voice}|{rate}|{pitch}|{text}".encode()).hexdigest()[:16]
        out = os.path.join(CACHE, f"{key}.{'mp3' if b == 'edge' else 'wav'}")
        if not (os.path.exists(out) and os.path.getsize(out) > 0):
            try:
                {"edge": _edge, "google": _google, "espeak": _espeak}[b](text, voice, rate, pitch, out)
            except Exception as e:  # noqa: BLE001 — 다음 백엔드로 폴백
                last = e
                if os.path.exists(out):
                    os.remove(out)
                print(f"[tts] {b} 실패 → 폴백: {type(e).__name__}")
                continue
        x = _decode(out)
        # 앞뒤 무음 정리
        nz = np.nonzero(np.abs(x) > 0.01)[0]
        if len(nz):
            x = x[max(0, nz[0] - 600): nz[-1] + 2000]
        return x, len(x) / SR
    raise RuntimeError(f"TTS 실패: {last}")
