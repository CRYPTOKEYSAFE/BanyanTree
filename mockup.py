"""
Banyan Throwdown — bilingual heat-card mockup (single page).
Event 1 / Heat 1 / Scaled (F). Landscape Letter.
Design: deep shield-black header, cream body, banyan-green accents,
bronze hairlines, sunrise-orange event number.
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
LOGO = os.path.join(HERE, "logo.png")  # drop the real logo here

# Palette from the official Banyan Throwdown shield
SHIELD_BLK = HexColor("#0E1310")
BRONZE     = HexColor("#B8935A")
BANYAN     = HexColor("#3E7A3A")
LEAF_DK    = HexColor("#1F4D2B")
CREAM      = HexColor("#F3EFE6")
SUNRISE    = HexColor("#E88A2A")
INK        = HexColor("#111111")
MUTED      = HexColor("#6B6B6B")
HAIR       = HexColor("#B8935A")

PAGE_W, PAGE_H = landscape(letter)
MARGIN = 0.35 * inch

# Embed IPAGothic — clean Japanese gothic, embeds as a real TTF subset
pdfmetrics.registerFont(TTFont("IPAGothic", "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf"))
JP = "IPAGothic"

lanes = [
    ("1", "Megumi Iha"),
    ("2", "Takako Anderson"),
    ("3", "Megumi Nakagawa"),
    ("4", "Chiemi Matayoshi"),
    ("5", "Cassandra Cartwright"),
    ("6", "Lisa Miller"),
]

# (reps, English name, Japanese name)
movements = [
    ("50",  "Single-Unders",                                "シングルアンダー"),
    ("40",  "Medicine Ball Bear Hug Squats (20 / 14 lb)",   "メディシンボール・ベアハグスクワット"),
    ("30",  "Knee Raises",                                  "ニーレイズ"),
    ("20",  "Medicine Ball Overhead Walking Lunges (20 / 14 lb)",
                                                            "メディシンボール・オーバーヘッドランジ"),
    ("10",  "Jumping Pull-Ups",                             "ジャンピングプルアップ"),
]

c = canvas.Canvas(OUT, pagesize=landscape(letter))

# ---------- Top branding band ----------
band_h = 0.70 * inch
c.setFillColor(SHIELD_BLK)
c.rect(0, PAGE_H - band_h, PAGE_W, band_h, fill=1, stroke=0)
# bronze hairline
c.setStrokeColor(BRONZE)
c.setLineWidth(0.8)
c.line(0, PAGE_H - band_h - 2, PAGE_W, PAGE_H - band_h - 2)

# logo (left)
logo_w = 0.55 * inch
if os.path.exists(LOGO):
    c.drawImage(LOGO, MARGIN, PAGE_H - band_h + 0.075 * inch,
                width=logo_w, height=logo_w, mask="auto", preserveAspectRatio=True)
else:
    # placeholder monogram
    c.setStrokeColor(BRONZE); c.setLineWidth(1.2)
    c.rect(MARGIN, PAGE_H - band_h + 0.075 * inch, logo_w, logo_w, stroke=1, fill=0)
    c.setFillColor(BRONZE); c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(MARGIN + logo_w/2, PAGE_H - band_h + 0.28 * inch, "BT")

# wordmark
c.setFillColor(CREAM)
c.setFont("Helvetica-Bold", 22)
tx = MARGIN + logo_w + 0.18 * inch
c.drawString(tx, PAGE_H - band_h + 0.30 * inch, "BANYAN THROWDOWN")
c.setFillColor(BRONZE)
c.setFont(JP, 9)
c.drawString(tx, PAGE_H - band_h + 0.14 * inch, "バニヤン・スローダウン")

# right side of band
c.setFillColor(CREAM); c.setFont("Helvetica-Bold", 8)
c.drawRightString(PAGE_W - MARGIN, PAGE_H - band_h + 0.44 * inch, "OFFICIAL JUDGE SCORECARD")
c.setFillColor(BRONZE); c.setFont(JP, 7)
c.drawRightString(PAGE_W - MARGIN, PAGE_H - band_h + 0.30 * inch, "公式ジャッジ採点カード")
c.setFillColor(CREAM); c.setFont("Helvetica", 7)
c.drawRightString(PAGE_W - MARGIN, PAGE_H - band_h + 0.14 * inch, "4/25 (Sat)  ·  @banyanroots_fitness")

# ---------- Cream body ----------
body_top = PAGE_H - band_h - 2
c.setFillColor(CREAM)
c.rect(0, 0, PAGE_W, body_top, fill=1, stroke=0)

# ---------- Event meta row ----------
y = body_top - 0.40 * inch
c.setFillColor(SUNRISE); c.setFont("Helvetica-Bold", 26)
c.drawString(MARGIN, y - 0.05 * inch, "EVENT 1")
c.setFillColor(INK); c.setFont("Helvetica-Bold", 13)
c.drawString(MARGIN + 1.55 * inch, y - 0.03 * inch, "10-Minute AMRAP")
c.setFillColor(MUTED); c.setFont(JP, 9)
c.drawString(MARGIN + 1.55 * inch, y - 0.22 * inch, "10分間AMRAP")

# right meta blocks
meta = [("HEAT / ヒート", "1"), ("DIVISION / 部門", "Scaled (F)"), ("START / 開始", "9:00")]
block_w = 1.60 * inch
bx = PAGE_W - MARGIN - block_w * len(meta)
for label, val in meta:
    c.setFillColor(MUTED); c.setFont("Helvetica", 7)
    c.drawString(bx, y + 0.08 * inch, label)
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 15)
    c.drawString(bx, y - 0.14 * inch, val)
    bx += block_w

# divider
y -= 0.32 * inch
c.setStrokeColor(HAIR); c.setLineWidth(0.6)
c.line(MARGIN, y, PAGE_W - MARGIN, y)

# ---------- Workout panel ----------
wo_h = 1.45 * inch
wo_top = y - 0.05 * inch
c.setFillColor(white)
c.rect(MARGIN, wo_top - wo_h, PAGE_W - 2*MARGIN, wo_h, fill=1, stroke=0)
c.setStrokeColor(HAIR); c.setLineWidth(0.5)
c.rect(MARGIN, wo_top - wo_h, PAGE_W - 2*MARGIN, wo_h, stroke=1, fill=0)

c.setFillColor(BANYAN); c.setFont("Helvetica-Bold", 10)
c.drawString(MARGIN + 0.14 * inch, wo_top - 0.20 * inch,
             "WORKOUT — As many rounds as possible in 10 minutes of:")
c.setFillColor(MUTED); c.setFont(JP, 8)
c.drawString(MARGIN + 0.14 * inch, wo_top - 0.36 * inch,
             "ワークアウト — 10分間で以下の種目をできるだけ多くのラウンド繰り返す：")

row_y = wo_top - 0.58 * inch
for reps, en, jp in movements:
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN + 0.30 * inch, row_y, reps)
    c.setFont("Helvetica", 11)
    c.drawString(MARGIN + 0.70 * inch, row_y, en)
    c.setFillColor(MUTED); c.setFont(JP, 8)
    c.drawString(MARGIN + 0.70 * inch, row_y - 0.14 * inch, jp)
    row_y -= 0.32 * inch
# (panel slightly tight with 5 movements — this is intentional for mockup review)

# ---------- Lane grid ----------
grid_top = wo_top - wo_h - 0.15 * inch
grid_bottom = MARGIN + 0.05 * inch
n = len(lanes)
col_w = (PAGE_W - 2 * MARGIN) / n

head_h = 0.50 * inch
for i, (lane, name) in enumerate(lanes):
    x0 = MARGIN + i * col_w
    c.setFillColor(SHIELD_BLK)
    c.rect(x0, grid_top - head_h, col_w, head_h, fill=1, stroke=0)
    c.setFillColor(BRONZE); c.setFont("Helvetica-Bold", 8)
    c.drawString(x0 + 0.10 * inch, grid_top - 0.18 * inch, f"LANE {lane}  ·  レーン{lane}")
    c.setFillColor(CREAM); c.setFont("Helvetica-Bold", 11)
    c.drawString(x0 + 0.10 * inch, grid_top - 0.40 * inch, name)

body_hg = grid_top - head_h - grid_bottom
c.setStrokeColor(HAIR); c.setLineWidth(0.5)
c.rect(MARGIN, grid_bottom, PAGE_W - 2*MARGIN, grid_top - head_h - grid_bottom + head_h, stroke=1, fill=0)
for i in range(1, n):
    xv = MARGIN + i * col_w
    c.line(xv, grid_bottom, xv, grid_top - head_h)

# per-lane fields (en / jp)
fields = [
    ("ROUNDS / ラウンド",               0.32 * inch, False),
    ("EXTRA REPS / 追加レップ",         0.32 * inch, False),
    ("TOTAL REPS / 合計レップ",         0.44 * inch, True),
    ("TIEBREAK / タイブレーク",         0.32 * inch, False),
    ("JUDGE — PRINT / ジャッジ 氏名",   0.32 * inch, False),
    ("JUDGE — SIGN / ジャッジ サイン",  0.32 * inch, False),
    ("ATHLETE — SIGN / 選手 サイン",    0.32 * inch, False),
]

for i in range(n):
    x0 = MARGIN + i * col_w
    cy = grid_top - head_h - 0.02 * inch
    for label, h, emphasize in fields:
        cy -= h
        c.setFillColor(MUTED); c.setFont("Helvetica", 6)
        c.drawString(x0 + 0.08 * inch, cy + h - 0.12 * inch, label)
        lx1 = x0 + 0.08 * inch
        lx2 = x0 + col_w - 0.08 * inch
        ly = cy + 0.04 * inch
        if emphasize:
            c.setStrokeColor(BANYAN); c.setLineWidth(1.2)
            c.rect(lx1, ly, lx2 - lx1, h - 0.14 * inch, stroke=1, fill=0)
        else:
            c.setStrokeColor(HexColor("#A79A85")); c.setLineWidth(0.4)
            c.line(lx1, ly, lx2, ly)

# ---------- Footer ----------
c.setFillColor(MUTED); c.setFont("Helvetica", 6.5)
c.drawString(MARGIN, 0.20 * inch,
             "Submit to the scoring table immediately after the heat.  Scores are final once signed.")
c.setFont(JP, 6.5)
c.drawString(MARGIN, 0.09 * inch,
             "ヒート終了後すぐに採点テーブルへ提出してください。署名後のスコアは確定となります。")
c.setFont("Helvetica", 6.5)
c.drawRightString(PAGE_W - MARGIN, 0.20 * inch, "E1 · H1 · Scaled (F)")

c.showPage()
c.save()
print("wrote", OUT)
