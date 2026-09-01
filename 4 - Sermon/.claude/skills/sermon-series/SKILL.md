---
name: sermon-series
description: Planifie une série de prédication expositive suivie (lectio continua) sur un livre de la Bible, conformée exclusivement à la théologie de John MacArthur. Fournir un livre; recevoir introduction, structure de l'argument, découpage en unités de texte, carte doctrinale, textes exigeants et notes de mise en oeuvre, en français canadien, sous forme de PDF, Markdown et présentation HTML.
---

# Série expositive — perspective John MacArthur

Découper un livre de la Bible en unités d'exposition suivies, dans l'ordre du texte.

**Un seul modèle : l'exposition suivie.** La série se construit sur un livre, parcouru du début à la fin. Elle ne se construit ni sur un thème, ni sur un besoin ressenti, ni sur un calendrier. Si la demande porte sur un sujet, redemander le livre : le sujet se prêche là où le texte le traite.

**Aucune variable `pastor-foundation`.** L'auteur est toujours **André-Guy Bruneau**; le texte de base est la **NEG79** (texte de *La Bible d'étude MacArthur*). Ne pas les demander.

---

## Le principe de découpage

**Le texte fixe les unités, pas le calendrier.** C'est le point qui sépare ce modèle de la planification de série courante, et il gouverne tout le reste.

Une unité d'exposition est une unité de sens du texte : une péricope narrative, une section argumentative, un développement de l'épître. On ne coupe pas au milieu d'un argument pour que la série tienne en six semaines, et on n'étire pas une unité sur trois dimanches pour remplir un trimestre. MacArthur a mis 43 ans à traverser le Nouveau Testament et huit ans sur Matthieu, non par lenteur mais parce que le nombre d'unités est une propriété du texte.

Ce qui en découle, et qui est délibérément absent de cette skill :

| Absent | Pourquoi |
|---|---|
| Options de titres pour bannière | Le titre nomme le texte, il ne vend pas la série. |
| Arc émotionnel de la série | L'arc appartient au livre biblique, pas au planificateur. |
| Plafond de durée « l'attention chute après 8 semaines » | Critère d'auditoire, non critère de texte. Argument traité dans *Ashamed of the Gospel*. |
| Stratégie de lancement, semaine teaser, mailer | Pragmatisme de croissance d'église. |
| Série thématique, florilège de versets | Le sujet se prêche là où le texte le traite. |

Le nombre d'unités est un **résultat**, jamais une contrainte d'entrée. Si le nombre de semaines demandé ne correspond pas au nombre d'unités du texte, le dire et proposer soit une portion cohérente du livre, soit la durée réelle.

---

## Échelle de sources

Identique à celle de `sermon-research`. Descendre dans l'ordre, s'arrêter au premier niveau qui traite réellement le texte, déclarer le niveau atteint dans `source_level`.

| Niveau | Source |
|---|---|
| 1 | Série de sermons Grace to You (`gty.org`) sur le livre |
| 2 | *MacArthur New Testament Commentary*, volume du livre |
| 3 | Notes de la *Bible d'étude MacArthur* |
| 4 | *MacArthur Bible Commentary* (un volume) |
| 5 | Cercle Grace / Master's Seminary appliquant sa méthode — **pas** la voix de MacArthur, nommer l'auteur réel |
| ∅ | Aucune de ces sources — lacune déclarée |

**Cas particulier, décisif pour cette skill :** MacArthur a prêché tout le Nouveau Testament verset par verset (achevé le 5 juin 2011), et il est mort le 14 juillet 2025 — le corpus est clos. Sur un livre du NT, le découpage en unités de MacArthur lui-même est donc **disponible et vérifiable** : le reprendre plutôt que d'en inventer un. Sur l'Ancien Testament, la couverture est partielle; là où elle manque, découper selon la méthode grammatico-historique et le déclarer au niveau ∅, sans attribuer le découpage à MacArthur.

Détail des sources : `../sermon-research/assets/references/commentary-sources.md`.

---

## Posture théologique

Celle de `sermon-research`, sans variante : inerrance et suffisance de l'Écriture; interprétation grammatico-historique littérale appliquée avec constance; doctrines de la grâce; justification par la foi seule; salut sous la seigneurie de Christ; cessationnisme; prémillénarisme dispensationaliste avec distinction durable entre Israël et l'Église; création en six jours; complémentarisme; église locale gouvernée par une pluralité d'anciens; prédication expositive verset par verset comme modèle normatif. Référence systématique : *Biblical Doctrine* (MacArthur et Mayhue).

Aucun cadre concurrent n'est présenté, pondéré, ni cité pour être réfuté.

---

## Entrées

| Entrée | Requis | Notes |
|---|---|---|
| Livre de la Bible | Oui | Livre entier ou portion cohérente (p. ex. « Jacques », « Romains 1-8 ») |
| Contraintes de calendrier | Non | Signalées comme contraintes, jamais utilisées pour recouper le texte |
| Cadence | Non | Hebdomadaire par défaut |

Un livre suffit. Si la demande est thématique, redemander le livre plutôt que de produire une série thématique.

---

## Les six étapes

**1. Introduction au livre.** Auteur, date, destinataires, occasion, thème central, situation historique. Ce que le livre fait comme document avant ce qu'il enseigne comme doctrine. 2-3 paragraphes.

**2. Structure de l'argument.** Le fil du livre en unités majeures, avec les charnières. C'est cette structure qui justifie le découpage de l'étape 3; sans elle, le découpage est arbitraire.

**3. Découpage en unités d'exposition.** Le livrable central. Pour chaque unité : numéro, passage, **base du découpage** (pourquoi la coupe tombe là — charnière argumentative, changement d'interlocuteur, inclusion, formule de transition), titre d'exposition, propos central en une phrase affirmative, et le niveau de source MacArthur pour cette unité précise.

Le titre nomme le texte et son propos. Pas de jeu de mots, pas de formule de campagne, pas d'uniformité imposée entre les titres.

**4. Carte doctrinale du livre.** Où chaque locus de *Biblical Doctrine* tombe dans le parcours : théologie propre, anthropologie, christologie, sotériologie, pneumatologie, ecclésiologie, eschatologie. Sert à voir ce que la série enseignera nécessairement, et ce qu'elle n'abordera pas.

**5. Textes exigeants.** Les passages qui demandent une décision doctrinale explicite avant d'y arriver au pupitre : textes contestés, textes que le cadre dispensationaliste ou cessationniste traite d'une manière précise, textes que l'assemblée entendra mal sans préparation. Pour chacun : la difficulté, la lecture retenue, et le niveau de source qui l'appuie.

**6. Notes de mise en oeuvre.** Cadence retenue et durée réelle qui en découle. Calibrage des unités (celles qui sont denses et pourraient se scinder, celles qui sont minces et se regroupent). Lacunes du corpus : les unités où aucune exposition de MacArthur n'existe.

---

## Sorties

Trois fichiers, même nom de base : **PDF**, **Markdown**, **présentation HTML**. Contenu intégralement en **français canadien**.

Prérequis : `pip install reportlab`.

1. Écrire le JSON dans un fichier temporaire (p. ex. `serie-temp.json`).
2. Exécuter `python assets/generate-pdf.py serie-temp.json` (produit le PDF **et** le Markdown).
3. Supprimer le JSON temporaire.
4. Rédiger la présentation HTML en adaptant `assets/template-presentation.html`, mêmes règles que `sermon-research` : charpente `<style>` / `<script>` intacte, ids de sections `#introduction`, `#argument`, `#unites`, `#doctrine`, `#textes-exigeants`, `#mise-en-oeuvre`, nav alignée sur les ids présents, pied sans logo de dépôt ni liens « retour ».
5. Indiquer les trois noms de fichiers et leur emplacement.

Nom de base : `Serie-MacArthur-<livre>` (p. ex. `Serie-MacArthur-Jacques.pdf/.md/.html`).

Emplacement : les trois fichiers sont écrits dans `4 - Sermon/` du dépôt CoramDeo, sauf si l'utilisateur indique un autre dossier.

### Structure JSON

```json
{
  "book": "Jacques",
  "series_title": "L'épreuve de la foi vivante",
  "date": "2026-07-27",
  "pastor_name": "André-Guy Bruneau",
  "source_level": "Niveau 1 — série Grace to You sur Jacques, et MacArthur NT Commentary",
  "book_survey": "Texte complet. Paragraphes séparés par \n\n.",
  "argument_structure": "Texte complet. Paragraphes séparés par \n\n.",
  "pericope_division": [
    {
      "unit": 1,
      "passage": "Jacques 1.1-12",
      "unit_basis": "Ouverture épistolaire suivie du premier développement sur l'épreuve, clos par la béatitude du verset 12.",
      "exposition_title": "L'épreuve qui produit la persévérance",
      "main_point": "Dieu emploie l'épreuve pour amener la foi à maturité, non pour la briser.",
      "doctrinal_locus": "Sanctification progressive",
      "macarthur_source": "Niveau 1"
    }
  ],
  "doctrinal_map": [
    {"locus": "Sotériologie — nature de la foi salvatrice", "units": "1, 5, 6", "note": "Le coeur du débat sur la foi et les oeuvres, traité dans The Gospel According to Jesus."}
  ],
  "difficult_texts": [
    {
      "passage": "Jacques 2.14-26",
      "issue": "Tension apparente avec la justification par la foi seule chez Paul.",
      "macarthur_reading": "Jacques traite de la démonstration de la foi devant les hommes, Paul de son fondement devant Dieu. Une foi qui ne produit rien n'est pas la foi qui justifie.",
      "source_level": "Niveau 1"
    }
  ],
  "preaching_notes": {
    "cadence": "Texte complet.",
    "unit_sizing": "Texte complet.",
    "gaps": "Texte complet."
  }
}
```

Notes :

- `source_level` est **obligatoire**, au niveau de la série et par unité (`macarthur_source`). Format : `Niveau <n> — <source précise>`, ou `Niveau ∅ — aucune exposition de MacArthur sur ce livre`.
- `pericope_division` compte autant d'entrées que le texte a d'unités. Ce nombre n'est pas négociable contre le calendrier.
- `pastor_name` vaut toujours « André-Guy Bruneau ». Aucun `church_name`.
- Aucun tiret cadratin dans le contenu.

---

## Interdits

- **Aucune série thématique ni florilège de versets.** Un livre, parcouru dans l'ordre.
- **Aucune coupe dictée par le calendrier.** Le nombre d'unités sort du texte.
- **Aucun titre de campagne**, aucune uniformité formelle imposée entre les titres.
- **Aucun arc émotionnel, aucune stratégie de lancement, aucun plafond de durée.**
- **Aucun découpage attribué à MacArthur sans source au niveau 1-4.**
- **Aucun cadre théologique concurrent**, ni présenté, ni pondéré, ni réfuté.
- **Aucun plan de sermon.** Le propos central d'une unité n'est pas un plan; la structure de chaque prédication appartient à la préparation hebdomadaire.

---

**Pourquoi le texte fixe le découpage :** dès que le calendrier décide où couper, c'est le calendrier qui décide ce que l'assemblée entendra. L'exposition suivie transfère cette décision au texte, ce qui est précisément son objet.
