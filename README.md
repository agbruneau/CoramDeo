# Études bibliques et préparation de prédication

> Ressource d'étude biblique et de préparation de prédication pour l'**Église Baptiste de
> Charlesbourg** (Québec ; pasteur Simon Ouellette). Le **Nouveau Testament est couvert en entier**
> (27 livres), complété par des **séries de l'Ancien Testament** (Genèse 1-11, Psaume 19, Psaume
> 119).

Ce dépôt rassemble le matériel produit pour des **expositions suivies** (*lectio continua*),
livre par livre. Pour chaque livre traité : un **plan de série de prédications**, une **recherche
exégétique** par péricope, une **recherche globale** d'introduction, une **page de présentation
web**, le **texte biblique de référence** (NEG 1979) et les **notes d'étude de John MacArthur**, le
tout dans un cadre baptiste réformé conforme à la théologie de MacArthur.

Les livres sont rangés dans des dossiers numérotés selon l'ordre canonique des **66 livres de la
Bible protestante** (39 livres de l'Ancien Testament, puis 27 du Nouveau) : `01 - Genèse` à
`66 - Apocalypse`. Le dossier `00 - Avant-propos/` réunit les pièces fondatrices du projet.

---

## `00 - Avant-propos/` : les fondations du dépôt

Avant les livres bibliques eux-mêmes, ce dossier rassemble les **références d'autorité**, les
**standards doctrinaux** et les **ressources spirituelles** qui encadrent tout le travail, ainsi
que l'**outillage** de production. C'est le socle sur lequel reposent toutes les recherches et
toutes les séries.

### Référence d'autorité doctrinale

- **[`NEG - MacArthur.pdf`](<00 - Avant-propos/NEG - MacArthur.pdf>)** : *La Sainte Bible avec
  commentaires de John MacArthur* (Société Biblique de Genève) sur le texte NEG 1979, soit la Bible
  complète (Ancien et Nouveau Testaments, **2216 pages**), avec pour chaque livre une introduction
  (titre, auteur et date, contexte, thèmes historiques et théologiques, problèmes d'interprétation,
  plan) puis le texte accompagné des notes d'étude verset par verset. C'est la **source qui tranche
  la conformité doctrinale** de tout le matériel produit ; elle prime sur la mémoire et sur les
  sources générales. Les fichiers de référence par livre (`NEG - <Livre>.md` et `JMA - <Livre>.md`)
  en sont extraits.

### Standards doctrinaux de l'Église

- **[`Confession de foi-EBC.pdf`](<00 - Avant-propos/Confession de foi-EBC.pdf>)** : la confession
  de foi de l'Église Baptiste de Charlesbourg (révisée en 2016). Elle énonce, article par article,
  les convictions de l'assemblée : autorité et inerrance des Écritures (66 livres), Trinité,
  création littérale en six jours, prémillénarisme prétribulationniste, retour imminent et corporel
  du Christ. Elle **ancre dans la vie de l'Église** le cadre théologique sous lequel le dépôt est
  produit.

### Ressources de discipulat et de piété

- **[`PrecisDicipulat.md`](<00 - Avant-propos/PrecisDicipulat.md>)** (et son `.pdf`) : un *Précis
  du discipulat chrétien*. Il pose que le discipulat **est** la vie chrétienne elle-même (et non un
  second niveau facultatif) : fruit nécessaire de la régénération, suivre Christ comme Seigneur
  (*Lordship Salvation*), nourri par la Parole suffisante, vécu dans l'Église locale et transmis
  par le mentorat, en vue de la conformité à Christ. Cadre MacArthur, sources documentées.
- **[`Coram Deo.pdf`](<00 - Avant-propos/Coram Deo.pdf>)** : ressource d'accompagnement pastoral
  — une page unique au format affiche (685 × 1391 pt), sans couche texte : c'est une image.
  *(Elle remplace `Coram Christo.pdf`, retiré du dépôt le 11 juillet 2026 —
  commits `ce7c098` et `72578e4`.)*
- **[`Vallée de la Vision/`](<00 - Avant-propos/Vallée de la Vision>)** : *La Vallée de la Vision*
  (`Vallée de la Vision.pdf`), le recueil de prières et de méditations puritaines (édition
  française, Publications Chrétiennes, 2023), soutien de la vie de prière personnelle et pastorale,
  accompagné d'une étude biblique PowerPoint (`La-Vallee-de-la-Vision-Etude-biblique.pptx`).
- **[`Puritains/`](<00 - Avant-propos/Puritains>)** : ressources complémentaires sur la
  spiritualité puritaine, un essai (`Essai - Les puritains.docx`), une synthèse
  (`Synthèse - Puritains.docx`) et une présentation
  (`Puritain - Toute la vie pour la gloire de Dieu.pptx`). Le dossier porte aussi
  **[`Guide Étude Biblique.md`](<00 - Avant-propos/Puritains/Guide Étude Biblique.md>)**
  (déposé le 25 juillet 2026) : une méthode d'étude personnelle — lecture quotidienne, notes
  manuscrites en Bible à marges larges, archivage en Bible intercalaire, langues originales.
  ⚠ *Ce guide décrit une méthode de travail ; il ne fait autorité sur aucun point doctrinal —
  cette autorité reste au `NEG - MacArthur.pdf`.*

### Outillage de production

- **`extract_nt.py`** et **`extract_at.py`** : régénèrent les fichiers de référence
  `NEG - <Livre>.md` / `JMA - <Livre>.md` depuis `NEG - MacArthur.pdf` (séparation des flux texte
  biblique / notes d'étude par police et taille ; exigent PyMuPDF).
- **`md-to-pdf.py`** : rend un `.md` en PDF au style maison, noir et orange (exige reportlab).
  Usage : `python md-to-pdf.py <fichier.md> [sortie.pdf]`. Ce n'est **pas un parseur Markdown
  général** : il ne couvre que les constructions présentes dans `PrecisDicipulat.md` (`#`, `##`,
  `###`, citations `>`, listes `-`, tableaux `|`, `**`, `*`) et insère une signature datée fixe
  sous le sous-titre. C'est l'outil qui a produit `PrecisDicipulat.pdf`.

---

## Couverture biblique

### Nouveau Testament : 27/27 livres complets

L'intégralité du Nouveau Testament est traitée : pour chaque livre, une série figée, une recherche
globale, une page d'accueil et **toutes les péricopes** (recherche `.md`, export `.pdf`, page
`index.html`), la réunion des péricopes recomposant le livre de son premier à son dernier verset.

| # | Livre | Péricopes | # | Livre | Péricopes |
|---|---|---|---|---|---|
| 40 | Matthieu | 89 | 54 | 1 Timothée | 18 |
| 41 | Marc | 82 | 55 | 2 Timothée | 13 |
| 42 | Luc | 129 | 56 | Tite | 8 |
| 43 | Jean | 53 | 57 | Philémon | 4 |
| 44 | Actes | 77 | 58 | Hébreux | 39 |
| 45 | Romains | 47 | 59 | Jacques | 12 |
| 46 | 1 Corinthiens | 55 | 60 | 1 Pierre | 17 |
| 47 | 2 Corinthiens | 42 | 61 | 2 Pierre | 10 |
| 48 | Galates | 23 | 62 | 1 Jean | 16 |
| 49 | Éphésiens | 24 | 63 | 2 Jean | 4 |
| 50 | Philippiens | 15 | 64 | 3 Jean | 4 |
| 51 | Colossiens | 14 | 65 | Jude | 7 |
| 52 | 1 Thessaloniciens | 11 | 66 | Apocalypse | 28 |
| 53 | 2 Thessaloniciens | 7 | | | |

L'épître de **Jacques** (12 péricopes plus site de présentation) est le **gabarit de référence**
(structure et système visuel) sur lequel les autres livres ont été modelés.

### Ancien Testament : séries complètes

Des séries de l'Ancien Testament ont été amenées au même niveau d'achèvement que le NT.

| # | Livre / portée | Série | Péricopes | État |
|---|---|---|---|---|
| 01 | Genèse 1 à 11 (« De Babel à Abraham ») | ✓ | 12 | Complet |
| 19 | Psaume 19 (« Dieu a parlé ») | ✓ | 4 | Complet |
| 19 | Psaume 119 (« Une lampe à mes pieds ») | ✓ | 22 (par strophes) | Complet |

---

## Cadre théologique

Tout le contenu est élaboré dans un cadre **baptiste réformé, conforme à la théologie de John
MacArthur** (Master's Seminary), en accord avec la
[confession de foi de l'Église](<00 - Avant-propos/Confession de foi-EBC.pdf>). La lecture est
volontairement faite à travers la **seule lentille de MacArthur** ; en cas de divergence
d'interprétation, c'est sa lecture qui tranche, et le `NEG - MacArthur.pdf` arbitre.

- herméneutique grammatico-historique, sens littéral, exposition suivie du texte ;
- **bibliologie** : inspiration verbale et plénière, infaillibilité et suffisance de l'Écriture ;
- **christologie** : pleine divinité éternelle et vraie humanité du Dieu-homme, naissance
  virginale ;
- **sotériologie** : élection, appel efficace et régénération monergiques (TULIP), justification
  forensique par la grâce seule au moyen de la foi seule (la foi étant elle-même un don), avec
  double imputation ; *Lordship salvation* (foi et repentance indissociables) ; persévérance des
  saints ; les œuvres **démontrent** la foi sans jamais mériter ni produire le salut (« la foi
  seule sauve, mais la foi qui sauve n'est jamais seule ») ;
- **ecclésiologie** : l'Église, mystère révélé dans le NT, distincte d'Israël ; sacerdoce de tous
  les croyants ; sacrifice unique de Christ (ni répétition sacrificielle ni régénération
  baptismale) ;
- **pneumatologie** : cessationnisme strict (les dons miraculeux et révélatoires ont cessé) ; le
  baptême de l'Esprit intervient à la conversion ;
- **eschatologie** : dispensationaliste et prémillénariste prétribulationniste ; distinction
  Israël / Église, promesses faites à Israël non spiritualisées, retour du Seigneur futur,
  littéral et imminent, suivi d'un règne millénaire terrestre.

Sources de référence : *La Bible d'étude MacArthur*, le *MacArthur New Testament Commentary*,
gty.org et *Biblical Doctrine* (MacArthur et Mayhue).

---

## Anatomie d'un livre traité

Chaque dossier de livre (`NN - <Livre>/`) contient :

- **`NEG - <Livre>.md`** : le **texte biblique** (NEG 1979), découpé en `## Chapitre N` puis en
  titres de section repris du plan MacArthur (`### I. Le test de la persévérance… (1: 2-12)`),
  chaque verset ouvert par son numéro en gras (`**2**`). Pas d'appareil de renvois marginaux.
  Les quatre livres à chapitre unique — Philémon, 2 Jean, 3 Jean, Jude — n'ont pas de niveau
  `## Chapitre` : leur texte s'ouvre directement sur le premier `### `.
- **`JMA - <Livre>.md`** : les **notes d'étude de *La Bible d'étude MacArthur*** (introduction du
  livre, plan, puis notes verset par verset). Ces deux fichiers sont **tirés exclusivement** de
  `NEG - MacArthur.pdf` et ne portent que sur le livre de leur dossier.
- **`00 - Introduction/`** : le **plan de série** (`Serie.md` / `.pdf`), la **recherche globale**
  du livre (`Recherche.md` / `.pdf`), la **page d'accueil** (`index.html`) et le logo
  (`LogoEBC.avif`).
- **`NN - <titre> (Réf c.v-v)/`** : un dossier par semaine de prédication (péricope), contenant la
  recherche exégétique (`Recherche-MacArthur-<Livre>-<c>-<v>-<v>.md` plus son `.pdf` : dans le nom
  de fichier, la référence s'écrit tout en traits d'union — `Recherche-MacArthur-Jacques-2-14-26.md`
  pour le dossier `05 - La foi qui agit (Jacques 2.14-26)`) et une page web `index.html`. Le numéro
  de semaine `NN` est sur deux chiffres (trois pour Luc et Actes).

**Gabarit d'une recherche exégétique** : Contexte du passage ; Arrière-plan historique et culturel ;
Étude des mots-clés (tableau de traductions comparées S21 / NEG79 / Darby / LSG / KJF) ; Apports des
commentateurs (prose MacArthur) ; Renvois et passages parallèles ; Thèmes théologiques (« Dans le
texte » plus « Pour votre assemblée ») ; Pistes de réflexion.

---

## Le site web

Chaque livre traité possède une **page de présentation** `00 - Introduction/index.html` et chaque
péricope sa propre page `index.html` : des pages web autonomes (HTML, CSS et JavaScript, sans
dépendance de build) reprenant un même système visuel (thème sombre à accents ambrés, polices serif
*Cormorant Garamond* et *EB Garamond*, barre de progression de lecture, révélation au défilement).
Le modèle de référence est
[`59 - Jacques/00 - Introduction/index.html`](<59 - Jacques/00 - Introduction/index.html>).

Un **index de navigation** [`index.html`](index.html) à la racine du dépôt fédère l'ensemble : il
relie les 30 pages de présentation des livres, regroupées par sections (Ancien Testament,
Évangiles, Histoire, épîtres pauliniennes, épîtres générales, Apocalypse), et pointe vers la
ressource *Coram Deo*. La navigation est **aller-retour** : chaque page de présentation renvoie
à cet index (« Tous les livres ») et chaque péricope renvoie à la présentation de son livre.

**Pour consulter une page :** l'ouvrir dans un navigateur. Aucune page n'appelle de ressource
externe (ni feuille de style, ni script, ni fonte distante) : *Cormorant Garamond* et *EB Garamond*
sont simplement déclarées en CSS avec repli sur Georgia et Times New Roman. Tout fonctionne hors
ligne.

---

## Structure du dépôt

```
.
├── README.md
├── index.html                                Index de navigation racine (les 30 livres + Coram Deo)
├── LogoEBC.avif                              Logo référencé par l'index racine
│
├── 00 - Avant-propos/                        Fondations : références, doctrine, piété, outillage
│   ├── NEG - MacArthur.pdf                    La Bible d'étude MacArthur (NEG) : arbitre de conformité
│   ├── Confession de foi-EBC.pdf             Confession de foi de l'Église (rév. 2016)
│   ├── PrecisDicipulat.md / .pdf             Précis du discipulat chrétien
│   ├── Coram Deo.pdf                         Ressource d'accompagnement pastoral (1 p., affiche image)
│   ├── Vallée de la Vision/                  Recueil de prières puritaines (PDF + étude PowerPoint)
│   ├── Puritains/                            Ressources puritaines + Guide Étude Biblique.md
│   └── extract_nt.py, extract_at.py, md-to-pdf.py   Outillage de production
│
├── 01 - Genèse/                              AT : Genèse 1 à 11 (série complète)
├── 19 - Psaume 19/  19 - Psaume 119/         AT : séries de Psaumes
│                                             (les 3 dossiers AT ont l'arborescence interne ci-dessous)
│
├── 40 - Matthieu/ … 66 - Apocalypse/         Nouveau Testament : les 27 livres (complets)
│   ├── NEG - <Livre>.md                       Texte biblique (NEG 1979)
│   ├── JMA - <Livre>.md                       Notes d'étude (La Bible d'étude MacArthur)
│   ├── 00 - Introduction/                     Série, recherche globale, page d'accueil, logo
│   └── NN - <titre> (Réf c.v-v)/              Un dossier par péricope (.md + .pdf + index.html)
```

Pour chaque recherche, le `.md` est la source rédigée et le `.pdf` en est l'export mis en page.
Les artefacts d'outillage local (p. ex. `ruvector.db`), le cache Python et les fichiers temporaires
sont exclus du dépôt via `.gitignore`.

---

## Crédits

- **Église Baptiste de Charlesbourg**, Charlesbourg (Québec) ; pasteur Simon Ouellette.
- Recherches et séries signées **AGB · EBC**.
- Textes bibliques : Nouvelle Édition de Genève 1979 (NEG) ; textes originaux NA28 / BHS.
- Notes d'étude : *La Sainte Bible avec commentaires de John MacArthur* (Société Biblique de
  Genève).

*Soli Deo Gloria.*
