# -*- coding: utf-8 -*-
"""
Extraction du Nouveau Testament depuis « NEG - MacArthur.pdf ».

Pour chaque livre du NT, produit deux fichiers dans son dossier :
  - NEG - <Livre>.md : texte biblique NEG (chapitres, peri­copes, versets numerotes)
  - JMA - <Livre>.md : notes d'etude MacArthur (intro, plan, notes verset par verset)

Separation par police + taille + region (haut texte / bas commentaire) :
  Utopia-Regular 8.5 / capitale 24      -> texte biblique NEG
  Humanist BoldCond ~7.1 (region haut)  -> numero de verset (NEG)
  Utopia-Semibold 8.0-8.9 inline        -> en-tete de peri­cope (NEG)
  Humanist Light ~6.7 (bande etroite)   -> renvois marginaux (exclus par defaut)
  Humanist Light ~7.8 (region bas)      -> commentaire MacArthur (JMA)
  Humanist BoldCond ~7.4 (region bas)   -> amorce de note c:v + lemme (JMA)
  Humanist Roman/Bold ~8.8              -> plan + tableaux d'etude (JMA)
"""
import fitz, re, sys, os

PDF = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'NEG - MacArthur.pdf')

# (num, nom de dossier/livre, page index PyMuPDF du debut de l'intro)
BOOKS = [
    (40, 'Matthieu', 1374), (41, 'Marc', 1439), (42, 'Luc', 1493), (43, 'Jean', 1560),
    (44, 'Actes', 1623), (45, 'Romains', 1684), (46, '1 Corinthiens', 1724),
    (47, '2 Corinthiens', 1762), (48, 'Galates', 1791), (49, 'Éphésiens', 1809),
    (50, 'Philippiens', 1827), (51, 'Colossiens', 1841), (52, '1 Thessaloniciens', 1854),
    (53, '2 Thessaloniciens', 1865), (54, '1 Timothée', 1872), (55, '2 Timothée', 1890),
    (56, 'Tite', 1901), (57, 'Philémon', 1908), (58, 'Hébreux', 1912), (59, 'Jacques', 1945),
    (60, '1 Pierre', 1958), (61, '2 Pierre', 1973), (62, '1 Jean', 1986), (63, '2 Jean', 2003),
    (64, '3 Jean', 2007), (65, 'Jude', 2011), (66, 'Apocalypse', 2018),
]
BACK_MATTER = 2057  # 1re page apres l'Apocalypse (Table des matieres / index)

TOP_MARGIN = 28      # y0 < TOP_MARGIN -> en-tete courant / pagination (rejete)
KEEP_XREF = False    # inclure les renvois marginaux (False = exclus)


def cat(s):
    """Categorie brute d'un span selon police + taille (region traitee ailleurs)."""
    f, sz = s['font'], s['size']
    if f.startswith('Utopia'):
        if 'Semibold' in f:
            return 'runhead' if sz > 9.05 else 'header'
        return 'chapnum' if sz >= 16 else 'bible'
    if f.startswith('Humanist'):
        if 'Light' in f:
            return 'commentary' if sz >= 7.3 else 'xref'
        if 'Bold' in f and 'Cond' in f:
            return 'boldcond'        # 7.1 num verset / 7.4 amorce note / 6.6 cle renvoi
        return 'apparatus'           # Roman/Bold ~8.8 : plan, tableaux
    return 'other'                   # ArialMT (filigrane), etc.


def clean(t):
    for ch in (' ', ' ', ' ', ' ', ' ', ' '):
        t = t.replace(ch, ' ')
    t = t.replace('\xad', '')        # soft hyphen residuel
    t = t.replace('‑', '-')          # tiret insecable -> tiret
    return t


def smart_join(acc, frag):
    """Concatene en gerant la cesure de fin de ligne.
    \xad (texte biblique) et ‑ (commentaire) = cesure -> oter le tiret.
    - (U+002D) = vrai trait d'union compose (ex. Jesus-Christ) -> garder, sans espace."""
    if not acc:
        return frag
    a = acc.rstrip()
    f = frag.lstrip()
    if a.endswith('\xad') or a.endswith('‑'):     # soft hyphen / U+2011 = cesure
        return a[:-1] + f
    if a.endswith('-'):                            # U+002D
        if f[:1].islower():                        # cesure (ex. Sal-mon) -> oter
            return a[:-1] + f
        return a + f                               # compose (Jesus-Christ) / plage (1-17) -> garder
    if acc.endswith(' ') or frag.startswith(' '):
        return acc + frag
    return acc + ' ' + frag


def page_spans(page):
    W = page.rect.width
    divider = W * 0.5
    raw = []
    for b in page.get_text('dict')['blocks']:
        if b.get('type') != 0:
            continue
        for l in b['lines']:
            for s in l['spans']:
                if not s['text'].strip():
                    continue
                y0 = s['bbox'][1]
                if y0 < TOP_MARGIN:
                    continue
                raw.append({'text': s['text'], 'x0': s['bbox'][0], 'y0': y0,
                            'size': s['size'], 'cat': cat(s)})
    # region : cy = haut du commentaire (1er span commentary)
    cy = min([s['y0'] for s in raw if s['cat'] == 'commentary'], default=1e9)
    for s in raw:
        s['col'] = 0 if s['x0'] < divider else 1
        if s['cat'] == 'boldcond':
            if s['y0'] >= cy:
                s['cat'] = 'comment_ref'
            elif s['size'] < 6.85:
                s['cat'] = 'xref_key'
            else:
                s['cat'] = 'versenum'
    return raw


def vlines(spans):
    """Groupe des spans en lignes visuelles, ordre de lecture (y puis x)."""
    spans = sorted(spans, key=lambda s: (round(s['y0']), s['x0']))
    out, cur, cy = [], [], None
    for s in spans:
        if cy is None or abs(s['y0'] - cy) <= 4:
            cur.append(s)
            if cy is None:
                cy = s['y0']
        else:
            out.append(sorted(cur, key=lambda z: z['x0']))
            cur, cy = [s], s['y0']
    if cur:
        out.append(sorted(cur, key=lambda z: z['x0']))
    return out


def extract_book(doc, start, end):
    # 1re page de texte biblique = 1re page avec une capitale de chapitre OU un
    # numero de verset (livres a 1 chapitre : Phm, 2-3 Jn, Jude -> pas de capitale)
    first_bible = start
    for p in range(start, end + 1):
        if any(s['cat'] in ('chapnum', 'versenum') and re.fullmatch(r'\d{1,3}', s['text'].strip())
               for s in page_spans(doc[p])):
            first_bible = p
            break

    neg = []        # evenements NEG : chap / head / verse / text
    intro = []      # (H|P, texte) pour l'intro JMA
    notes = []      # ('ref'|'note', texte) commentaire JMA
    apparatus = []  # plan + tableaux (JMA)

    for p in range(start, end + 1):
        spans = page_spans(doc[p])
        if not spans:
            continue

        if p < first_bible:                       # ---- page d'intro ----
            for col in (0, 1):
                for vl in vlines([s for s in spans if s['col'] == col and s['cat'] != 'other']):
                    txt = ''.join(z['text'] for z in vl)
                    if not txt.strip():
                        continue
                    is_head = all(z['cat'] in ('header', 'runhead') for z in vl)
                    is_app = any(z['cat'] == 'apparatus' for z in vl)
                    intro.append(('H' if is_head else ('A' if is_app else 'P'), txt))
            continue

        for col in (0, 1):                        # ---- page texte + commentaire ----
            colspans = [s for s in spans if s['col'] == col]

            # texte biblique : bible / chapnum / header / versenum
            bible = [s for s in colspans if s['cat'] in ('bible', 'chapnum', 'header', 'versenum')]
            for vl in vlines(bible):
                cats = {z['cat'] for z in vl}
                for z in vl:
                    if z['cat'] == 'chapnum' and re.fullmatch(r'\d{1,3}', z['text'].strip()):
                        neg.append({'t': 'chap', 'n': z['text'].strip()})
                if cats == {'header'} or cats == {'header', 'chapnum'}:
                    t = ''.join(z['text'] for z in vl if z['cat'] == 'header')
                    if t.strip():
                        neg.append({'t': 'head', 'text': t})
                    continue
                buf = ''
                for z in vl:
                    if z['cat'] == 'chapnum':
                        continue
                    if z['cat'] == 'versenum' and re.fullmatch(r'\d{1,3}(-\d{1,3})?', z['text'].strip()):
                        if buf.strip():
                            neg.append({'t': 'text', 'text': buf})
                            buf = ''
                        neg.append({'t': 'verse', 'n': z['text'].strip()})
                    else:
                        buf += z['text']
                if buf.strip():
                    neg.append({'t': 'text', 'text': buf})

            # commentaire MacArthur : comment_ref (gras) + commentary (corps)
            comm = [s for s in colspans if s['cat'] in ('comment_ref', 'commentary')]
            for vl in vlines(comm):
                for z in vl:
                    kind = 'ref' if z['cat'] == 'comment_ref' else 'note'
                    notes.append((kind, z['text']))

            # plan / tableaux
            for vl in vlines([s for s in colspans if s['cat'] == 'apparatus']):
                apparatus.append(''.join(z['text'] for z in vl))

            # renvois marginaux (optionnel)
            if KEEP_XREF:
                for vl in vlines([s for s in colspans if s['cat'] in ('xref', 'xref_key')]):
                    apparatus.append('RENVOI ' + ''.join(z['text'] for z in vl))

    return neg, intro, notes, apparatus


def fmt_ref(t):
    """Normalise « 1: 1 » -> « 1.1 » dans une amorce de note."""
    t = clean(t)
    t = re.sub(r'(\d)\s*:\s*(\d)', r'\1.\2', t)
    return t


MARKER = re.compile(r'^(\d{1,2}\.|[A-Z]\.|[IVXLC]+\.)\s')


def render_neg(name, neg):
    out = [f'# NEG - {name}', '',
           f'> Texte biblique - Nouvelle Edition de Geneve 1979.  '
           f'Source : *La Sainte Bible avec commentaires de John MacArthur* (Societe Biblique de Geneve).',
           '']
    verse = None
    buf = ''
    pend_head = ''

    def flush_verse():
        nonlocal buf
        s = re.sub(r'[ \t]+', ' ', clean(buf)).strip()
        if verse is not None and s:
            out.append(f'**{verse}** {s}')
        buf = ''

    def flush_head():
        nonlocal pend_head
        h = re.sub(r'[ \t]+', ' ', clean(pend_head)).strip()
        if h:
            out.extend(['', f'### {h}', ''])
        pend_head = ''

    for ev in neg:
        if ev['t'] == 'head':
            if not pend_head:
                flush_verse()
            tx = ev['text']
            if pend_head and MARKER.match(clean(tx).strip()):
                flush_head()
                pend_head = tx
            else:
                pend_head = smart_join(pend_head, tx) if pend_head else tx
            continue
        if pend_head:
            flush_head()
        if ev['t'] == 'chap':
            flush_verse()
            out.extend(['', f'## Chapitre {ev["n"]}', ''])
            verse = '1'
            buf = ''
        elif ev['t'] == 'verse':
            if ev['n'] != verse:        # numero repete (verset coupe par une colonne/page) -> fusionner
                flush_verse()
                verse = ev['n']
        elif ev['t'] == 'text':
            buf = smart_join(buf, ev['text'])
    if pend_head:
        flush_head()
    flush_verse()
    return '\n'.join(out).rstrip() + '\n'


def render_jma(name, intro, notes, apparatus):
    out = [f'# JMA - {name}', '',
           f'> Notes d\'etude de *La Sainte Bible avec commentaires de John MacArthur* '
           f'(Societe Biblique de Geneve), texte NEG 1979.', '', '## Introduction', '']

    def finish(parts):
        return re.sub(r'[ \t]+', ' ', clean(smart_reduce(parts))).strip()

    para = []
    for kind, txt in intro:
        if kind == 'H' and 0 < len(txt.strip()) < 55:
            if para:
                out.extend([finish(para), ''])
                para = []
            out.extend([f'### {clean(txt).strip()}', ''])
        else:
            para.append(txt)
    if para:
        out.append(finish(para))

    if apparatus:
        out.extend(['', '## Plan et tableaux', '', finish(apparatus)])

    out.append('')
    out.append('## Notes verset par verset')
    out.append('')
    # assembler les notes : chaque amorce 'ref' demarre un paragraphe
    cur_ref = ''
    cur_body = ''
    blocks = []

    def push():
        if cur_ref or cur_body.strip():
            r = fmt_ref(cur_ref).strip()
            b = re.sub(r'[ \t]+', ' ', clean(cur_body)).strip()
            blocks.append(f'**{r}** {b}'.strip())

    prev = None
    for kind, txt in notes:
        if kind == 'ref':
            if prev == 'note':       # nouvelle note
                push()
                cur_ref, cur_body = '', ''
            cur_ref = smart_join(cur_ref, txt)
        else:
            cur_body = smart_join(cur_body, txt)
        prev = kind
    push()
    out.append('\n\n'.join(blocks))
    return '\n'.join(out).rstrip() + '\n'


def smart_reduce(lines):
    acc = ''
    for l in lines:
        acc = smart_join(acc, l)
    return acc


def main():
    doc = fitz.open(PDF)

    if len(sys.argv) > 1 and sys.argv[1] == '--debug':
        p = int(sys.argv[2])
        for s in sorted(page_spans(doc[p]), key=lambda z: (z['col'], round(z['y0']), z['x0'])):
            print(f"col{s['col']} y={s['y0']:5.0f} x={s['x0']:4.0f} sz={s['size']:4.1f} "
                  f"{s['cat']:11s}| {clean(s['text'])[:52]}")
        return

    targets = BOOKS
    if len(sys.argv) > 1:
        want = sys.argv[1]
        targets = [b for b in BOOKS if b[1] == want or str(b[0]) == want]

    for num, name, start in targets:
        idx = next(k for k, b in enumerate(BOOKS) if b[0] == num)
        end = (BOOKS[idx + 1][2] - 1) if idx + 1 < len(BOOKS) else BACK_MATTER - 1
        neg, intro, notes, apparatus = extract_book(doc, start, end)
        d = os.path.join(os.path.dirname(PDF), f'{num} - {name}')
        with open(os.path.join(d, f'NEG - {name}.md'), 'w', encoding='utf-8') as f:
            f.write(render_neg(name, neg))
        with open(os.path.join(d, f'JMA - {name}.md'), 'w', encoding='utf-8') as f:
            f.write(render_jma(name, intro, notes, apparatus))
        nverse = sum(1 for e in neg if e['t'] == 'verse')
        print(f'{num} - {name}: p.{start}-{end} | {nverse} versets, '
              f'{len(notes)} frag. notes, {len(intro)} l. intro, {len(apparatus)} l. plan')


if __name__ == '__main__':
    main()
