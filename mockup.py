"""
Banyan Throwdown — judge heat card, v3.
Bolder, more defined visual hierarchy. Filled section heads,
thicker rules, tinted scoring zones, graph-paper tally.
"""
import os
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "mockup.pdf")
LOGO = os.path.join(HERE, "logo.png")

# Palette
INK      = HexColor("#0E0E0E")
MUTED    = HexColor("#555555")
RULE_LT  = HexColor("#BDBDBD")
BANYAN   = HexColor("#2E6B34")
BANYAN_D = HexColor("#1F4D2B")   # deep shield green
BANYAN_L = HexColor("#E6F0E5")   # pale green tint for TOTAL zone
ACCENT   = HexColor("#E07A1F")   # sunrise orange (logo)
PAGE_BG  = HexColor("#ECE8DD")   # warm neutral page background
GRAY_L   = HexColor("#E2DED1")   # section tint (harmonized with page bg)
GRAY_M   = HexColor("#C9C3B2")
GRAPH    = HexColor("#BDB8A8")
WHITE_B  = HexColor("#FFFFFF")   # true white for score boxes

pdfmetrics.registerFont(
    TTFont("IPAGothic", "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf")
)
JP = "IPAGothic"

PAGE_W, PAGE_H = landscape(letter)
OUTER = 0.20 * inch     # outer page frame inset
M = 0.38 * inch         # content margin (inside the frame)

lanes = [
    ("1", "Megumi Iha"),
    ("2", "Takako Anderson"),
    ("3", "Megumi Nakagawa"),
    ("4", "Chiemi Matayoshi"),
    ("5", "Cassandra Cartwright"),
    ("6", "Lisa Miller"),
]

movements = [
    ("50",  "Single-Unders",                                "シングルアンダー"),
    ("40",  "Medicine Ball Bear Hug Squats (20 / 14 lb)",   "メディシンボール・ベアハグスクワット"),
    ("30",  "Knee Raises",                                  "ニーレイズ"),
    ("20",  "Medicine Ball Overhead Walking Lunges (20 / 14 lb)",
                                                            "メディシンボール・オーバーヘッドランジ"),
    ("10",  "Jumping Pull-Ups",                             "ジャンピングプルアップ"),
]

c = canvas.Canvas(OUT, pagesize=landscape(letter))

# ============================================================
# PAGE BACKGROUND (warm neutral — not brown, not stark white)
# ============================================================
c.setFillColor(PAGE_BG)
c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

# ============================================================
# GEOMETRY
# ============================================================
HEADER_H  = 0.72 * inch
META_H    = 0.58 * inch
WORKOUT_H = 2.00 * inch
GAP       = 0.10 * inch
FOOTER_H  = 0.42 * inch

page_top    = PAGE_H - OUTER     # everything lives under this
page_bot    = OUTER
y_header_b  = page_top - HEADER_H
y_meta_b    = y_header_b - META_H
y_wo_t      = y_meta_b - 0.04 * inch
y_wo_b      = y_wo_t - WORKOUT_H
y_grid_t    = y_wo_b - GAP
y_grid_b    = page_bot + FOOTER_H

# ============================================================
# HEADER BAND (shield-black with banyan stripe)
# ============================================================
c.setFillColor(INK)
c.rect(OUTER, y_header_b, PAGE_W - 2*OUTER, HEADER_H, fill=1, stroke=0)
c.setFillColor(BANYAN)
c.rect(OUTER, y_header_b - 0.08 * inch, PAGE_W - 2*OUTER, 0.08 * inch,
       fill=1, stroke=0)

# logo
logo_size = 0.60 * inch
lx = M
ly = y_header_b + (HEADER_H - logo_size) / 2
if os.path.exists(LOGO):
    c.drawImage(LOGO, lx, ly, width=logo_size, height=logo_size,
                mask="auto", preserveAspectRatio=True)
else:
    c.setStrokeColor(BANYAN); c.setLineWidth(2)
    c.rect(lx, ly, logo_size, logo_size, stroke=1, fill=0)
    c.setFillColor(BANYAN); c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(lx + logo_size/2, ly + 0.18 * inch, "BT")

# wordmark
wx = lx + logo_size + 0.22 * inch
c.setFillColor(white); c.setFont("Helvetica-Bold", 26)
c.drawString(wx, y_header_b + 0.32 * inch, "BANYAN THROWDOWN")
c.setFillColor(HexColor("#CFCFCF")); c.setFont(JP, 11)
c.drawString(wx, y_header_b + 0.12 * inch, "バニヤン・スローダウン")

# right header
c.setFillColor(white); c.setFont("Helvetica-Bold", 10)
c.drawRightString(PAGE_W - M, y_header_b + 0.48 * inch, "OFFICIAL JUDGE SCORECARD")
c.setFillColor(HexColor("#CFCFCF")); c.setFont(JP, 9)
c.drawRightString(PAGE_W - M, y_header_b + 0.31 * inch, "公式ジャッジ採点カード")
c.setFillColor(ACCENT); c.setFont("Helvetica-Bold", 9)
c.drawRightString(PAGE_W - M, y_header_b + 0.12 * inch,
                  "4/25 (Sat)  ·  @banyan_throwdown")

# ============================================================
# META ROW
# ============================================================
c.setFillColor(GRAY_L)
c.rect(OUTER, y_meta_b, PAGE_W - 2*OUTER, META_H, fill=1, stroke=0)

meta_y_mid = y_meta_b + META_H / 2

c.setFillColor(ACCENT); c.setFont("Helvetica-Bold", 30)
c.drawString(M, meta_y_mid - 0.13 * inch, "EVENT 1")

ex = M + 1.85 * inch
c.setFillColor(INK); c.setFont("Helvetica-Bold", 16)
c.drawString(ex, meta_y_mid + 0.03 * inch, "10-Minute AMRAP")
c.setFillColor(MUTED); c.setFont(JP, 10)
c.drawString(ex, meta_y_mid - 0.18 * inch, "10分間 AMRAP")

meta = [("HEAT", "1"), ("DIVISION", "Scaled (F)"), ("START", "9:00")]
block_w = 1.55 * inch
bx = PAGE_W - M - block_w * len(meta)
for i, (label, val) in enumerate(meta):
    if i > 0:
        c.setStrokeColor(GRAY_M); c.setLineWidth(0.6)
        c.line(bx - 0.02 * inch, y_meta_b + 0.12 * inch,
               bx - 0.02 * inch, y_meta_b + META_H - 0.12 * inch)
    c.setFillColor(MUTED); c.setFont("Helvetica-Bold", 8)
    c.drawString(bx, meta_y_mid + 0.17 * inch, label)
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 19)
    c.drawString(bx, meta_y_mid - 0.15 * inch, val)
    bx += block_w

c.setStrokeColor(INK); c.setLineWidth(1.2)
c.line(OUTER, y_meta_b, PAGE_W - OUTER, y_meta_b)

# ============================================================
# WORKOUT PANEL — banyan header bar, white body
# ============================================================
# header strip (banyan green)
wh_h = 0.34 * inch
c.setFillColor(BANYAN_D)
c.rect(M, y_wo_t - wh_h, PAGE_W - 2*M, wh_h, fill=1, stroke=0)
c.setFillColor(white); c.setFont("Helvetica-Bold", 11)
c.drawString(M + 0.15 * inch, y_wo_t - 0.22 * inch,
             "WORKOUT — As many rounds as possible in 10 minutes of:")
c.setFont(JP, 9)
c.drawRightString(PAGE_W - M - 0.15 * inch, y_wo_t - 0.22 * inch,
                  "ワークアウト ー 10分間、以下の種目を可能な限り繰り返す。")

# body (white fill so movement list stands out on warm page bg)
body_t = y_wo_t - wh_h
body_b = y_wo_b
c.setFillColor(WHITE_B); c.setStrokeColor(INK); c.setLineWidth(1.2)
c.rect(M, body_b, PAGE_W - 2*M, body_t - body_b, stroke=1, fill=1)
# (redraw top border aligned with the green strip)
c.setFillColor(INK); c.setFont("Helvetica-Bold", 12)

en_y = body_t - 0.28 * inch
for reps, en, jp in movements:
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 13)
    c.drawString(M + 0.30 * inch, en_y, reps)
    c.setFont("Helvetica", 12)
    c.drawString(M + 0.90 * inch, en_y, en)
    c.setFillColor(MUTED); c.setFont(JP, 8.5)
    c.drawString(M + 0.90 * inch, en_y - 0.14 * inch, jp)
    en_y -= 0.28 * inch

# ============================================================
# LANE GRID
# ============================================================
n = len(lanes)
col_w = (PAGE_W - 2*M) / n
grid_h = y_grid_t - y_grid_b

# outer frame (white fill so lane interiors pop against warm page bg)
c.setFillColor(WHITE_B); c.setStrokeColor(INK); c.setLineWidth(1.5)
c.rect(M, y_grid_b, PAGE_W - 2*M, grid_h, stroke=1, fill=1)

# column headers — banyan-green lane tab on top of black name strip
tab_h = 0.20 * inch    # green tab with LANE #
name_h = 0.38 * inch   # black strip with athlete name
head_h = tab_h + name_h

for i, (lane, name) in enumerate(lanes):
    x0 = M + i * col_w
    # green tab
    c.setFillColor(BANYAN)
    c.rect(x0, y_grid_t - tab_h, col_w, tab_h, fill=1, stroke=0)
    c.setFillColor(white); c.setFont("Helvetica-Bold", 9)
    c.drawString(x0 + 0.10 * inch, y_grid_t - 0.14 * inch, f"LANE {lane}")
    c.setFont(JP, 8)
    c.drawRightString(x0 + col_w - 0.10 * inch, y_grid_t - 0.14 * inch, f"レーン{lane}")
    # black name strip
    c.setFillColor(INK)
    c.rect(x0, y_grid_t - head_h, col_w, name_h, fill=1, stroke=0)
    c.setFillColor(white)
    max_w = col_w - 0.20 * inch
    fs = 13
    while fs > 9 and c.stringWidth(name, "Helvetica-Bold", fs) > max_w:
        fs -= 0.5
    c.setFont("Helvetica-Bold", fs)
    c.drawString(x0 + 0.10 * inch, y_grid_t - head_h + 0.13 * inch, name)

# vertical dividers below the header
c.setStrokeColor(INK); c.setLineWidth(0.8)
for i in range(1, n):
    xv = M + i * col_w
    c.line(xv, y_grid_b, xv, y_grid_t - head_h)

# per-lane body
body_top = y_grid_t - head_h

# budget per field (sums to ~ body_h)
TALLY_H  = 1.32 * inch
NUM_H    = 0.44 * inch
TOTAL_H  = 0.56 * inch
SIG_H    = 0.32 * inch

def section_label(x_l, y_top, width, height, text, jp_text, tint=None):
    """Colored/tinted section label bar."""
    if tint is not None:
        c.setFillColor(tint)
        c.rect(x_l, y_top - height, width, height, fill=1, stroke=0)
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 7.5)
    c.drawString(x_l + 0.06 * inch, y_top - 0.12 * inch, text)
    if jp_text:
        c.setFillColor(MUTED); c.setFont(JP, 7)
        c.drawRightString(x_l + width - 0.06 * inch,
                          y_top - 0.12 * inch, jp_text)

for i in range(n):
    x0 = M + i * col_w
    inner_l = x0 + 0.08 * inch
    inner_r = x0 + col_w - 0.08 * inch
    y = body_top

    # --- TALLY area (graph-paper) ---
    c.setFillColor(GRAY_L)
    c.rect(inner_l, y - 0.18 * inch, inner_r - inner_l, 0.18 * inch, fill=1, stroke=0)
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 7.5)
    c.drawString(inner_l + 0.06 * inch, y - 0.12 * inch, "TALLY")
    c.setFillColor(MUTED); c.setFont(JP, 7)
    c.drawRightString(inner_r - 0.06 * inch, y - 0.12 * inch, "カウント")
    tb_t = y - 0.18 * inch
    tb_b = tb_t - (TALLY_H - 0.18 * inch)
    # graph-paper lines
    c.setStrokeColor(GRAPH); c.setLineWidth(0.4)
    step = 0.14 * inch
    yy = tb_t - step
    while yy > tb_b + 0.02 * inch:
        c.line(inner_l + 0.02 * inch, yy, inner_r - 0.02 * inch, yy)
        yy -= step
    xx = inner_l + step
    while xx < inner_r - 0.02 * inch:
        c.line(xx, tb_t - 0.02 * inch, xx, tb_b + 0.02 * inch)
        xx += step
    # frame
    c.setStrokeColor(INK); c.setLineWidth(0.8)
    c.rect(inner_l, tb_b, inner_r - inner_l, tb_t - tb_b, stroke=1, fill=0)
    y = tb_b - 0.04 * inch

    # --- ROUNDS + EXTRA REPS side by side ---
    half = (inner_r - inner_l - 0.06 * inch) / 2
    c.setFillColor(GRAY_L)
    c.rect(inner_l, y - 0.18 * inch, half, 0.18 * inch, fill=1, stroke=0)
    c.rect(inner_l + half + 0.06 * inch, y - 0.18 * inch, half, 0.18 * inch,
           fill=1, stroke=0)
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 7.5)
    c.drawString(inner_l + 0.06 * inch, y - 0.12 * inch, "ROUNDS")
    c.drawString(inner_l + half + 0.12 * inch, y - 0.12 * inch, "EXTRA REPS")
    # number boxes (white fill for write-on clarity)
    c.setFillColor(WHITE_B); c.setStrokeColor(INK); c.setLineWidth(1.0)
    c.rect(inner_l, y - NUM_H, half, NUM_H - 0.18 * inch, stroke=1, fill=1)
    c.rect(inner_l + half + 0.06 * inch, y - NUM_H, half, NUM_H - 0.18 * inch,
           stroke=1, fill=1)
    y = y - NUM_H - 0.05 * inch

    # --- TOTAL REPS (banyan-filled header + tinted green fill box) ---
    c.setFillColor(BANYAN_D)
    c.rect(inner_l, y - 0.20 * inch, inner_r - inner_l, 0.20 * inch,
           fill=1, stroke=0)
    c.setFillColor(white); c.setFont("Helvetica-Bold", 8)
    c.drawString(inner_l + 0.06 * inch, y - 0.13 * inch, "TOTAL REPS")
    c.setFont(JP, 7.5)
    c.drawRightString(inner_r - 0.06 * inch, y - 0.13 * inch, "合計レップ")
    # big box with pale green fill
    c.setFillColor(BANYAN_L)
    c.rect(inner_l, y - TOTAL_H, inner_r - inner_l, TOTAL_H - 0.20 * inch,
           fill=1, stroke=0)
    c.setStrokeColor(BANYAN_D); c.setLineWidth(1.6)
    c.rect(inner_l, y - TOTAL_H, inner_r - inner_l, TOTAL_H - 0.20 * inch,
           fill=0, stroke=1)
    y = y - TOTAL_H - 0.04 * inch

    # --- 3 signature lines ---
    for label, jp_lbl in [
        ("JUDGE NAME  (print)",  "ジャッジ氏名"),
        ("JUDGE  (signature)",   "ジャッジ サイン"),
        ("ATHLETE  (signature)", "選手 サイン"),
    ]:
        c.setFillColor(MUTED); c.setFont("Helvetica-Bold", 7)
        c.drawString(inner_l, y - 0.10 * inch, label)
        c.setFillColor(HexColor("#888888")); c.setFont(JP, 6.5)
        c.drawRightString(inner_r, y - 0.10 * inch, jp_lbl)
        c.setStrokeColor(INK); c.setLineWidth(0.7)
        c.line(inner_l, y - SIG_H + 0.05 * inch, inner_r, y - SIG_H + 0.05 * inch)
        y -= SIG_H

# ============================================================
# FOOTER  (shaded band, inset within the outer frame)
# ============================================================
footer_top = page_bot + FOOTER_H - 0.05 * inch
c.setFillColor(GRAY_L)
c.rect(OUTER, page_bot, PAGE_W - 2*OUTER, FOOTER_H - 0.05 * inch,
       fill=1, stroke=0)
c.setStrokeColor(INK); c.setLineWidth(1.0)
c.line(OUTER, footer_top, PAGE_W - OUTER, footer_top)

c.setFillColor(INK); c.setFont("Helvetica-Bold", 8)
c.drawString(M, page_bot + 0.22 * inch,
             "Submit to the scoring table immediately after the heat.  "
             "Scores are final once signed.")
c.setFillColor(MUTED); c.setFont(JP, 8.5)
c.drawString(M, page_bot + 0.08 * inch,
             "ヒート終了後、速やかに採点テーブルへご提出ください。署名後のスコアは確定となります。")
c.setFillColor(INK); c.setFont("Helvetica-Bold", 9)
c.drawRightString(PAGE_W - M, page_bot + 0.15 * inch, "E1  ·  H1  ·  Scaled (F)")

# ============================================================
# OUTER FRAME  (drawn last, sits on top of everything)
# ============================================================
c.setStrokeColor(INK); c.setLineWidth(2.8)
c.rect(OUTER, OUTER, PAGE_W - 2*OUTER, PAGE_H - 2*OUTER,
       stroke=1, fill=0)

c.showPage()
c.save()
print("wrote", OUT)
