"""
Banyan Tree Throwdown — heat card mockup (single page).
Lane-wise scorecard for Event 1, Heat 1, Scaled (F).
Landscape Letter, professional CrossFit competition aesthetic.
"""
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.pdfgen import canvas

OUT = "/home/user/BanyanTree/mockup.pdf"

BANYAN_GREEN = HexColor("#1F4D2B")
INK = HexColor("#111111")
RULE = HexColor("#333333")
MUTED = HexColor("#666666")
BG_TINT = HexColor("#F3EFE6")

PAGE_W, PAGE_H = landscape(letter)
MARGIN = 0.35 * inch

lanes = [
    ("1", "Megumi Iha"),
    ("2", "Takako Anderson"),
    ("3", "Megumi Nakagawa"),
    ("4", "Chiemi Matayoshi"),
    ("5", "Cassandra Cartwright"),
    ("6", "Lisa Miller"),
]

movements = [
    ("50",  "Single-Unders"),
    ("40",  "Medicine Ball Bear Hug Squats (20 / 14 lb)"),
    ("30",  "Knee Raises"),
    ("20",  "Medicine Ball Overhead Walking Lunges (20 / 14 lb)"),
    ("10",  "Jumping Pull-Ups"),
]

c = canvas.Canvas(OUT, pagesize=landscape(letter))

# ---------- Top branding stripe ----------
stripe_h = 0.55 * inch
c.setFillColor(BANYAN_GREEN)
c.rect(0, PAGE_H - stripe_h, PAGE_W, stripe_h, fill=1, stroke=0)

c.setFillColor(white)
c.setFont("Helvetica-Bold", 20)
c.drawString(MARGIN, PAGE_H - stripe_h + 0.17 * inch, "BANYAN TREE THROWDOWN")
c.setFont("Helvetica", 10)
c.drawRightString(PAGE_W - MARGIN, PAGE_H - stripe_h + 0.20 * inch, "OFFICIAL JUDGE SCORECARD")

# ---------- Meta row (Event / Heat / Division / Start) ----------
y = PAGE_H - stripe_h - 0.45 * inch
c.setFillColor(INK)
c.setFont("Helvetica-Bold", 22)
c.drawString(MARGIN, y, "EVENT 1")
c.setFont("Helvetica", 13)
c.setFillColor(MUTED)
c.drawString(MARGIN + 1.05 * inch, y + 2, "10-Minute AMRAP")

# right-side meta blocks
meta_items = [("HEAT", "1"), ("DIVISION", "Scaled (F)"), ("START", "9:00")]
block_w = 1.55 * inch
x = PAGE_W - MARGIN - block_w * len(meta_items)
for label, val in meta_items:
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawString(x, y + 14, label)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(x, y - 4, val)
    x += block_w

# horizontal rule
y -= 0.25 * inch
c.setStrokeColor(RULE)
c.setLineWidth(0.8)
c.line(MARGIN, y, PAGE_W - MARGIN, y)

# ---------- Workout box ----------
y -= 0.05 * inch
wo_h = 1.15 * inch
c.setFillColor(BG_TINT)
c.rect(MARGIN, y - wo_h, PAGE_W - 2 * MARGIN, wo_h, fill=1, stroke=0)

c.setFillColor(BANYAN_GREEN)
c.setFont("Helvetica-Bold", 10)
c.drawString(MARGIN + 0.12 * inch, y - 0.18 * inch, "WORKOUT  —  As many rounds as possible in 10 minutes of:")

c.setFillColor(INK)
c.setFont("Helvetica", 11)
row_y = y - 0.38 * inch
for reps, name in movements:
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN + 0.30 * inch, row_y, reps)
    c.setFont("Helvetica", 11)
    c.drawString(MARGIN + 0.70 * inch, row_y, name)
    row_y -= 0.16 * inch

y = y - wo_h - 0.18 * inch

# ---------- Lane grid ----------
grid_top = y
grid_bottom = MARGIN + 0.05 * inch
grid_h = grid_top - grid_bottom
n = len(lanes)
col_w = (PAGE_W - 2 * MARGIN) / n

# header band
head_h = 0.48 * inch
for i, (lane, name) in enumerate(lanes):
    x0 = MARGIN + i * col_w
    c.setFillColor(INK)
    c.rect(x0, grid_top - head_h, col_w, head_h, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x0 + 0.10 * inch, grid_top - 0.17 * inch, f"LANE {lane}")
    c.setFont("Helvetica-Bold", 12)
    # truncate long names
    disp = name if c.stringWidth(name, "Helvetica-Bold", 12) < col_w - 0.2*inch else name
    c.drawString(x0 + 0.10 * inch, grid_top - 0.38 * inch, disp)

# body
body_top = grid_top - head_h
body_h = body_top - grid_bottom

c.setStrokeColor(RULE)
c.setLineWidth(0.6)
# outer rect
c.rect(MARGIN, grid_bottom, PAGE_W - 2 * MARGIN, body_h, stroke=1, fill=0)
# vertical lane dividers
for i in range(1, n):
    x = MARGIN + i * col_w
    c.line(x, grid_bottom, x, body_top)

# per-lane scoring fields
field_labels = [
    ("ROUNDS COMPLETED", 0.34 * inch),
    ("EXTRA REPS", 0.34 * inch),
    ("TOTAL REPS", 0.44 * inch),
    ("TIEBREAK (time at 30 K/R)", 0.34 * inch),
    ("JUDGE  (print)", 0.34 * inch),
    ("JUDGE  (signature)", 0.34 * inch),
    ("ATHLETE  (signature)", 0.34 * inch),
]

for i in range(n):
    x0 = MARGIN + i * col_w
    cy = body_top - 0.06 * inch
    for label, h in field_labels:
        cy -= h
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 6.5)
        c.drawString(x0 + 0.08 * inch, cy + h - 0.12 * inch, label)
        # write line
        c.setStrokeColor(HexColor("#999999"))
        c.setLineWidth(0.4)
        lx1 = x0 + 0.08 * inch
        lx2 = x0 + col_w - 0.08 * inch
        ly = cy + 0.04 * inch
        c.line(lx1, ly, lx2, ly)
        # emphasize TOTAL REPS box
        if label == "TOTAL REPS":
            c.setStrokeColor(BANYAN_GREEN)
            c.setLineWidth(1.2)
            c.rect(lx1, ly, lx2 - lx1, h - 0.14 * inch, stroke=1, fill=0)

# ---------- Footer ----------
c.setFillColor(MUTED)
c.setFont("Helvetica", 7)
c.drawString(MARGIN, 0.20 * inch, "Submit this card to the scoring table immediately after the heat.  Scores are final once signed.")
c.drawRightString(PAGE_W - MARGIN, 0.20 * inch, "E1 / H1 / Scaled (F)")

c.showPage()
c.save()
print("wrote", OUT)
