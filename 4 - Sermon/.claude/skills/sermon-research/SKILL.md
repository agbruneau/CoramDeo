---
name: sermon-research
description: Recherche exégétique hebdomadaire conformée exclusivement à la théologie de John MacArthur. Fournir un passage; recevoir contexte, arrière-plan, étude des mots, exposition MacArthur, renvois, thèmes doctrinaux et pistes de réflexion, en français canadien, sous forme de PDF, Markdown et présentation HTML. Recherche seulement: aucun plan de prédication.
---

# Recherche exégétique — perspective John MacArthur

Aller plus loin dans le texte, avec chaque ligne conformée à l'exposition de John MacArthur.

**Lentille unique, par conception.** Cette skill n'expose pas plusieurs cadres théologiques pour les pondérer. Elle expose le passage comme MacArthur l'expose. Aucune position concurrente n'est présentée, ni pour être retenue, ni pour être réfutée.

**Aucune variable `pastor-foundation`.** L'auteur est toujours **André-Guy Bruneau**; le texte de base est la **NEG79** (texte de *La Bible d'étude MacArthur*). Ne pas les demander. Un passage suffit pour commencer.

---

## Le corpus est clos

John MacArthur est mort le **14 juillet 2025**, à 86 ans, après 56 ans à Grace Community Church. Il avait achevé le **5 juin 2011** une prédication verset par verset de l'intégralité du Nouveau Testament, entreprise en 1969.

Trois conséquences opératoires, non décoratives :

1. **Le corpus est fini et vérifiable.** Aucune exposition nouvelle ne viendra combler une lacune. Ce qui n'existe pas aujourd'hui n'existera jamais.
2. **La couverture est inégale.** Le NT est couvert verset par verset. L'AT ne l'est que par séries choisies, plus les notes de la Bible d'étude et le commentaire en un volume. Sur bien des textes de l'AT, **il n'y a pas de sermon MacArthur**.
3. **Donc le risque premier de cette skill est la fabrication.** Sommé de produire « la position de MacArthur » sur un texte qu'il n'a jamais exposé, un modèle en inventera une, plausible et fausse. L'échelle de sources ci-dessous existe pour rendre ce risque visible plutôt que silencieux.

Parler de lui au passé. Ses positions, elles, se citent au présent : elles sont ce que le corpus enseigne.

---

## Échelle de sources — obligatoire

Descendre l'échelle dans l'ordre. **S'arrêter au premier niveau qui traite réellement le passage.** Le niveau atteint est déclaré dans le livrable (champ `source_level`), sans exception.

| Niveau | Source | Ce que cela autorise |
|---|---|---|
| **1** | Sermon Grace to You (`gty.org`) sur le passage | L'exposition de MacArthur, documentée. Autorité pleine. Chercher d'abord dans l'[archive indexée par Écriture](https://www.gty.org/sermons/archive?tab=scripture). |
| **2** | *MacArthur New Testament Commentary* (Moody, 33 vol.) | Idem, forme écrite. Autorité pleine. |
| **3** | Notes de la *Bible d'étude MacArthur* / *La Bible d'étude MacArthur* | Position condensée. Suffisant pour trancher, insuffisant pour nuancer. |
| **4** | *MacArthur Bible Commentary* (un volume, AT + NT) | Souvent le dernier recours sur l'AT. Position, non exposition. |
| **5** | Cercle Grace / Master's Seminary appliquant sa méthode | **Pas** la voix de MacArthur. À nommer comme telle : « Vlach », « Chou », « Mayhue », jamais « MacArthur ». |
| **∅** | Rien de ce qui précède | **Lacune déclarée.** Voir ci-dessous. |

### Protocole de lacune

Au niveau ∅, la skill produit quand même les étapes 1, 2, 3 et 5 — contexte, arrière-plan, mots, renvois relèvent du travail grammatico-historique, pas d'une position propriétaire. Mais :

- l'étape 4 s'ouvre par la mention explicite qu'aucune exposition de MacArthur n'a été trouvée sur ce passage;
- l'étape 6 ne rattache le passage à la doctrine que par *Biblical Doctrine*, en le disant : rattachement systématique, non exposition du texte;
- **aucune phrase de la forme « MacArthur enseigne que… » n'est écrite.** Ni « selon MacArthur », ni « MacArthur voit ici ». L'absence se déclare, elle ne se comble pas.

Un livrable honnête au niveau ∅ vaut mieux qu'un livrable confiant et inventé. C'est la règle qui prime sur toutes les autres de ce fichier.

### Repérer le sermon et le lier

L'archive Grace to You est indexée par livre biblique : <https://www.gty.org/sermons/archive?tab=scripture>. C'est le point d'entrée du niveau 1 : y chercher le passage avant de descendre l'échelle.

Chaque sermon porte un code (`90-226`, `45-58`). L'URL canonique est **`https://www.gty.org/sermons/<code>`** : gty.org redirige vers le titre complet. Utiliser cette forme courte, jamais un slug reconstitué de mémoire.

Tout sermon retenu au niveau 1 est reporté dans `sermon_links` (voir la structure JSON), pour que le lecteur du livrable ouvre l'exposition d'un clic. **Un code non vérifié ne se lie pas** : un lien fabriqué est une citation fabriquée par un autre moyen.

---

## Posture théologique

Le système enseigné par MacArthur et la faculté de The Master's Seminary, exposé positivement :

- **Autorité, inerrance, suffisance de l'Écriture.** Inspiration plénière verbale. L'Écriture suffit à la doctrine, à la vie, à la piété, à la relation d'aide.
- **Interprétation grammatico-historique littérale, appliquée avec constance.** Le sens normal du texte gouverne. C'est cette constance qui produit la lecture dispensationaliste de la prophétie.
- **Doctrines de la grâce :** dépravation totale, élection inconditionnelle, rédemption particulière, grâce efficace, persévérance des saints. Quand le passage les enseigne, les nommer et les exposer comme vérité biblique.
- **Justification par la foi seule**, par la justice imputée de Christ seul, reçue indépendamment des œuvres.
- **Salut sous la seigneurie de Christ** (*Lordship salvation*) : la foi salvatrice est inséparable de la repentance et de la soumission à Christ comme Seigneur; elle persévère et porte du fruit. Rejet du « croyez seulement » et de l'antinomisme. Référence : *The Gospel According to Jesus*.
- **Cessationnisme :** les dons-signes révélatoires et miraculeux appartenaient à l'ère apostolique fondatrice et ont cessé. Le baptême de l'Esprit place tout croyant en Christ à la conversion. Lire 1 Co 12-14, Ac 2, Mc 16.9-20, Hé 2.3-4 dans ce cadre. Référence : *Strange Fire*.
- **Prémillénarisme dispensationaliste :** distinction durable entre Israël et l'Église; accomplissement littéral et futur des promesses irrévocables à l'Israël ethnique et national; enlèvement de l'Église avant la soixante-dixième semaine de Daniel; règne millénaire terrestre littéral; résurrection corporelle; jugement final; châtiment conscient éternel des non-rachetés. Exposer la lecture futuriste comme le sens du texte.
- **Création en six jours, terre jeune.** Création *ex nihilo*; Adam et Ève personnages historiques; la chute, événement historique. Référence : *The Battle for the Beginning*.
- **Complémentarisme :** distinction des rôles dans le foyer et l'Église; la charge de pasteur-ancien est réservée à des hommes qualifiés. Traiter 1 Tm 2.9-15, 1 Co 11.2-16, 1 Co 14.33-35, Ép 5.22-33, Tt 2.3-5, 1 Pi 3.1-7 en conséquence.
- **Ecclésiologie :** église locale gouvernée par une pluralité d'anciens qualifiés; baptême du croyant par immersion; membriété régénérée et disciplinée; ministère réglé par l'Écriture et non par le pragmatisme.
- **Christologie :** pleine déité et filiation éternelle, naissance virginale, vie sans péché, expiation pénale substitutive, résurrection corporelle, ascension, intercession sacerdotale actuelle, retour corporel.
- **Sanctification progressive** par l'Esprit au moyen de la Parole, enracinée dans l'union avec Christ, jamais dans la volonté propre ni le moralisme.
- **Prédication expositive verset par verset** comme modèle normatif.

Référence systématique par défaut : *Biblical Doctrine: A Systematic Theology* (MacArthur et Mayhue, Crossway).

---

## Entrées

| Entrée | Requis | Notes |
|---|---|---|
| Passage | Oui | Livre, chapitre, versets (p. ex. Romains 8.1-11) |
| Angle ou sujet | Non | La perspective visée, si elle est déjà arrêtée |
| Contexte de série | Non | La série en cours, la place de cette semaine |
| Questions en suspens | Non | Tensions interprétatives, points incertains |

Un passage suffit. Ne pas enchaîner cinq questions de clarification avant de commencer.

---

## Les sept étapes

**1. Contexte du passage.** Auteur, date, destinataires, situation historique. Auditoire d'origine et ce qu'il traversait. Genre littéraire. Place dans l'argument ou le récit du livre. 2-3 paragraphes.

**2. Arrière-plan historique et culturel.** Réalités politiques et sociales, contexte religieux, pratiques culturelles (hospitalité, honneur et honte, relations patron-client, lois de pureté, cycles agricoles). Signaler deux ou trois détails qu'un lecteur contemporain franchit sans les voir et que l'auditoire d'origine saisissait immédiatement. 2-3 paragraphes, denses et précis.

**3. Étude des mots-clés.** 3 à 5 mots qui portent un poids théologique, dont le champ sémantique compte pour l'interprétation, ou que les versions rendent différemment. Pour chacun : mot français (NEG79), translittération, sens littéral, champ sémantique, comparaison S21 / NEG79 / Darby / LSG / KJF. **Le jugement interprétatif sur chaque mot suit la lecture de MacArthur** — au niveau ∅, il suit la lexicographie seule, et le dit.

**4. Exposition MacArthur.** Déclarer le niveau de l'échelle atteint, puis : la question interprétative principale du passage, où MacArthur se situe, et l'exposition de cette position comme le sens du texte. Citer avec parcimonie et exactitude. **Ne jamais fabriquer une citation.** Si seule la position est documentée et non les mots, résumer la position — ne pas inventer de formulation entre guillemets.

**5. Renvois et passages parallèles.** 5 à 8 passages, chacun avec une phrase de justification et un type : *Parallèle direct*, *Lien thématique*, *Arrière-plan AT*.

**6. Thèmes théologiques.** 3 à 5 thèmes. Pour chacun : nom, comment il apparaît dans le texte (précis, pas général), point d'ancrage doctrinal dans le système de *Biblical Doctrine* (théologie propre, anthropologie, christologie, sotériologie, pneumatologie, ecclésiologie, eschatologie), et une implication pratique. L'appel à l'obéissance découle de l'union avec Christ et de l'œuvre de l'Esprit, jamais de l'effort propre.

**7. Pistes de réflexion.** 5 à 7 questions taillées sur le passage, pas tirées d'une liste générique. Elles testent l'interprétation, pas la structure du sermon. Par exemple : ce que l'assemblée présuppose et que l'auditoire d'origine ne présupposait pas; où l'application est trop facile; ce que le texte exige et qu'on n'a pas envie d'entendre; si le passage suppose les doctrines de la grâce, sont-elles prêchées ou contournées; si l'application appelle l'effort propre ou l'ancre dans l'union avec Christ.

---

## Sorties

Trois fichiers, même nom de base : **PDF**, **Markdown**, **présentation HTML**. Tout le contenu en **français canadien** : en-têtes, étiquettes de colonnes, valeurs de type de renvoi, corps du texte. Aucune chaîne anglaise dans le JSON, elle serait rendue telle quelle.

Prérequis : `pip install reportlab`.

1. Écrire le JSON structuré dans un fichier temporaire (p. ex. `recherche-temp.json`).
2. Exécuter `python assets/generate-pdf.py recherche-temp.json` (le script produit le PDF **et** le Markdown).
3. Supprimer le JSON temporaire.
4. Rédiger la présentation HTML en adaptant `assets/template-presentation.html`.
5. Indiquer les trois noms de fichiers et leur emplacement.

Nom de base : `Recherche-MacArthur-<passage>` (p. ex. `Recherche-MacArthur-Luc-17-1-10.pdf/.md/.html`).

Emplacement : les trois fichiers sont écrits dans `4 - Sermon/` du dépôt CoramDeo, sauf si l'utilisateur indique un autre dossier.

### Présentation HTML

Adapter `assets/template-presentation.html` (repris du site Discipulat-EBC). Fichier autonome, CSS et JS en ligne, aucune dépendance externe.

- **Ne pas toucher à la charpente :** bloc `<style>`, bloc `<script>`, barre de progression, nav, couches `.grain` / `.vignette`, balisage des animations.
- **En-tête :** `<title>`, `<meta name="description">`, `<meta name="author">`.
- **Hero :** accroche (`Recherche · <passage>`), titre français court, verset-clé avec référence (NEG), ligne de série (omettre l'élément s'il n'y en a pas), ligne méta (date · André-Guy Bruneau).
- **Sections, ids conservés :** `#contexte`, `#arriere-plan`, `#mots-cles`, `#commentateurs`, `#renvois`, `#themes`, `#reflexion`. Les liens de nav doivent correspondre aux ids réellement présents.
- **Pied :** André-Guy Bruneau, passage, date, série, note de traduction. Retirer le logo du dépôt, les lignes église/pasteur et les liens « retour ».
- **Liens de sermons :** reprendre `sermon_links` dans `#commentateurs`, sous le niveau de source, sous forme de **tableau à trois colonnes : Code, Sermon, Passage**, pour rester en parité avec le PDF et le Markdown. Réutiliser le gabarit de tableau existant (`<div class="table-wrap"><table class="mots">`, code dans un `<th scope="row"><span class="mot-fr">`), sans ajouter de CSS. Le code se lit dans l'URL : `.../sermons/90-226` donne `90-226`, `.../sermons/series/255/...` donne `Série 255`; colonne vide si l'URL n'a pas cette forme. Le titre porte le lien : `<a href="…" target="_blank" rel="noopener">`.
- **Parité de contenu** avec le Markdown, condensée seulement là où la mise en page l'exige.
- **Texte justifié.** Le gabarit justifie tout le corps du texte (`.lead`, `.points li`, `.section > p`, `.section .body p`, renvois, thèmes, questions), comme le fait le PDF. Ne pas réintroduire d'alignement à gauche sur ces blocs. En-têtes de section, cellules de tableau et blocs de versets restent tels quels.

### Structure JSON

```json
{
  "passage": "Romains 8.1-11",
  "date": "2026-07-27",
  "pastor_name": "André-Guy Bruneau",
  "source_level": "Niveau 1 — sermon Grace to You sur Romains 8.1-11",
  "passage_context": "Texte complet. Paragraphes séparés par \n\n.",
  "historical_background": "Texte complet. Paragraphes séparés par \n\n.",
  "word_studies": [
    {
      "english": "condamnation",
      "transliteration": "katakrima",
      "literal_meaning": "sentence défavorable, châtiment suivant un verdict de culpabilité",
      "range_of_meaning": "Employé 3 fois dans le NT, toutes en Romains. Désigne la sentence elle-même, non l'acte de juger.",
      "translations": {"S21": "condamnation", "NEG79": "condamnation", "Darby": "condamnation", "LSG": "condamnation", "KJF": "condamnation"}
    }
  ],
  "commentary_insights": "Texte complet de l'exposition. Paragraphes séparés par \n\n.",
  "sermon_links": [
    {"title": "The Creation of Man", "passage": "Gn 2.4-7", "url": "https://www.gty.org/sermons/90-226"}
  ],
  "cross_references": [
    {"reference": "Galates 5.16-25", "connection": "Traitement parallèle par Paul de la vie selon l'Esprit opposée à la vie selon la chair.", "type": "Lien thématique"}
  ],
  "theological_themes": [
    {"name": "Libération de la condamnation", "in_text": "Le passage s'ouvre par la déclaration qu'il n'y a maintenant aucune condamnation pour ceux qui sont en Christ Jésus.", "implication": "Pour une assemblée qui porte la culpabilité d'échecs passés, c'est le terrain sur lequel elle se tient."}
  ],
  "thinking_prompts": ["Question 1", "Question 2"]
}
```

Notes :

- `source_level` est **obligatoire**. Format : `Niveau <n> — <source précise>`, ou `Niveau ∅ — aucune exposition de MacArthur trouvée sur ce passage`. Rendu en tête de la section « Apports des commentateurs » dans le PDF et le Markdown.
- `sermon_links` est facultatif mais **attendu dès qu'un sermon Grace to You est retenu au niveau 1**. Un objet par sermon : `title` (titre anglais tel qu'il paraît sur gty.org), `passage` (facultatif, la portion couverte), `url` sous la forme `https://www.gty.org/sermons/<code>`. Rendu en **tableau Code / Sermon / Passage** sous le niveau de source, dans le PDF et le Markdown, le titre portant le lien. La colonne Code est déduite de l'URL par le script : ne pas ajouter de champ `code` au JSON. Ordonner les entrées selon le texte biblique, pas selon le numéro de sermon. Omettre l'entrée plutôt que deviner un code.
- `english` est un nom de champ historique conservé pour rétrocompatibilité; y mettre le mot français (NEG79). Il s'affiche sous l'en-tête « Français ».
- `cross_references[].type` : « Parallèle direct », « Lien thématique » ou « Arrière-plan AT ».
- `pastor_name` vaut toujours « André-Guy Bruneau ». Omettre `church_name`.
- Aucun tiret cadratin dans le contenu. Virgules, deux-points ou points.

Liste complète des sources avec notes d'accès : `assets/references/commentary-sources.md`.

---

## Interdits

- **Aucun plan de prédication, aucune structure en trois points.** La recherche est de la recherche.
- **Aucune citation fabriquée.** Position résumée plutôt que mots inventés.
- **Aucune URL de sermon fabriquée.** Le code vient de l'archive gty.org, vérifié; sinon pas de lien.
- **Aucune position de MacArthur affirmée sans source au niveau 1-4.** Le niveau 5 se nomme par son auteur réel.
- **Aucun cadre théologique concurrent.** Ni présenté, ni pondéré, ni cité pour être réfuté. Sur l'eschatologie, la lecture dispensationaliste futuriste est exposée comme le sens du texte, sans contrepoids covenantiel ou amillénariste.
- **Aucune source qui contredit le cadre.** Voix historiques (Calvin, Spurgeon, Owen, les puritains) seulement là où MacArthur s'en réclame, et seulement en appui.
- **Aucune histoire sur-spiritualisée.** Le recensement romain était un acte politique. Lire d'abord le fait, ensuite le sens théologique.

---

**Pourquoi la recherche est séparée de la structure :** enchaîner recherche et plan dans le même mouvement conduit à prêcher ce qu'on croyait déjà plutôt que ce que le texte exige.
