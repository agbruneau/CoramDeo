# -*- coding: utf-8 -*-
"""Extraction AT ciblee depuis « NEG - MacArthur.pdf » pour les 3 series du dossier To Do.
Reutilise integralement la machinerie de extract_nt.py (separation des flux par police).
Produit, par passage vise : NEG - <nom>.md (texte) + JMA - <nom>.md (intro livre + notes du passage).

Usage : python extract_at.py [--inspect]
  --inspect : ecrit dans _at_tmp/ et affiche les diagnostics (ne touche pas aux dossiers finaux).
"""
import fitz, re, os, sys, importlib.util

ROOT = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('ent', os.path.join(ROOT, 'extract_nt.py'))
ent = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ent)
doc = fitz.open(ent.PDF)

# Intro du livre des Psaumes (commune aux 2 series de Psaumes) : p.766-767
PS_INTRO = (766, 769)

# nom affiche | dossier | fichier NEG | fichier JMA | (intro_start, txt_start, txt_end) | chapitres a garder
JOBS = [
    dict(name='Genèse', folder='01 - Genèse',
         neg='NEG - Genèse.md', jma='JMA - Genèse.md',
         intro=32, txt=(46, 62), chapters={str(i) for i in range(1, 12)},
         ps_intro=None),
    dict(name='Psaume 19', folder='19 - Psaume 19',
         neg='NEG - Psaume 19.md', jma='JMA - Psaume 19.md',
         intro=781, txt=(781, 783), chapters={'19'},
         ps_intro=PS_INTRO),
    dict(name='Psaume 119', folder='19 - Psaume 119',
         neg='NEG - Psaume 119.md', jma='JMA - Psaume 119.md',
         intro=863, txt=(863, 869), chapters={'119'},
         ps_intro=PS_INTRO),
]


def keep_neg(neg, chapters):
    out, keep = [], False
    for ev in neg:
        if ev['t'] == 'chap':
            keep = ev['n'] in chapters
        if keep:
            out.append(ev)
    # oter un en-tete orphelin de fin (titre du psaume/chapitre suivant qui precede son numero)
    while out and out[-1]['t'] == 'head':
        out.pop()
    return out


def chap_of_block(block):
    m = re.match(r'\*\*(\d+)[.\s]', block.strip())
    return m.group(1) if m else None


def trim_jma_notes(jma_md, chapters):
    head, sep, notes = jma_md.partition('## Notes verset par verset')
    if not sep:
        return jma_md
    blocks = [b.strip() for b in notes.split('\n\n') if b.strip()]
    # tronquer apres la derniere note numerotee du chapitre cible (oter les orphelins
    # d'un psaume/chapitre voisin dont l'amorce c.v a saute), en gardant les sous-lemmes
    # (None) qui suivent une note numerotee du bon chapitre.
    last_in = max((i for i, b in enumerate(blocks) if chap_of_block(b) in chapters), default=-1)
    if last_in < 0:
        return head + sep + '\n'
    current_in, kept = False, []
    for b in blocks[:last_in + 1]:
        c = chap_of_block(b)
        if c is not None:
            current_in = c in chapters
        if current_in:
            kept.append(b)
    return head + sep + '\n\n' + '\n\n'.join(kept) + '\n'


def build(job):
    name = job['name']
    # texte + notes du passage
    neg, p_intro, notes, app = ent.extract_book(doc, job['intro'], job['txt'][1])
    neg = keep_neg(neg, job['chapters'])
    # intro : pour les Psaumes, prendre l'intro du LIVRE des Psaumes ; sinon l'intro extraite
    if job['ps_intro']:
        _, p_intro, _, app = ent.extract_book(doc, job['ps_intro'][0], job['ps_intro'][1])
    neg_md = ent.render_neg(name, neg)
    jma_md = ent.render_jma(name, p_intro, notes, app)
    jma_md = trim_jma_notes(jma_md, job['chapters'])
    return neg_md, jma_md


def accents(s):
    a = sum(1 for c in s if c in 'éèêëàâäîïôöûùüçÉÈÊËÀÂÄÎÏÔÖÛÙÜÇ')
    return round(a / (len(s.encode('utf-8')) / 1000), 1) if s else 0


def main():
    inspect = '--inspect' in sys.argv
    for job in JOBS:
        neg_md, jma_md = build(job)
        outdir = os.path.join(ROOT, '_at_tmp') if inspect else os.path.join(ROOT, job['folder'])
        os.makedirs(outdir, exist_ok=True)
        with open(os.path.join(outdir, job['neg']), 'w', encoding='utf-8') as f:
            f.write(neg_md)
        with open(os.path.join(outdir, job['jma']), 'w', encoding='utf-8') as f:
            f.write(jma_md)
        chaps = re.findall(r'## Chapitre (\d+)', neg_md)
        nverse = neg_md.count('\n**') + (1 if neg_md.lstrip().startswith('**') else 0)
        nnotes = jma_md.partition('## Notes verset par verset')[2].count('\n\n**')
        print(f"[{job['name']:11s}] NEG: chap={chaps} versets~{nverse} acc={accents(neg_md)}/Ko "
              f"| JMA: notes~{nnotes} acc={accents(jma_md)}/Ko | -> {outdir}")


if __name__ == '__main__':
    main()
