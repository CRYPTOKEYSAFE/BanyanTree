"""
Banyan Throwdown — judge heat card, v2.
Event 1 / Heat 1 / Scaled (F). Landscape US Letter.

Design goals:
- White paper, bold black ink, ONE accent color (banyan green).
- Bilingual only where it earns its place (wordmark, event title,
  workout heading and movement names, footer instruction).
- Tally area per lane — judges tick reps as they count.
- Explicit vertical geometry, no overlaps.
- Japanese (IPAGothic) never below 8pt.
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
INK     = HexColor("#111111")
MUTED   = HexColor("#6A6A6A")
HAIR    = HexColor("#DADADA")
BANYAN  = HexColor("#2E6B34")   # banyan green accent
BANYAN2 = HexColor("#1F4D2B")   # deep green for TOTAL box
ACCENT  = HexColor("#E07A1F")   # sunrise orange — used sparingly

pdfmetrics.registerFont(
    TTFont("IPAGothic", "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf")
)
JP = "IPAGothic"

PAGE_W, PAGE_H = landscape(letter)       # 11" x 8.5"
M = 0.40 * inch                          # page margin

lanes = [
    ("1", "Megumi Iha"),
    ("2", "Takako Anderson"),
    ("3", "Megumi Nakagawa"),
    ("4", "Chiemi Matayoshi"),
    ("5", "Cassandra Cartwright"),
    ("6", "Lisa Miller"),
]

# (reps, English, Japanese)
movements = [
    ("50",  "Single-Unders",                                "シングルアンダー"),
    ("40",  "Medicine Ball Bear Hug Squats (20 / 14 lb)",   "メディシンボール・ベアハグスクワット"),
    ("30",  "Knee Raises",                                  "ニーレイズ"),
    ("20",  "Medicine Ball Overhead Walking Lunges (20 / 14 lb)",
                                                            "メディシンボール・オーバーヘッドランジ"),
    ("10",  "Jumping Pull-Ups",                             "ジャンピングプルアップ"),
]

c = canvas.Canvas(OUT, pagesize=landscape(letter))
c.setStrokeColor(INK)

# ============================================================
# VERTICAL GEOMETRY  (computed top-down, all explicit)
# ============================================================
HEADER_H  = 0.70 * inch
META_H    = 0.55 * inch
WORKOUT_H = 1.85 * inch
GRID_TOP_GAP = 0.12 * inch
FOOTER_H  = 0.45 * inch

y_header_bottom   = PAGE_H - HEADER_H
y_meta_bottom     = y_header_bottom - META_H
y_workout_top     = y_meta_bottom - 0.05 * inch
y_workout_bottom  = y_workout_top - WORKOUT_H
y_grid_top        = y_workout_bottom - GRID_TOP_GAP
y_grid_bottom     = M + FOOTER_H

# ============================================================
# HEADER BAND
# ============================================================
c.setFillColor(INK)
c.rect(0, y_header_bottom, PAGE_W, HEADER_H, fill=1, stroke=0)
# thin banyan accent stripe along the bottom of the band
c.setFillColor(BANYAN)
c.rect(0, y_header_bottom - 0.06 * inch, PAGE_W, 0.06 * inch, fill=1, stroke=0)

# logo (or monogram placeholder)
logo_size = 0.55 * inch
lx = M
ly = y_header_bottom + (HEADER_H - logo_size) / 2
if os.path.exists(LOGO):
    c.drawImage(LOGO, lx, ly, width=logo_size, height=logo_size,
                mask="auto", preserveAspectRatio=True)
else:
    c.setStrokeColor(BANYAN); c.setLineWidth(1.2)
    c.rect(lx, ly, logo_size, logo_size, stroke=1, fill=0)
    c.setFillColor(BANYAN); c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(lx + logo_size/2, ly + 0.16 * inch, "BT")

# wordmark
wx = lx + logo_size + 0.20 * inch
c.setFillColor(white); c.setFont("Helvetica-Bold", 24)
c.drawString(wx, y_header_bottom + 0.30 * inch, "BANYAN THROWDOWN")
c.setFillColor(HexColor("#B8B8B8")); c.setFont(JP, 10)
c.drawString(wx, y_header_bottom + 0.13 * inch, "バニヤン・スローダウン")

# right side of header
c.setFillColor(white); c.setFont("Helvetica-Bold", 9)
c.drawRightString(PAGE_W - M, y_header_bottom + 0.42 * inch, "OFFICIAL JUDGE SCORECARD")
c.setFillColor(HexColor("#B8B8B8")); c.setFont(JP, 9)
c.drawRightString(PAGE_W - M, y_header_bottom + 0.27 * inch, "公式ジャッジ採点カード")
c.setFillColor(white); c.setFont("Helvetica", 8)
c.drawRightString(PAGE_W - M, y_header_bottom + 0.10 * inch,
                  "4/25 (Sat)  ·  @banyan_throwdown")

# ============================================================
# META ROW (Event title + heat/division/start)
# ============================================================
meta_y_mid = y_meta_bottom + META_H / 2

# Event number in orange
c.setFillColor(ACCENT); c.setFont("Helvetica-Bold", 28)
c.drawString(M, meta_y_mid - 0.14 * inch, "EVENT 1")

# Event subtitle (EN big, JP small below)
ex = M + 1.75 * inch
c.setFillColor(INK); c.setFont("Helvetica-Bold", 15)
c.drawString(ex, meta_y_mid + 0.02 * inch, "10-Minute AMRAP")
c.setFillColor(MUTED); c.setFont(JP, 9)
c.drawString(ex, meta_y_mid - 0.18 * inch, "10分間 AMRAP")

# Right meta blocks — EN labels only (universal)
meta = [("HEAT", "1"), ("DIVISION", "Scaled (F)"), ("START", "9:00")]
block_w = 1.50 * inch
bx = PAGE_W - M - block_w * len(meta)
for label, val in meta:
    c.setFillColor(MUTED); c.setFont("Helvetica-Bold", 7.5)
    c.drawString(bx, meta_y_mid + 0.14 * inch, label)
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 17)
    c.drawString(bx, meta_y_mid - 0.14 * inch, val)
    bx += block_w

# thin divider below meta
c.setStrokeColor(INK); c.setLineWidth(0.6)
c.line(M, y_meta_bottom, PAGE_W - M, y_meta_bottom)

# ============================================================
# WORKOUT PANEL
# ============================================================
c.setStrokeColor(INK); c.setLineWidth(0.8)
c.rect(M, y_workout_bottom, PAGE_W - 2*M, WORKOUT_H, stroke=1, fill=0)

# left edge accent
c.setFillColor(BANYAN)
c.rect(M, y_workout_bottom, 0.08 * inch, WORKOUT_H, fill=1, stroke=0)

# heading (bilingual)
tx = M + 0.25 * inch
c.setFillColor(INK); c.setFont("Helvetica-Bold", 11)
c.drawString(tx, y_workout_top - 0.22 * inch,
             "WORKOUT — As many rounds as possible in 10 minutes of:")
c.setFillColor(MUTED); c.setFont(JP, 9)
c.drawString(tx, y_workout_top - 0.40 * inch,
             "ワークアウト — 10分間、以下の種目を可能な限り繰り返す。")

# movement rows — explicit stack, 0.26" per movement (0.14" EN + 0.12" JP)
en_y = y_workout_top - 0.60 * inch
for reps, en, jp in movements:
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 12)
    c.drawString(tx + 0.05 * inch, en_y, reps)
    c.setFont("Helvetica", 11)
    c.drawString(tx + 0.55 * inch, en_y, en)
    c.setFillColor(MUTED); c.setFont(JP, 8)
    c.drawString(tx + 0.55 * inch, en_y - 0.13 * inch, jp)
    en_y -= 0.26 * inch

# ============================================================
# LANE GRID
# ============================================================
n = len(lanes)
col_w = (PAGE_W - 2*M) / n
grid_h = y_grid_top - y_grid_bottom

# outer border
c.setStrokeColor(INK); c.setLineWidth(0.8)
c.rect(M, y_grid_bottom, PAGE_W - 2*M, grid_h, stroke=1, fill=0)

# column head
head_h = 0.45 * inch
for i, (lane, name) in enumerate(lanes):
    x0 = M + i * col_w
    c.setFillColor(INK)
    c.rect(x0, y_grid_top - head_h, col_w, head_h, fill=1, stroke=0)
    c.setFillColor(HexColor("#CFCFCF")); c.setFont("Helvetica-Bold", 8)
    c.drawString(x0 + 0.10 * inch, y_grid_top - 0.16 * inch, f"LANE {lane}")
    c.setFillColor(white)
    # auto-shrink long names to fit col width
    max_w = col_w - 0.20 * inch
    fs = 12
    while fs > 8 and c.stringWidth(name, "Helvetica-Bold", fs) > max_w:
        fs -= 0.5
    c.setFont("Helvetica-Bold", fs)
    c.drawString(x0 + 0.10 * inch, y_grid_top - 0.36 * inch, name)

# vertical dividers for body
c.setStrokeColor(INK); c.setLineWidth(0.6)
for i in range(1, n):
    xv = M + i * col_w
    c.line(xv, y_grid_bottom, xv, y_grid_top - head_h)

# per-lane body: TALLY (big), ROUNDS, EXTRA, TOTAL (box), JUDGE sig, ATHLETE sig
body_top = y_grid_top - head_h
body_h   = body_top - y_grid_bottom
# budget (total ≈ body_h):
TALLY_H  = 1.00 * inch
NUM_H    = 0.32 * inch   # ROUNDS / EXTRA REPS row
TOTAL_H  = 0.50 * inch   # TOTAL (boxed)
SIG_H    = 0.32 * inch   # per signature line (3 lines)
# remainder distributed automatically

for i in range(n):
    x0 = M + i * col_w
    inner_l = x0 + 0.10 * inch
    inner_r = x0 + col_w - 0.10 * inch
    y = body_top - 0.05 * inch

    # TALLY area
    c.setFillColor(MUTED); c.setFont("Helvetica-Bold", 7)
    c.drawString(inner_l, y - 0.10 * inch, "TALLY")
    c.setFont(JP, 7.5)
    c.drawString(inner_l + 0.45 * inch, y - 0.10 * inch, "カウント")
    # light dotted grid inside tally box
    tb_top = y - 0.14 * inch
    tb_bot = tb_top - (TALLY_H - 0.18 * inch)
    c.setStrokeColor(HAIR); c.setLineWidth(0.4)
    c.rect(inner_l, tb_bot, inner_r - inner_l, tb_top - tb_bot, stroke=1, fill=0)
    # dot grid for tally marks — visible but not overpowering
    step = 0.14 * inch
    c.setFillColor(HexColor("#BFBFBF"))
    yy = tb_top - step
    while yy > tb_bot + 0.02 * inch:
        xx = inner_l + step
        while xx < inner_r - 0.02 * inch:
            c.circle(xx, yy, 0.55, stroke=0, fill=1)
            xx += step
        yy -= step

    y = tb_bot - 0.08 * inch

    # ROUNDS + EXTRA REPS side by side
    half = (inner_r - inner_l - 0.06 * inch) / 2
    c.setFillColor(MUTED); c.setFont("Helvetica-Bold", 7)
    c.drawString(inner_l, y - 0.10 * inch, "ROUNDS")
    c.drawString(inner_l + half + 0.06 * inch, y - 0.10 * inch, "EXTRA REPS")
    # boxes
    c.setStrokeColor(INK); c.setLineWidth(0.6)
    c.rect(inner_l, y - NUM_H, half, NUM_H - 0.12 * inch, stroke=1, fill=0)
    c.rect(inner_l + half + 0.06 * inch, y - NUM_H, half, NUM_H - 0.12 * inch,
           stroke=1, fill=0)
    y = y - NUM_H - 0.06 * inch

    # TOTAL REPS — emphasized green box
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 8)
    c.drawString(inner_l, y - 0.10 * inch, "TOTAL REPS")
    c.setStrokeColor(BANYAN2); c.setLineWidth(1.5)
    c.rect(inner_l, y - TOTAL_H, inner_r - inner_l, TOTAL_H - 0.14 * inch,
           stroke=1, fill=0)
    y = y - TOTAL_H - 0.04 * inch

    # three separate signature lines: judge name, judge sig, athlete sig
    for label in ("JUDGE NAME  (print)", "JUDGE  (signature)", "ATHLETE  (signature)"):
        c.setFillColor(MUTED); c.setFont("Helvetica-Bold", 7)
        c.drawString(inner_l, y - 0.10 * inch, label)
        c.setStrokeColor(HexColor("#888888")); c.setLineWidth(0.5)
        c.line(inner_l, y - SIG_H + 0.06 * inch, inner_r, y - SIG_H + 0.06 * inch)
        y -= SIG_H

# ============================================================
# FOOTER
# ============================================================
fy = M + 0.06 * inch
c.setFillColor(INK); c.setFont("Helvetica", 7.5)
c.drawString(M, fy + 0.18 * inch,
             "Submit to the scoring table immediately after the heat.  "
             "Scores are final once signed.")
c.setFillColor(MUTED); c.setFont(JP, 8)
c.drawString(M, fy + 0.04 * inch,
             "ヒート終了後、速やかに採点テーブルへご提出ください。署名後のスコアは確定となります。")
c.setFillColor(MUTED); c.setFont("Helvetica-Bold", 8)
c.drawRightString(PAGE_W - M, fy + 0.10 * inch, "E1 · H1 · Scaled (F)")

c.showPage()
c.save()
print("wrote", OUT)
