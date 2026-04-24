# PRD — Landing Page « Coram Deo »

**Version :** 1.0
**Date :** 2026-04-23
**Auteur :** André-Guy Bruneau
**Source :** Prototype papier manuscrit (Coram Deo.pdf)
**Statut :** Brouillon pour implémentation

---

## 1. Vue d'ensemble

### 1.1 Contexte
Le prototype papier présente un schéma théologique réformé structuré en mind-map manuscrit, intitulé **« Coram Deo »** (locution latine signifiant *« devant la face de Dieu »*, concept cher à R.C. Sproul). Le document synthétise une vision pastorale complète articulant l'Évangile, la Trinité-Providence, le Pensum (disciplines chrétiennes) et le Disciple.

### 1.2 Objectif du produit
Transposer fidèlement ce schéma manuscrit en une **landing page HTML unique, statique, responsive, en thème sombre (dark mode) avec accent orange**, servant de porte d'entrée visuelle et conceptuelle à un ministère ou ressource en ligne de théologie réformée francophone.

### 1.3 Proposition de valeur
- Offrir une **cartographie visuelle immédiate** de la vision Coram Deo.
- Servir de **référence rapide** pour disciples, pasteurs, étudiants en théologie.
- Établir une **identité visuelle chaleureuse et contemplative** (dark + orange = atmosphère de lampe à huile, de veille théologique, rappel patristique).

---

## 2. Persona cible

| Persona | Profil | Besoin |
|---|---|---|
| **Le disciple** | Chrétien engagé, lecteur régulier de la Bible | Vue d'ensemble mémorisable de sa marche chrétienne |
| **Le pasteur / prédicateur** | Ministre réformé | Cadre systématique pour prédication expositoire |
| **L'étudiant en théologie** | Séminariste, auditeur libre | Schéma pédagogique articulé (systématique + pratique) |
| **Le visiteur curieux** | Chercheur spirituel | Première exposition claire à la théologie réformée |

---

## 3. Analyse détaillée du prototype papier

Le schéma manuscrit se décompose en **cinq grandes sections verticales** reliées par des accolades latérales et un diagramme central en triangle.

### 3.1 Section A — **Évangile** (accolade gauche)

#### 3.1.1 Vision → Luc
- **Christologie** ⇒ Emmanuel
  - Prophète
  - Sacrificateur
  - Roi / Seigneur
  - *Référence : Hébreux*
- **Ecclésiologie** ⇒ Corps du Christ
  - Anthropologie — *Romains 7*
  - Sotériologie — *Romains 8*
  - Eschatologie — *Apocalypse 21*

#### 3.1.2 Mission → Actes
- **Matthieu 22.37-40** (les deux commandements) :
  - Aime ton Dieu
  - Aime ton prochain
- **Matthieu 28.19-20** (la Grande Commission) :
  - Faire des disciples
  - Enseigner, mentorer

#### 3.1.3 Pérégrination → Hébreux / Romains
(La vie chrétienne comme pèlerinage — étrangers et voyageurs)

### 3.2 Section B — **Trinité-Providence** (diagramme central en triangle)

Triangle équilatéral avec une **croix rose/violette au centre** :

```
              PÈRE
             (croix)
            /       \
           /         \
     Parole         Paraclet
         /    ┌─────┐   \
        /     │Prédic.│    \
       /      │Prière │     \
      /       │Piété  │      \
     /        └─────┘         \
   FILS ────────────── SAINT-ESPRIT
         Trinité-Providence
```

- **Références bibliques adjacentes** :
  - Genèse 1 à 11 (côté gauche)
  - Psaume 19 (côté droit)
  - Psaume 119 (côté droit)

### 3.3 Section C — **Pensum** (accolade gauche — disciplines)

- **Parole** ⇒ Théologie Systématique
- **Prédication** ⇒ Expositoire / Thématique
- **Prière** ⇒ Adoration, Confession, Supplication, Intercession, Doxologie (**ACSID**)
- **Piété** ⇒ Orthodoxie / Orthopraxie (Foi / Œuvre)
- **Paraclet** ⇒ appelé à côté du disciple
  - Convaincre le monde
  - Enseigner et rappeler
  - Intercéder et consoler

### 3.4 Section D — **Disciple** (accolade gauche)

#### 3.4.1 Communion avec la Trinité
- **Père** : origine, architecte, souverain
- **Fils** : médiateur, exécuteur
- **Saint-Esprit** : applicateur, vérificateur

#### 3.4.2 Homme racheté (quatre relations)
1. Homme pieux avec son Dieu
2. Homme pieux avec les autres
3. Homme pieux et son travail
4. Homme pieux et sa fin

### 3.5 Section E — **Conclusion / Doxologie**
- **« Révérer l'Éternel »**
- *Ecclésiaste 12.13-14* (« Crains Dieu et observe ses commandements… »)

---

## 4. Exigences fonctionnelles

### EF-1 — Structure narrative de la page (one-page scroll)
La landing page DOIT présenter les sections dans l'ordre suivant, en scroll vertical :

1. **Hero** — Titre « Coram Deo » + sous-titre + Ecclésiaste 12.13-14 ou tagline
2. **Évangile** — Vision / Mission / Pérégrination (3 colonnes ou cartes)
3. **Trinité-Providence** — diagramme triangulaire interactif (SVG)
4. **Pensum** — liste des cinq disciplines (Parole, Prédication, Prière, Piété, Paraclet)
5. **Disciple** — Communion trinitaire + Homme racheté (4 relations)
6. **Doxologie finale** — « Révérer l'Éternel » + Ecclésiaste 12.13-14 en pleine largeur
7. **Footer** — crédits, références bibliques, liens éventuels

### EF-2 — Diagramme trinitaire SVG
- Triangle équilatéral en SVG natif (scalable, pas d'image bitmap).
- Trois sommets étiquetés : **Père** (haut), **Fils** (bas-gauche), **Saint-Esprit** (bas-droit).
- Croix orange au centre du triangle.
- Arêtes étiquetées : **Parole** (Père↔Fils) et **Paraclet** (Père↔Saint-Esprit).
- Zone intérieure listant : **Prédication / Prière / Piété**.
- Base du triangle : libellé **« Trinité-Providence »**.
- Au survol (hover) de chaque sommet/arête → infobulle avec référence biblique (Genèse 1-11, Psaume 19, Psaume 119).

### EF-3 — Navigation
- Barre de navigation fixe (sticky) en haut, transparente au repos, opaque au scroll.
- Ancres vers chaque section : Évangile · Trinité · Pensum · Disciple · Doxologie.
- Défilement doux (`scroll-behavior: smooth`).

### EF-4 — Références bibliques
- Toutes les références bibliques DOIVENT apparaître en **texte lisible** (pas seulement en attribut).
- Format standard : « Matthieu 22.37-40 » (version NEG 1979 ou Segond 21 à confirmer).
- Style visuel distinctif (couleur orange atténuée, italique ou petite capitale).

### EF-5 — Contenu textuel complet
La page DOIT intégrer **100 %** des éléments du prototype papier — aucune omission du schéma manuscrit.

### EF-6 — Responsive
- Desktop (≥ 1024 px) : mise en page multi-colonnes, diagramme large.
- Tablette (768-1023 px) : réorganisation en 2 colonnes.
- Mobile (≤ 767 px) : empilement vertical complet, diagramme adapté.

---

## 5. Exigences non-fonctionnelles

### ENF-1 — Palette dark mode + orange
| Usage | Couleur | Hex |
|---|---|---|
| Fond principal | Gris très foncé | `#0F0F10` |
| Fond élevé (cartes) | Charbon | `#1A1A1D` |
| Bordures subtiles | Gris ardoise | `#27272A` |
| Texte principal | Blanc cassé | `#F5F5F4` |
| Texte secondaire | Gris clair | `#A1A1AA` |
| Accent primaire (orange) | Orange braise | `#F97316` |
| Accent primaire hover | Orange vif | `#FB923C` |
| Accent profond (croix, titres) | Orange ambre | `#EA580C` |
| Référence biblique | Orange pâle | `#FED7AA` |

### ENF-2 — Typographie
- **Titres** : serif moderne et solennel — `Cormorant Garamond` ou `Crimson Pro` (Google Fonts).
- **Corps** : sans-serif neutre et lisible — `Inter` ou `Geist`.
- **Accent liturgique / locutions latines** : italique serif.
- Échelle typographique : `clamp()` pour fluid typography (ex. `clamp(2rem, 5vw, 4.5rem)` pour H1).

### ENF-3 — Performance
- Un seul fichier `index.html` autonome, CSS inline ou `<style>` intégré.
- Aucune dépendance JavaScript externe (ou minimale — vanilla JS uniquement).
- Poids total < 150 KB (hors polices web).
- Score Lighthouse ≥ 95 sur Performance, Accessibilité, SEO.

### ENF-4 — Accessibilité (WCAG 2.1 AA)
- Contraste texte / fond ≥ 4.5:1 (le combo `#F5F5F4` sur `#0F0F10` = 17.5:1 ✓).
- Structure sémantique HTML5 : `<header>`, `<main>`, `<section>`, `<article>`, `<footer>`.
- Hiérarchie correcte des titres `<h1>` → `<h3>`.
- SVG du triangle : attribut `role="img"` + `<title>` + `<desc>`.
- Support clavier complet (focus visible en orange).
- `prefers-reduced-motion` respecté.

### ENF-5 — SEO & métadonnées
- `<title>` : « Coram Deo — Devant la face de Dieu »
- `<meta name="description">` : synthèse de la vision en ≤ 160 caractères.
- Open Graph + Twitter Card (image OG à générer ultérieurement).
- Balises `lang="fr"`, charset UTF-8, viewport responsive.
- Schéma JSON-LD `WebPage` minimal.

### ENF-6 — Compatibilité navigateurs
- Chrome, Edge, Firefox, Safari (deux dernières versions majeures).
- Dégradation gracieuse sur navigateurs sans `backdrop-filter`.

---

## 6. Parti pris esthétique et voix éditoriale

### 6.1 Atmosphère visuelle
- **Contemplative et solennelle** — éviter tout effet tape-à-l'œil.
- **Dark mode liturgique** — évoque la lampe à huile, la veille de prière, le manuscrit patristique.
- **Orange = flamme, braise, Pentecôte** — rappel discret du Saint-Esprit et de la Parole « comme un feu » (Jérémie 23.29).
- Micro-animations sobres : fade-in au scroll, pas de parallax agressif.

### 6.2 Voix éditoriale
- **Ton** : pastoral, confessant, révérentiel.
- **Français soutenu** sans jargon inaccessible.
- **Fidélité au vocabulaire réformé** : « Éternel » (YHWH), « pensum », « pérégrination », « Paraclet ».
- Aucun anglicisme de marketing (pas de « empower », « journey »…).

### 6.3 Éléments graphiques suggérés
- Filet orange fin (1 px) en séparateur de sections.
- Croix stylisée en SVG (clin d'œil à la croix centrale du prototype).
- Accolades décoratives SVG à gauche des grandes sections (fidélité au manuscrit).
- Fond subtil : texture bruit (`noise.svg`) à 2-3 % d'opacité pour éviter le « plat numérique ».

---

## 7. Architecture de l'information & wireframe textuel

```
┌─────────────────────────────────────────────────────┐
│  [Nav sticky] Évangile · Trinité · Pensum · Disciple │
├─────────────────────────────────────────────────────┤
│                                                     │
│              C O R A M   D E O                      │
│           « Devant la face de Dieu »                │
│     Ecclésiaste 12.13 — Crains Dieu et observe      │
│                                                     │
├─────────────────────────────────────────────────────┤
│  I. L'ÉVANGILE                                      │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐              │
│  │ Vision  │  │ Mission │  │Pérégrin.│              │
│  │  (Luc)  │  │ (Actes) │  │(Héb/Rom)│              │
│  └─────────┘  └─────────┘  └─────────┘              │
├─────────────────────────────────────────────────────┤
│  II. LA TRINITÉ-PROVIDENCE                          │
│                   [SVG Triangle]                    │
│           Père / Fils / Saint-Esprit                │
│        Parole ─ Prédication ─ Paraclet              │
│              Prière · Piété                         │
├─────────────────────────────────────────────────────┤
│  III. LE PENSUM                                     │
│  • Parole → Théologie Systématique                  │
│  • Prédication → Expositoire / Thématique           │
│  • Prière → A.C.S.I.D.                              │
│  • Piété → Orthodoxie / Orthopraxie                 │
│  • Paraclet → Convainc, Enseigne, Intercède         │
├─────────────────────────────────────────────────────┤
│  IV. LE DISCIPLE                                    │
│  Communion trinitaire (3 rôles)                     │
│  Homme racheté (4 relations)                        │
├─────────────────────────────────────────────────────┤
│  V. RÉVÉRER L'ÉTERNEL                               │
│       Ecclésiaste 12.13-14 (pleine largeur)         │
└─────────────────────────────────────────────────────┘
│  Footer : références · crédits                      │
└─────────────────────────────────────────────────────┘
```

---

## 8. Livrables

| # | Livrable | Format | Notes |
|---|---|---|---|
| 1 | `index.html` | HTML5 autonome | CSS intégré, SVG inline |
| 2 | `PRD.md` | Markdown | Ce document |
| 3 | (optionnel) `favicon.svg` | SVG | Croix orange stylisée |
| 4 | (optionnel) `og-image.png` | PNG 1200×630 | Image Open Graph |

---

## 9. Critères d'acceptation

- [ ] Tous les éléments textuels du prototype papier sont présents (vérification croisée section par section).
- [ ] Le diagramme trinitaire est en SVG natif, responsive, avec tooltips.
- [ ] Thème sombre avec accent orange conforme à la palette ENF-1.
- [ ] Score Lighthouse ≥ 95 sur les quatre catégories.
- [ ] Responsive vérifié sur 375 px, 768 px, 1024 px, 1440 px.
- [ ] Toutes les références bibliques sont lisibles et correctement formatées.
- [ ] Navigation sticky fonctionnelle avec ancres.
- [ ] Aucune erreur console, aucun warning HTML/CSS (W3C validator).
- [ ] Testé sur Chrome, Firefox, Safari, Edge (dernières versions).

---

## 10. Hors périmètre (non-goals)

- Pas de CMS, pas de backend.
- Pas de formulaire d'inscription / newsletter (phase 2).
- Pas de traduction multilingue (français uniquement).
- Pas d'intégration audio/vidéo de prédications (phase 2).
- Pas de système de commentaires ou interaction sociale.

---

## 11. Risques et mitigations

| Risque | Impact | Mitigation |
|---|---|---|
| Densité théologique trop forte pour un visiteur non-initié | Moyen | Tooltips + glossaire déroulant en phase 2 |
| Diagramme SVG complexe sur mobile | Moyen | Version simplifiée < 768 px (empilement vertical des trois personnes) |
| Contraste orange sur fond sombre insuffisant pour petit texte | Faible | Utiliser `#FED7AA` (orange pâle) pour texte < 14 px |
| Confusion de la palette avec branding commercial | Faible | Serif classique + vocabulaire liturgique = ancrage sacré |

---

## 12. Références

- **R.C. Sproul**, *Before the Face of God* (1992) — source du concept Coram Deo.
- **MacArthur Study Bible** (LSB / NASB) — appareil de notes.
- **Reformation Study Bible** (Sproul, éd.) — appareil de notes.
- **NEG 1979 / Segond 21** — version biblique recommandée pour les citations.
- **Confession de foi de Westminster** (1647) — cadre doctrinal implicite.

---

*Soli Deo Gloria*
