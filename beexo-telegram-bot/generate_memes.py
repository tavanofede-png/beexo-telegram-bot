"""
Generador de memes con ilustraciones temáticas para Beexo Wallet Bot.
Cada meme tiene una escena visual que representa su contenido:
- Personas en diferentes poses (preocupadas, celebrando, corriendo)
- Objetos cripto (monitores con gráficos, teléfonos, billeteras, candados)
- Escenas completas (trading desk, familia en mesa, persona en cama)
La escena se elige automáticamente analizando el texto del meme.
Ejecutar: python generate_memes.py
"""

import os
import math
import random
import textwrap
from PIL import Image, ImageDraw, ImageFont

from memes_data import MEMES_DATA

MEMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "memes")
os.makedirs(MEMES_DIR, exist_ok=True)

W, H = 800, 600

# =============================================================
# UTILIDADES
# =============================================================

def get_font(size, bold=True):
    candidates = (
        ["C:/Windows/Fonts/impact.ttf", "C:/Windows/Fonts/arialbd.ttf"]
        if bold
        else ["C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/segoeui.ttf"]
    )
    for fp in candidates:
        if os.path.exists(fp):
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()


def h2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def dim(c, f=0.5):
    r, g, b = h2rgb(c) if isinstance(c, str) else c
    return (int(r * f), int(g * f), int(b * f))


def brt(c, f=1.3):
    r, g, b = h2rgb(c) if isinstance(c, str) else c
    return (min(255, int(r * f)), min(255, int(g * f)), min(255, int(b * f)))


def gradient(draw, w, h, c1, c2):
    r1, g1, b1 = h2rgb(c1) if isinstance(c1, str) else c1
    r2, g2, b2 = h2rgb(c2) if isinstance(c2, str) else c2
    for y in range(h):
        t = y / h
        draw.line([(0, y), (w, y)], fill=(
            int(r1 + (r2 - r1) * t),
            int(g1 + (g2 - g1) * t),
            int(b1 + (b2 - b1) * t),
        ))


def draw_text_block(draw, text, font, y_start, w, fill="white",
                    stroke_w=5, stroke_fill="black", max_chars=26):
    lines = textwrap.wrap(text, width=max_chars)
    y = y_start
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        x = (w - tw) // 2
        draw.text((x, y), line, font=font, fill=fill,
                  stroke_width=stroke_w, stroke_fill=stroke_fill)
        y += th + 8
    return y


def draw_hexagon(draw, cx, cy, size, color, width=2):
    pts = []
    for i in range(6):
        a = math.radians(60 * i - 30)
        pts.append((cx + size * math.cos(a), cy + size * math.sin(a)))
    draw.polygon(pts, outline=color, width=width)


# =============================================================
# COMPONENTES REUTILIZABLES
# =============================================================

def draw_person(d, x, y, s, c, pose="stand"):
    """Persona estilo flat design con diversas poses."""
    hr = int(s * 0.16)
    d.ellipse([(x - hr, y - hr), (x + hr, y + hr)], outline=c, width=3)
    be = y + int(s * 0.45)
    d.line([(x, y + hr), (x, be)], fill=c, width=3)
    if pose == "stand":
        d.line([(x, y + int(s * 0.18)), (x - int(s * 0.22), y + int(s * 0.32))], fill=c, width=2)
        d.line([(x, y + int(s * 0.18)), (x + int(s * 0.22), y + int(s * 0.32))], fill=c, width=2)
        d.line([(x, be), (x - int(s * 0.16), be + int(s * 0.28))], fill=c, width=2)
        d.line([(x, be), (x + int(s * 0.16), be + int(s * 0.28))], fill=c, width=2)
    elif pose == "worried":
        d.line([(x, y + int(s * 0.18)), (x - int(s * 0.15), y - int(s * 0.02))], fill=c, width=2)
        d.line([(x, y + int(s * 0.18)), (x + int(s * 0.15), y - int(s * 0.02))], fill=c, width=2)
        d.line([(x, be), (x - int(s * 0.14), be + int(s * 0.28))], fill=c, width=2)
        d.line([(x, be), (x + int(s * 0.14), be + int(s * 0.28))], fill=c, width=2)
    elif pose == "celebrate":
        d.line([(x, y + int(s * 0.18)), (x - int(s * 0.28), y - int(s * 0.12))], fill=c, width=2)
        d.line([(x, y + int(s * 0.18)), (x + int(s * 0.28), y - int(s * 0.12))], fill=c, width=2)
        d.line([(x, be), (x - int(s * 0.18), be + int(s * 0.25))], fill=c, width=2)
        d.line([(x, be), (x + int(s * 0.18), be + int(s * 0.25))], fill=c, width=2)
    elif pose == "sitting":
        d.line([(x, y + int(s * 0.18)), (x + int(s * 0.25), y + int(s * 0.18))], fill=c, width=2)
        d.line([(x, y + int(s * 0.18)), (x + int(s * 0.2), y + int(s * 0.25))], fill=c, width=2)
        d.line([(x, be), (x + int(s * 0.18), be)], fill=c, width=2)
        d.line([(x + int(s * 0.18), be), (x + int(s * 0.18), be + int(s * 0.25))], fill=c, width=2)
        d.line([(x, be), (x - int(s * 0.08), be)], fill=c, width=2)
        d.line([(x - int(s * 0.08), be), (x - int(s * 0.08), be + int(s * 0.25))], fill=c, width=2)
    elif pose == "run":
        d.line([(x, y + int(s * 0.18)), (x - int(s * 0.28), y + int(s * 0.08))], fill=c, width=2)
        d.line([(x, y + int(s * 0.18)), (x + int(s * 0.22), y + int(s * 0.28))], fill=c, width=2)
        d.line([(x, be), (x - int(s * 0.22), be + int(s * 0.18))], fill=c, width=2)
        d.line([(x, be), (x + int(s * 0.18), be + int(s * 0.22))], fill=c, width=2)


def draw_phone(d, x, y, pw, ph, c):
    """Smartphone con pantalla."""
    d.rounded_rectangle([(x, y), (x + pw, y + ph)], radius=12, outline=c, width=3)
    sx, sy = x + 5, y + int(ph * 0.08)
    sw, sh = pw - 10, int(ph * 0.82)
    d.rectangle([(sx, sy), (sx + sw, sy + sh)], fill=dim(c, 0.12))
    d.rounded_rectangle([(x + pw // 2 - 8, y + ph - 10), (x + pw // 2 + 8, y + ph - 3)], radius=3, fill=c)
    return sx, sy, sw, sh


def draw_monitor(d, x, y, mw, mh, c):
    """Monitor de PC con soporte."""
    d.rectangle([(x, y), (x + mw, y + mh)], outline=c, width=3)
    d.rectangle([(x + 5, y + 5), (x + mw - 5, y + mh - 5)], fill=(12, 15, 25))
    cx = x + mw // 2
    d.rectangle([(cx - 12, y + mh), (cx + 12, y + mh + 22)], fill=c)
    d.rectangle([(cx - 28, y + mh + 22), (cx + 28, y + mh + 30)], fill=c)
    return x + 8, y + 8, mw - 16, mh - 16


def draw_candles(d, sx, sy, sw, sh, n=8, trend="down"):
    """Velas japonesas dentro de un área delimitada."""
    green = dim("#22cc66", 0.8)
    red = dim("#ee3344", 0.8)
    cw = max(sw // (n + 1), 6)
    gap = max((sw - cw * n) // (n + 1), 3)
    for i in range(n):
        cx = sx + gap + i * (cw + gap) + cw // 2
        if trend == "down":
            by = sy + int(sh * 0.1) + int(i * sh * 0.08)
        elif trend == "up":
            by = sy + int(sh * 0.85) - int(i * sh * 0.08)
        else:
            by = sy + sh // 2 + int(15 * math.sin(i * 0.9))
        is_up = random.random() > (0.7 if trend == "down" else 0.3)
        cc = green if is_up else red
        ch = random.randint(int(sh * 0.06), int(sh * 0.2))
        d.line([(cx, by - 8), (cx, by + ch + 8)], fill=cc, width=1)
        d.rectangle([(cx - cw // 2, by), (cx + cw // 2, by + ch)], fill=cc)


def draw_coin(d, x, y, r, c, sym="B"):
    """Moneda cripto con símbolo."""
    d.ellipse([(x - r, y - r), (x + r, y + r)], outline=c, width=2)
    d.ellipse([(x - r + 3, y - r + 3), (x + r - 3, y + r - 3)], outline=c, width=1)
    f = get_font(int(r * 1.1))
    bb = d.textbbox((0, 0), sym, font=f)
    d.text((x - (bb[2] - bb[0]) // 2, y - (bb[3] - bb[1]) // 2 - 2), sym, font=f, fill=c)


# =============================================================
# 20 ESCENAS ILUSTRATIVAS
# =============================================================

def scene_chart_falling(d, W, H, ac):
    """Monitor con gráfico rojo cayendo + persona preocupada."""
    c = dim(ac, 0.75)
    mx, my = W // 2 - 130, 160
    sx, sy, sw, sh = draw_monitor(d, mx, my, 260, 185, c)
    draw_candles(d, sx, sy, sw, sh, n=9, trend="down")
    d.line([(sx, sy + 15), (sx + sw, sy + sh - 10)], fill=dim("#ff4444", 0.6), width=2)
    ax = mx + 290
    ay = my + 30
    d.line([(ax, ay), (ax, ay + 110)], fill=dim("#ff4444", 0.7), width=5)
    d.polygon([(ax - 18, ay + 95), (ax + 18, ay + 95), (ax, ay + 125)], fill=dim("#ff4444", 0.7))
    draw_person(d, mx - 70, my + 75, 120, c, "worried")
    f = get_font(28)
    d.text((ax - 30, ay - 30), "-42%", font=f, fill=dim("#ff4444", 0.65),
           stroke_width=2, stroke_fill="black")


def scene_chart_pump(d, W, H, ac):
    """Gráfico verde subiendo con persona celebrando."""
    c = dim(ac, 0.75)
    gc = dim("#22cc66", 0.7)
    mx, my = W // 2 - 130, 165
    sx, sy, sw, sh = draw_monitor(d, mx, my, 260, 180, c)
    draw_candles(d, sx, sy, sw, sh, n=9, trend="up")
    ax = mx + 285
    d.line([(ax, my + 150), (ax, my + 30)], fill=gc, width=5)
    d.polygon([(ax - 18, my + 45), (ax + 18, my + 45), (ax, my + 18)], fill=gc)
    draw_person(d, mx - 65, my + 70, 120, c, "celebrate")
    f = get_font(28)
    d.text((ax - 30, my), "+87%", font=f, fill=gc, stroke_width=2, stroke_fill="black")
    for _ in range(5):
        sx2 = random.randint(mx, mx + 260)
        sy2 = random.randint(my, my + 180)
        ss = random.randint(4, 10)
        d.line([(sx2 - ss, sy2), (sx2 + ss, sy2)], fill=gc, width=1)
        d.line([(sx2, sy2 - ss), (sx2, sy2 + ss)], fill=gc, width=1)


def scene_phone_obsession(d, W, H, ac):
    """Teléfono grande con gráfico + persona mirando obsesivamente."""
    c = dim(ac, 0.75)
    px, py, pw, ph = W // 2 - 55, 140, 110, 200
    sx, sy, sw, sh = draw_phone(d, px, py, pw, ph, c)
    draw_candles(d, sx + 3, sy + 10, sw - 6, sh - 20, n=5, trend="mixed")
    pts = []
    for i in range(6):
        x = sx + 5 + i * (sw - 10) // 5
        y2 = sy + 15 + random.randint(10, sh - 40)
        pts.append((x, y2))
    for i in range(len(pts) - 1):
        d.line([pts[i], pts[i + 1]], fill=brt(c), width=2)
    for ox, oy in [(px - 55, py + 70), (px + pw + 25, py + 100)]:
        r2 = 18
        d.arc([(ox - r2, oy - r2), (ox + r2, oy + r2)], start=20, end=290, fill=c, width=2)
        d.polygon([(ox + r2 - 5, oy - 6), (ox + r2 + 5, oy - 6), (ox + r2, oy + 5)], fill=c)
    d.ellipse([(px + pw - 8, py + 5), (px + pw + 8, py + 21)], fill=dim("#ff4444", 0.7))
    nf = get_font(12)
    d.text((px + pw - 4, py + 6), "99", font=nf, fill="white")
    draw_person(d, px - 80, py + 45, 105, c, "stand")


def scene_no_money(d, W, H, ac):
    """Billetera vacía con telarañas + persona triste."""
    c = dim(ac, 0.7)
    wx, wy = W // 2 - 70, 195
    ww, wh = 140, 100
    d.rounded_rectangle([(wx, wy), (wx + ww, wy + wh)], radius=12, outline=c, width=3)
    d.line([(wx, wy + wh // 2), (wx + ww, wy + wh // 2)], fill=c, width=2)
    d.line([(wx + 15, wy + 10), (wx + ww - 15, wy + wh // 2 - 5)], fill=dim(c, 0.3), width=1)
    d.line([(wx + ww - 15, wy + 10), (wx + 15, wy + wh // 2 - 5)], fill=dim(c, 0.3), width=1)
    d.line([(wx + ww // 2, wy + 5), (wx + ww // 2, wy + wh // 2 - 5)], fill=dim(c, 0.3), width=1)
    mx2, my2 = wx + ww // 2 + 30, wy - 15
    d.ellipse([(mx2 - 3, my2 - 3), (mx2 + 3, my2 + 3)], fill=c)
    d.polygon([(mx2 - 2, my2), (mx2 - 10, my2 - 10), (mx2 - 5, my2)], outline=c, width=1)
    d.polygon([(mx2 + 2, my2), (mx2 + 10, my2 - 10), (mx2 + 5, my2)], outline=c, width=1)
    f = get_font(32)
    d.text((wx + ww // 2 - 40, wy + wh + 10), "$0.00", font=f, fill=dim(c, 0.8),
           stroke_width=2, stroke_fill="black")
    draw_person(d, wx - 70, wy + 20, 110, c, "worried")
    for i in range(3):
        cx2 = wx + ww + 30 + i * 35
        cy2 = wy + 30 + i * 25
        draw_coin(d, cx2, cy2, 14, dim(c, 0.4), "$")
        d.line([(cx2 - 8, cy2 - 8), (cx2 + 8, cy2 + 8)], fill=dim("#ff4444", 0.5), width=2)
        d.line([(cx2 + 8, cy2 - 8), (cx2 - 8, cy2 + 8)], fill=dim("#ff4444", 0.5), width=2)


def scene_vault_lock(d, W, H, ac):
    """Candado grande sobre escudo + cadenas de seguridad."""
    c = dim(ac, 0.75)
    sx, sy, ss = W // 2, 200, 100
    pts = [
        (sx, sy - int(ss * 0.1)),
        (sx + ss, sy + int(ss * 0.25)),
        (sx + int(ss * 0.85), sy + int(ss * 0.75)),
        (sx, sy + ss + 20),
        (sx - int(ss * 0.85), sy + int(ss * 0.75)),
        (sx - ss, sy + int(ss * 0.25)),
    ]
    d.polygon(pts, fill=dim(c, 0.15), outline=c, width=3)
    lx, ly = sx, sy + int(ss * 0.35)
    ls = 45
    d.rounded_rectangle([(lx - ls // 2, ly), (lx + ls // 2, ly + int(ls * 0.7))],
                        radius=6, outline=brt(c), width=3)
    d.arc([(lx - int(ls * 0.3), ly - int(ls * 0.45)), (lx + int(ls * 0.3), ly + int(ls * 0.12))],
          start=180, end=0, fill=brt(c), width=3)
    d.ellipse([(lx - 5, ly + int(ls * 0.22)), (lx + 5, ly + int(ls * 0.32))], fill=brt(c))
    d.polygon([(lx - 3, ly + int(ls * 0.32)), (lx + 3, ly + int(ls * 0.32)),
               (lx, ly + int(ls * 0.5))], fill=brt(c))
    for side in [-1, 1]:
        for i in range(4):
            cx2 = sx + side * (ss + 35)
            cy2 = sy + 10 + i * 30
            d.rounded_rectangle([(cx2 - 8, cy2), (cx2 + 8, cy2 + 18)], radius=4, outline=c, width=2)
    d.line([(sx - 12, sy - 20), (sx - 3, sy - 10)], fill=dim("#22cc66", 0.7), width=3)
    d.line([(sx - 3, sy - 10), (sx + 15, sy - 32)], fill=dim("#22cc66", 0.7), width=3)
    for _ in range(4):
        sx2 = random.randint(80, W - 80)
        sy2 = random.randint(140, H - 140)
        ss2 = random.randint(4, 8)
        d.line([(sx2 - ss2, sy2), (sx2 + ss2, sy2)], fill=dim(c, 0.3), width=1)
        d.line([(sx2, sy2 - ss2), (sx2, sy2 + ss2)], fill=dim(c, 0.3), width=1)


def scene_hacker_attack(d, W, H, ac):
    """Figura encapuchada en laptop + calavera + código verde."""
    c = dim(ac, 0.7)
    rc = dim("#ff4444", 0.6)
    lx, ly = W // 2 - 80, 240
    lw, lh = 160, 100
    d.rectangle([(lx, ly), (lx + lw, ly + lh)], outline=c, width=3)
    d.rectangle([(lx + 4, ly + 4), (lx + lw - 4, ly + lh - 4)], fill=(8, 12, 20))
    d.rounded_rectangle([(lx - 20, ly + lh), (lx + lw + 20, ly + lh + 15)], radius=3, outline=c, width=2)
    code_font = get_font(11, bold=False)
    for i, txt in enumerate(["0x4F...steal()", ">> crack_pwd", "$ ssh root@...", "rm -rf /*", "GET /seed..."]):
        d.text((lx + 10, ly + 10 + i * 16), txt, font=code_font, fill=dim("#00ff00", 0.5))
    hx, hy = W // 2, ly - 55
    d.arc([(hx - 30, hy - 35), (hx + 30, hy + 25)], start=180, end=0, fill=c, width=3)
    d.line([(hx - 30, hy - 5), (hx - 30, hy + 30)], fill=c, width=3)
    d.line([(hx + 30, hy - 5), (hx + 30, hy + 30)], fill=c, width=3)
    d.ellipse([(hx - 12, hy), (hx - 4, hy + 6)], fill=rc)
    d.ellipse([(hx + 4, hy), (hx + 12, hy + 6)], fill=rc)
    skx, sky = W // 2 + 160, 210
    d.ellipse([(skx - 18, sky - 20), (skx + 18, sky + 10)], outline=rc, width=2)
    d.ellipse([(skx - 8, sky - 10), (skx - 3, sky - 3)], fill=rc)
    d.ellipse([(skx + 3, sky - 10), (skx + 8, sky - 3)], fill=rc)
    d.polygon([(W // 2 - 170, 220), (W // 2 - 150, 185), (W // 2 - 130, 220)], outline=rc, width=2)
    d.line([(W // 2 - 150, 195), (W // 2 - 150, 210)], fill=rc, width=2)


def scene_diamond_hodl(d, W, H, ac):
    """Diamante grande con manos sosteniéndolo + destellos."""
    c = dim(ac, 0.8)
    dx, dy = W // 2, 240
    s = 65
    d.polygon([(dx - s, dy), (dx - s // 2, dy - s), (dx + s // 2, dy - s), (dx + s, dy)],
              fill=dim(c, 0.2), outline=c, width=3)
    d.polygon([(dx - s, dy), (dx + s, dy), (dx, dy + int(s * 1.4))],
              fill=dim(c, 0.15), outline=c, width=3)
    d.line([(dx - s // 2, dy - s), (dx - s // 4, dy)], fill=c, width=1)
    d.line([(dx + s // 2, dy - s), (dx + s // 4, dy)], fill=c, width=1)
    d.line([(dx - s, dy), (dx, dy + s // 2)], fill=c, width=1)
    d.line([(dx + s, dy), (dx, dy + s // 2)], fill=c, width=1)
    d.line([(dx - s // 4, dy), (dx, dy + int(s * 1.4))], fill=c, width=1)
    d.line([(dx + s // 4, dy), (dx, dy + int(s * 1.4))], fill=c, width=1)
    for side in [-1, 1]:
        hx = dx + side * 40
        hy = dy + int(s * 1.4) + 10
        d.rounded_rectangle([(hx - 15, hy), (hx + 15, hy + 25)], radius=5, outline=c, width=2)
        for fi in range(-2, 3):
            fx = hx + fi * 6
            d.line([(fx, hy), (fx, hy - 12)], fill=c, width=2)
    sparkles = [(dx - 90, dy - 40), (dx + 95, dy - 30), (dx - 80, dy + 50),
                (dx + 85, dy + 60), (dx, dy - s - 25), (dx - 110, dy + 90), (dx + 110, dy + 90)]
    for sx2, sy2 in sparkles:
        ss = random.randint(6, 14)
        d.line([(sx2 - ss, sy2), (sx2 + ss, sy2)], fill=c, width=1)
        d.line([(sx2, sy2 - ss), (sx2, sy2 + ss)], fill=c, width=1)
    for side in [-1, 1]:
        ax = dx + side * 130
        d.line([(ax, 170), (ax, 260)], fill=dim("#ff4444", 0.4), width=2)
        d.polygon([(ax - 8, 248), (ax + 8, 248), (ax, 268)], fill=dim("#ff4444", 0.4))
        d.line([(ax, 270), (ax + side * 20, 290)], fill=dim("#ff4444", 0.3), width=1)


def scene_to_the_moon(d, W, H, ac):
    """Cohete volando hacia la luna, estrellas y monedas."""
    c = dim(ac, 0.75)
    mx2, my2, mr = W - 130, 190, 55
    d.ellipse([(mx2 - mr, my2 - mr), (mx2 + mr, my2 + mr)], fill=dim(c, 0.2), outline=c, width=2)
    d.ellipse([(mx2 - 20, my2 - 15), (mx2 - 8, my2 - 5)], outline=dim(c, 0.4), width=1)
    d.ellipse([(mx2 + 10, my2 + 5), (mx2 + 22, my2 + 18)], outline=dim(c, 0.4), width=1)
    d.ellipse([(mx2 - 5, my2 + 15), (mx2 + 5, my2 + 25)], outline=dim(c, 0.4), width=1)
    rx, ry = 250, 340
    s = 110
    d.rounded_rectangle([(rx - 18, ry - int(s * 0.45)), (rx + 18, ry + int(s * 0.3))],
                        radius=18, outline=c, width=3)
    d.polygon([(rx, ry - int(s * 0.7)), (rx - 18, ry - int(s * 0.4)), (rx + 18, ry - int(s * 0.4))],
              fill=dim(c, 0.3), outline=c, width=2)
    d.polygon([(rx - 18, ry + int(s * 0.15)), (rx - 35, ry + int(s * 0.35)),
               (rx - 18, ry + int(s * 0.3))], fill=c)
    d.polygon([(rx + 18, ry + int(s * 0.15)), (rx + 35, ry + int(s * 0.35)),
               (rx + 18, ry + int(s * 0.3))], fill=c)
    d.ellipse([(rx - 8, ry - int(s * 0.2)), (rx + 8, ry - int(s * 0.05))], outline=c, width=2)
    d.polygon([(rx - 10, ry + int(s * 0.3)), (rx + 10, ry + int(s * 0.3)),
               (rx, ry + int(s * 0.55))], fill=brt(c))
    d.polygon([(rx - 5, ry + int(s * 0.3)), (rx + 5, ry + int(s * 0.3)),
               (rx, ry + int(s * 0.45))], fill=dim("#ffff00", 0.6))
    for i in range(5):
        ty = ry + int(s * 0.55) + i * 20
        tw = 12 - i * 2
        if tw > 0:
            d.ellipse([(rx - tw, ty), (rx + tw, ty + 8)], outline=dim(c, 0.3 - i * 0.04), width=1)
    for _ in range(12):
        sx2 = random.randint(50, W - 50)
        sy2 = random.randint(140, H - 140)
        ss = random.randint(2, 6)
        d.line([(sx2 - ss, sy2), (sx2 + ss, sy2)], fill=dim(c, 0.5), width=1)
        d.line([(sx2, sy2 - ss), (sx2, sy2 + ss)], fill=dim(c, 0.5), width=1)
    for cx2, cy2 in [(180, 200), (350, 190), (480, 250)]:
        draw_coin(d, cx2, cy2, 14, dim(c, 0.5), "B")


def scene_fees_burning(d, W, H, ac):
    """Billetes en llamas + medidor de gas + persona sorprendida."""
    c = dim(ac, 0.75)
    bx, by = W // 2 - 50, 230
    for i in range(3):
        ox, oy = i * 8, i * 5
        d.rounded_rectangle([(bx + ox, by + oy), (bx + 100 + ox, by + 50 + oy)],
                            radius=4, outline=c, width=2)
        f = get_font(22)
        d.text((bx + 30 + ox, by + 12 + oy), "$", font=f, fill=c)
    for i in range(5):
        fx = bx + 10 + i * 22
        fy = by - 10
        fs = random.randint(22, 40)
        flame = [
            (fx, fy), (fx + int(fs * 0.3), fy - int(fs * 0.5)),
            (fx + int(fs * 0.15), fy - int(fs * 0.3)),
            (fx, fy - fs), (fx - int(fs * 0.15), fy - int(fs * 0.3)),
            (fx - int(fs * 0.3), fy - int(fs * 0.5)),
        ]
        d.polygon(flame, fill=dim("#ff6600", 0.3), outline=dim("#ff6600", 0.6), width=2)
    gx, gy = W // 2 + 130, 200
    d.rounded_rectangle([(gx, gy), (gx + 50, gy + 80)], radius=6, outline=c, width=2)
    d.rectangle([(gx + 5, gy + 5), (gx + 45, gy + 35)], outline=c, width=1)
    d.arc([(gx + 40, gy), (gx + 70, gy + 30)], start=270, end=90, fill=c, width=2)
    d.line([(gx + 55, gy + 15), (gx + 55, gy + 40)], fill=c, width=2)
    gf = get_font(14)
    d.text((gx + 10, gy + 42), "GAS", font=gf, fill=c)
    d.text((gx + 5, gy + 58), "$999", font=get_font(18), fill=dim("#ff4444", 0.7))
    draw_person(d, W // 2 - 130, by - 20, 110, c, "worried")


def scene_scam_alert(d, W, H, ac):
    """Triángulo de advertencia + teléfono con DMs falsos."""
    c = dim(ac, 0.75)
    rc = dim("#ff4444", 0.7)
    tx, ty = W // 2, 185
    ts = 75
    d.polygon([(tx, ty), (tx + ts, ty + int(ts * 1.5)), (tx - ts, ty + int(ts * 1.5))],
              fill=dim(rc, 0.15), outline=rc, width=4)
    d.line([(tx, ty + int(ts * 0.45)), (tx, ty + int(ts * 0.95))], fill=rc, width=5)
    d.ellipse([(tx - 4, ty + int(ts * 1.05)), (tx + 4, ty + int(ts * 1.15))], fill=rc)
    px, py, pw, ph = W // 2 + 115, 200, 80, 150
    sx, sy, sw, sh = draw_phone(d, px, py, pw, ph, c)
    for i, txt in enumerate(["Hola!", "Soy soporte", "Envia seed", "..."]):
        my2 = sy + 8 + i * 28
        d.rounded_rectangle([(sx + 3, my2), (sx + sw - 3, my2 + 22)], radius=5,
                            outline=dim(c, 0.4), width=1)
        cf = get_font(10, bold=False)
        d.text((sx + 8, my2 + 4), txt, font=cf, fill=dim(c, 0.6))
    for _ in range(4):
        xx = random.randint(W // 2 - 170, W // 2 - 100)
        xy = random.randint(200, 380)
        xs = random.randint(10, 16)
        d.line([(xx - xs, xy - xs), (xx + xs, xy + xs)], fill=rc, width=2)
        d.line([(xx + xs, xy - xs), (xx - xs, xy + xs)], fill=rc, width=2)
    skx, sky = W // 2 - 140, 270
    d.ellipse([(skx - 14, sky - 14), (skx + 14, sky + 6)], outline=rc, width=2)
    d.ellipse([(skx - 6, sky - 6), (skx - 2, sky)], fill=rc)
    d.ellipse([(skx + 2, sky - 6), (skx + 6, sky)], fill=rc)


def scene_night_check(d, W, H, ac):
    """Persona en cama mirando teléfono brillando en la oscuridad."""
    c = dim(ac, 0.65)
    bed_x, bed_y = 150, 310
    bed_w = 300
    d.rounded_rectangle([(bed_x, bed_y), (bed_x + bed_w, bed_y + 55)], radius=8, outline=c, width=2)
    d.rounded_rectangle([(bed_x + 5, bed_y - 20), (bed_x + 80, bed_y + 10)], radius=10, outline=c, width=2)
    d.ellipse([(bed_x + 30, bed_y - 35), (bed_x + 60, bed_y - 5)], outline=c, width=2)
    d.line([(bed_x + 65, bed_y + 5), (bed_x + bed_w - 10, bed_y + 5)], fill=c, width=2)
    px, py = bed_x + 180, bed_y - 60
    pw, ph = 50, 80
    sx, sy, sw, sh = draw_phone(d, px, py, pw, ph, brt(c))
    for i in range(3):
        g = 5 + i * 6
        d.rounded_rectangle([(px - g, py - g), (px + pw + g, py + ph + g)],
                            radius=14 + g, outline=dim(c, 0.15 - i * 0.04), width=1)
    for i in range(4):
        cx2 = sx + 5 + i * 10
        cy2 = sy + 10 + random.randint(5, sh - 25)
        ch = random.randint(8, 20)
        cc = dim("#ff4444", 0.6) if random.random() > 0.3 else dim("#22cc66", 0.5)
        d.rectangle([(cx2, cy2), (cx2 + 6, cy2 + ch)], fill=cc)
    wndx, wndy = W - 180, 175
    d.rectangle([(wndx, wndy), (wndx + 100, wndy + 80)], outline=c, width=2)
    d.line([(wndx + 50, wndy), (wndx + 50, wndy + 80)], fill=c, width=1)
    d.line([(wndx, wndy + 40), (wndx + 100, wndy + 40)], fill=c, width=1)
    d.ellipse([(wndx + 65, wndy + 8), (wndx + 90, wndy + 33)], fill=dim(c, 0.3), outline=c, width=1)
    for _ in range(4):
        sx2 = wndx + random.randint(5, 55)
        sy2 = wndy + random.randint(5, 35)
        d.ellipse([(sx2, sy2), (sx2 + 3, sy2 + 3)], fill=c)
    zf = get_font(20)
    d.text((bed_x + 100, bed_y - 50), "Z", font=zf, fill=dim(c, 0.3))
    d.text((bed_x + 120, bed_y - 65), "Z", font=get_font(16), fill=dim(c, 0.25))
    d.text((bed_x + 135, bed_y - 75), "z", font=get_font(12), fill=dim(c, 0.2))


def scene_family_talk(d, W, H, ac):
    """Mesa con familia conversando, uno habla de cripto, otros confundidos."""
    c = dim(ac, 0.7)
    mx2, my2 = W // 2, 340
    mw = 260
    d.rounded_rectangle([(mx2 - mw // 2, my2), (mx2 + mw // 2, my2 + 20)],
                        radius=5, fill=dim(c, 0.2), outline=c, width=2)
    d.line([(mx2 - mw // 2 + 20, my2 + 20), (mx2 - mw // 2 + 15, my2 + 65)], fill=c, width=3)
    d.line([(mx2 + mw // 2 - 20, my2 + 20), (mx2 + mw // 2 - 15, my2 + 65)], fill=c, width=3)
    draw_person(d, mx2 - 90, my2 - 75, 90, c, "celebrate")
    draw_person(d, mx2 + 90, my2 - 75, 90, c, "worried")
    draw_person(d, mx2, my2 - 80, 85, c, "stand")
    bx, by2 = mx2 - 155, 170
    d.rounded_rectangle([(bx, by2), (bx + 80, by2 + 40)], radius=10, outline=c, width=2)
    d.polygon([(bx + 50, by2 + 40), (bx + 40, by2 + 55), (bx + 60, by2 + 40)], outline=c, width=2)
    bf = get_font(18)
    d.text((bx + 10, by2 + 8), "BTC!", font=bf, fill=c)
    bx2 = mx2 + 80
    d.rounded_rectangle([(bx2, by2 + 10), (bx2 + 60, by2 + 45)], radius=10, outline=c, width=2)
    d.polygon([(bx2 + 15, by2 + 45), (bx2 + 10, by2 + 58), (bx2 + 25, by2 + 45)], outline=c, width=2)
    d.text((bx2 + 17, by2 + 16), "??", font=get_font(20), fill=c)
    for dx2 in [-60, 0, 60]:
        d.ellipse([(mx2 + dx2 - 15, my2 - 10), (mx2 + dx2 + 15, my2 + 5)], outline=dim(c, 0.3), width=1)


def scene_trading_pro(d, W, H, ac):
    """Setup de trading: dos monitores, persona sentada, café."""
    c = dim(ac, 0.7)
    dx, dy = 160, 360
    dw = 480
    d.rectangle([(dx, dy), (dx + dw, dy + 10)], fill=dim(c, 0.3), outline=c, width=2)
    d.line([(dx + 30, dy + 10), (dx + 30, dy + 50)], fill=c, width=3)
    d.line([(dx + dw - 30, dy + 10), (dx + dw - 30, dy + 50)], fill=c, width=3)
    sx, sy, sw, sh = draw_monitor(d, 200, 190, 180, 130, c)
    draw_candles(d, sx, sy, sw, sh, n=7, trend="up")
    sx2, sy2, sw2, sh2 = draw_monitor(d, 420, 195, 180, 125, c)
    draw_candles(d, sx2, sy2, sw2, sh2, n=7, trend="down")
    d.line([(sx, sy + sh - 10), (sx + sw, sy + 10)], fill=dim("#22cc66", 0.5), width=2)
    d.line([(sx2, sy2 + 10), (sx2 + sw2, sy2 + sh2 - 10)], fill=dim("#ff4444", 0.5), width=2)
    draw_person(d, 390, 290, 80, c, "sitting")
    d.rounded_rectangle([(335, 340), (355, 358)], radius=3, outline=c, width=2)
    d.arc([(355, 340), (368, 355)], start=270, end=90, fill=c, width=2)
    for i in range(3):
        d.arc([(338 + i * 5, 322 - i * 6), (348 + i * 5, 340 - i * 6)],
              start=0, end=180, fill=dim(c, 0.3), width=1)


def scene_bull(d, W, H, ac):
    """Toro embistiendo con flecha verde grande detrás."""
    c = dim(ac, 0.75)
    gc = dim("#22cc66", 0.6)
    d.polygon([(150, 400), (650, 400), (400, 150)], fill=dim("#22cc66", 0.06), outline=gc, width=2)
    bx, by = 350, 310
    d.ellipse([(bx - 85, by - 40), (bx + 85, by + 40)], fill=dim(c, 0.2), outline=c, width=3)
    hx, hy = bx + 100, by - 25
    d.ellipse([(hx - 22, hy - 18), (hx + 22, hy + 18)], fill=dim(c, 0.2), outline=c, width=3)
    d.arc([(hx + 5, hy - 50), (hx + 45, hy - 5)], start=200, end=350, fill=brt(c), width=4)
    d.arc([(hx + 5, hy + 5), (hx + 45, hy + 45)], start=10, end=160, fill=brt(c), width=4)
    d.ellipse([(hx + 5, hy - 5), (hx + 11, hy + 1)], fill=c)
    d.line([(bx + 83, by - 8), (hx - 20, hy + 3)], fill=c, width=3)
    legs = [(bx + 45, by + 40), (bx + 25, by + 40), (bx - 35, by + 40), (bx - 55, by + 40)]
    for i, (lx, ly) in enumerate(legs):
        ext = 10 if i % 2 == 0 else -8
        d.line([(lx, ly), (lx + ext, ly + 55)], fill=c, width=3)
        d.line([(lx + ext, ly + 55), (lx + ext + 8, ly + 55)], fill=c, width=2)
    d.arc([(bx - 120, by - 25), (bx - 75, by + 10)], start=190, end=350, fill=c, width=2)
    for i in range(3):
        cx2 = bx - 110 - i * 30
        cy2 = by + 60 + random.randint(-8, 8)
        cr = random.randint(8, 16)
        d.ellipse([(cx2 - cr, cy2 - cr), (cx2 + cr, cy2 + cr)], outline=dim(c, 0.3), width=1)


def scene_bear(d, W, H, ac):
    """Oso con gráfico rojo descendente detrás."""
    c = dim(ac, 0.75)
    rc = dim("#ff4444", 0.6)
    d.polygon([(150, 170), (650, 170), (400, 430)], fill=dim("#ff4444", 0.06), outline=rc, width=2)
    bx, by = W // 2, 270
    d.ellipse([(bx - 65, by - 30), (bx + 65, by + 70)], fill=dim(c, 0.2), outline=c, width=3)
    d.ellipse([(bx - 35, by - 75), (bx + 35, by - 10)], fill=dim(c, 0.2), outline=c, width=3)
    d.ellipse([(bx - 42, by - 82), (bx - 22, by - 60)], fill=dim(c, 0.2), outline=c, width=2)
    d.ellipse([(bx + 22, by - 82), (bx + 42, by - 60)], fill=dim(c, 0.2), outline=c, width=2)
    d.ellipse([(bx - 16, by - 55), (bx - 8, by - 45)], fill=c)
    d.ellipse([(bx + 8, by - 55), (bx + 16, by - 45)], fill=c)
    d.ellipse([(bx - 6, by - 38), (bx + 6, by - 28)], fill=c)
    d.arc([(bx - 12, by - 30), (bx + 12, by - 18)], start=0, end=180, fill=c, width=2)
    for side in [-1, 1]:
        px = bx + side * 55
        py = by + 70
        d.line([(px, by + 30), (px, py + 40)], fill=c, width=3)
        for gi in range(-1, 2):
            d.line([(px + gi * 5, py + 40), (px + gi * 5 + side * 3, py + 50)], fill=c, width=2)
    pts = [(120, 210)]
    for i in range(8):
        xx = 120 + (i + 1) * 70
        yy = 210 + (i + 1) * 18 + random.randint(-8, 8)
        pts.append((xx, yy))
    for i in range(len(pts) - 1):
        d.line([pts[i], pts[i + 1]], fill=dim(rc, 0.4), width=2)


def scene_beexo_hive(d, W, H, ac):
    """Panal de abejas con monedas y abeja grande."""
    c = dim(ac, 0.7)
    hs = 38
    for row in range(5):
        for col in range(6):
            cx = W // 2 - 130 + col * int(hs * 1.75)
            cy = 170 + row * int(hs * 1.5)
            if row % 2:
                cx += int(hs * 0.87)
            draw_hexagon(d, cx, cy, hs, c, width=2)
            if random.random() < 0.3:
                draw_coin(d, cx, cy, 12, dim(c, 0.5), "B")
    bee_x, bee_y = W // 2 + 140, 230
    d.ellipse([(bee_x - 20, bee_y - 12), (bee_x + 20, bee_y + 12)],
              fill=dim("#ffc947", 0.3), outline=c, width=2)
    d.line([(bee_x - 8, bee_y - 11), (bee_x - 8, bee_y + 11)], fill=c, width=2)
    d.line([(bee_x + 5, bee_y - 12), (bee_x + 5, bee_y + 12)], fill=c, width=2)
    d.ellipse([(bee_x - 30, bee_y - 8), (bee_x - 18, bee_y + 8)], outline=c, width=2)
    d.ellipse([(bee_x - 5, bee_y - 28), (bee_x + 15, bee_y - 8)], outline=dim(c, 0.5), width=1)
    d.ellipse([(bee_x + 5, bee_y - 25), (bee_x + 22, bee_y - 10)], outline=dim(c, 0.5), width=1)
    d.line([(bee_x + 20, bee_y), (bee_x + 32, bee_y)], fill=c, width=2)
    draw_hexagon(d, W // 2, H // 2, 95, dim(c, 0.15), width=2)


def scene_fomo_crowd(d, W, H, ac):
    """Multitud corriendo hacia pantalla con gráfico verde."""
    c = dim(ac, 0.7)
    gc = dim("#22cc66", 0.6)
    sx, sy = W - 200, 185
    d.rectangle([(sx, sy), (sx + 120, sy + 100)], outline=gc, width=3)
    d.rectangle([(sx + 4, sy + 4), (sx + 116, sy + 96)], fill=(10, 15, 10))
    d.polygon([(sx + 60, sy + 15), (sx + 90, sy + 50), (sx + 70, sy + 50)], fill=gc)
    d.rectangle([(sx + 45, sy + 50), (sx + 70, sy + 85)], fill=gc)
    gf = get_font(16)
    d.text((sx + 25, sy + 105), "+1000%", font=gf, fill=gc)
    positions = [(150, 290), (220, 310), (300, 280), (370, 320), (440, 295)]
    for px, py in positions:
        draw_person(d, px, py, 80 + random.randint(-5, 5), c, "run")
    draw_person(d, 90, 320, 65, dim(c, 0.4), "stand")
    for i in range(4):
        ddx = 120 + i * 45
        dy2 = 380 + random.randint(-5, 5)
        dr = random.randint(5, 10)
        d.ellipse([(ddx - dr, dy2 - dr), (ddx + dr, dy2 + dr)], outline=dim(c, 0.2), width=1)


def scene_dyor_brain(d, W, H, ac):
    """Cerebro con lupa, libros y bombilla de idea."""
    c = dim(ac, 0.75)
    bx, by = W // 2, 260
    d.ellipse([(bx - 50, by - 45), (bx + 10, by + 30)], outline=c, width=3)
    d.ellipse([(bx - 10, by - 45), (bx + 50, by + 30)], outline=c, width=3)
    d.ellipse([(bx - 40, by - 55), (bx + 5, by - 10)], outline=c, width=2)
    d.ellipse([(bx - 5, by - 55), (bx + 40, by - 10)], outline=c, width=2)
    d.arc([(bx - 30, by - 35), (bx + 30, by + 5)], start=20, end=160, fill=dim(c, 0.4), width=1)
    d.arc([(bx - 25, by - 15), (bx + 25, by + 20)], start=200, end=340, fill=dim(c, 0.4), width=1)
    lx, ly = bx + 90, by - 10
    lr = 28
    d.ellipse([(lx - lr, ly - lr), (lx + lr, ly + lr)], outline=c, width=3)
    d.line([(lx + int(lr * 0.7), ly + int(lr * 0.7)),
            (lx + int(lr * 1.4), ly + int(lr * 1.4))], fill=c, width=4)
    for i in range(3):
        lbx = bx - 140
        lby = by + 20 - i * 18
        d.rectangle([(lbx, lby), (lbx + 50, lby + 14)], outline=c, width=2)
        d.line([(lbx + 3, lby + 7), (lbx + 47, lby + 7)], fill=dim(c, 0.3), width=1)
    qf = get_font(24)
    for qx, qy in [(bx - 80, by - 70), (bx + 75, by - 65), (bx - 90, by + 40), (bx + 110, by + 30)]:
        d.text((qx, qy), "?", font=qf, fill=dim(c, 0.4))
    blx, bly = bx, by - 85
    d.ellipse([(blx - 12, bly - 14), (blx + 12, bly + 10)], outline=brt(c), width=2)
    d.rectangle([(blx - 6, bly + 10), (blx + 6, bly + 18)], outline=brt(c), width=1)
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        d.line([(blx + int(16 * math.cos(a)), bly + int(16 * math.sin(a))),
                (blx + int(24 * math.cos(a)), bly + int(24 * math.sin(a)))], fill=brt(c), width=1)


def scene_password_fail(d, W, H, ac):
    """Pantalla con password débil + candado roto + hacker."""
    c = dim(ac, 0.7)
    rc = dim("#ff4444", 0.7)
    mx, my = W // 2 - 120, 185
    sx, sy, sw, sh = draw_monitor(d, mx, my, 240, 170, c)
    d.rounded_rectangle([(sx + 20, sy + 20), (sx + sw - 20, sy + 45)], radius=5, outline=c, width=1)
    uf = get_font(11, bold=False)
    d.text((sx + 25, sy + 25), "user: beexer123", font=uf, fill=dim(c, 0.6))
    d.rounded_rectangle([(sx + 20, sy + 55), (sx + sw - 20, sy + 80)], radius=5, outline=c, width=1)
    d.text((sx + 25, sy + 60), "pass: 1234", font=uf, fill=rc)
    d.rounded_rectangle([(sx + 60, sy + 90), (sx + sw - 60, sy + 110)], radius=5,
                        fill=dim(c, 0.3), outline=c, width=1)
    d.text((sx + 75, sy + 93), "LOGIN", font=get_font(12), fill=c)
    d.rounded_rectangle([(sx + 20, sy + 120), (sx + sw - 20, sy + 145)], radius=5,
                        fill=dim(rc, 0.2), outline=rc, width=1)
    d.text((sx + 30, sy + 125), "HACKED!", font=get_font(14), fill=rc)
    lkx, lky = mx + 280, my + 50
    d.rounded_rectangle([(lkx - 20, lky + 15), (lkx + 20, lky + 45)], radius=4, outline=rc, width=2)
    d.arc([(lkx - 14, lky - 10), (lkx + 14, lky + 25)], start=180, end=0, fill=rc, width=2)
    d.line([(lkx - 5, lky + 20), (lkx + 5, lky + 30)], fill=rc, width=2)
    d.line([(lkx + 5, lky + 30), (lkx - 3, lky + 40)], fill=rc, width=2)
    draw_person(d, mx - 60, my + 50, 100, dim(c, 0.5), "run")


def scene_two_opinions(d, W, H, ac):
    """Dos personas cara a cara: SELL vs HODL."""
    c = dim(ac, 0.7)
    gc = dim("#22cc66", 0.6)
    rc = dim("#ff4444", 0.6)
    draw_person(d, 200, 280, 110, rc, "celebrate")
    draw_person(d, 600, 280, 110, gc, "stand")
    bx, by2 = 140, 175
    d.rounded_rectangle([(bx, by2), (bx + 90, by2 + 45)], radius=12,
                        fill=dim(rc, 0.15), outline=rc, width=2)
    d.polygon([(bx + 50, by2 + 45), (bx + 45, by2 + 60), (bx + 60, by2 + 45)],
              fill=dim(rc, 0.15), outline=rc, width=2)
    sf = get_font(22)
    d.text((bx + 12, by2 + 8), "SELL!", font=sf, fill=rc)
    bx2 = 555
    d.rounded_rectangle([(bx2, by2), (bx2 + 95, by2 + 45)], radius=12,
                        fill=dim(gc, 0.15), outline=gc, width=2)
    d.polygon([(bx2 + 30, by2 + 45), (bx2 + 25, by2 + 60), (bx2 + 40, by2 + 45)],
              fill=dim(gc, 0.15), outline=gc, width=2)
    d.text((bx2 + 8, by2 + 8), "HODL!", font=sf, fill=gc)
    ccx = W // 2
    pts = [(ccx - 50, 350)]
    for i in range(6):
        x = ccx - 50 + (i + 1) * 17
        y = 350 + random.randint(-30, 30)
        pts.append((x, y))
    for i in range(len(pts) - 1):
        d.line([pts[i], pts[i + 1]], fill=c, width=2)
    vf = get_font(32)
    d.text((ccx - 20, 280), "VS", font=vf, fill=dim(c, 0.5), stroke_width=2, stroke_fill="black")


# =============================================================
# SELECCIÓN DE ESCENA POR CONTENIDO DEL MEME
# =============================================================

KEYWORD_SCENE_MAP = [
    (["dormir", "3am", "noche", "despertar", "levant", "cama", "insomnio", "madrugada"], "night_check"),
    (["abuela", "novia", "novio", "mama", "papa", "familia", "navidad", "terrenito", "cena", "regalo"], "family_talk"),
    (["amigos", "me dicen", "todos dicen", "le digo", "le explic", "mi ex"], "two_opinions"),
    (["hack", "password", "contrasena", "clave", "1234", "firulais", "crackea", "sim swap"], "hacker_attack"),
    (["scam", "estafa", "phishing", "cuidado", "peligro", "falso", "rug pull"], "scam_alert"),
    (["soporte", " dm", "privado", "hola como"], "scam_alert"),
    (["seed", "12 palabra", "frase secreta", "semilla", "frase de"], "vault_lock"),
    (["2fa", "verificacion", "backup", "llave", "caja fuerte", "candado", "not your keys"], "vault_lock"),
    (["hodl", "diamond", "diamante", "holdea", "holdear", "no vendo", "no vendi", "paper hands"], "diamond_hodl"),
    (["moon", "luna", "x1000", "cohete", "to the moon", "vuela"], "to_the_moon"),
    (["fee", " gas ", "comision", "swap", "gwei", "departamento"], "fees_burning"),
    (["portfolio", "balance", "abro", "cierro", "cada 5 min", "pantalla", "app"], "phone_obsession"),
    (["trad", "vela", "analisis", "nociones", "grafico", "indicador"], "trading_pro"),
    (["plata", "ahorro", "banco", "colectivo", "broke", "no tengo", "vacio", "pobre", "cuenta del banco"], "no_money"),
    (["fomo", "viral", "trending", "todos compr"], "fomo_crowd"),
    (["dyor", "investig", "research", "cerebro", "genio", "experto"], "dyor_brain"),
    (["bull", "toro", "alcist"], "bull"),
    (["bear", "oso", "bajist"], "bear"),
    (["beexo", "beexer", "comunidad"], "beexo_hive"),
    (["sube", "subio", "pump", "dispara", "verde", "recuper"], "chart_pump"),
    (["cae", "cayo", "baja", "dump", "dip", "fondo", "pierde", "rojo", "crash", "desploma", "sotano"], "chart_falling"),
]

CATEGORY_FALLBACK = {
    "dip": "chart_falling", "security": "vault_lock", "hodl": "diamond_hodl",
    "scam": "scam_alert", "fomo": "fomo_crowd", "gas": "fees_burning",
    "portfolio": "phone_obsession", "trading": "trading_pro", "family": "family_talk",
    "market": "bull", "beexo": "beexo_hive", "news": "chart_pump",
}

SCENE_FUNCTIONS = {
    "chart_falling": scene_chart_falling, "chart_pump": scene_chart_pump,
    "phone_obsession": scene_phone_obsession, "no_money": scene_no_money,
    "vault_lock": scene_vault_lock, "hacker_attack": scene_hacker_attack,
    "diamond_hodl": scene_diamond_hodl, "to_the_moon": scene_to_the_moon,
    "fees_burning": scene_fees_burning, "scam_alert": scene_scam_alert,
    "night_check": scene_night_check, "family_talk": scene_family_talk,
    "trading_pro": scene_trading_pro, "bull": scene_bull, "bear": scene_bear,
    "beexo_hive": scene_beexo_hive, "fomo_crowd": scene_fomo_crowd,
    "dyor_brain": scene_dyor_brain, "password_fail": scene_password_fail,
    "two_opinions": scene_two_opinions,
}


def pick_scene(top_text, bottom_text, category=None, idx=0):
    """Selecciona la escena que mejor representa el contenido del meme."""
    text = f"{top_text} {bottom_text}".lower()
    for keywords, scene in KEYWORD_SCENE_MAP:
        if any(k in text for k in keywords):
            return scene
    if category and category in CATEGORY_FALLBACK:
        return CATEGORY_FALLBACK[category]
    if idx < 15: return "chart_falling"
    if idx < 35: return "vault_lock"
    if idx < 55: return "diamond_hodl"
    if idx < 75: return "scam_alert"
    if idx < 95: return "fomo_crowd"
    if idx < 110: return "fees_burning"
    if idx < 130: return "phone_obsession"
    if idx < 150: return "trading_pro"
    if idx < 170: return "family_talk"
    if idx < 190: return "bull"
    return "beexo_hive"


# =============================================================
# CREAR MEME CON ILUSTRACIÓN + VIGNETTE + TEXTO
# =============================================================

def create_meme(filename, top_text, bottom_text, grad_top, grad_bottom,
                accent, sep_style="line", icon_text="VS", category=None, idx=0):
    """Crea un meme con ilustración temática, vignette y texto."""
    # 1) Base RGBA con gradiente
    base = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    bd = ImageDraw.Draw(base)
    gradient(bd, W, H, grad_top, grad_bottom)

    # 2) Dibujar escena temática
    scene_name = pick_scene(top_text, bottom_text, category, idx)
    scene_fn = SCENE_FUNCTIONS.get(scene_name)
    if scene_fn:
        scene_fn(bd, W, H, accent)

    # 3) Barras de acento
    ac_rgb = h2rgb(accent) if isinstance(accent, str) else accent
    bd.rectangle([(0, 0), (W, 5)], fill=ac_rgb)
    bd.rectangle([(0, H - 5), (W, H)], fill=ac_rgb)

    # 4) Vignette semi-transparente para legibilidad del texto
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for y in range(195):
        a = int(175 * (1 - y / 195) ** 1.3)
        od.line([(0, y), (W, y)], fill=(0, 0, 0, a))
    for y in range(H - 195, H):
        a = int(175 * ((y - (H - 195)) / 195) ** 1.3)
        od.line([(0, y), (W, y)], fill=(0, 0, 0, a))

    img = Image.alpha_composite(base, ov)
    td = ImageDraw.Draw(img)

    # 5) Texto superior (blanco)
    top_font = get_font(46)
    draw_text_block(td, top_text, top_font, 30, W,
                    fill="white", stroke_w=5, stroke_fill="#000000", max_chars=26)

    # 6) Texto inferior (color acento)
    bottom_font = get_font(42)
    draw_text_block(td, bottom_text, bottom_font, H - 170, W,
                    fill=accent, stroke_w=4, stroke_fill="#000000", max_chars=28)

    # 7) Badge ícono
    if icon_text:
        icon_font = get_font(20)
        bb = td.textbbox((0, 0), icon_text, font=icon_font)
        iw = bb[2] - bb[0]
        td.rounded_rectangle([(12, H - 38), (12 + iw + 16, H - 12)], radius=6, fill=ac_rgb)
        td.text((20, H - 36), icon_text, font=icon_font, fill="white")

    # 8) Branding Beexo
    draw_hexagon(td, W - 50, H - 25, 10, ac_rgb, width=2)
    bf = get_font(13, bold=False)
    td.text((W - 38, H - 32), "BEEXO", font=bf, fill=ac_rgb)

    path = os.path.join(MEMES_DIR, filename)
    img.convert("RGB").save(path, "PNG", quality=95)
    print(f"  [OK] {filename}  [{scene_name}]")
    return path


def get_category_from_index(idx):
    if idx < 15: return "dip"
    if idx < 35: return "security"
    if idx < 55: return "hodl"
    if idx < 75: return "scam"
    if idx < 95: return "fomo"
    if idx < 110: return "gas"
    if idx < 130: return "portfolio"
    if idx < 150: return "trading"
    if idx < 170: return "family"
    if idx < 190: return "market"
    return "beexo"


def main():
    print(f"Generando {len(MEMES_DATA)} memes con ilustraciones tematicas...\n")
    random.seed(42)
    for idx, m in enumerate(MEMES_DATA):
        cat = get_category_from_index(idx)
        create_meme(
            filename=m["file"],
            top_text=m["top"],
            bottom_text=m["bottom"],
            grad_top=m["grad_top"],
            grad_bottom=m["grad_bottom"],
            accent=m["accent"],
            sep_style=m["sep"],
            icon_text=m["icon"],
            category=cat,
            idx=idx,
        )
    print(f"\n{len(MEMES_DATA)} memes generados en: {MEMES_DIR}")


if __name__ == "__main__":
    main()
