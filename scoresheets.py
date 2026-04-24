"""
Banyan Throwdown — full individual scorecard generator.
46 athletes × 4 events = 184 pages, portrait US Letter.
One athlete per page. Bilingual. Gender-tailored weights.
"""
import os
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "scoresheets.pdf")
LOGO = os.path.join(HERE, "logo.png")

# ----- palette (frozen from v4 mockup) -----
INK      = HexColor("#0E0E0E")
MUTED    = HexColor("#555555")
BANYAN   = HexColor("#2E6B34")
BANYAN_D = HexColor("#1F4D2B")
BANYAN_L = HexColor("#E6F0E5")
ACCENT   = HexColor("#E07A1F")
PAGE_BG  = HexColor("#ECE8DD")
GRAY_L   = HexColor("#E2DED1")
GRAPH    = HexColor("#BDB8A8")
WHITE_B  = HexColor("#FFFFFF")

pdfmetrics.registerFont(
    TTFont("IPAGothic", "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf"))
JP = "IPAGothic"

PAGE_W, PAGE_H = portrait(A4)  # 8.5 x 11
OUTER = 0.22 * inch
M     = 0.40 * inch

# ============================================================
# DATA: heats / lanes / athletes / divisions / times
# ============================================================
# Start time per (event, heat)
START = {
    (1,1): "9:00",   (1,2): "9:15",   (1,3): "9:30",   (1,4): "9:45",
    (1,5): "10:00",  (1,6): "10:15",  (1,7): "10:30",  (1,8): "10:45", (1,9): "11:00",
    (2,1): "11:30",  (2,2): "11:45",  (2,3): "12:00",  (2,4): "12:15",
    (2,5): "12:30",  (2,6): "12:45",  (2,7): "13:00",  (2,8): "13:15", (2,9): "13:30",
    (3,1): "14:30",  (3,2): "14:35",  (3,3): "14:40",  (3,4): "14:45",
    (3,5): "14:50",  (3,6): "14:55",  (3,7): "15:00",  (3,8): "15:05", (3,9): "15:10",
    (4,1): "15:40",  (4,2): "15:50",  (4,3): "16:00",  (4,4): "16:10",
    (4,5): "16:20",  (4,6): "16:30",  (4,7): "16:40",  (4,8): "16:50", (4,9): "17:00",
}

# Division per heat (same across all 4 events)
DIV = {
    1: "Scaled (F)", 2: "Scaled (F)",
    3: "Scaled (M)", 4: "Scaled (M)",
    5: "RX (F)",
    6: "RX (M)", 7: "RX (M)", 8: "RX (M)", 9: "RX (M)",
}

# Roster: heat -> list of (lane, name) in lane order
ROSTER = {
    1: [("1","Megumi Iha"),("2","Takako Anderson"),("3","Megumi Nakagawa"),
        ("4","Chiemi Matayoshi"),("5","Cassandra Cartwright"),("6","Lisa Miller")],
    2: [("1","Ashley Lawson"),("2","Joanna Morla"),("3","Sae Maehara"),
        ("4","Destinee Byrd"),("5","Chinaeme Ozobu")],
    3: [("1","Soho Aka"),("2","Satoshi Inafuku"),("3","Hikaru Kato"),
        ("4","Naoto Yamazaki"),("5","Yoshitomo Uehara")],
    4: [("1","Masataka Chikamura"),("2","Takumi Goya"),
        ("3","Kiyofumi Suzuki"),("4","Ryu Ariano")],
    5: [("1","Rebecca Gass"),("2","Kanako Kambara"),("3","Chinami Cobb"),
        ("4","Courtney Carter"),("5","Emily Chism")],
    6: [("1","Kouki Ishimine"),("2","Yuma Tamaki"),("3","Sho Maezawa"),
        ("4","Hirotaka Sunagawa"),("5","Takahiro Suzuki")],
    7: [("1","Akinari Mekaru"),("2","Chen ChunHao"),("3","Masaki Miyagi"),
        ("4","Hiroki Nakasone"),("5","Blake Roy")],
    8: [("1","Zen Miyazato"),("2","Ryo Takaesu"),("3","Yoji Ozawa"),
        ("4","Yuya Sawa"),("5","Josh Imel")],
    9: [("1","Daiki Shimoji"),("2","Brandon Kroll"),("3","Tomoaki Matsuyama"),
        ("4","Alejandro Fierro"),("5","JJ Vantonder"),("6","Blayne Butler")],
}

def gender(div):      return "M" if "(M)" in div else "F"
def scaled_or_rx(div): return "Scaled" if div.startswith("Scaled") else "RX"

# ============================================================
# WORKOUTS — returns title, subtitle_jp, list of (reps, en, jp) rows,
# and format_hint ("amrap", "amrap+1rm", "fortime", "fortime_cap")
# ============================================================
def workout(event, div):
    rx = scaled_or_rx(div) == "RX"
    g  = gender(div)
    if event == 1:
        if rx:
            rows = [
                ("50",  "Double-Unders",                                 "ダブルアンダー"),
                ("40",  "Wall Ball Shots (20 lb)",                       "ウォールボール (20 lb)"),
                ("30",  "Toes-to-Bar",                                   "トゥーズトゥーバー"),
                ("20",  "Dumbbell Overhead Walking Lunges (50 lb)",      "ダンベル・オーバーヘッドランジ (50 lb)"),
                ("10",  "Bar Muscle-Ups",                                "バーマッスルアップ"),
            ]
        else:
            mb = "20 lb" if g == "M" else "14 lb"
            rows = [
                ("50",  "Single-Unders",                                 "シングルアンダー"),
                ("40",  f"Medicine Ball Bear Hug Squats ({mb})",         f"メディシンボール・ベアハグスクワット ({mb})"),
                ("30",  "Knee Raises",                                   "ニーレイズ"),
                ("20",  f"Medicine Ball Overhead Walking Lunges ({mb})", f"メディシンボール・オーバーヘッドランジ ({mb})"),
                ("10",  "Jumping Pull-Ups",                              "ジャンピングプルアップ"),
            ]
        return "10-Minute AMRAP", "10分間 AMRAP", rows, "amrap"

    if event == 2:
        if rx:
            db  = "50 lb" if g == "M" else "35 lb"
            box = '24"' if g == "M" else '20"'
            a1  = [("A1","2-Minute AMRAP","2分間 AMRAP"),
                   ("—",  f"Dumbbell Box Step-Overs ({db}, {box})",
                          f"ダンベル・ボックスステップオーバー ({db}, {box})")]
        else:
            mb  = "20 lb" if g == "M" else "14 lb"
            box = '24"' if g == "M" else '20"'
            a1  = [("A1","2-Minute AMRAP","2分間 AMRAP"),
                   ("—",  f"Medicine Ball Box Step-Overs ({mb}, {box})",
                          f"メディシンボール・ボックスステップオーバー ({mb}, {box})")]
        rest = [("—", "Rest 2 Minutes", "休憩 2分")]
        a2   = [("A2","6-Minute Window","6分間"),
                ("—",  "Build to 1-Rep Max Hang Clean & Jerk",
                       "ハングクリーン&ジャーク 1RM（6分間で最大重量）")]
        return "Two-Part Event", "2パート構成", a1 + rest + a2, "amrap+1rm"

    if event == 3:
        row_m = "500 m Row" if g == "M" else "400 m Row"
        row_j = "ローイング 500 m" if g == "M" else "ローイング 400 m"
        rows = [
            ("20", "Burpees Over the Rower",  "バーピー・オーバー・ローイング"),
            ("—",  row_m,                      row_j),
        ]
        return "For Time", "タイム制", rows, "fortime"

    if event == 4:
        if rx:
            dl  = "225 lb" if g == "M" else "155 lb"
            rows = [
                ("15", "Handstand Push-Ups",                            "ハンドスタンドプッシュアップ"),
                ("9",  f"Deadlifts ({dl})",                             f"デッドリフト ({dl})"),
                ("12", "Handstand Push-Ups",                            "ハンドスタンドプッシュアップ"),
                ("12", f"Deadlifts ({dl})",                             f"デッドリフト ({dl})"),
                ("9",  "Handstand Push-Ups",                            "ハンドスタンドプッシュアップ"),
                ("15", f"Deadlifts ({dl})",                             f"デッドリフト ({dl})"),
            ]
        else:
            dl  = "135 lb" if g == "M" else "85 lb"
            rows = [
                ("15", "Hand-Release Push-Ups",                         "ハンドリリースプッシュアップ"),
                ("9",  f"Deadlifts ({dl})",                             f"デッドリフト ({dl})"),
                ("12", "Hand-Release Push-Ups",                         "ハンドリリースプッシュアップ"),
                ("12", f"Deadlifts ({dl})",                             f"デッドリフト ({dl})"),
                ("9",  "Hand-Release Push-Ups",                         "ハンドリリースプッシュアップ"),
                ("15", f"Deadlifts ({dl})",                             f"デッドリフト ({dl})"),
            ]
        return "For Time  ·  5-Minute Cap", "タイム制 ・ 制限時間5分", rows, "fortime_cap"
    raise ValueError(event)

# ============================================================
# VERTICAL GEOMETRY  (budgeted, asserted)
# ============================================================
HEADER_H   = 0.82 * inch
EVENT_H    = 0.50 * inch
ATHLETE_H  = 1.15 * inch
WORKOUT_H  = 2.35 * inch
SCORE_H    = 3.00 * inch
SIG_H      = 1.05 * inch
FOOTER_H   = 0.45 * inch
GAP        = 0.08 * inch

def verify_budget():
    used = (HEADER_H + EVENT_H + ATHLETE_H + WORKOUT_H + SCORE_H
            + SIG_H + FOOTER_H + 6 * GAP + 2 * OUTER)
    avail = PAGE_H
    assert used <= avail, f"budget overflow: used={used:.2f} avail={avail:.2f}"
    print(f"budget OK: used={used:.2f}in of {avail:.2f}in  (slack {avail-used:.2f})")

# ============================================================
# DRAW ONE CARD
# ============================================================
def draw_card(c, event, heat, lane, name, division, start):
    # page bg
    c.setFillColor(PAGE_BG)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    page_top = PAGE_H - OUTER
    page_bot = OUTER
    cur_y = page_top

    # ---- HEADER BAND ----
    c.setFillColor(INK)
    c.rect(OUTER, cur_y - HEADER_H, PAGE_W - 2*OUTER, HEADER_H, fill=1, stroke=0)
    c.setFillColor(BANYAN)
    c.rect(OUTER, cur_y - HEADER_H - 0.07*inch, PAGE_W - 2*OUTER, 0.07*inch,
           fill=1, stroke=0)

    # logo or monogram
    lsize = 0.60 * inch
    lx = OUTER + 0.15 * inch
    ly = cur_y - HEADER_H + (HEADER_H - lsize) / 2
    if os.path.exists(LOGO):
        c.drawImage(LOGO, lx, ly, width=lsize, height=lsize,
                    mask="auto", preserveAspectRatio=True)
    else:
        c.setStrokeColor(BANYAN); c.setLineWidth(2)
        c.rect(lx, ly, lsize, lsize, stroke=1, fill=0)
        c.setFillColor(BANYAN); c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(lx + lsize/2, ly + 0.20*inch, "BT")

    wx = lx + lsize + 0.22 * inch
    c.setFillColor(white); c.setFont("Helvetica-Bold", 22)
    c.drawString(wx, cur_y - 0.36*inch, "BANYAN THROWDOWN")
    c.setFillColor(HexColor("#CFCFCF")); c.setFont(JP, 10)
    c.drawString(wx, cur_y - 0.54*inch, "バニヤン・スローダウン")

    c.setFillColor(white); c.setFont("Helvetica-Bold", 9)
    c.drawRightString(PAGE_W - OUTER - 0.15*inch, cur_y - 0.30*inch,
                      "OFFICIAL JUDGE SCORECARD")
    c.setFillColor(HexColor("#CFCFCF")); c.setFont(JP, 8)
    c.drawRightString(PAGE_W - OUTER - 0.15*inch, cur_y - 0.47*inch,
                      "公式ジャッジ採点カード")
    c.setFillColor(ACCENT); c.setFont("Helvetica-Bold", 8)
    c.drawRightString(PAGE_W - OUTER - 0.15*inch, cur_y - 0.63*inch,
                      "4/25 (Sat)  ·  @banyan_throwdown")

    cur_y -= HEADER_H + GAP

    # ---- EVENT TITLE ROW ----
    title_en, title_jp, rows, fmt = workout(event, division)
    c.setFillColor(ACCENT); c.setFont("Helvetica-Bold", 30)
    event_label = f"EVENT {event}"
    c.drawString(M, cur_y - 0.35*inch, event_label)
    subtitle_x = M + c.stringWidth(event_label, "Helvetica-Bold", 30) + 0.25*inch
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 15)
    c.drawString(subtitle_x, cur_y - 0.20*inch, title_en)
    c.setFillColor(MUTED); c.setFont(JP, 10)
    c.drawString(subtitle_x, cur_y - 0.38*inch, title_jp)
    # start time right-aligned
    c.setFillColor(MUTED); c.setFont("Helvetica-Bold", 8)
    c.drawRightString(PAGE_W - M, cur_y - 0.12*inch, "START TIME")
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 22)
    c.drawRightString(PAGE_W - M, cur_y - 0.38*inch, start)
    cur_y -= EVENT_H + GAP
    # divider
    c.setStrokeColor(INK); c.setLineWidth(1.0)
    c.line(OUTER, cur_y + GAP/2, PAGE_W - OUTER, cur_y + GAP/2)

    # ---- ATHLETE BLOCK (big name, lane/heat/division tiles) ----
    c.setFillColor(WHITE_B); c.setStrokeColor(INK); c.setLineWidth(1.2)
    c.rect(M, cur_y - ATHLETE_H, PAGE_W - 2*M, ATHLETE_H, fill=1, stroke=1)
    # banyan tab on top
    c.setFillColor(BANYAN_D)
    c.rect(M, cur_y - 0.26*inch, PAGE_W - 2*M, 0.26*inch, fill=1, stroke=0)
    c.setFillColor(white); c.setFont("Helvetica-Bold", 9)
    c.drawString(M + 0.15*inch, cur_y - 0.18*inch, "ATHLETE  /  選手")
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(PAGE_W - M - 0.15*inch, cur_y - 0.18*inch,
                      f"HEAT {heat}  ·  LANE {lane}  ·  {division}")

    # auto-size name to fit
    max_w = PAGE_W - 2*M - 0.40*inch
    fs = 34
    while fs > 18 and c.stringWidth(name, "Helvetica-Bold", fs) > max_w:
        fs -= 0.5
    c.setFillColor(INK); c.setFont("Helvetica-Bold", fs)
    c.drawString(M + 0.22*inch, cur_y - ATHLETE_H + 0.30*inch, name)

    cur_y -= ATHLETE_H + GAP

    # ---- WORKOUT PANEL ----
    # green header strip
    wh_h = 0.32 * inch
    c.setFillColor(BANYAN_D)
    c.rect(M, cur_y - wh_h, PAGE_W - 2*M, wh_h, fill=1, stroke=0)
    c.setFillColor(white); c.setFont("Helvetica-Bold", 10)
    c.drawString(M + 0.15*inch, cur_y - 0.20*inch,
                 "WORKOUT  /  ワークアウト")
    c.setFont(JP, 9)
    c.drawRightString(PAGE_W - M - 0.15*inch, cur_y - 0.20*inch, title_jp)

    body_t = cur_y - wh_h
    body_b = cur_y - WORKOUT_H
    c.setFillColor(WHITE_B); c.setStrokeColor(INK); c.setLineWidth(1.0)
    c.rect(M, body_b, PAGE_W - 2*M, body_t - body_b, fill=1, stroke=1)

    # movement rows
    n_rows = len(rows)
    row_top = body_t - 0.18*inch
    row_h = min(0.32*inch, (body_t - body_b - 0.20*inch) / n_rows)
    for reps, en, jp in rows:
        c.setFillColor(INK); c.setFont("Helvetica-Bold", 13)
        c.drawString(M + 0.25*inch, row_top - 0.02*inch, reps)
        c.setFont("Helvetica", 12)
        c.drawString(M + 0.80*inch, row_top - 0.02*inch, en)
        c.setFillColor(MUTED); c.setFont(JP, 9)
        c.drawString(M + 0.80*inch, row_top - 0.18*inch, jp)
        row_top -= row_h

    cur_y -= WORKOUT_H + GAP

    # ---- SCORING ZONE (event-specific) ----
    draw_score(c, cur_y, SCORE_H, fmt)
    cur_y -= SCORE_H + GAP

    # ---- SIGNATURES ----
    c.setFillColor(WHITE_B); c.setStrokeColor(INK); c.setLineWidth(1.0)
    c.rect(M, cur_y - SIG_H, PAGE_W - 2*M, SIG_H, fill=1, stroke=1)
    slots = [("JUDGE — PRINTED NAME",  "ジャッジ 氏名"),
             ("JUDGE — SIGNATURE",     "ジャッジ サイン"),
             ("ATHLETE — SIGNATURE",   "選手 サイン")]
    sy = cur_y - 0.22*inch
    slot_h = SIG_H / 3
    for en, jp in slots:
        c.setFillColor(MUTED); c.setFont("Helvetica-Bold", 8)
        c.drawString(M + 0.20*inch, sy, en)
        c.setFont(JP, 7.5)
        c.drawRightString(PAGE_W - M - 0.20*inch, sy, jp)
        c.setStrokeColor(INK); c.setLineWidth(0.7)
        c.line(M + 0.20*inch, sy - 0.20*inch, PAGE_W - M - 0.20*inch, sy - 0.20*inch)
        sy -= slot_h

    cur_y -= SIG_H + GAP

    # ---- FOOTER ----
    c.setFillColor(GRAY_L)
    c.rect(OUTER, page_bot, PAGE_W - 2*OUTER, FOOTER_H - 0.04*inch,
           fill=1, stroke=0)
    c.setStrokeColor(INK); c.setLineWidth(0.8)
    c.line(OUTER, page_bot + FOOTER_H - 0.04*inch,
           PAGE_W - OUTER, page_bot + FOOTER_H - 0.04*inch)
    c.setFillColor(INK); c.setFont("Helvetica", 7.5)
    c.drawString(M, page_bot + 0.22*inch,
                 "Submit to the scoring table immediately after the heat.  "
                 "Scores are final once signed.")
    c.setFillColor(MUTED); c.setFont(JP, 7.5)
    c.drawString(M, page_bot + 0.09*inch,
                 "ヒート終了後、速やかに採点テーブルへご提出ください。署名後のスコアは確定となります。")
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 8)
    c.drawRightString(PAGE_W - M, page_bot + 0.15*inch,
                      f"E{event}  ·  H{heat}  ·  L{lane}  ·  {division}")

    # ---- OUTER FRAME ----
    c.setStrokeColor(INK); c.setLineWidth(2.6)
    c.rect(OUTER, OUTER, PAGE_W - 2*OUTER, PAGE_H - 2*OUTER,
           stroke=1, fill=0)

    c.showPage()


def draw_score(c, top_y, height, fmt):
    """Scoring zone, variant per event."""
    left = M
    right = PAGE_W - M
    # outer box with banyan header strip
    sh_h = 0.32*inch
    c.setFillColor(BANYAN_D)
    c.rect(left, top_y - sh_h, right - left, sh_h, fill=1, stroke=0)
    c.setFillColor(white); c.setFont("Helvetica-Bold", 10)
    c.drawString(left + 0.15*inch, top_y - 0.20*inch,
                 "SCORE  /  スコア記入欄")
    # body
    b_t = top_y - sh_h
    b_b = top_y - height
    c.setFillColor(WHITE_B); c.setStrokeColor(INK); c.setLineWidth(1.0)
    c.rect(left, b_b, right - left, b_t - b_b, fill=1, stroke=1)

    if fmt == "amrap":
        # big tally box on left + rounds/extra/total stacked on right
        gutter = 0.15*inch
        right_w = 2.5*inch
        tally_l = left + 0.15*inch
        tally_r = right - right_w - gutter
        tally_t = b_t - 0.15*inch
        tally_b = b_b + 0.20*inch
        # label
        c.setFillColor(INK); c.setFont("Helvetica-Bold", 9)
        c.drawString(tally_l, tally_t + 0.01*inch, "TALLY")
        c.setFillColor(MUTED); c.setFont(JP, 8)
        c.drawString(tally_l + 0.55*inch, tally_t + 0.01*inch, "カウント")
        # graph-paper grid
        c.setStrokeColor(GRAPH); c.setLineWidth(0.35)
        step = 0.17*inch
        yy = tally_t - 0.05*inch
        while yy > tally_b + 0.02*inch:
            c.line(tally_l, yy, tally_r, yy); yy -= step
        xx = tally_l + step
        while xx < tally_r - 0.02*inch:
            c.line(xx, tally_t - 0.05*inch, xx, tally_b + 0.02*inch); xx += step
        c.setStrokeColor(INK); c.setLineWidth(1.0)
        c.rect(tally_l, tally_b, tally_r - tally_l, tally_t - 0.05*inch - tally_b,
               stroke=1, fill=0)

        # right column: ROUNDS / EXTRA REPS / TOTAL REPS
        rx = tally_r + gutter
        rw = right - 0.15*inch - rx
        field_top = b_t - 0.15*inch
        # ROUNDS
        _field_box(c, rx, field_top, rw, 0.70*inch, "ROUNDS COMPLETED",
                   "完了ラウンド", huge=True)
        field_top -= 0.80*inch
        _field_box(c, rx, field_top, rw, 0.70*inch, "EXTRA REPS",
                   "追加レップ", huge=True)
        field_top -= 0.80*inch
        _field_box(c, rx, field_top, rw, 0.80*inch, "TOTAL REPS",
                   "合計レップ", emphasize=True, huge=True)

    elif fmt == "amrap+1rm":
        # left: A1 reps box; right: A2 1RM weight box
        col_gap = 0.18*inch
        col_w = (right - left - col_gap - 0.30*inch) / 2
        lx = left + 0.15*inch; rx = lx + col_w + col_gap
        # A1 header
        _field_box(c, lx, b_t - 0.15*inch, col_w, 2.25*inch,
                   "A1 — BOX STEP-OVER REPS (2 min)",
                   "A1 ステップオーバー レップ (2分)",
                   emphasize=True, huge=True)
        _field_box(c, rx, b_t - 0.15*inch, col_w, 2.25*inch,
                   "A2 — 1RM HANG CLEAN & JERK  (lb)",
                   "A2 1RM ハングクリーン&ジャーク（lb）",
                   emphasize=True, huge=True)

    elif fmt == "fortime":
        col_gap = 0.18*inch
        col_w = (right - left - col_gap - 0.30*inch) / 2
        lx = left + 0.15*inch; rx = lx + col_w + col_gap
        _field_box(c, lx, b_t - 0.15*inch, col_w, 2.25*inch,
                   "FINISH TIME  (mm:ss)",
                   "タイム (分:秒)",
                   emphasize=True, huge=True)
        _field_box(c, rx, b_t - 0.15*inch, col_w, 2.25*inch,
                   "IF DNF — REPS COMPLETED",
                   "時間内未完の場合 — 完了レップ数",
                   huge=True)

    elif fmt == "fortime_cap":
        col_gap = 0.18*inch
        col_w = (right - left - col_gap - 0.30*inch) / 2
        lx = left + 0.15*inch; rx = lx + col_w + col_gap
        _field_box(c, lx, b_t - 0.15*inch, col_w, 2.25*inch,
                   "FINISH TIME  (mm:ss — cap 5:00)",
                   "タイム (分:秒 — 制限5:00)",
                   emphasize=True, huge=True)
        _field_box(c, rx, b_t - 0.15*inch, col_w, 2.25*inch,
                   "IF CAPPED — TOTAL REPS DONE",
                   "制限時間終了時 — 合計レップ数",
                   huge=True)


def _field_box(c, x, y_top, w, h, label_en, label_jp,
               emphasize=False, huge=False):
    """Draw a labeled score-entry box."""
    # label
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 8.5)
    c.drawString(x, y_top - 0.10*inch, label_en)
    c.setFillColor(MUTED); c.setFont(JP, 7.5)
    c.drawString(x, y_top - 0.22*inch, label_jp)
    # box
    box_y = y_top - h
    if emphasize:
        c.setFillColor(BANYAN_L)
        c.rect(x, box_y, w, h - 0.28*inch, fill=1, stroke=0)
        c.setStrokeColor(BANYAN_D); c.setLineWidth(1.6)
    else:
        c.setFillColor(WHITE_B)
        c.rect(x, box_y, w, h - 0.28*inch, fill=1, stroke=0)
        c.setStrokeColor(INK); c.setLineWidth(1.0)
    c.rect(x, box_y, w, h - 0.28*inch, fill=0, stroke=1)


# ============================================================
# RENDER
# ============================================================
def main():
    verify_budget()
    c = canvas.Canvas(OUT, pagesize=portrait(A4))
    c.setTitle("Banyan Throwdown — Judge Scorecards")
    c.setAuthor("Anthony")
    count = 0
    for event in (1, 2, 3, 4):
        for heat in range(1, 10):
            division = DIV[heat]
            start    = START[(event, heat)]
            for lane, name in ROSTER[heat]:
                draw_card(c, event, heat, lane, name, division, start)
                count += 1
    c.save()
    print(f"wrote {OUT}  pages={count}")
    assert count == 184, f"expected 184 pages, got {count}"

if __name__ == "__main__":
    main()
