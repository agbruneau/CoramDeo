#!/usr/bin/env python3
"""Shared PDF helpers for the pastor-ai-skills PDF generators.

ponytail: minimal but complete implementation of the API the skill
generators import (colors, fonts, CONTENT_WIDTH, and the build/section
helpers). Built-in Type1 fonts only (WinAnsi covers French accents +
guillemets), so no font files to ship. Upgrade path: drop in real
small-caps/serif TTFs and register them if the look needs sharpening.
"""

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
)

# --- Palette ("Quiet Doctrine") ---
NAVY = HexColor("#1A2A40")
GOLD = HexColor("#B8893A")
SLATE = HexColor("#5A5A5A")
LIGHT_BG = HexColor("#F7F3EA")
RULE_GRAY = HexColor("#CCCCCC")
WHITE = colors.white
INK = HexColor("#222222")

# --- Fonts ---
# Default to built-in Type1 fonts (WinAnsi: French accents + guillemets, no
# files to ship). But WinAnsi lacks Latin-Extended glyphs like the macron
# vowels used in Greek/Hebrew transliteration (ō, ē, ā), which render as a
# missing-glyph box. So prefer a real Unicode serif (Times New Roman TTF) when
# it's installed, and fall back to the built-ins when it isn't.
SERIF_BODY = "Times-Roman"
SERIF_BOLD = "Times-Bold"
SERIF_ITALIC = "Times-Italic"
SMALL_CAPS = "Helvetica"  # stand-in for true small caps; used at ~8pt


def _register_unicode_serif():
    """Register a Unicode serif family from the system fonts; return its
    (regular, bold, italic) font names, or None when none is found (then the
    built-in serif is kept). Tries the common serif on each OS so the skill
    renders macrons on Windows, macOS and Linux/CI, not just one machine."""
    import os
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    # Candidate families, in order, as (regular, bold, italic, bold-italic).
    families = [
        ("times.ttf", "timesbd.ttf", "timesi.ttf", "timesbi.ttf"),                 # Windows / macOS: Times New Roman
        ("DejaVuSerif.ttf", "DejaVuSerif-Bold.ttf",
         "DejaVuSerif-Italic.ttf", "DejaVuSerif-BoldItalic.ttf"),                   # Linux: DejaVu
        ("LiberationSerif-Regular.ttf", "LiberationSerif-Bold.ttf",
         "LiberationSerif-Italic.ttf", "LiberationSerif-BoldItalic.ttf"),          # Linux: Liberation
    ]
    search_dirs = [
        os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts"),
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "Windows", "Fonts"),
        "/Library/Fonts", os.path.expanduser("~/Library/Fonts"),
        "/usr/share/fonts", "/usr/share/fonts/truetype",
        "/usr/share/fonts/truetype/dejavu", "/usr/share/fonts/truetype/liberation",
        os.path.expanduser("~/.fonts"),
    ]

    def find(filename):
        for d in search_dirs:
            if d and os.path.exists(os.path.join(d, filename)):
                return os.path.join(d, filename)
        return None

    names = ("SerifUni", "SerifUni-Bold", "SerifUni-Italic", "SerifUni-BoldItalic")
    for faces in families:
        paths = [find(fn) for fn in faces]
        if not all(paths):
            continue
        try:
            for name, path in zip(names, paths):
                pdfmetrics.registerFont(TTFont(name, path))
            # Family mapping so <b>/<i> markup inside Paragraphs resolves correctly.
            pdfmetrics.registerFontFamily(
                "SerifUni", normal=names[0], bold=names[1],
                italic=names[2], boldItalic=names[3],
            )
            return names[0], names[1], names[2]
        except Exception:
            continue
    return None


_uni_serif = _register_unicode_serif()
if _uni_serif:
    SERIF_BODY, SERIF_BOLD, SERIF_ITALIC = _uni_serif

# --- Page geometry ---
PAGE_W, PAGE_H = letter
LEFT_MARGIN = RIGHT_MARGIN = 0.9 * inch
TOP_MARGIN = 0.85 * inch
BOTTOM_MARGIN = 0.85 * inch
CONTENT_WIDTH = PAGE_W - LEFT_MARGIN - RIGHT_MARGIN


def create_doc(output_path, title="", author=""):
    """Return a SimpleDocTemplate sized to the shared geometry."""
    return SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=LEFT_MARGIN,
        rightMargin=RIGHT_MARGIN,
        topMargin=TOP_MARGIN,
        bottomMargin=BOTTOM_MARGIN,
        title=title,
        author=author,
    )


def build_styles():
    """Return the style dict every generator helper references by key."""
    return {
        "body": ParagraphStyle(
            "body", fontName=SERIF_BODY, fontSize=10.5, leading=15.5,
            textColor=INK, alignment=TA_JUSTIFY, spaceAfter=7,
        ),
        "body_bold": ParagraphStyle(
            "body_bold", fontName=SERIF_BOLD, fontSize=11.5, leading=15,
            textColor=NAVY, spaceBefore=8, spaceAfter=2,
        ),
        "body_label": ParagraphStyle(
            "body_label", fontName=SMALL_CAPS, fontSize=7.5, leading=10,
            textColor=GOLD, spaceBefore=3, spaceAfter=1,
        ),
        "body_content_tight": ParagraphStyle(
            "body_content_tight", fontName=SERIF_BODY, fontSize=10, leading=14,
            textColor=INK, alignment=TA_JUSTIFY, spaceAfter=3,
        ),
        "section_header": ParagraphStyle(
            "section_header", fontName=SERIF_BOLD, fontSize=14.5, leading=17,
            textColor=NAVY, spaceBefore=16, spaceAfter=3,
        ),
        "table_header": ParagraphStyle(
            "table_header", fontName="Helvetica-Bold", fontSize=8.5, leading=11,
            textColor=NAVY,
        ),
        "table_cell": ParagraphStyle(
            "table_cell", fontName=SERIF_BODY, fontSize=9, leading=12.5,
            textColor=INK,
        ),
        "table_cell_bold": ParagraphStyle(
            "table_cell_bold", fontName=SERIF_BOLD, fontSize=9, leading=12.5,
            textColor=NAVY,
        ),
        "xref_head": ParagraphStyle(
            "xref_head", fontName=SERIF_BOLD, fontSize=10.5, leading=14,
            textColor=NAVY, spaceBefore=7, spaceAfter=1,
        ),
        "xref_body": ParagraphStyle(
            "xref_body", fontName=SERIF_BODY, fontSize=10, leading=14,
            textColor=INK, alignment=TA_JUSTIFY, leftIndent=12, spaceAfter=2,
        ),
        "prompt": ParagraphStyle(
            "prompt", fontName=SERIF_BODY, fontSize=10.5, leading=15,
            textColor=INK, alignment=TA_JUSTIFY,
        ),
    }


def section_header(story, title, styles):
    """Navy serif header with a gold underrule."""
    story.append(Paragraph(title, styles["section_header"]))
    story.append(HRFlowable(
        width="100%", thickness=1, color=GOLD,
        spaceBefore=1, spaceAfter=8, lineCap="round",
    ))


def add_section(story, title, text, styles):
    """Header followed by body paragraphs (split on blank lines)."""
    section_header(story, title, styles)
    for para in str(text).split("\n\n"):
        para = para.strip()
        if para:
            story.append(Paragraph(para, styles["body"]))


def add_title_banner(story, banner_title, passage, meta_parts, styles):
    """Top-of-document banner: kicker, passage, meta line, gold rule."""
    kicker = ParagraphStyle(
        "kicker", fontName=SMALL_CAPS, fontSize=9, leading=12,
        textColor=GOLD, spaceAfter=4,
    )
    title_style = ParagraphStyle(
        "banner_title", fontName=SERIF_BOLD, fontSize=22, leading=25,
        textColor=NAVY, spaceAfter=4,
    )
    meta_style = ParagraphStyle(
        "banner_meta", fontName=SERIF_ITALIC, fontSize=10, leading=13,
        textColor=SLATE, spaceAfter=6,
    )

    story.append(HRFlowable(width="100%", thickness=2, color=NAVY,
                            spaceAfter=8, lineCap="round"))
    story.append(Paragraph(banner_title, kicker))
    if passage:
        story.append(Paragraph(passage, title_style))
    meta_parts = [p for p in (meta_parts or []) if p]
    if meta_parts:
        story.append(Paragraph("  ·  ".join(meta_parts), meta_style))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD,
                            spaceBefore=2, spaceAfter=12, lineCap="round"))


def make_page_footer(scope="church", language="fr", label=None):
    """Return an onPage callback drawing a footer rule + page number.

    `label` overrides the default footer caption; callers that omit it keep
    the historic sermon-research caption, so existing generators are unaffected.
    """
    page_word = "Page"
    if label is None:
        if language == "fr":
            label = "Recherche exégétique · perspective John MacArthur"
        else:
            label = "Sermon research · John MacArthur perspective"

    def _footer(canvas, doc):
        canvas.saveState()
        y = BOTTOM_MARGIN - 22
        canvas.setStrokeColor(RULE_GRAY)
        canvas.setLineWidth(0.5)
        canvas.line(LEFT_MARGIN, y + 10, PAGE_W - RIGHT_MARGIN, y + 10)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(SLATE)
        canvas.drawString(LEFT_MARGIN, y, label)
        canvas.drawRightString(
            PAGE_W - RIGHT_MARGIN, y, f"{page_word} {doc.page}"
        )
        canvas.restoreState()

    return _footer
