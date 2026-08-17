#!/usr/bin/env python3
"""Rend un .md de synthese doctrinale en .pdf au style maison (noir + orange, serif).

Usage: python md-to-pdf.py <fichier.md> [sortie.pdf]
Couvre exactement les constructions presentes dans PrecisDicipulat.md :
titre (#), sous-titre (###), sections (##), citations (>), listes (-),
tableaux (|), gras (**), italique (*). Pas un parseur Markdown general.
"""
import re
import sys
import os

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak,
)

# Palette maison (extraite de 59 - Jacques/00 - Introduction/index.html)
INK    = HexColor("#1b1b1b")
BROWN  = HexColor("#7a4218")   # titres
ORANGE = HexColor("#e8843c")   # accents, filets
CREAM  = HexColor("#faf3ec")   # fond des encadres
MUTE   = HexColor("#8a7f72")   # byline, labels
RULE   = HexColor("#c9c2ba")

BYLINE = os.environ.get("MD2PDF_BYLINE", "21 juin 2026  ·  AGB  ·  EBC")

S = {
    "title":  ParagraphStyle("title", fontName="Times-Bold", fontSize=23, leading=27,
                             textColor=BROWN, alignment=TA_CENTER, spaceAfter=4),
    "sub":    ParagraphStyle("sub", fontName="Times-Italic", fontSize=12.5, leading=16,
                             textColor=INK, alignment=TA_CENTER, spaceAfter=6),
    "byline": ParagraphStyle("byline", fontName="Times-Roman", fontSize=9, leading=12,
                             textColor=MUTE, alignment=TA_CENTER, spaceAfter=2),
    "h2":     ParagraphStyle("h2", fontName="Times-Bold", fontSize=14.5, leading=18,
                             textColor=BROWN, spaceBefore=11, spaceAfter=4),
    "body":   ParagraphStyle("body", fontName="Times-Roman", fontSize=10.5, leading=15,
                             textColor=INK, alignment=TA_JUSTIFY, spaceAfter=6),
    "bullet": ParagraphStyle("bullet", fontName="Times-Roman", fontSize=10.5, leading=15,
                             textColor=INK, alignment=TA_JUSTIFY, leftIndent=16,
                             firstLineIndent=-11, spaceAfter=4),
    "quote":  ParagraphStyle("quote", fontName="Times-Roman", fontSize=10, leading=14.5,
                             textColor=INK, alignment=TA_JUSTIFY, spaceAfter=5),
    "th":     ParagraphStyle("th", fontName="Times-Bold", fontSize=9.5, leading=12,
                             textColor=BROWN),
    "td":     ParagraphStyle("td", fontName="Times-Roman", fontSize=9.5, leading=12.5,
                             textColor=INK),
}


def inline(text):
    """Echappe XML puis applique gras/italique. → hors WinAnsi, on le remplace."""
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = text.replace("→", "&gt;")  # ponytail: → absent de WinAnsi, rendu en >
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)
    return text


def callout(lines):
    """Encadre cream + barre orange a gauche (un paragraphe par ligne >)."""
    paras = [Paragraph(inline(l), S["quote"]) for l in lines]
    t = Table([[None, paras]], colWidths=[4, None])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), ORANGE),
        ("BACKGROUND", (1, 0), (1, -1), CREAM),
        ("LEFTPADDING", (0, 0), (0, -1), 0), ("RIGHTPADDING", (0, 0), (0, -1), 0),
        ("LEFTPADDING", (1, 0), (1, -1), 12), ("RIGHTPADDING", (1, 0), (1, -1), 12),
        ("TOPPADDING", (1, 0), (1, -1), 9), ("BOTTOMPADDING", (1, 0), (1, -1), 9),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def table(rows, width):
    header, body = rows[0], rows[1:]
    ncol = len(header)
    if header[0].strip() == "#":          # colonne numero etroite
        w0 = 0.05 * width
        cols = [w0] + [(width - w0) / (ncol - 1)] * (ncol - 1)
    else:
        cols = [width / ncol] * ncol
    data = [[Paragraph(inline(c), S["th"]) for c in header]]
    data += [[Paragraph(inline(c), S["td"]) for c in r] for r in body]
    t = Table(data, colWidths=cols, repeatRows=1)
    t.setStyle(TableStyle([
        ("LINEABOVE", (0, 0), (-1, 0), 1.2, BROWN),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, BROWN),
        ("LINEBELOW", (0, 1), (-1, -2), 0.25, RULE),
        ("LINEBELOW", (0, -1), (-1, -1), 0.8, BROWN),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def split_row(line):
    cells = line.strip().strip("|").split("|")
    return [c.strip() for c in cells]


def is_sep(line):
    return bool(re.match(r"^\s*\|[\s:\-|]+\|\s*$", line))


def build(md_path, pdf_path):
    raw = open(md_path, encoding="utf-8").read().splitlines()
    doc = SimpleDocTemplate(pdf_path, pagesize=letter,
                            leftMargin=0.5 * inch, rightMargin=0.5 * inch,
                            topMargin=0.5 * inch, bottomMargin=0.5 * inch)
    cw = doc.width
    story, i, first_h = [], 0, True
    while i < len(raw):
        line = raw[i].rstrip()
        if not line.strip():
            i += 1
            continue
        if line.startswith("# "):
            story.append(Paragraph(inline(line[2:]), S["title"]))
        elif line.startswith("### "):
            story.append(Paragraph(inline(line[4:]), S["sub"]))
            story.append(Spacer(1, 4))
            story.append(Paragraph(BYLINE, S["byline"]))
            story.append(HRFlowable(width="40%", thickness=0.8, color=ORANGE,
                                    spaceBefore=8, spaceAfter=4, hAlign="CENTER"))
        elif line.startswith("## "):
            story.append(Paragraph(inline(line[3:]), S["h2"]))
            story.append(HRFlowable(width="100%", thickness=0.8, color=ORANGE,
                                    spaceBefore=1, spaceAfter=6))
        elif line.strip() == "<!-- pagebreak -->":
            story.append(PageBreak())
        elif line.strip() == "---":
            pass  # les filets de section sont portes par les en-tetes
        elif line.startswith(">"):
            buf = []
            while i < len(raw) and raw[i].lstrip().startswith(">"):
                buf.append(raw[i].lstrip()[1:].strip())
                i += 1
            story.append(Spacer(1, 2)); story.append(callout(buf)); story.append(Spacer(1, 6))
            continue
        elif line.lstrip().startswith("|"):
            rows = []
            while i < len(raw) and raw[i].lstrip().startswith("|"):
                if not is_sep(raw[i]):
                    rows.append(split_row(raw[i]))
                i += 1
            story.append(Spacer(1, 2)); story.append(table(rows, cw)); story.append(Spacer(1, 8))
            continue
        elif line.startswith("- "):
            while i < len(raw) and raw[i].startswith("- "):
                story.append(Paragraph("•  " + inline(raw[i][2:]), S["bullet"]))
                i += 1
            continue
        else:
            story.append(Paragraph(inline(line), S["body"]))
        i += 1
    doc.build(story)


if __name__ == "__main__":
    src = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(src)[0] + ".pdf"
    build(src, out)
    print("PDF genere :", os.path.abspath(out))
