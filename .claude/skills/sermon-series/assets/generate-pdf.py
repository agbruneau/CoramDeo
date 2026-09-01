#!/usr/bin/env python3
"""
Generateur de plan de serie expositive (perspective John MacArthur).

Convertit un JSON de plan de serie en PDF formate et en Markdown miroir.
Modele: exposition suivie d'un livre (lectio continua), decoupee selon les
unites du texte et non selon un nombre de semaines fixe d'avance.

Usage: python generate-pdf.py <input.json> [output.pdf]

Requis: pip install reportlab
"""

import json
import sys
import os

_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_here, "..", "..", "..", "shared"))

from pdf_utils import (
    NAVY, GOLD, RULE_GRAY, CONTENT_WIDTH, SMALL_CAPS,
    build_styles, section_header, add_section, add_title_banner,
    make_page_footer, create_doc,
)
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

FOOTER_LABEL = "Plan de serie expositive \u00b7 perspective John MacArthur"


# --- Table helper (local: pdf_utils n'expose pas add_table) ---

def _rule_table(story, headers, rows, col_fractions, styles):
    """Table 'Quiet Doctrine': pas de remplissage, filets fins entre les lignes."""
    header_row = [Paragraph(h, styles["table_header"]) for h in headers]
    data = [header_row]
    for row in rows:
        data.append([Paragraph(str(c or ""), styles["table_cell"]) for c in row])

    col_widths = [f * CONTENT_WIDTH for f in col_fractions]
    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ("LINEABOVE", (0, 0), (-1, 0), 1.2, NAVY),
        ("LINEBELOW", (0, 0), (-1, 0), 0.4, NAVY),
        ("TOPPADDING", (0, 0), (-1, 0), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 1), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 9),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 1), (-1, -2), 0.25, RULE_GRAY),
        ("LINEBELOW", (0, -1), (-1, -1), 0.6, NAVY),
    ]))
    story.append(table)
    story.append(Spacer(1, 18))


def add_source_level(story, source_level, styles):
    """Niveau de l'echelle de sources MacArthur atteint pour cette serie."""
    section_header(story, "Niveau de source", styles)
    story.append(Paragraph(
        source_level or
        "Non declare. Traiter ce plan comme non attribue a John MacArthur.",
        styles["body"],
    ))


def add_pericopes(story, pericopes, styles):
    """Le coeur du plan: le decoupage en unites de texte."""
    section_header(story, "D\u00e9coupage en unit\u00e9s d'exposition", styles)
    if not pericopes:
        story.append(Paragraph("Aucune unit\u00e9 fournie.", styles["body"]))
        return

    headers = ["No", "Passage", "Base du d\u00e9coupage", "Titre", "Propos central", "Source"]
    rows = []
    for p in pericopes:
        rows.append([
            p.get("unit", ""),
            p.get("passage", ""),
            p.get("unit_basis", ""),
            p.get("exposition_title", ""),
            p.get("main_point", ""),
            p.get("macarthur_source", ""),
        ])
    _rule_table(story, headers, rows, [0.05, 0.14, 0.21, 0.16, 0.29, 0.15], styles)


def add_doctrinal_map(story, entries, styles):
    """Ou chaque locus doctrinal tombe dans le livre."""
    section_header(story, "Carte doctrinale du livre", styles)
    if not entries:
        story.append(Paragraph("Aucun locus fourni.", styles["body"]))
        return
    headers = ["Locus (Biblical Doctrine)", "Unit\u00e9s", "Note"]
    rows = [[e.get("locus", ""), e.get("units", ""), e.get("note", "")] for e in entries]
    _rule_table(story, headers, rows, [0.28, 0.14, 0.58], styles)


def add_difficult_texts(story, entries, styles):
    """Textes qui exigent un traitement doctrinal explicite avant d'y arriver."""
    section_header(story, "Textes exigeants", styles)
    if not entries:
        story.append(Paragraph("Aucun texte signal\u00e9.", styles["body"]))
        return

    for e in entries:
        story.append(Paragraph(e.get("passage", ""), styles["body_bold"]))
        if e.get("issue"):
            story.append(Paragraph("Difficult\u00e9", styles["body_label"]))
            story.append(Paragraph(e["issue"], styles["body_content_tight"]))
        if e.get("macarthur_reading"):
            story.append(Paragraph("Lecture retenue", styles["body_label"]))
            story.append(Paragraph(e["macarthur_reading"], styles["body_content_tight"]))
        if e.get("source_level"):
            story.append(Paragraph("Niveau de source", styles["body_label"]))
            story.append(Paragraph(e["source_level"], styles["body_content_tight"]))
        story.append(Spacer(1, 8))


def add_preaching_notes(story, notes, styles):
    section_header(story, "Notes de mise en oeuvre", styles)
    labels = [
        ("cadence", "Cadence"),
        ("unit_sizing", "Calibrage des unit\u00e9s"),
        ("gaps", "Lacunes du corpus"),
    ]
    for key, label in labels:
        if notes.get(key):
            story.append(Paragraph(label, styles["body_label"]))
            story.append(Paragraph(notes[key], styles["body_content_tight"]))


# --- Markdown ---

def _md_cell(text):
    if text is None:
        return ""
    return str(text).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def generate_markdown(data, output_path):
    lines = []
    book = data.get("book", "")
    lines.append(f"# S\u00e9rie expositive : {book}".rstrip())
    lines.append("")

    if data.get("series_title"):
        lines.append(f"**{data['series_title']}**")
        lines.append("")

    meta = [p for p in [data.get("date"), data.get("pastor_name")] if p]
    if meta:
        lines.append(" \u00b7 ".join(meta))
        lines.append("")

    lines.append("---")
    lines.append("")

    lines.append("## Niveau de source")
    lines.append("")
    lines.append(data.get("source_level") or
                 "Non d\u00e9clar\u00e9. Traiter ce plan comme non attribu\u00e9 \u00e0 John MacArthur.")
    lines.append("")

    if data.get("book_survey"):
        lines.append("## Introduction au livre")
        lines.append("")
        lines.append(data["book_survey"].strip())
        lines.append("")

    if data.get("argument_structure"):
        lines.append("## Structure de l'argument")
        lines.append("")
        lines.append(data["argument_structure"].strip())
        lines.append("")

    if data.get("pericope_division"):
        lines.append("## D\u00e9coupage en unit\u00e9s d'exposition")
        lines.append("")
        lines.append("| No | Passage | Base du d\u00e9coupage | Titre | Propos central | Source |")
        lines.append("|---|---|---|---|---|---|")
        for p in data["pericope_division"]:
            lines.append("| {} | {} | {} | {} | {} | {} |".format(
                _md_cell(p.get("unit", "")),
                f"**{_md_cell(p.get('passage', ''))}**",
                _md_cell(p.get("unit_basis", "")),
                _md_cell(p.get("exposition_title", "")),
                _md_cell(p.get("main_point", "")),
                _md_cell(p.get("macarthur_source", "")),
            ))
        lines.append("")

    if data.get("doctrinal_map"):
        lines.append("## Carte doctrinale du livre")
        lines.append("")
        lines.append("| Locus (Biblical Doctrine) | Unit\u00e9s | Note |")
        lines.append("|---|---|---|")
        for e in data["doctrinal_map"]:
            lines.append("| {} | {} | {} |".format(
                _md_cell(e.get("locus", "")),
                _md_cell(e.get("units", "")),
                _md_cell(e.get("note", "")),
            ))
        lines.append("")

    if data.get("difficult_texts"):
        lines.append("## Textes exigeants")
        lines.append("")
        for e in data["difficult_texts"]:
            lines.append(f"### {e.get('passage', '')}")
            lines.append("")
            for key, label in [("issue", "Difficult\u00e9"),
                               ("macarthur_reading", "Lecture retenue"),
                               ("source_level", "Niveau de source")]:
                if e.get(key):
                    lines.append(f"**{label}**")
                    lines.append("")
                    lines.append(e[key])
                    lines.append("")

    notes = data.get("preaching_notes") or {}
    if any(notes.values()):
        lines.append("## Notes de mise en oeuvre")
        lines.append("")
        for key, label in [("cadence", "Cadence"),
                           ("unit_sizing", "Calibrage des unit\u00e9s"),
                           ("gaps", "Lacunes du corpus")]:
            if notes.get(key):
                lines.append(f"**{label}**")
                lines.append("")
                lines.append(notes[key])
                lines.append("")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines).rstrip() + "\n")
    return os.path.abspath(output_path)


# --- Generateur principal ---

def generate_pdf(json_path, output_path=None):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not output_path:
        book = data.get("book", "serie")
        safe = book.replace(":", "-").replace(" ", "-").replace(".", "-")
        output_path = f"Serie-MacArthur-{safe}.pdf"

    doc = create_doc(
        output_path,
        title=f"S\u00e9rie expositive : {data.get('book', '')}",
        author=data.get("pastor_name", ""),
    )
    styles = build_styles()
    story = []

    meta_parts = [p for p in [data.get("date"), data.get("pastor_name")] if p]
    subtitle = data.get("book", "")
    if data.get("series_title"):
        subtitle = f"{subtitle} \u00b7 {data['series_title']}"
    add_title_banner(story, "S\u00c9RIE EXPOSITIVE (PERSPECTIVE MACARTHUR)",
                     subtitle, meta_parts, styles)

    add_source_level(story, data.get("source_level", ""), styles)

    if data.get("book_survey"):
        add_section(story, "Introduction au livre", data["book_survey"], styles)

    if data.get("argument_structure"):
        add_section(story, "Structure de l'argument", data["argument_structure"], styles)

    add_pericopes(story, data.get("pericope_division", []), styles)

    if data.get("doctrinal_map"):
        add_doctrinal_map(story, data["doctrinal_map"], styles)

    if data.get("difficult_texts"):
        add_difficult_texts(story, data["difficult_texts"], styles)

    if data.get("preaching_notes"):
        add_preaching_notes(story, data["preaching_notes"], styles)

    page_footer = make_page_footer(language="fr", label=FOOTER_LABEL)
    doc.build(story, onFirstPage=page_footer, onLaterPages=page_footer)

    md_path = os.path.splitext(output_path)[0] + ".md"
    md_result = generate_markdown(data, md_path)
    return os.path.abspath(output_path), md_result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate-pdf.py <input.json> [output.pdf]")
        sys.exit(1)
    pdf_path, md_path = generate_pdf(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    print(f"PDF genere : {pdf_path}")
    print(f"Markdown genere : {md_path}")
