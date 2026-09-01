# Sources — cadre John MacArthur exclusif

Liste des ressources sur lesquelles s'appuient les skills `sermon-research` et `sermon-series`. Le cadre interprétatif est **John MacArthur exclusivement**.

## Le corpus est clos

MacArthur est mort le **14 juillet 2025** (86 ans, pneumonie), après 56 ans à Grace Community Church. Il avait achevé le **5 juin 2011** la prédication verset par verset de tout le Nouveau Testament, commencée en 1969.

Ce corpus est donc **fini, vérifiable et inégal** : le NT est couvert verset par verset; l'AT ne l'est que par séries choisies, plus les notes de la Bible d'étude et le commentaire en un volume. Sur bien des textes de l'AT, il n'existe aucune exposition de MacArthur, et il n'en existera jamais.

## Échelle de sources

Descendre dans l'ordre, s'arrêter au premier niveau qui traite réellement le passage, déclarer le niveau atteint dans le livrable (`source_level`).

| Niveau | Source | Statut |
|---|---|---|
| 1 | Sermon Grace to You — [archive par Écriture](https://www.gty.org/sermons/archive?tab=scripture) | Exposition documentée. Autorité pleine. Lier le sermon : `https://www.gty.org/sermons/<code>`. |
| 2 | *MacArthur New Testament Commentary* | Exposition documentée. Autorité pleine. |
| 3 | Notes de la *Bible d'étude MacArthur* | Position condensée. Trancher oui, nuancer non. |
| 4 | *MacArthur Bible Commentary* (un volume) | Position, non exposition. Souvent le dernier recours sur l'AT. |
| 5 | Cercle Grace / Master's Seminary | **Pas** la voix de MacArthur. Nommer l'auteur réel. |
| ∅ | Rien de ce qui précède | Lacune déclarée. Ne jamais écrire « MacArthur enseigne que… ». |

Le niveau ∅ n'est pas un échec de la skill : c'est son garde-fou. Un corpus clos a des trous, et les déclarer est la seule alternative honnête à les combler par invention.

### Lier le sermon cité

L'archive Grace to You s'indexe par livre biblique : <https://www.gty.org/sermons/archive?tab=scripture>. Chaque sermon porte un code (`90-226`, `45-58`) et se lie sous la forme courte **`https://www.gty.org/sermons/<code>`**, que gty.org redirige vers le titre complet. Cette forme évite d'inventer un slug.

Les sermons retenus au niveau 1 passent dans le champ `sermon_links` du JSON et sortent en liens cliquables dans le PDF, le Markdown et la présentation HTML. Un code non vérifié ne se lie pas.

---

Sources fall into three groups: **MacArthur's own corpus** (the governing voice), the **Grace / Master's Seminary circle** (used to fill out his exposition, never to redirect it), and **background / reference works** that are theology-neutral (lexicons, language tools, historical background). Historic Reformed voices (Calvin, Spurgeon, Owen, the Puritans) are consulted **only where MacArthur himself appeals to them**, and only in support of his reading.

---

## Group 1 — John MacArthur's Corpus (the governing voice)

These are the sources whose readings set the interpretation. When they treat a passage or doctrine, they decide the frame.

### Verse-by-verse exposition

| Name | Description | Access |
|---|---|---|
| **The MacArthur New Testament Commentary** (Moody, 33+ vols.) | John MacArthur's verse-by-verse exposition of the entire NT. The default first reference for any NT passage. Direct, application-driven, grammatical-historical, dispensational, Lordship-salvation framing. | Paid. Print, Logos, partial free excerpts via [gty.org](https://www.gty.org). |
| **Grace To You sermon archive** | Free transcripts and audio of MacArthur's sermons going back to 1969, covering most of the NT verse by verse and large portions of the OT. Often the cleanest record of MacArthur's actual exposition of a given passage. **Search here first**, via the scripture-indexed archive. Individual sermon: `https://www.gty.org/sermons/<code>`. | Free. [Archive by Scripture](https://www.gty.org/sermons/archive?tab=scripture). |
| **The MacArthur Study Bible** (LSB / NASB / ESV; French: *La Bible d'étude MacArthur*, base Segond / NEG) | One-volume study notes by MacArthur. Faster lookup than the full commentary; same theological frame. The French edition (*La Bible d'étude MacArthur*) makes the notes directly usable for French output; NEG79 is its base text. | Paid. Print and Logos. French edition: Société Biblique de Genève / Éditions Impact. |
| **The MacArthur Bible Commentary** | Single-volume condensation covering the whole Bible (OT and NT). Use when there is no full MacArthur NT volume on the passage, or for OT work. | Paid. Print and Logos. |

### MacArthur's topical and doctrinal works

Cite these when the passage touches a doctrine MacArthur has treated at length.

| Title | Doctrinal locus it governs |
|---|---|
| **Biblical Doctrine: A Systematic Theology of the Christian Faith** (MacArthur and Richard Mayhue, eds., Crossway) | **The default systematic-theology reference for this skill.** Comprehensive statement of MacArthur's system across all loci. Cite by chapter/topic for doctrinal weight. |
| **The Gospel According to Jesus** | Lordship salvation, the nature of saving faith, repentance, easy-believism. |
| **The Gospel According to the Apostles** | Justification, sanctification, assurance, the relationship of faith and works. |
| **Strange Fire** | Cessationism, the Holy Spirit, the charismatic question, 1 Cor 12-14, Acts 2. |
| **The Battle for the Beginning** | Six-day young-earth creation, Genesis 1-3, the historical Adam. |
| **Slave** | The believer's identity as *doulos* of Christ; *doulos* word study. |
| **The Truth War** | Inerrancy, sufficiency, contending for the faith, discernment. |
| **Hard to Believe** | The cost of discipleship, the narrow gate. |
| **Ashamed of the Gospel** | The sufficiency of Scripture for ministry; against pragmatism / seeker-sensitivity. |
| **Our Sufficiency in Christ; Found: God's Will; The Vanishing Conscience; Saved Without a Doubt; Twelve Ordinary Men; Twelve Unlikely Heroes; A Tale of Two Sons; The Murder of Jesus; The Glory of Heaven** | Topical exposition useful where the passage overlaps the subject. |

---

## Group 2 — The Grace / Master's Seminary Circle (supporting, never redirecting)

These authors teach within MacArthur's exact framework. They are used to fill out exegetical and doctrinal detail under MacArthur's frame, not to introduce a competing reading.

| Name | Contribution | Access |
|---|---|---|
| **Richard Mayhue** | Co-editor of *Biblical Doctrine*; pastoral theology, hermeneutics, eschatology. *How to Interpret the Bible for Yourself*, *Christ's Prophetic Plans* (with MacArthur). | Print and Logos. |
| **Michael J. Vlach** | Master's Seminary theologian on **Israel, the Church, and dispensationalism**. *He Will Reign Forever*, *Has the Church Replaced Israel?* The first stop on the future of national Israel and the millennium. | Print. |
| **Abner Chou** | Master's University/Seminary on **hermeneutics**; *The Hermeneutics of the Biblical Writers* (the "inspired-author" / prophetic-apostolic method). Grounds the grammatical-historical, authorial-intent approach. | Print. |
| **Nathan Busenitz** | Master's Seminary on church history, cessationism, justification. *Long Before Luther* (justification through church history), contributions to *Biblical Doctrine*. | Print. |
| **Tom Pennington** | *A Body of Divinity*-style teaching; the well-known "case for cessationism" exposition. Pastoral exposition within the frame. | Sermons / print. |
| **Mike Riccardi** | Grace Community Church / Master's Seminary on soteriology, the gospel, sanctification. | Sermons / print. |
| **Phil Johnson** | Executive director of Grace to You; editor of many MacArthur volumes; sharp on the Doctrines of Grace and discernment. | [gty.org](https://www.gty.org), *Pyromaniacs* archive. |
| **The Master's Seminary Journal (TMSJ)** | Peer exposition and doctrinal articles from MacArthur's faculty. Useful for technical questions handled within the frame. | Free archive at [tms.edu](https://www.tms.edu). |
| **Iain H. Murray** | MacArthur's authorized biographer (*John MacArthur: Servant of the Word and Flock*); Banner of Truth. Background on MacArthur's ministry and commitments. | Print. |

---

## Group 3 — Historic Voices (only where MacArthur uses them)

MacArthur stands in continuity with the Reformers and Puritans on the Doctrines of Grace and frequently cites them. In this skill they appear **only where MacArthur himself appeals to them**, and only to reinforce his exposition — never as an independent authority that reshapes the read.

| Name | When it appears here |
|---|---|
| **John Calvin — Commentaries / Institutes** | Where MacArthur cites Calvin on sovereignty, election, or a specific text. Public domain ([CCEL](https://ccel.org/ccel/calvin)). |
| **Charles Spurgeon — sermons / Treasury of David** | Where MacArthur draws on Spurgeon for the doctrines of grace or a Psalms exposition. Public domain ([spurgeon.org](https://www.spurgeon.org)). |
| **John Owen, the Puritans** | Where MacArthur appeals to Puritan treatment of sin, sanctification, or the atonement (e.g., Owen on mortification). |

Do not import these voices to set a frame MacArthur has not himself adopted. If MacArthur does not use them on a given point, leave them out.

---

## Background and Reference Works (theology-neutral)

These answer historical, lexical, or geographical questions. They do not set the interpretive frame; they serve the grammatical-historical work MacArthur's method requires.

| Name | Description | Access |
|---|---|---|
| **IVP Bible Background Commentary: New / Old Testament** (Keener; Walton, Matthews, Chavalas) | Compact cultural and historical background, passage by passage. | Paid. Print and digital. |
| **Zondervan Illustrated Bible Backgrounds Commentary** | Archaeology, maps, cultural notes. | Paid. Print and Logos. |
| **NIDNTTE / NIDOTTE** | Serious word studies (NT / OT theology and exegesis). | Paid. Print and Logos. |
| **BDAG** (Bauer-Danker-Arndt-Gingrich) | Standard NT Greek lexicon. | Paid. Logos. |
| **HALOT** | Standard OT Hebrew lexicon. | Paid. Logos. |
| **Strong's, Thayer's, BDB** | Older lexicons; freely available for quick lookup. | Free. Blue Letter Bible. |

---

## Digital Platforms

| Name | Description | Free or Paid |
|---|---|---|
| **[gty.org](https://www.gty.org)** | MacArthur's full sermon archive ([indexed by Scripture](https://www.gty.org/sermons/archive?tab=scripture)), study Bible articles, *Strange Fire* / *The Gospel According to Jesus* materials, blog. **The primary tool for this skill.** | Free. |
| **[tms.edu](https://www.tms.edu)** | The Master's Seminary; faculty resources, TMSJ archive, chapel messages. | Free. |
| **La Bible d'étude MacArthur** (Éditions Impact / Société Biblique de Genève) | French MacArthur Study Bible (base NEG / Segond). The French-language form of MacArthur's notes. | Paid. Print and digital. |
| **Logos Bible Software** | Aggregates the MacArthur NT Commentary, MacArthur Study Bible, *Biblical Doctrine*, and Master's Seminary collections. The standard tool for working the corpus in depth. | Paid. |
| **Blue Letter Bible** ([blueletterbible.org](https://www.blueletterbible.org)) | Interlinear, lexicons (Strong's, Thayer's, BDB), original-language lookup for the word studies. | Free. |
| **Bible Hub** ([biblehub.com](https://biblehub.com)) | Parallel translations and interlinear for language work. | Free. |

---

## How This Skill Uses These Sources

The skill defaults to **MacArthur's own corpus for the interpretive frame** (Grace to You sermon first, then the NT Commentary and Study Bible notes), pulls the **Grace / Master's Seminary circle** to fill out doctrinal and exegetical detail under that frame, and uses **theology-neutral background works** for grammar, lexicon, and historical context.

When citing a position by name, the skill names MacArthur (or the circle author). It does not fabricate direct quotes; if only the position is documented, it summarizes rather than invents words. The skill does not introduce a competing interpretive framework: the reading is John MacArthur's, expounded positively.

If you have direct access through gty.org, Logos, or print, reading MacArthur's actual exposition of the passage after the research summary is always worth the time.
