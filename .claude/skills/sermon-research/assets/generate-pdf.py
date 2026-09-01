#!/usr/bin/env python3
"""
Sermon Research PDF Generator (perspective John MacArthur)
Converts structured sermon research JSON into a formatted PDF document
and an accompanying Markdown document.

Usage: python generate-pdf.py <input.json> [output.pdf]

Required: pip install reportlab
"""

import json
import re
import sys
import os

_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_here, "..", "..", "..", "shared"))

from pdf_utils import (
    NAVY, GOLD, SLATE, LIGHT_BG, RULE_GRAY, WHITE, CONTENT_WIDTH,
    SERIF_BODY, SERIF_BOLD, SERIF_ITALIC, SMALL_CAPS,
    build_styles, section_header, add_section, add_title_banner,
    make_page_footer, create_doc,
)
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.units import inch


# --- Sermon-specific layout functions ---


# Map des types de renvois utilisés dans `cross_references[].type`.
# Accepte les anciennes valeurs anglaises pour rétro-compatibilité.
CROSS_REF_TYPE_LABELS = {
    "Direct parallel": "Parallèle direct",
    "Thematic connection": "Lien thématique",
    "OT background": "Arrière-plan AT",
    "Parallèle direct": "Parallèle direct",
    "Lien thématique": "Lien thématique",
    "Arrière-plan AT": "Arrière-plan AT",
}


def add_word_studies(story, word_studies, styles):
    """Quiet Doctrine table: open editorial, no fills, hairline rules between rows."""
    section_header(story, "Étude des mots-clés", styles)

    if not word_studies:
        story.append(Paragraph("Aucune étude de mots fournie.", styles["body"]))
        return

    headers = [
        "Français", "Translit.",
        "Sens littéral", "Champ sémantique", "Traductions comparées"
    ]

    header_row = [Paragraph(h, styles["table_header"]) for h in headers]
    table_data = [header_row]

    for ws in word_studies:
        translations = ws.get("translations", {})
        # Translation list rendered with small caps source label + serif value
        trans_parts = []
        for k, v in translations.items():
            trans_parts.append(
                f'<font name="{SMALL_CAPS}" size="8" color="#5A5A5A">{k}</font>'
                f'&nbsp;{v}'
            )
        trans_text = " &nbsp;·&nbsp; ".join(trans_parts) if trans_parts else ""

        row = [
            Paragraph(ws.get("english", ""), styles["table_cell_bold"]),
            Paragraph(f'<i>{ws.get("transliteration", "")}</i>', styles["table_cell"]),
            Paragraph(ws.get("literal_meaning", ""), styles["table_cell"]),
            Paragraph(ws.get("range_of_meaning", ""), styles["table_cell"]),
            Paragraph(trans_text, styles["table_cell"]),
        ]
        table_data.append(row)

    # Column widths sum to CONTENT_WIDTH (auto-scales with page margins)
    col_fractions = [0.146, 0.131, 0.162, 0.277, 0.284]  # sums to 1.0
    col_widths = [f * CONTENT_WIDTH for f in col_fractions]

    table = Table(table_data, colWidths=col_widths, repeatRows=1)

    style_commands = [
        # Header row — open, no fill; bold rule above, hairline rule below
        ("LINEABOVE", (0, 0), (-1, 0), 1.2, NAVY),
        ("LINEBELOW", (0, 0), (-1, 0), 0.4, NAVY),
        ("TOPPADDING", (0, 0), (-1, 0), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 7),
        # All cells
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 1), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 9),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        # Hairline rules between rows only — no vertical lines, no alternating fills
        ("LINEBELOW", (0, 1), (-1, -2), 0.25, RULE_GRAY),
        ("LINEBELOW", (0, -1), (-1, -1), 0.6, NAVY),
    ]

    table.setStyle(TableStyle(style_commands))
    story.append(table)
    story.append(Spacer(1, 18))


def add_commentary_insights(story, insights, source_level, styles, sermon_links=None):
    """Exposition section, preceded by the mandatory source-ladder statement.

    `source_level` records which rung of the MacArthur source ladder actually
    backs this exposition (or that none does). It is rendered before the body
    so a reader can never mistake a level-5 or level-empty file for documented
    MacArthur exposition.
    """
    section_header(story, "Apports des commentateurs", styles)

    if source_level:
        story.append(Paragraph("Niveau de source", styles["body_label"]))
        story.append(Paragraph(source_level, styles["body_content_tight"]))
        story.append(Spacer(1, 6))
    else:
        story.append(Paragraph("Niveau de source", styles["body_label"]))
        story.append(Paragraph(
            "Non déclaré. Traiter cette section comme non attribuée à John MacArthur.",
            styles["body_content_tight"],
        ))
        story.append(Spacer(1, 6))

    if sermon_links:
        add_sermon_links(story, sermon_links, styles)

    for para in str(insights or "").split("\n\n"):
        para = para.strip()
        if para:
            story.append(Paragraph(para, styles["body"]))


def sermon_code(url):
    """Extrait le code Grace to You de l'URL, pour la colonne « Code » du tableau.

    https://www.gty.org/sermons/90-226              -> 90-226
    .../sermons/90-208/creation-believe-it-or-not   -> 90-208
    .../library/sermons-library/90-221/the-rest...  -> 90-221
    .../sermons/series/255/the-battle-for-the-...   -> Série 255

    Retourne une chaîne vide si l'URL n'a aucune de ces formes : la colonne
    reste alors vide plutôt que d'afficher un code deviné.
    """
    url = str(url or "")
    m = re.search(r"/sermons/series/(\d+)", url)
    if m:
        return "Série " + m.group(1)
    m = re.search(r"/(?:sermons|sermons-library)/([^/?#]+)", url)
    if m:
        return m.group(1)
    return ""


def add_sermon_links(story, links, styles):
    """Tableau des sermons Grace to You qui appuient l'exposition.

    Trois colonnes : code, titre cliquable, passage couvert. Le code est déduit
    de l'URL, il n'y a pas de champ JSON à remplir.

    Forme d'URL canonique : https://www.gty.org/sermons/<code> (gty.org redirige
    vers le titre complet). Ne jamais fabriquer de slug.
    """
    story.append(Paragraph("Sermons Grace to You", styles["body_label"]))

    headers = ["Code", "Sermon", "Passage"]
    table_data = [[Paragraph(h, styles["table_header"]) for h in headers]]

    for link in links:
        url = str(link.get("url", "")).strip()
        title = str(link.get("title", "")).strip() or url
        passage = str(link.get("passage", "")).strip()
        if url:
            title = f'<a href="{url}" color="#1A2A40"><u>{title}</u></a>'
        table_data.append([
            Paragraph(sermon_code(url), styles["table_cell_bold"]),
            Paragraph(title, styles["table_cell"]),
            Paragraph(passage, styles["table_cell"]),
        ])

    col_fractions = [0.15, 0.62, 0.23]  # somme = 1.0
    table = Table(
        table_data,
        colWidths=[f * CONTENT_WIDTH for f in col_fractions],
        repeatRows=1,
    )
    table.setStyle(TableStyle([
        # En-tête : ouvert, sans aplat, filet fort au-dessus, hairline en dessous
        ("LINEABOVE", (0, 0), (-1, 0), 1.2, NAVY),
        ("LINEBELOW", (0, 0), (-1, 0), 0.4, NAVY),
        ("TOPPADDING", (0, 0), (-1, 0), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 7),
        # Toutes les cellules
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 1), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        # Filets entre les lignes seulement, aucun trait vertical
        ("LINEBELOW", (0, 1), (-1, -2), 0.25, RULE_GRAY),
        ("LINEBELOW", (0, -1), (-1, -1), 0.6, NAVY),
    ]))

    story.append(table)
    story.append(Spacer(1, 12))


def add_cross_references(story, cross_refs, styles):
    """Quiet Doctrine: definition-list format. Bold reference + small-caps type tag,
    connection set on a new line with a hanging indent."""
    section_header(story, "Renvois et passages parall\u00e8les", styles)

    if not cross_refs:
        story.append(Paragraph("Aucun renvoi fourni.", styles["body"]))
        return

    for ref in cross_refs:
        reference = ref.get("reference", "")
        connection = ref.get("connection", "")
        conn_type = ref.get("type", "")
        conn_type_fr = CROSS_REF_TYPE_LABELS.get(conn_type, conn_type)

        type_html = (
            f' &nbsp;<font name="{SMALL_CAPS}" size="8" color="#5A5A5A">'
            f'\u00b7&nbsp;{conn_type_fr}</font>'
        ) if conn_type_fr else ""

        story.append(Paragraph(reference + type_html, styles["xref_head"]))
        story.append(Paragraph(connection, styles["xref_body"]))


def add_theological_themes(story, themes, styles):
    """Quiet Doctrine: serif theme name, no underline; small caps quiet labels in slate."""
    section_header(story, "Thèmes théologiques", styles)

    if not themes:
        story.append(Paragraph("Aucun thème fourni.", styles["body"]))
        return

    for theme in themes:
        name = theme.get("name", "")
        in_text = theme.get("in_text", "")
        implication = theme.get("implication", "")

        # Theme name in serif bold; spacing handled by style spaceAfter
        story.append(Paragraph(name, styles["body_bold"]))

        if in_text:
            story.append(Paragraph("Dans le texte", styles["body_label"]))
            story.append(Paragraph(in_text, styles["body_content_tight"]))

        if implication:
            story.append(Paragraph("Pour votre assemblée", styles["body_label"]))
            story.append(Paragraph(implication, styles["body_content_tight"]))

        story.append(Spacer(1, 8))


def _shaded_prompts_table(rows, top_pad, bot_pad):
    """Build one segment of the prompts shaded box.

    Each prompt is its own row in the table so reportlab can split the box
    naturally across pages while preserving the gold-bar + cream-background
    visual treatment on every continuation.
    """
    gold_bar_width = 4
    content_col_width = CONTENT_WIDTH - gold_bar_width - 2
    t = Table(rows, colWidths=[gold_bar_width, content_col_width])
    cmds = [
        # Gold bar (col 0)
        ("BACKGROUND", (0, 0), (0, -1), GOLD),
        ("LEFTPADDING", (0, 0), (0, -1), 0),
        ("RIGHTPADDING", (0, 0), (0, -1), 0),
        ("TOPPADDING", (0, 0), (0, -1), 0),
        ("BOTTOMPADDING", (0, 0), (0, -1), 0),
        # Cream content (col 1)
        ("BACKGROUND", (1, 0), (1, -1), LIGHT_BG),
        ("LEFTPADDING", (1, 0), (1, -1), 14),
        ("RIGHTPADDING", (1, 0), (1, -1), 14),
        # Inter-row vertical breathing
        ("TOPPADDING", (1, 0), (1, -1), 4),
        ("BOTTOMPADDING", (1, 0), (1, -1), 4),
        # First-row top padding (closes the box top)
        ("TOPPADDING", (1, 0), (1, 0), top_pad),
        # Last-row bottom padding (closes the box bottom)
        ("BOTTOMPADDING", (1, -1), (1, -1), bot_pad),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]
    t.setStyle(TableStyle(cmds))
    return t


def add_thinking_prompts(story, prompts, styles):
    """Render prompts as a shaded box with a gold left border.

    Strategy: bind the section header to the FIRST prompt only (KeepTogether)
    so the header never orphans, but let the remaining prompts flow as a
    separate splittable table. The visual look is a single continuous box,
    even when the box breaks across pages.
    """
    if not prompts:
        section_header(story, "Pistes de réflexion", styles)
        story.append(Paragraph("Aucune piste fournie.", styles["body"]))
        return

    rows = [
        [None, Paragraph(f"<b>{i}.</b>  {prompt}", styles["prompt"])]
        for i, prompt in enumerate(prompts, 1)
    ]

    section_para = Paragraph("Pistes de réflexion", styles["section_header"])

    # First prompt: glued to the section header (anti-orphan)
    first_table = _shaded_prompts_table(
        [rows[0]],
        top_pad=12,
        bot_pad=12 if len(rows) == 1 else 4,
    )
    story.append(KeepTogether([section_para, first_table]))

    # Remaining prompts: free-flowing splittable table
    if len(rows) > 1:
        rest_table = _shaded_prompts_table(rows[1:], top_pad=4, bot_pad=12)
        story.append(rest_table)


# --- Markdown Generator ---


def _md_escape_cell(text):
    """Escape pipe and newline characters so the cell stays inside one Markdown table row."""
    if text is None:
        return ""
    return str(text).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def _md_paragraphs(text):
    """Normalize a multi-paragraph string for Markdown output (strip trailing whitespace)."""
    if not text:
        return ""
    return text.strip()


def generate_markdown(data, output_path):
    """Write a Markdown file mirroring the PDF structure."""
    lines = []

    passage = data.get("passage", "")
    lines.append(f"# Recherche exégétique (perspective MacArthur) : {passage}".rstrip())
    lines.append("")

    meta_parts = [p for p in [data.get("date"), data.get("pastor_name"), data.get("church_name")] if p]
    if meta_parts:
        lines.append(" · ".join(f"**{p}**" for p in meta_parts))
        lines.append("")

    lines.append("---")
    lines.append("")

    if data.get("passage_context"):
        lines.append("## Contexte du passage")
        lines.append("")
        lines.append(_md_paragraphs(data["passage_context"]))
        lines.append("")

    if data.get("historical_background"):
        lines.append("## Arrière-plan historique et culturel")
        lines.append("")
        lines.append(_md_paragraphs(data["historical_background"]))
        lines.append("")

    if data.get("word_studies"):
        lines.append("## Étude des mots-clés")
        lines.append("")
        lines.append("| Français | Translit. | Sens littéral | Champ sémantique | Traductions comparées |")
        lines.append("|---|---|---|---|---|")
        for ws in data["word_studies"]:
            translations = ws.get("translations", {}) or {}
            trans_text = " · ".join(f"_{k}_ {v}" for k, v in translations.items())
            lines.append(
                "| {english} | {translit} | {literal} | {range_} | {trans} |".format(
                    english=f"**{_md_escape_cell(ws.get('english', ''))}**",
                    translit=f"_{_md_escape_cell(ws.get('transliteration', ''))}_",
                    literal=_md_escape_cell(ws.get("literal_meaning", "")),
                    range_=_md_escape_cell(ws.get("range_of_meaning", "")),
                    trans=_md_escape_cell(trans_text),
                )
            )
        lines.append("")

    if data.get("commentary_insights") or data.get("source_level"):
        lines.append("## Apports des commentateurs")
        lines.append("")
        lines.append("**Niveau de source**")
        lines.append("")
        lines.append(
            data.get("source_level")
            or "Non déclaré. Traiter cette section comme non attribuée à John MacArthur."
        )
        lines.append("")
        if data.get("sermon_links"):
            lines.append("**Sermons Grace to You**")
            lines.append("")
            lines.append("| Code | Sermon | Passage |")
            lines.append("|---|---|---|")
            for link in data["sermon_links"]:
                url = str(link.get("url", "")).strip()
                title = _md_escape_cell(str(link.get("title", "")).strip() or url)
                passage = _md_escape_cell(str(link.get("passage", "")).strip())
                if url:
                    title = f"[{title}]({url})"
                lines.append(f"| {sermon_code(url)} | {title} | {passage} |")
            lines.append("")
        if data.get("commentary_insights"):
            lines.append(_md_paragraphs(data["commentary_insights"]))
            lines.append("")

    if data.get("cross_references"):
        lines.append("## Renvois et passages parallèles")
        lines.append("")
        for ref in data["cross_references"]:
            reference = ref.get("reference", "")
            connection = ref.get("connection", "")
            conn_type = ref.get("type", "")
            conn_type_fr = CROSS_REF_TYPE_LABELS.get(conn_type, conn_type)
            head = f"**{reference}**"
            if conn_type_fr:
                head += f" · _{conn_type_fr}_"
            lines.append(head)
            if connection:
                lines.append("")
                lines.append(connection)
            lines.append("")

    if data.get("theological_themes"):
        lines.append("## Thèmes théologiques")
        lines.append("")
        for theme in data["theological_themes"]:
            name = theme.get("name", "")
            in_text = theme.get("in_text", "")
            implication = theme.get("implication", "")
            if name:
                lines.append(f"### {name}")
                lines.append("")
            if in_text:
                lines.append("**Dans le texte**")
                lines.append("")
                lines.append(in_text)
                lines.append("")
            if implication:
                lines.append("**Pour votre assemblée**")
                lines.append("")
                lines.append(implication)
                lines.append("")

    if data.get("thinking_prompts"):
        lines.append("## Pistes de réflexion")
        lines.append("")
        for i, prompt in enumerate(data["thinking_prompts"], 1):
            lines.append(f"{i}. {prompt}")
        lines.append("")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines).rstrip() + "\n")

    return os.path.abspath(output_path)


# --- Main Generator ---

def generate_pdf(json_path, output_path=None):
    """Generate a formatted PDF from sermon research JSON data."""

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not output_path:
        passage = data.get("passage", "recherche")
        safe_name = passage.replace(":", "-").replace(" ", "-")
        output_path = f"Recherche-MacArthur-{safe_name}.pdf"

    doc = create_doc(
        output_path,
        title=f"Recherche exégétique (perspective MacArthur) : {data.get('passage', '')}",
        author=data.get("pastor_name", ""),
    )

    styles = build_styles()
    story = []

    # Title banner
    meta_parts = []
    if data.get("date"):
        meta_parts.append(data["date"])
    if data.get("pastor_name"):
        meta_parts.append(data["pastor_name"])
    if data.get("church_name"):
        meta_parts.append(data["church_name"])

    add_title_banner(story, "RECHERCHE EXÉGÉTIQUE (PERSPECTIVE MACARTHUR)", data.get("passage", ""), meta_parts, styles)

    # Sections
    if data.get("passage_context"):
        add_section(story, "Contexte du passage", data["passage_context"], styles)

    if data.get("historical_background"):
        add_section(
            story, "Arrière-plan historique et culturel",
            data["historical_background"], styles
        )

    if data.get("word_studies"):
        add_word_studies(story, data["word_studies"], styles)

    if data.get("commentary_insights") or data.get("source_level"):
        add_commentary_insights(
            story, data.get("commentary_insights", ""),
            data.get("source_level", ""), styles,
            data.get("sermon_links"),
        )

    if data.get("cross_references"):
        add_cross_references(story, data["cross_references"], styles)

    if data.get("theological_themes"):
        add_theological_themes(story, data["theological_themes"], styles)

    if data.get("thinking_prompts"):
        add_thinking_prompts(story, data["thinking_prompts"], styles)

    page_footer = make_page_footer("church", language="fr")
    doc.build(story, onFirstPage=page_footer, onLaterPages=page_footer)

    md_path = os.path.splitext(output_path)[0] + ".md"
    md_result = generate_markdown(data, md_path)

    return os.path.abspath(output_path), md_result


# --- CLI Entry ---

def _selftest():
    """Vérifie l'extraction du code de sermon depuis les formes d'URL gty.org."""
    cases = {
        "https://www.gty.org/sermons/90-226": "90-226",
        "https://www.gty.org/sermons/90-208/creation-believe-it-or-not-part-1": "90-208",
        "https://www.gty.org/library/sermons-library/90-221/the-rest-of-creation": "90-221",
        "https://www.gty.org/sermons/series/255/the-battle-for-the-beginning": "Série 255",
        "https://www.gty.org/sermons/1615": "1615",
        "https://example.org/quelque-chose": "",
        "": "",
        None: "",
    }
    for url, expected in cases.items():
        got = sermon_code(url)
        assert got == expected, f"sermon_code({url!r}) = {got!r}, attendu {expected!r}"
    print("selftest OK :", len(cases), "cas")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        _selftest()
        sys.exit(0)

    if len(sys.argv) < 2:
        print("Usage: python generate-pdf.py <input.json> [output.pdf]")
        print("       python generate-pdf.py --selftest")
        sys.exit(1)

    json_input = sys.argv[1]
    pdf_output = sys.argv[2] if len(sys.argv) > 2 else None

    pdf_path, md_path = generate_pdf(json_input, pdf_output)
    print(f"PDF généré : {pdf_path}")
    print(f"Markdown généré : {md_path}")
