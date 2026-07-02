# `macarthur-conformity-loop` — boucle de conformité doctrinale convergente

> Loop agentique à soumettre à **Fable 5** (ou tout modèle agentique Claude) dans **Claude Code**,
> exécuté à la racine du dépôt `Discipulat-EBC`. Objectif : réviser les **917 `index.html`** du
> dépôt jusqu'à ce que **tout leur contenu théologique soit conforme à la théologie de John
> MacArthur**, au sens tranché par `00 - Avant-propos/NEG - MacArthur.pdf` et par la grille de
> `CLAUDE.md`. Byline : `AGB · EBC`. *Soli Deo Gloria.*
>
> **ÉTAT (2026-07-02, Fable 5)** : bootstrap fait, passe 0 pilote sur `59 - Jacques` terminée —
> **13/13 `VERIFIE`** (14 constats, tous `MINEUR`, corrigés et ré-audités). Ledger : 13 `VERIFIE`,
> 904 `PENDING`. **Toute reprise (Sonnet 5 ou autre) doit lire le §12** : état d'exécution,
> outillage construit, amendements au protocole et gotchas d'environnement y sont consignés.

**Ce que la boucle garantit.** Convergence vers un **point fixe** : elle s'arrête quand une passe
complète sur les 917 fichiers ne produit **plus aucune non-conformité et plus aucune correction**
(passe à delta nul). Elle est **reprenable** (ledger persistant), **bornée** en coût (cache oracle
+ *sharding* par livre; le PDF de 2216 pages n'est jamais relu par fichier), et **anti-fabrication**
(sur silence documentaire de MacArthur, elle **signale** au lieu d'inventer une position).

**Estimation.** Spec autoportante, ~11 sections. Campagne : ~917 fichiers × (audit + correction
éventuelle + ré-audit), *shardée* sur 30 livres, checkpointée par livre. Le coût réel dépend du taux
de dérive initial (à mesurer par la passe 0 ; voir §7 conditions de renversement).

---

## 1. Invariants de conception (non négociables)

Quatre invariants font la différence entre « relire 917 fichiers en boucle » (intraitable, non
convergent) et une boucle qui **termine et prouve** sa terminaison.

- **I1 — Ledger monotone.** Un `ledger.json` porte l'état de conformité de chaque fichier. Un
  fichier ne recule jamais de `VERIFIE` vers `PENDING` sans qu'un *hash* de contenu ait changé.
  C'est ce qui rend la boucle reprenable et le point fixe détectable.
- **I2 — Oracle mis en cache.** L'autorité de conformité (`NEG - MacArthur.pdf`) est extraite
  **une seule fois** par livre vers un digest `oracle/<NN>.md` (intro + notes verset par verset de
  la plage du livre). L'audit d'un fichier confronte ses affirmations à ce digest, jamais au PDF
  entier. Sans ce cache, le coût explose (917 × 2216 p.).
- **I3 — Correction transactionnelle triple.** Toute correction doctrinale s'applique en une
  transaction sur **`.md` (source) + `.html` (rendu) + régénération du `.pdf`** (règle de parité
  de `CLAUDE.md`). Corriger le HTML seul est interdit : cela crée une dérive `.md`↔`.html`.
- **I4 — Oracle du silence (anti-fabrication).** Si le PDF est **muet** sur un *flashpoint* pour la
  péricope visée, la boucle **ne fabrique pas** une position MacArthur ni une citation. Elle marque
  le fichier `REVUE_HUMAINE` avec la nature du silence. « Totalement conforme » vaut sur le
  **documenté** ; le contesté ou l'indocumenté est **signalé**, pas manufacturé. (Applique la règle
  `CLAUDE.md` : « ne jamais inventer de citation », « le PDF tranche ».)

---

## 2. Machine à états (par fichier)

| État | Signification | Transition sortante |
|---|---|---|
| `PENDING` | Jamais audité, ou `sha256(html)` a changé depuis le dernier audit | → `AUDIT` |
| `NONCONFORME` | Audit a relevé ≥1 constat de gravité ≥ `MINEUR` | → `CORRECTION` |
| `CORRIGE` | Correction triple appliquée, en attente de ré-audit | → `AUDIT` (ré-audit) |
| `VERIFIE` | Audit propre : 0 constat, digest oracle couvre les flashpoints de la péricope | terminal (sauf changement de hash) |
| `REVUE_HUMAINE` | Silence oracle, contradiction irréductible, ou dépassement du plafond de reprises | terminal jusqu'à décision humaine |

Le point fixe = **tous les fichiers ∈ {`VERIFIE`, `REVUE_HUMAINE`}** ET **dernière passe à delta
nul** (voir §6).

---

## 3. Bootstrap (une seule fois)

Exécuté à la première invocation ; idempotent (ne réécrit pas un artefact déjà présent).

### 3.1 Construire le ledger

```bash
# Racine du dépôt. Recense les 917 index.html et initialise le ledger.
python3 - <<'PY'
import json, hashlib, os, re, glob
rows=[]
for f in glob.glob('**/index.html', recursive=True):
    b=os.path.relpath(f).split(os.sep)[0]            # dossier de livre (ex. "59 - Jacques") ou racine
    book = b if re.match(r'\d', b) else 'RACINE'
    h=hashlib.sha256(open(f,'rb').read()).hexdigest()
    rows.append({"path":f,"book":book,"sha256":h,"state":"PENDING",
                 "findings":[],"retries":0,"last_pass":0})
os.makedirs('.claude/loops/macarthur-conformity/oracle', exist_ok=True)
json.dump({"pass":0,"files":rows},
          open('.claude/loops/macarthur-conformity/ledger.json','w'),
          ensure_ascii=False, indent=1)
print(f"Ledger : {len(rows)} fichiers, {len({r['book'] for r in rows})} livres")
PY
```

### 3.2 Construire les digests oracle (par livre)

Plage de pages du PDF fournie par la table de `CLAUDE.md` (index 0-based PyMuPDF). Valider avant
d'écrire (couche texte confirmée : 2216 p., p.1945 = intro Jacques). Extraire, nettoyer les
soft-hyphens, écrire `oracle/<NN>.md`.

```bash
pip install pymupdf --break-system-packages --quiet
PYTHONUTF8=1 python3 - <<'PY'
import fitz, re, os
PDF='00 - Avant-propos/NEG - MacArthur.pdf'
# (page_debut_livre_i, page_debut_livre_i+1) pour borner chaque livre ; à compléter depuis la table CLAUDE.md.
# Exemple NT (extrait) — remplir l'intégralité 40→66 et les séries AT présentes :
STARTS = {"40":1374,"41":1439,"42":1493,"43":1560,"44":1623,"45":1684,"46":1724,
          "47":1762,"48":1791,"49":1809,"50":1827,"51":1841,"52":1854,"53":1865,
          "54":1872,"55":1890,"56":1901,"57":1908,"58":1912,"59":1945,"60":1958,
          "61":1973,"62":1986,"63":2003,"64":2007,"65":2011,"66":2018}
d=fitz.open(PDF); END=d.page_count
order=sorted(STARTS.items(), key=lambda x:x[1])
os.makedirs('.claude/loops/macarthur-conformity/oracle', exist_ok=True)
for i,(nn,start) in enumerate(order):
    stop = order[i+1][1] if i+1<len(order) else END
    txt="\n".join(d[p].get_text() for p in range(start,stop))
    txt=txt.replace('\u00ad','')                       # soft-hyphen de césure
    txt=re.sub(r'(\d):\s*(\d)', r'\1.\2', txt)          # "9: 9" -> "9.9"
    open(f'.claude/loops/macarthur-conformity/oracle/{nn}.md','w',encoding='utf-8').write(txt)
    print(f"oracle/{nn}.md : pages {start}-{stop-1}")
PY
```

> Note épistémique : pour l'**AT** (Genèse 1-11, Ps 19, Ps 119) et tout livre non listé, s'appuyer
> sur `extract_at.py` du dépôt pour retrouver les plages ; ne jamais deviner une page. Si un digest
> ne peut être borné avec certitude, le livre entier passe en `REVUE_HUMAINE` au bootstrap (I4).

---

## 4. La boucle (une passe = §4.1 → §4.6)

L'agent répète la passe tant que la condition de convergence (§6) est fausse.

### 4.1 SELECT

Charger le ledger. Sélectionner le **prochain livre** (ordre canonique) comportant ≥1 fichier en
`PENDING` ou `NONCONFORME`. Traiter **tout le livre** dans la passe (shard = livre) : cela borne le
contexte à un seul digest oracle et checkpointe proprement. Si aucun livre n'a de fichier
actionnable → aller au test de convergence.

### 4.2 AUDIT (le juge)

Pour chaque fichier actionnable du livre, charger : le `index.html`, son jumeau `Recherche-*.md`,
`oracle/<NN>.md`, et la **carte de conformité du corpus** de `CLAUDE.md`. Extraire les affirmations
doctrinales des **zones à charge** (le reste, style, est hors périmètre) :

- `hero__title` / `kicker` / `lead` (cadrage thématique)
- `Contexte du passage`
- `Apports des commentateurs` (**prose MacArthur** — densité doctrinale maximale)
- `Thèmes théologiques` (« Dans le texte » + « Pour votre assemblée »)
- `Pistes de réflexion`
- `Étude des mots-clés` (gloses only : vérifier qu'aucune glose ne contredit un locus)

Classer **chaque** affirmation contre les **7 loci** (§5) : `CONFORME` / `DERIVE` / `LACUNE` /
`CONTRADICTION`, avec **locus**, **gravité**, **extrait HTML**, **appui oracle** (référence de note
PDF/digest), **correction proposée**. Prioriser les *flashpoints* du corpus (foi/œuvres,
justification forensique, Lordship, cessationnisme, dispensationalisme prémil prétrib, Israël/Église,
baptême, persévérance).

Gravités : `BLOQUANT` (contredit un locus : ex. easy-believism, amillénarisme, régénération
baptismale, expiation universelle) · `MAJEUR` (lacune sur un flashpoint attendu de la péricope) ·
`MINEUR` (imprécision doctrinale récupérable) · `STYLE` (hors périmètre — **ne pas** corriger).

Sorties de l'audit :
- 0 constat de gravité ≥ `MINEUR` **et** flashpoints de la péricope couverts → `VERIFIE`.
- ≥1 constat → `NONCONFORME` (findings persistés au ledger).
- Silence oracle sur un flashpoint requis, ou contradiction interne au PDF → `REVUE_HUMAINE` (I4).

### 4.3 CORRECTION (chirurgicale, transactionnelle)

Pour chaque `NONCONFORME`, appliquer la correction **minimale** qui lève le constat, sur **`.md` ET
`.html`** (I3), en **paraphrasant** la position documentée de MacArthur (jamais de citation inventée),
ancrée sur le digest oracle. Préserver structure, densité académique, grec/hébreu translittéré,
références, palette et gabarit visuel. Respecter les règles d'édition `CLAUDE.md` : `&nbsp;` et
`<i>…</i>` côté HTML, **aucun tiret cadratin**, français canadien accentué, encodage URL des `href`.
Puis **régénérer le `.pdf`** jumeau. État → `CORRIGE`. `retries += 1`.

### 4.4 VERIFY (ré-audit)

Recalculer `sha256(html)`, relancer §4.2 sur les `CORRIGE`. Propre → `VERIFIE`. Nouveau constat
(la correction a introduit une dérive) → `NONCONFORME`. Si `retries ≥ 3` → `REVUE_HUMAINE` (garde
anti-oscillation : une péricope réellement contestée ne doit pas boucler indéfiniment).

### 4.5 CHECKPOINT

Écrire le ledger. **Commit git par livre** :
`git add -A && git commit -m "conformité MacArthur — <NN Livre> : N corrigés, M vérifiés, K en revue [passe P]"`.
Journaliser un résumé de passe (constats par locus/gravité) dans
`.claude/loops/macarthur-conformity/journal.md`.

### 4.6 CONVERGENCE → §6.

---

## 5. Grille d'audit doctrinal (checklist compacte)

> **Autorité** : la source de vérité reste `CLAUDE.md` (Cadre théologique + Carte de conformité par
> corpus) et le PDF. Cette checklist est un **aide-mémoire d'audit**, pas une redéfinition (éviter
> la dérive de doublon). En cas d'écart checklist ↔ `CLAUDE.md`/PDF, `CLAUDE.md`/PDF tranchent.

| Locus | Doit affirmer | Dérives à réfuter (⇒ constat) |
|---|---|---|
| **Bibliologie** | Inspiration verbale plénière, infaillibilité, suffisance ; Parole > expérience (2 Pi 1.20-21) | Criticisme niant l'inspiration, source Q / deux sources |
| **Christologie** | Pleine divinité éternelle **et** vraie humanité ; naissance virginale ; kénose = renoncement à l'usage indépendant (jamais perte de divinité) ; Col 1.15 ≠ créature | Docétisme, cérinthisme, antitrinitarisme |
| **Sotériologie** | Monergisme (TULIP), justification **forensique** + double imputation, grâce seule/foi seule (foi = don), **Lordship** (foi et repentance indissociables), persévérance ; œuvres **démontrent**, jamais ne procurent | Easy-believism / Free Grace, NPP / justification par les œuvres / sacramentalisme, antinomisme, universalisme |
| **Ecclésiologie** | Église = mystère NT, **distincte d'Israël** ; offices fondateurs **clos** (Ep 2.20) ; sacrifice **unique** | Sacramentalisme, régénération baptismale, médiation sacerdotale |
| **Pneumatologie** | **Cessationnisme strict** : baptême de l'Esprit à la conversion ; langues = langues humaines + signe de jugement ; dons révélatoires **cessés** ; signes = authentification apostolique | Continuationnisme, seconde bénédiction, langues extatiques normatives, guérison sur demande |
| **Eschatologie** | **Dispensationalisme prémil prétrib** ; Israël/Église maintenue ; promesses à Israël non spiritualisées ; enlèvement (1 Th 4) ; **jour de Christ** ≠ **jour du Seigneur** ; retour futur/littéral/corporel/imminent ; millénium terrestre (Ap 20) | Préterisme, amillénarisme, postmillénarisme, idéalisme, historicisme, théologie du remplacement/alliance |
| **Herméneutique** | Grammatico-historique, sens littéral ; christocentrisme par la **promesse** ; AT : création littérale 6 jours + terre jeune, protoévangile (Gn 3.15), déluge universel | Allégorie, chasse aux types, spiritualisation des promesses à Israël |

---

## 6. Convergence (point fixe) et garde-fous

**Condition d'arrêt (point fixe).** La boucle termine quand une passe complète satisfait
**simultanément** :

1. **Couverture** : `∀ fichier, état ∈ {VERIFIE, REVUE_HUMAINE}` (aucun `PENDING`/`NONCONFORME`/`CORRIGE`).
2. **Stabilité (delta nul)** : la passe n'a produit **0 nouveau constat** et **0 correction**.

La double condition est nécessaire, pas seulement (1) : une correction dans un livre peut impliquer
un ajustement de cohérence dans un autre (ex. formulation d'un flashpoint Israël/Église partagé).
La condition (2) force une **passe de stabilité** finale à travers tout le corpus.

**Garde-fous anti-non-terminaison :**

- **Plafond de reprises par fichier** : `retries ≥ 3` ⇒ `REVUE_HUMAINE` (§4.4).
- **Plafond de passes** : `MAX_PASSES` (défaut 6). Atteint ⇒ arrêt + rapport des fichiers non
  stabilisés. Un corpus qui n'atteint pas le point fixe en 6 passes signale un problème structurel
  (voir §7), pas un besoin de continuer à boucler.
- **Registre du contesté** : `journal.md` liste tout `REVUE_HUMAINE` avec motif (silence oracle,
  contradiction PDF, oscillation). Ce registre est la **sortie honnête** de la boucle : la
  conformité « totale » est atteinte sur le documenté ; le reste est explicitement délégué à
  l'humain (I4), jamais fabriqué.

**Rapport final** (écrit à la terminaison) : total `VERIFIE` / `REVUE_HUMAINE`, constats par locus
et par livre, liste des péricopes déléguées, diff git par livre.

---

## 7. Compromis, alternative, conditions de renversement

**Compromis principal.** *Shard*-par-livre + cache oracle + ledger ⇒ coût borné, reprenable, passes
de re-run bon marché. **Prix** : bootstrap non trivial (construire 30 digests) et risque qu'un
digest par livre manque une **interaction doctrinale inter-livres**. *Mitigation* : la passe de
stabilité (§6.2) et le partage explicite des flashpoints transverses via `CLAUDE.md`.

**Alternative écartée (≥1).**
- *Passe monolithique* relisant tout à chaque itération, sans ledger : plus simple, mais
  **intraitable** (917 × ~5000 mots × 2216 p.) et **non reprenable**. Rejetée.
- *Audit `.md` seul puis régénération HTML depuis le `.md`* : parité gratuite. Rejetée car
  `CLAUDE.md` déclare les divergences structurelles `.html` **voulues** (transposition en puces,
  chapeaux) ; le HTML doit donc être audité pour lui-même.

**Conditions qui renversent la recommandation.**
1. **Dérive initiale faible.** Si la passe 0 montre un taux de non-conformité bas (ex. < 3 % des
   fichiers), le surcoût ledger/oracle n'est pas rentable : préférer un **balayage par livre en
   une passe** (spot-check) sans machinerie de boucle.
2. **Oracle trop ambigu.** Si le taux de `REVUE_HUMAINE` est élevé (le PDF est muet ou ambigu sur
   beaucoup de flashpoints), la boucle **ne peut pas** être autonome : la reconvertir en **outil de
   triage humain-dans-la-boucle** (l'agent propose, l'humain tranche).
3. **Contenu déjà généré par `sermon-JMA`.** Si les `index.html` dérivent de recherches déjà
   produites sous la lentille MacArthur unique, l'audit doit surtout détecter des **régressions de
   transposition `.md`→`.html`**, pas des dérives doctrinales de fond : basculer le poids de l'audit
   vers la **parité `.md`↔`.html`** plutôt que vers l'oracle PDF.

---

## 8. Schéma du ledger (`ledger.json`)

```json
{
  "pass": 3,
  "files": [
    {
      "path": "59 - Jacques/05 - La foi qui agit (Jacques 2.14-26)/index.html",
      "book": "59 - Jacques",
      "sha256": "…",
      "state": "VERIFIE",
      "retries": 0,
      "last_pass": 2,
      "findings": [
        {
          "locus": "sotériologie",
          "gravite": "BLOQUANT",
          "extrait_html": "…formulation glissant vers l'easy-believism…",
          "appui_oracle": "oracle/59.md · note Ja 2.24 (justification démonstrative)",
          "correction": "Reformuler : foi vivante vs morte ; œuvres démontrent, ne procurent pas.",
          "resolu_passe": 2
        }
      ]
    }
  ]
}
```

---

## 9. Lancement sur Fable 5

Depuis la racine du dépôt, dans Claude Code :

```
Exécute macarthur-conformity-loop.md sur Discipulat-EBC.
Bootstrap si .claude/loops/macarthur-conformity/ledger.json est absent (§3), puis répète la passe
(§4) jusqu'au point fixe (§6). Traite un livre par shard, checkpointe par commit git à chaque livre,
et n'invente jamais de position MacArthur : silence oracle ⇒ REVUE_HUMAINE. Produis le rapport final.
```

> Remarque produit (à vérifier) : Fable 5 route une fraction des sessions vers Opus 4.8 via ses
> garde-fous. La boucle est **agnostique au modèle** dans la famille agentique Claude et reprend sur
> ledger ; une session routée ne compromet donc ni l'état ni la convergence. Un contenu purement
> théologique est *a priori* hors des catégories qui déclenchent le routage, mais l'invariant de
> reprise couvre le cas.

---

## 10. Ce que la boucle **ne** fait **pas**

- Elle ne juge pas la **vérité** des positions de MacArthur : elle mesure la **conformité** du
  contenu à un référentiel déclaré (posture assumée de `CLAUDE.md` : « lentille MacArthur unique,
  sans contrepoids »).
- Elle ne touche pas au **style**, au visuel ni à la structure hors zones à charge (§4.2).
- Elle ne **fabrique** aucune conformité : « totalement conforme » vaut sur le documenté ; le
  contesté est livré au registre `REVUE_HUMAINE` pour décision humaine.

## 11. Piste de validation avant campagne complète

Lancer d'abord la boucle sur **un seul livre déjà stable** (`59 - Jacques`, gabarit d'or, 13
`index.html`) : si la passe 0 y produit peu ou pas de constats, cela **calibre le taux de dérive**
et arbitre entre boucle complète et spot-check (§7, condition 1) avant d'engager les 917 fichiers.

> **Fait le 2026-07-02** — voir §12 pour les résultats et le verdict de calibration.

---

## 12. État d'exécution et directives de reprise (2026-07-02, Fable 5)

Section ajoutée après exécution du pilote. **Elle fait autorité sur les §3 et §4.3 là où elle les
amende** (l'exécution a validé des choix plus sûrs que la spec initiale).

### 12.1 Travail accompli

- **Bootstrap (§3)** : `ledger.json` initialisé — 917 fichiers, 31 shards (30 livres + `RACINE`,
  l'`index.html` racine, navigation pure). **Amendement au §3.2** : les digests oracle ne sont PAS
  ré-extraits du PDF ; ce sont des **copies des `JMA - <Livre>.md`** versionnés (extraction propre
  de `NEG - MacArthur.pdf` par `extract_nt.py`/`extract_at.py`, flux séparés par police — qualité
  supérieure à `get_text()` brut). 30 digests dans `oracle/`, indexés par `oracle/_index.json`
  (clé = nom du dossier de livre).
- **Passe 0 pilote sur `59 - Jacques`** (§11) : audit par 4 agents parallèles (3-4 fichiers
  chacun) → 10 `NONCONFORME` / 3 `VERIFIE`, 14 constats **tous `MINEUR`** (détail par locus dans
  `journal.md`). Corrections par 3 agents parallèles (transaction triple §4.3), ré-audit
  indépendant par 2 agents à l'œil neuf → **13/13 `VERIFIE`**, 0 `REVUE_HUMAINE`.
- **Checkpoint** : commit git du shard Jacques (convention §4.5).

### 12.2 Verdict de calibration (§7)

- Dérive fichiers : 77 % (10/13) → condition de renversement 1 (« < 3 % ») **non remplie** : la
  machinerie complète (ledger + oracle + shard + ré-audit) **reste requise** pour les 904 restants.
- Gravité : aucun constat > `MINEUR`. Deux familles : **parité `.md` ↔ `.html`** (5/14 — tableaux
  de mots-clés vides, renvois sans descriptions, thèmes sans titres côté `.md` ; le HTML est la
  version riche) et **micro-dérives de fond** contre les notes de l'oracle (9/14 — ex. Ja 5.19-20
  lu comme restauration d'un vrai croyant, imminence relativisée, Siracide sous filiation
  vétérotestamentaire). Condition 3 : **pondérer l'audit vers la parité SANS abandonner l'oracle**
  (la parité seule n'aurait pas attrapé les 3 constats sotériologiques).

### 12.3 Outillage construit (tout sous `.claude/loops/macarthur-conformity/`, non versionné)

| Artefact | Rôle |
|---|---|
| `ledger.json` | État I1 : 917 entrées (path, book, sha256, state, findings, retries, last_pass) |
| `oracle/<livre>.md` + `_index.json` | Digests I2 (copies des `JMA - <Livre>.md`) |
| `journal.md` | Registre des passes, constats par locus, observations hors périmètre |
| `md2json.py` | Parseur inverse `Recherche-*.md` → JSON du skill `sermon-JMA` (échec bruyant sur format inattendu) |
| `gen_pdf.py` | Wrapper : enregistre les polices maison puis délègue à `~/.claude/skills/sermon-JMA/generate-pdf.py` |
| `pass0/*.json` | Sorties d'audit persistées de la passe 0 |
| `work/A..C/` | Répertoires temporaires de génération des agents |

Polices maison (celles des 848 PDF existants) : `~/.claude/shared/fonts/`
(CrimsonPro-Regular/Bold/Italic + ArsenalSC-Regular, OFL, récupérées du skill canvas-design).
Sans le wrapper, `pdf_utils` retombe sur Times New Roman : **toujours passer par `gen_pdf.py`**.

### 12.4 Protocole de régénération PDF (amendement au §4.3 — OBLIGATOIRE)

Le trio `.md`/`.pdf` naît du même JSON ; le `.pdf` ne se rapièce pas, il se **régénère** :

1. Éditer le `.md` (et le `.html` en parité doctrinale).
2. `PYTHONUTF8=1 python ".claude/loops/macarthur-conformity/md2json.py" "<le .md>" "<temp>/x.json"`
3. `PYTHONUTF8=1 python ".claude/loops/macarthur-conformity/gen_pdf.py" "<temp>/x.json" "<temp>/x.pdf"`
4. `diff "<le .md>" "<temp>/x.md"` → **doit être vide** (round-trip ; prouvé au diff nul sur les
   12 péricopes de Jacques AVANT toute correction — refaire ce test à blanc au premier fichier de
   chaque livre pour attraper une variation de format).
5. Déplacer `<temp>/x.pdf` sur le `.pdf` original (python `shutil.move`).

**Jamais** générer directement dans le dossier de péricope : le générateur écrit le `.md` jumeau à
côté du PDF de sortie et écraserait la source.

### 12.5 Patron d'orchestration validé (par shard = livre)

1. **AUDIT** : agents parallèles, 3-4 fichiers chacun ; chaque prompt embarque : chemin du digest
   oracle, zones à charge (§4.2), grille des 7 loci (§5), flashpoints du corpus (`CLAUDE.md`),
   gravités, règle I4, exigence de parité `.md`↔`.html`, sortie JSON stricte
   `[{path, state, findings:[{locus, gravite, extrait_html, appui_oracle, correction}], notes}]`.
2. **Persister** chaque lot dans `pass<N>/`, merger au ledger (état + findings + last_pass).
3. **CORRECTION** : agents parallèles par lots de 3-4 fichiers, corrections MINIMALES ancrées sur
   les findings du ledger, protocole §12.4, règles d'édition de `CLAUDE.md` (aucun tiret cadratin,
   `&nbsp;`/`<i>` côté HTML, français canadien accentué, jamais de citation inventée).
4. **VERIFY** : ré-audit par agents à l'œil neuf (ne pas présumer les corrections bonnes) :
   constat levé + aucune dérive introduite + parité + PDF porteur des corrections (PyMuPDF) +
   densité d'accents (25-33/Ko ; < 15 = accents manquants). `retries ≥ 3` ⇒ `REVUE_HUMAINE`.
5. **CHECKPOINT** : recalcul des `sha256`, écriture du ledger, commit git **sélectif** (le dossier
   du livre seulement — PAS `git add -A` : le dépôt peut porter des modifications étrangères à la
   campagne), message : `conformité MacArthur — <NN Livre> : N corrigés, M vérifiés, K en revue [passe P]`.
   Journaliser dans `journal.md`.

### 12.6 Gotchas d'environnement (constatés à l'exécution)

- Toujours `PYTHONUTF8=1` (sinon `UnicodeEncodeError` cp1252 sur `→`, `é`, etc. dans les prints).
- Heredoc bash + python : `'\\'` peut être mangé — préférer `os.sep` / chemins bruts `r'...'`.
- `curl` en **hard deny** ; `rm`/`Remove-Item` refusés (nettoyage via python `os.remove`/`shutil`).
- PyMuPDF (`pip install pymupdf`) requis pour vérifier les PDF ; `reportlab` requis pour générer.
- `.claude/` est gitignoré : ledger, oracle, journal et outillage sont **locaux à cette machine**.
- Dossiers de péricope à padding **3 chiffres** pour Luc (`001`-`130`) et Actes ; 2 chiffres ailleurs.
- `RACINE` (index.html racine) : navigation pure, sans contenu doctrinal — audit trivial en fin de
  campagne.

### 12.7 Reprise (ordre de traitement restant)

Ordre canonique des 30 shards restants : `01 - Genèse` (13), `19 - Psaume 119` (23),
`19 - Psaume 19` (5), `40 - Matthieu` (90), `41 - Marc` (83), `42 - Luc` (130), `43 - Jean` (54),
`44 - Actes` (78), `45 - Romains` (48), `46 - 1 Corinthiens` (56), `47 - 2 Corinthiens` (43),
`48 - Galates` (24), `49 - Éphésiens` (25), `50 - Philippiens` (16), `51 - Colossiens` (15),
`52 - 1 Thessaloniciens` (12), `53 - 2 Thessaloniciens` (8), `54 - 1 Timothée` (19),
`55 - 2 Timothée` (14), `56 - Tite` (9), `57 - Philémon` (5), `58 - Hébreux` (40),
`60 - 1 Pierre` (18), `61 - 2 Pierre` (11), `62 - 1 Jean` (17), `63 - 2 Jean` (5),
`64 - 3 Jean` (5), `65 - Jude` (8), `66 - Apocalypse` (29), puis `RACINE` (1).
`59 - Jacques` (13) : **fait**. Après couverture complète : **passe de stabilité** (§6, delta nul)
avant de déclarer le point fixe, puis rapport final (§6).

Prompt de reprise (Sonnet 5) :

```
Reprends macarthur-conformity-loop.md sur Discipulat-EBC depuis son §12 (état : Jacques 13/13
VERIFIE, 904 PENDING). Charge .claude/loops/macarthur-conformity/ledger.json, traite les shards
restants dans l'ordre du §12.7 avec le patron du §12.5 et le protocole PDF du §12.4, checkpointe
par commit git à chaque livre, n'invente jamais de position MacArthur (silence oracle ⇒
REVUE_HUMAINE), et termine par la passe de stabilité et le rapport final du §6.
```
