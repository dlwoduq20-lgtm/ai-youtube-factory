"""레퍼런스 쇼츠 분석 스크립트 (CLAUDE.md 섹션 2).

사용법:
    pip install yt-dlp faster-whisper
    python ref/analyze.py                # 기본 레퍼런스 2개
    python ref/analyze.py <id 또는 url> ...

하는 일:
  1. yt-dlp 로 영상을 ref/ 에 받는다 (이미 있으면 건너뜀). 분석 전용, 소재 재사용 금지.
  2. faster-whisper(일본어)로 전사 → ref/{id}.transcript.json
  3. 나레이션 속도(표기 글자/초), 총 길이, 첫 발화 시각, 컷 간격(ffmpeg scdet)을 계산
  4. ref/analysis.md 에 수치 + 전사문을 저장 (말투·자막·BGM 등 정성 항목은 사람이 영상을 보고 채운다)
"""
import json
import re
import statistics
import subprocess
import sys
from pathlib import Path

REF = Path(__file__).resolve().parent
DEFAULT_IDS = ["O_m23xvtGtU", "SB9KFy_UqkA"]
WHISPER_MODEL = "large-v3"  # 느리면 "medium"
SCENE_THRESHOLD = 10.0  # scdet 임계값 (0~100). 컷이 너무 많이/적게 잡히면 조정


def video_id(arg):
    m = re.search(r"(?:shorts/|v=|youtu\.be/)([\w-]{11})", arg)
    return m.group(1) if m else arg


def download(vid):
    path = REF / f"{vid}.mp4"
    if not path.exists():
        subprocess.run(["yt-dlp", "-f", "bv*+ba/b", "--merge-output-format", "mp4",
                        "-o", str(path), f"https://www.youtube.com/shorts/{vid}"], check=True)
    return path


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def scene_cuts(path):
    # scdet 가 stderr 로 "lavfi.scd.time: 1.234" 형태로 컷 시각을 찍는다
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-vf",
                          f"scdet=threshold={SCENE_THRESHOLD}", "-an", "-f", "null", "-"],
                         capture_output=True, text=True)
    return [float(t) for t in re.findall(r"lavfi\.scd\.time:\s*([\d.]+)", out.stderr)]


def transcribe(path, vid):
    cache = REF / f"{vid}.transcript.json"
    if cache.exists():
        return json.loads(cache.read_text())
    from faster_whisper import WhisperModel
    model = WhisperModel(WHISPER_MODEL, compute_type="int8")
    segs, _ = model.transcribe(str(path), language="ja", vad_filter=True)
    data = [{"start": s.start, "end": s.end, "text": s.text.strip()} for s in segs]
    cache.write_text(json.dumps(data, ensure_ascii=False, indent=1))
    return data


def count_chars(text):
    # 실제 표기 글자 수: 공백·구두점·기호는 제외
    return len(re.sub(r"[\s、。！？!?「」『』（）()・…ー〜~,.\"'　]", "", text))


def analyze(vid):
    path = download(vid)
    total = duration(path)
    segs = transcribe(path, vid)
    chars = sum(count_chars(s["text"]) for s in segs)
    speech = sum(s["end"] - s["start"] for s in segs)
    cuts = scene_cuts(path)
    bounds = [0.0] + cuts + [total]
    gaps = [b - a for a, b in zip(bounds, bounds[1:])]
    return {
        "id": vid,
        "total": total,
        "first_speech": segs[0]["start"] if segs else None,
        "first_sentence_end": segs[0]["end"] if segs else None,
        "chars": chars,
        "cps_speech": chars / speech if speech else 0,
        "cps_total": chars / total,
        "cuts": len(cuts),
        "cut_avg": statistics.mean(gaps),
        "cut_median": statistics.median(gaps),
        "segs": segs,
    }


def report(results):
    lines = ["# 레퍼런스 분석", "",
             "자동 측정값 (ref/analyze.py). 말투·자막·BGM 등 정성 항목은 영상을 직접 보고 아래에 기록.", "",
             "| 항목 | " + " | ".join(r["id"] for r in results) + " |",
             "|---|" + "---|" * len(results)]
    rows = [
        ("영상 총 길이 (초)", lambda r: f"{r['total']:.1f}"),
        ("나레이션 속도 — 발화 구간 기준 (자/초)", lambda r: f"{r['cps_speech']:.1f}"),
        ("나레이션 속도 — 전체 길이 기준 (자/초)", lambda r: f"{r['cps_total']:.1f}"),
        ("총 글자 수", lambda r: str(r["chars"])),
        ("첫 발화 시작 (초)", lambda r: f"{r['first_speech']:.2f}"),
        ("첫 문장(훅) 끝 (초)", lambda r: f"{r['first_sentence_end']:.2f}"),
        ("컷 수", lambda r: str(r["cuts"])),
        ("컷 간격 평균 / 중앙값 (초)", lambda r: f"{r['cut_avg']:.2f} / {r['cut_median']:.2f}"),
    ]
    for name, fn in rows:
        lines.append(f"| {name} | " + " | ".join(fn(r) for r in results) + " |")
    lines += ["", "## 정성 항목 (수동 기록)", "",
              "- 문장 끝 말투 패턴:", "- 1인칭/화자 캐릭터 성격:", "- 자막 위치·크기·색·외곽선:",
              "- BGM/효과음 사용 방식:", "- 마무리 방식:", ""]
    for r in results:
        lines += [f"## 전사문 — {r['id']}", ""]
        lines += [f"- `{s['start']:5.2f}–{s['end']:5.2f}` {s['text']}" for s in r["segs"]]
        lines.append("")
    (REF / "analysis.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines[:4 + 2 + len(rows)]))


if __name__ == "__main__":
    ids = [video_id(a) for a in sys.argv[1:]] or DEFAULT_IDS
    report([analyze(v) for v in ids])
