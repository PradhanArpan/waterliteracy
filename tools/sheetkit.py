"""Shared styles and helpers for the practice workbooks."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule

F = "Arial"
TITLE = Font(name=F, size=15, bold=True, color="13234A")
H = Font(name=F, size=10, bold=True, color="FFFFFF")
B = Font(name=F, size=10)
BOLD = Font(name=F, size=10, bold=True)
NOTE = Font(name=F, size=9, italic=True, color="6B6B6B")
INP = Font(name=F, size=11, bold=True, color="0000FF")
HEAD = PatternFill("solid", fgColor="13234A")
YEL = PatternFill("solid", fgColor="FFF2CC")
GRN = PatternFill("solid", fgColor="E2EFDA")
thin = Side(style="thin", color="BFBFBF")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
WRAP = Alignment(wrap_text=True, vertical="top")
MAXR = 20000
REGISTRY = []          # (sheet, answer cell, kind, answer) for automated testing          # formula ranges reach this row so learners can paste longer records


def hdr(ws, row, labels, col=1):
    for i, t in enumerate(labels):
        c = ws.cell(row=row, column=col + i, value=t)
        c.font, c.fill, c.border = H, HEAD, BOX
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)


def put(ws, ref, v, font=B, fill=None, fmt=None, wrap=False):
    c = ws[ref]; c.value = v; c.font = font; c.border = BOX
    if fill: c.fill = fill
    if fmt: c.number_format = fmt
    if wrap: c.alignment = WRAP
    return c


def text(ws, ref, v, font=B):
    c = ws[ref]; c.value = v; c.font = font; c.alignment = WRAP


def widths(ws, w):
    for col, x in w.items(): ws.column_dimensions[col].width = x


def check_style(ws, rng):
    first = rng.split(":")[0]
    ws.conditional_formatting.add(rng, FormulaRule(formula=[f'LEFT({first},1)="✓"'], fill=GRN, font=Font(name=F, bold=True, color="2E7D32")))
    ws.conditional_formatting.add(rng, FormulaRule(formula=[f'LEFT({first},1)="✗"'], fill=PatternFill("solid", fgColor="FDE2E1"), font=Font(name=F, bold=True, color="B71C1C")))


def num_check(cell, answer, tol="0.02"):
    return f'=IF({cell}="","",IF(ABS({cell}-({answer}))<=MAX(ABS({answer})*{tol},0.01),"✓ Correct","✗ Try again"))'


def txt_check(cell, answer):
    ans = answer if answer.startswith("=") is False else answer[1:]
    target = f'"{ans}"' if not answer.startswith("=") else ans
    return f'=IF(OR({cell}="",{cell}="choose"),"",IF({cell}={target},"✓ Correct","✗ Try again"))'


def dv_list(ws, cells, options):
    dv = DataValidation(type="list", formula1='"' + ",".join(options) + '"', allow_blank=True)
    ws.add_data_validation(dv)
    for c in cells: dv.add(c)


def start_sheet(wb, title, lines):
    ws = wb.active; ws.title = "Start here"
    widths(ws, {"A": 3, "B": 105})
    text(ws, "B2", title, TITLE)
    text(ws, "B3", "Hydroinformatics in a Changing Climate: Water Data Literacy for All · CuX, CHRIST (Deemed to be University)", NOTE)
    base = [("How to use this workbook", BOLD),
            ("This is the spreadsheet version of this module's practice activities. Same data, same questions and same answers as the Colab practice notebooks.", B),
            ("1. Go to File → Make a copy so you have your own version.", B),
            ("2. Type or choose your answers in the YELLOW cells with blue text. The CHECK column shows ✓ (correct) or ✗ (try again).", B),
            ("3. Green cells are calculated by formulas. Click one to see how it is worked out.", B)]
    for i, (t, f) in enumerate(base + [("", B)] + lines):
        text(ws, f"B{5+i}", t, f)
    return ws


def questions(ws, row, items, col_letters=("B", "C", "D", "E"), hint_col=None):
    """items: (label, question, kind, answer, options_or_None, fmt, hint). kind 'num' or 'txt'.
    answer: Excel expression for 'num'; text (or '=expr') for 'txt'. Returns next free row."""
    q, t, a, c = col_letters
    hdr(ws, row, ["#", "Question", "Your answer", "Check"] + (["Hint"] if hint_col else []), col=ord(q) - 64)
    r0 = row + 1
    for i, (lab, question, kind, ans, opts, fmt, hint) in enumerate(items):
        r = r0 + i
        put(ws, f"{q}{r}", lab, BOLD); put(ws, f"{t}{r}", question, wrap=True)
        put(ws, f"{a}{r}", None, INP, YEL, fmt)
        REGISTRY.append((ws.title, f"{a}{r}", kind, ans))
        if kind == "num":
            put(ws, f"{c}{r}", num_check(f"{a}{r}", ans, "0.02" if fmt not in ("0", "#,##0") else "0"), BOLD)
        else:
            put(ws, f"{c}{r}", txt_check(f"{a}{r}", ans), BOLD)
            dv_list(ws, [f"{a}{r}"], opts)
        if hint_col and hint:
            put(ws, f"{hint_col}{r}", hint, NOTE, wrap=True)
        ws.row_dimensions[r].height = 32
    last = r0 + len(items) - 1
    put(ws, f"{t}{last+1}", f"Score (out of {len(items)})", BOLD)
    put(ws, f"{c}{last+1}", f'=COUNTIF({c}{r0}:{c}{last},"✓*")', BOLD, GRN)
    check_style(ws, f"{c}{r0}:{c}{last}")
    return last + 3
