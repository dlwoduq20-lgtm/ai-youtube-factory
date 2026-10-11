"""만평 쇼츠용 경량 2D 모션그래픽 엔진 (pycairo + Pillow).

- 좌표계: 1080x1920 (세로 쇼츠), 30fps
- 텍스트는 Pillow 로 한글 폰트를 래스터화한 뒤 cairo 서피스로 캐시해서 사용
"""
import math
import os
import random

import cairo
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = {
    "jua": os.path.join(ROOT, "assets", "fonts", "Jua.ttf"),
    "black": os.path.join(ROOT, "assets", "fonts", "BlackHanSans.ttf"),
}

INK = (0.07, 0.07, 0.09)


# ---------------------------------------------------------------- easing
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def prog(t, t0, t1):
    """t 가 [t0, t1] 구간에서 0→1 로 진행하는 비율."""
    if t1 <= t0:
        return 1.0 if t >= t1 else 0.0
    return clamp((t - t0) / (t1 - t0))


def lerp(a, b, k):
    return a + (b - a) * k


def ease_out_cubic(x):
    return 1 - (1 - x) ** 3


def ease_in_cubic(x):
    return x ** 3


def ease_in_out(x):
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def ease_out_back(x, s=1.9):
    x -= 1
    return 1 + (s + 1) * x ** 3 + s * x ** 2


def ease_out_elastic(x):
    if x <= 0 or x >= 1:
        return clamp(x)
    return 2 ** (-10 * x) * math.sin((x * 10 - 0.75) * (2 * math.pi) / 3) + 1


def ease_out_bounce(x):
    n, d = 7.5625, 2.75
    if x < 1 / d:
        return n * x * x
    if x < 2 / d:
        x -= 1.5 / d
        return n * x * x + 0.75
    if x < 2.5 / d:
        x -= 2.25 / d
        return n * x * x + 0.9375
    x -= 2.625 / d
    return n * x * x + 0.984375


def hexc(h, a=None):
    h = h.lstrip("#")
    c = tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return c if a is None else c + (a,)


def wobble(t, seed, amp=1.0, freq=1.0):
    """부드러운 의사 노이즈 (손그림 흔들림용)."""
    return amp * (math.sin(t * freq * 2.1 + seed * 1.7) * 0.6
                  + math.sin(t * freq * 3.7 + seed * 4.3) * 0.4)


# ---------------------------------------------------------------- text
_font_cache = {}
_text_cache = {}


def _font(name, size):
    key = (name, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(FONTS.get(name, name), size)
    return _font_cache[key]


# 한글 폰트에 없는 기호(· ↑ ↓ → … ① 등)는 이 폰트로 대신 그린다
FALLBACK_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
_cmap_cache = {}


def _cmap(path):
    if path not in _cmap_cache:
        from fontTools.ttLib import TTFont
        _cmap_cache[path] = set(TTFont(path).getBestCmap())
    return _cmap_cache[path]


def _missing(text, font):
    if not os.path.exists(FALLBACK_FONT):
        return False
    cmap = _cmap(FONTS[font])
    return any(ord(ch) not in cmap for ch in text if ch not in " \n")


def _line_image(line, size, font, fill, stroke, stroke_fill):
    """한 줄을 글자 단위로 주 폰트/대체 폰트 구간으로 나눠 기준선에 맞춰 이어 그린다."""
    cmap = _cmap(FONTS[font])
    runs = []
    for ch in line:
        fb = ch != " " and ord(ch) not in cmap
        if runs and runs[-1][1] == fb:
            runs[-1][0] += ch
        else:
            runs.append([ch, fb])
    fonts = {False: _font(font, size), True: _font(FALLBACK_FONT, size)}
    asc = max(fonts[fb].getmetrics()[0] for _, fb in runs) if runs else size
    desc = max(fonts[fb].getmetrics()[1] for _, fb in runs) if runs else 0
    widths = [fonts[fb].getlength(txt) for txt, fb in runs]
    pad = 4 + stroke
    w, h = math.ceil(sum(widths)) + pad * 2, asc + desc + pad * 2
    img = Image.new("RGBA", (max(w, 1), max(h, 1)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x = pad
    for (txt, fb), wd in zip(runs, widths):
        d.text((x, pad + asc), txt, font=fonts[fb], fill=fill, anchor="ls",
               stroke_width=stroke, stroke_fill=stroke_fill)
        x += wd
    return img


def pil_to_surface(img):
    arr = np.asarray(img.convert("RGBA"), dtype=np.uint16)
    a = arr[..., 3:4]
    rgb = (arr[..., :3] * a // 255).astype(np.uint8)
    bgra = np.concatenate([rgb[..., ::-1], a.astype(np.uint8)], axis=2)
    h, w = bgra.shape[:2]
    stride = cairo.ImageSurface.format_stride_for_width(cairo.FORMAT_ARGB32, w)
    buf = np.zeros((h, stride), dtype=np.uint8)
    buf[:, :w * 4] = bgra.reshape(h, w * 4)
    data = bytearray(buf.tobytes())
    # pycairo 가 버퍼 참조를 유지하므로 data 수명은 서피스와 같다
    surf = cairo.ImageSurface.create_for_data(data, cairo.FORMAT_ARGB32, w, h, stride)
    return surf


def text_surface(text, size, font="jua", fill="#111111", stroke=0,
                 stroke_fill="#111111", spacing=10, align="center"):
    key = (text, size, font, fill, stroke, stroke_fill, spacing, align)
    if key in _text_cache:
        return _text_cache[key]
    if _missing(text, font):
        lines = [_line_image(ln, size, font, fill, stroke, stroke_fill) for ln in text.split("\n")]
        w = max(im.width for im in lines)
        h = sum(im.height for im in lines) + spacing * (len(lines) - 1)
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        y = 0
        for im in lines:
            x = (w - im.width) // 2 if align == "center" else 0
            img.alpha_composite(im, (x, y))
            y += im.height + spacing
        surf = pil_to_surface(img)
        _text_cache[key] = (surf, w, h)
        return _text_cache[key]
    f = _font(font, size)
    tmp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    bbox = tmp.multiline_textbbox((0, 0), text, font=f, stroke_width=stroke,
                                  spacing=spacing, align=align)
    bbox = [math.floor(bbox[0]), math.floor(bbox[1]), math.ceil(bbox[2]), math.ceil(bbox[3])]
    pad = 4
    w, h = bbox[2] - bbox[0] + pad * 2, bbox[3] - bbox[1] + pad * 2
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(img).multiline_text(
        (pad - bbox[0], pad - bbox[1]), text, font=f, fill=fill,
        stroke_width=stroke, stroke_fill=stroke_fill, spacing=spacing, align=align)
    surf = pil_to_surface(img)
    _text_cache[key] = (surf, w, h)
    return _text_cache[key]


def draw_text(ctx, text, x, y, size, font="jua", fill="#111111", stroke=0,
              stroke_fill="#111111", scale=1.0, rot=0.0, alpha=1.0,
              anchor=(0.5, 0.5), spacing=10, align="center"):
    if alpha <= 0.003 or scale < 0.01 or not text:
        return 0, 0
    surf, w, h = text_surface(text, size, font, fill, stroke, stroke_fill, spacing, align)
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(scale, scale)
    ctx.set_source_surface(surf, -w * anchor[0], -h * anchor[1])
    ctx.paint_with_alpha(clamp(alpha))
    ctx.restore()
    return w * scale, h * scale


def text_size(text, size, font="jua", stroke=0, spacing=10):
    _, w, h = text_surface(text, size, font, "#000000", stroke, "#000000", spacing)
    return w, h


# ---------------------------------------------------------------- shapes
def set_rgb(ctx, c, alpha=1.0):
    if isinstance(c, str):
        c = hexc(c)
    if len(c) == 4:
        ctx.set_source_rgba(*c)
    else:
        ctx.set_source_rgba(c[0], c[1], c[2], alpha)


def fill_stroke(ctx, fill, lw=6, stroke=INK, alpha=1.0):
    if fill is not None:
        set_rgb(ctx, fill, alpha)
        if lw > 0:
            ctx.fill_preserve()
        else:
            ctx.fill()
    if lw > 0:
        set_rgb(ctx, stroke, alpha)
        ctx.set_line_width(lw)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()


def rrect(ctx, x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    ctx.close_path()


def ellipse(ctx, cx, cy, rx, ry):
    ctx.save()
    ctx.translate(cx, cy)
    ctx.scale(max(rx, 0.01), max(ry, 0.01))
    ctx.new_sub_path()
    ctx.arc(0, 0, 1, 0, 2 * math.pi)
    ctx.restore()


def thick_line(ctx, pts, width, color, outline=6, alpha=1.0):
    """외곽선 있는 굵은 선 (팔, 밧줄 등)."""
    for lw, col in ((width + outline * 2, INK), (width, color)):
        ctx.new_path()
        ctx.move_to(*pts[0])
        for p in pts[1:]:
            ctx.line_to(*p)
        set_rgb(ctx, col, alpha)
        ctx.set_line_width(lw)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.stroke()


def star_burst(ctx, cx, cy, r_out, r_in, n=12, rot=0.0, seed=0):
    rnd = random.Random(seed)
    ctx.new_path()
    for i in range(n * 2):
        a = rot + i * math.pi / n
        r = r_out * (0.85 + 0.3 * rnd.random()) if i % 2 == 0 else r_in
        x, y = cx + math.cos(a) * r, cy + math.sin(a) * r
        (ctx.move_to if i == 0 else ctx.line_to)(x, y)
    ctx.close_path()


def speech_bubble(ctx, cx, cy, w, h, tail_to, fill="#FFFFFF", lw=7, spiky=False, seed=1):
    """말풍선. spiky=True 이면 외침 풍선."""
    if spiky:
        rnd = random.Random(seed)
        n = 22
        ctx.new_path()
        for i in range(n * 2):
            a = i * math.pi / n
            k = 1.0 if i % 2 == 0 else 0.78
            k *= 0.95 + 0.1 * rnd.random()
            x, y = cx + math.cos(a) * w / 2 * k, cy + math.sin(a) * h / 2 * k
            (ctx.move_to if i == 0 else ctx.line_to)(x, y)
        ctx.close_path()
        fill_stroke(ctx, fill, lw)
        return
    # 꼬리
    tx, ty = tail_to
    ang = math.atan2(ty - cy, tx - cx)
    bw = min(w, h) * 0.18
    ctx.new_path()
    ctx.move_to(cx + math.cos(ang + 1.57) * bw, cy + math.sin(ang + 1.57) * bw)
    ctx.line_to(tx, ty)
    ctx.line_to(cx + math.cos(ang - 1.57) * bw, cy + math.sin(ang - 1.57) * bw)
    ctx.close_path()
    fill_stroke(ctx, fill, lw)
    ellipse(ctx, cx, cy, w / 2, h / 2)
    fill_stroke(ctx, fill, lw)
    # 꼬리 이음새 가리기
    ellipse(ctx, cx, cy, w / 2 - lw * 0.6, h / 2 - lw * 0.6)
    set_rgb(ctx, fill)
    ctx.fill()


def speed_lines(ctx, cx, cy, r0, r1, n, t, color=INK, alpha=0.35, seed=3):
    rnd = random.Random(seed + int(t * 12))
    set_rgb(ctx, color, alpha)
    for i in range(n):
        a = i / n * 2 * math.pi + rnd.uniform(-0.04, 0.04)
        rr = r0 + rnd.uniform(0, 80)
        da = rnd.uniform(0.006, 0.018)
        ctx.new_path()
        ctx.move_to(cx + math.cos(a - da) * r1, cy + math.sin(a - da) * r1)
        ctx.line_to(cx + math.cos(a) * rr, cy + math.sin(a) * rr)
        ctx.line_to(cx + math.cos(a + da) * r1, cy + math.sin(a + da) * r1)
        ctx.close_path()
        ctx.fill()


def halftone(w, h, color, step=26, rmax=6.5, angle=0.4):
    """망점 패턴 서피스 (만화 질감)."""
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    c = cairo.Context(surf)
    set_rgb(c, color)
    ca, sa = math.cos(angle), math.sin(angle)
    span = int(max(w, h) * 1.5 / step)
    for i in range(-span, span):
        for j in range(-span, span):
            x = (i * ca - j * sa) * step + w / 2
            y = (i * sa + j * ca) * step + h / 2
            if -10 < x < w + 10 and -10 < y < h + 10:
                r = rmax * (0.35 + 0.65 * (y / h))
                c.new_sub_path()
                c.arc(x, y, r, 0, 2 * math.pi)
    c.fill()
    return surf


def paper_texture(w, h, base="#F6EEDC", seed=7):
    rng = np.random.default_rng(seed)
    b = np.array(hexc(base)) * 255
    noise = rng.normal(0, 5, (h // 4, w // 4, 1))
    img = np.clip(b[None, None, :] + noise, 0, 255).astype(np.uint8)
    pil = Image.fromarray(img, "RGB").resize((w, h), Image.BILINEAR)
    return pil_to_surface(pil)


# ---------------------------------------------------------------- frame io
def new_frame():
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    return surf, cairo.Context(surf)


def surface_bytes(surf):
    surf.flush()
    stride = surf.get_stride()
    buf = np.frombuffer(surf.get_data(), dtype=np.uint8).reshape(H, stride)
    return buf[:, :W * 4].tobytes()
