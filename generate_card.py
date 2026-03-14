"""
Generate a pixel-art themed birthday card with QR code for Dima.
Dark code-editor aesthetic, matching the game's visual style.
"""

from PIL import Image, ImageDraw, ImageFont
import qrcode
import random

# --- Config ---
W, H = 1080, 1920
URL = "https://xeroxinn.github.io/dima-birthday/"
OUT = "/Users/igorraev/Work/Development/.tmp/dima-birthday/output/card.png"

# Colors (matching game palette)
BG = (15, 14, 23)
SURFACE = (26, 26, 46)
PANEL = (22, 33, 62)
ACCENT = (0, 212, 255)
GREEN = (0, 255, 136)
RED = (255, 71, 87)
YELLOW = (255, 211, 42)
ORANGE = (255, 159, 67)
PINK = (255, 107, 157)
PURPLE = (168, 85, 247)
TEXT = (232, 232, 232)
DIM = (74, 74, 106)

random.seed(42)

img = Image.new('RGB', (W, H), BG)
draw = ImageDraw.Draw(img)

# --- Background gradient ---
for y in range(H):
    t = y / H
    r = int(15 + t * 12)
    g = int(14 + t * 6)
    b = int(23 + t * 20)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# --- Stars ---
for _ in range(150):
    x = random.randint(0, W)
    y = random.randint(0, H)
    brightness = random.randint(30, 130)
    size = random.choice([1, 1, 1, 2, 2])
    c = (brightness, brightness, brightness + 30)
    if size == 1:
        draw.point((x, y), fill=c)
    else:
        draw.rectangle([x, y, x+1, y+1], fill=c)

# --- Floating code symbols ---
code_syms = ['{ }', '< >', '//', '=>', 'fn', 'if', '0x', '&&', '++', '[]', '()', '!=', '##', '<<', '->']
try:
    sym_font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 20)
except:
    sym_font = ImageFont.load_default()

for sym in code_syms:
    x = random.randint(20, W - 60)
    y = random.randint(50, H - 50)
    draw.text((x, y), sym, fill=(DIM[0]//3, DIM[1]//3, DIM[2]//3), font=sym_font)

# --- Font loader ---
def load_font(size):
    paths = [
        "/Users/igorraev/Library/Fonts/PressStart2P-Regular.ttf",
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/Courier.dfont",
    ]
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except:
            continue
    return ImageFont.load_default()

font_title = load_font(44)
font_dima = load_font(64)
font_sub = load_font(26)
font_body = load_font(22)
font_small = load_font(18)
font_tiny = load_font(14)

# --- Helper: centered text ---
def center_text(y, text, font, color):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    draw.text(((W - w) // 2, y), text, fill=color, font=font)
    return w

def center_text_glow(y, text, font, color, glow_radius=3):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    x = (W - w) // 2
    glow = (color[0]//5, color[1]//5, color[2]//5)
    for offset in range(glow_radius, 0, -1):
        draw.text((x + offset, y + offset), text, fill=glow, font=font)
    draw.text((x, y), text, fill=color, font=font)
    return w

# --- Pixel art helpers ---
def draw_px(pixels, ox, oy, s, color):
    for px, py in pixels:
        draw.rectangle([ox+px*s, oy+py*s, ox+px*s+s-1, oy+py*s+s-1], fill=color)

def draw_heart(ox, oy, s=4, color=PINK):
    draw_px([(1,0),(2,0),(4,0),(5,0),
             (0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),
             (0,2),(1,2),(2,2),(3,2),(4,2),(5,2),(6,2),
             (1,3),(2,3),(3,3),(4,3),(5,3),
             (2,4),(3,4),(4,4),(3,5)], ox, oy, s, color)

def draw_controller(ox, oy, s=5):
    body = [(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),
            (1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),
            (0,2),(1,2),(2,2),(3,2),(4,2),(5,2),(6,2),(7,2),(8,2),(9,2),
            (0,3),(1,3),(2,3),(3,3),(4,3),(5,3),(6,3),(7,3),(8,3),(9,3),
            (1,4),(2,4),(3,4),(7,4),(8,4),(1,5),(2,5),(7,5),(8,5)]
    draw_px(body, ox, oy, s, PURPLE)
    draw_px([(2,2),(3,2),(3,1),(3,3)], ox, oy, s, TEXT)
    draw_px([(7,2),(6,3)], ox, oy, s, RED)

def draw_tea(ox, oy, s=5):
    cup = [(1,0),(2,0),(3,0),(4,0),
           (0,1),(1,1),(2,1),(3,1),(4,1),(5,1),
           (0,2),(1,2),(2,2),(3,2),(4,2),(5,2),
           (0,3),(1,3),(2,3),(3,3),(4,3),(5,3),
           (1,4),(2,4),(3,4),(4,4)]
    draw_px(cup, ox, oy, s, ACCENT)
    draw_px([(2,-1),(3,-2)], ox, oy, s, (100,100,140))
    draw.rectangle([ox+6*s, oy+1*s, ox+6*s+s-1, oy+3*s+s-1], fill=ACCENT)

def draw_bug(ox, oy, s=5):
    draw_px([(2,0),(3,0),(2,1),(3,1),(1,2),(2,2),(3,2),(4,2),
             (1,3),(2,3),(3,3),(4,3),(2,4),(3,4)], ox, oy, s, RED)
    draw_px([(0,2),(5,2),(0,3),(5,3)], ox, oy, s, ORANGE)

def draw_sword(ox, oy, s=4):
    """Simple Dark Souls bonfire/sword pixel art"""
    blade = [(3,0),(3,1),(3,2),(3,3),(3,4),(3,5),(3,6)]
    guard = [(1,7),(2,7),(3,7),(4,7),(5,7)]
    grip = [(3,8),(3,9),(3,10)]
    pommel = [(2,11),(3,11),(4,11)]
    draw_px(blade, ox, oy, s, TEXT)
    draw_px(guard, ox, oy, s, YELLOW)
    draw_px(grip, ox, oy, s, ORANGE)
    draw_px(pommel, ox, oy, s, YELLOW)

def draw_skull(ox, oy, s=4):
    """YOU DIED skull"""
    top = [(1,0),(2,0),(3,0),(4,0),
           (0,1),(1,1),(2,1),(3,1),(4,1),(5,1),
           (0,2),(1,2),(2,2),(3,2),(4,2),(5,2)]
    eyes = [(1,1),(4,1)]
    jaw = [(1,3),(2,3),(3,3),(4,3),
           (1,4),(3,4),(5,4)]  # teeth gaps
    draw_px(top, ox, oy, s, TEXT)
    draw_px(eyes, ox, oy, s, RED)
    draw_px(jaw, ox, oy, s, (180,180,180))

# --- Decorative pixel border ---
def pixel_border(y, c1=GREEN, c2=ACCENT):
    for x in range(0, W, 8):
        c = c1 if (x // 8) % 2 == 0 else c2
        draw.rectangle([x, y, x+6, y+4], fill=c)

# ====== LAYOUT ======

# --- Top border ---
pixel_border(50)

# --- Pixel art icons row ---
draw_controller(70, 85, 5)
draw_bug(W//2 - 15, 90, 5)
draw_tea(W - 140, 85, 5)

# --- Title: С ДНЁМ РОЖДЕНИЯ! ---
center_text_glow(190, "С ДНЁМ", font_title, ACCENT, 3)
center_text_glow(250, "РОЖДЕНИЯ!", font_title, ACCENT, 3)

# --- ДИМА ---
center_text_glow(360, "ДИМА", font_dima, GREEN, 4)

# --- Decorative line ---
pixel_border(455, PINK, PURPLE)

# --- Subtitle ---
center_text(490, "Но подарок нужно", font_sub, TEXT)
center_text(530, "заслужить...", font_sub, YELLOW)

# --- Pixel art: sword + skull flanking subtitle ---
draw_sword(140, 480, 4)
draw_skull(W - 180, 490, 4)

# --- QR Code section ---
qr_y_start = 610

# Generate QR
qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=2)
qr.add_data(URL)
qr.make(fit=True)
qr_img = qr.make_image(fill_color=(0, 255, 136), back_color=(15, 14, 23)).convert('RGB')
qr_size = 480
qr_img = qr_img.resize((qr_size, qr_size), Image.NEAREST)

# QR frame
fp = 24
fx = (W - qr_size) // 2 - fp
fy = qr_y_start - fp
fw = qr_size + 2 * fp
fh = qr_size + 2 * fp

# Frame with double border
draw.rectangle([fx-3, fy-3, fx+fw+3, fy+fh+3], fill=None, outline=ACCENT, width=2)
draw.rectangle([fx, fy, fx+fw, fy+fh], fill=SURFACE, outline=GREEN, width=3)

# Corner accents
cs = 14
for cx, cy in [(fx, fy), (fx+fw-cs, fy), (fx, fy+fh-cs), (fx+fw-cs, fy+fh-cs)]:
    draw.rectangle([cx, cy, cx+cs, cy+cs], fill=ACCENT)

# Paste QR
img.paste(qr_img, ((W - qr_size) // 2, qr_y_start))

# --- Scan instructions ---
inst_y = qr_y_start + qr_size + 60

# Arrow triangles pointing up
for i in range(5):
    ax = W//2 - 20 + i * 10
    draw.polygon([(ax, inst_y - 25), (ax+5, inst_y - 35), (ax+10, inst_y - 25)], fill=GREEN)

# Step 1
center_text(inst_y, "1. ОТСКАНИРУЙ", font_body, GREEN)
# Down arrow
bbox_arr = draw.textbbox((0, 0), "v", font=font_small)
draw.text((W//2 - 5, inst_y + 38), "v", fill=DIM, font=font_small)
# Step 2
center_text(inst_y + 60, "2. ПРОЙДИ ИГРУ", font_body, ACCENT)
draw.text((W//2 - 5, inst_y + 98), "v", fill=DIM, font=font_small)
# Step 3
center_text(inst_y + 120, "3. ПОЛУЧИ ПОДАРОК", font_body, YELLOW)

# --- Hearts flanking instructions ---
draw_heart(60, inst_y + 40, 5, PINK)
draw_heart(W - 100, inst_y + 40, 5, RED)

# --- Decorative line ---
deco_y = inst_y + 190
pixel_border(deco_y, GREEN, DIM)

# --- Dark Souls flavor section ---
ds_y = deco_y + 40

# Terminal-style block
term_x = 100
term_w = W - 200
term_h = 230
draw.rectangle([term_x, ds_y, term_x + term_w, ds_y + term_h], fill=(12, 11, 20), outline=DIM, width=1)

# Terminal top bar dots
for i, c in enumerate([RED, YELLOW, GREEN]):
    draw.ellipse([term_x + 12 + i*22, ds_y + 10, term_x + 22 + i*22, ds_y + 20], fill=c)

# Terminal content
ty = ds_y + 38
lines = [
    ("$ cat warning.txt", GREEN),
    ("", None),
    ("// WARNING:", ORANGE),
    ("// Dark Souls скиллы", DIM),
    ("// не помогут...", DIM),
    ("// Или помогут? ;)", PURPLE),
    ("", None),
    ("$ echo 'YOU DIED'", GREEN),
    ("YOU DIED 💀", RED),
]
for text, color in lines:
    if color:
        draw.text((term_x + 20, ty), text, fill=color, font=font_tiny)
    ty += 24

# --- Fun facts section ---
facts_y = ds_y + term_h + 30

center_text(facts_y, "// LOADING FACTS...", font_small, DIM)

fact_lines = [
    ("490+ часов в Dark Souls", PURPLE),
    ("Просыпается раньше будильника", TEXT),
    ("Чай > Кофе (всегда)", ACCENT),
    ("Налоговая подана в марте", GREEN),
]

fy = facts_y + 32
for text, color in fact_lines:
    center_text(fy, text, font_tiny, color)
    fy += 24

# --- Skyline at bottom ---
sky_y = H - 140
SKYLINE = [3,5,4,8,6,3,10,7,4,5,12,8,5,3,6,9,4,7,5,3,6,4,8,5,3,7,10,6,4,5]
block_w = W // len(SKYLINE)
for i, h in enumerate(SKYLINE):
    bx = i * block_w
    by = sky_y + (12 - h) * 5
    bot = H - 50
    if by >= bot:
        continue
    draw.rectangle([bx, by, bx + block_w - 2, bot], fill=(18, 17, 28))
    # Window lights
    for wy in range(by + 6, bot - 10, 12):
        for wx in range(bx + 4, bx + block_w - 6, 10):
            if random.random() < 0.35:
                wc = random.choice([YELLOW, ACCENT, ORANGE])
                draw.rectangle([wx, wy, wx+4, wy+4], fill=(wc[0]//4, wc[1]//4, wc[2]//4))

# Church dome (Tbilisi vibe) - center
dome_x = W // 2 - 20
dome_y = sky_y - 10
draw_px([(2,0),(3,0),(4,0),
         (1,1),(2,1),(3,1),(4,1),(5,1),
         (0,2),(1,2),(2,2),(3,2),(4,2),(5,2),(6,2)], dome_x, dome_y, 4, (22, 21, 34))
# Cross on top
draw_px([(3,-2),(3,-1),(2,-1),(4,-1)], dome_x, dome_y, 4, YELLOW)

# --- Bottom credits ---
pixel_border(H - 65, PURPLE, PINK)

center_text(H - 48, "from Igor & Marina", font_tiny, DIM)
# Hearts next to credits
draw_heart(W//2 - 150, H - 52, 3, PINK)
draw_heart(W//2 + 120, H - 52, 3, RED)

# --- Save ---
img.save(OUT, 'PNG', optimize=True)
print(f"Card saved to {OUT}")
print(f"Size: {W}x{H}")
