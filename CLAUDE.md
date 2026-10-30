# Conférence Tolkien — instructions pour l'IA

Ce dépôt contient la source d'une conférence sur J.R.R. Tolkien. Il est organisé en trois niveaux :

1. `1-brief/` — **source de vérité**, rédigée par l'auteur. Ne pas modifier sans demande explicite.
1.5. `1.5-brief-by-AI/` — propositions de contenu rédigées par l'IA, non validées. Ne jamais
   les utiliser pour générer des slides tant que l'auteur ne les a pas reportées dans `1-brief/`.
   Les sources téléchargées sont dans `sources/`.
   Tous les extraits de `sources/anything_you_can_imagine/` sont issus du livre
   « Anything You Can Imagine: Peter Jackson and the Making of Middle-earth » de Ian Nathan (2018).
   Les fichiers `*.fr.md` qui s'y trouvent sont des traductions faites par l'IA.
1.6. `1.6-brief-fact-added-by-AI/` — faits ajoutés par l'IA dans les slides sans figurer dans
   le brief, à vérifier par l'auteur (voir « Faits ajoutés par l'IA » ci-dessous).
2. `2-slides/` — sources des slides (Marp), produites en grande partie par l'IA à partir du niveau 1.
3. `3-presentation/` — résultat du build (HTML + PDF). Ne jamais éditer à la main.

## Avant de rédiger des slides

Lire dans cet ordre :
1. `1-brief/conference.md` — public, durée, objectif
2. `1-brief/plan.md` — structure et minutage
3. `1-brief/style.md` — ton et règles visuelles
4. `1-brief/textes/` — le contenu de fond, partie par partie
5. `1-brief/citations.md` et `1-brief/sources.md`

## Règles de contenu

- **Citations** : n'utiliser QUE celles de `1-brief/citations.md`, mot pour mot, avec leur référence. Ne jamais inventer, compléter ni reformuler une citation. Si une slide en appelle une qui manque, laisser un `<!-- TODO citation : ... -->` et le signaler.
- **Faits** (dates, noms, publications, lieux) : s'appuyer sur `1-brief/textes/` et `1-brief/sources.md`. En cas de doute, le signaler plutôt que d'affirmer.
- **Noms propres** : suivre la graphie et la traduction fixées dans `1-brief/style.md`.
- Le propos appartient à l'auteur : ne pas ajouter de thèse ou d'interprétation absente du brief.

## Faits ajoutés par l'IA

Quand une slide contient un fait qui ne figure pas dans `1-brief/` (par exemple les dates
d'une frise chronologique, un lieu, un nom, une année de publication), le consigner pour
vérification dans `1.6-brief-fact-added-by-AI/` :

- **Arborescence** : un fichier par fichier source du brief, au même chemin relatif.
  Un fait ajouté sur une slide tirée de `1-brief/textes/02-vie.md` va dans
  `1.6-brief-fact-added-by-AI/textes/02-vie.md` ; une slide tirée de `1-brief/plan.md` va
  dans `1.6-brief-fact-added-by-AI/plan.md`.
- **Contenu** : pour chaque fait, la slide concernée (titre), le fait tel qu'il apparaît
  à l'écran ou dans les notes, et sa source (`sources/…`, `1.5-brief-by-AI/…`) ou la
  mention **[IA, à vérifier]** s'il vient des seules connaissances de l'IA.
- **Ne pas consigner** un fait déjà présent dans `1-brief/` ou dans les slides existantes
  avant la modification, ni un fait déjà listé dans le fichier `1.6` correspondant.
- Quand l'auteur a reporté un fait dans `1-brief/`, le retirer du fichier `1.6`.

## Règles de rédaction des slides

- Format : Marp, fichier unique `2-slides/slides.md`, thème `tolkien` (`2-slides/theme/tolkien.css`).
- Une idée par slide. Peu de texte à l'écran ; le développement va dans les notes orateur.
- Notes orateur : en commentaire HTML `<!-- ... -->` sous chaque slide, rédigées à partir de `1-brief/textes/`.
- Chaque partie du plan commence par une slide de section (`<!-- _class: section -->`).
- Respecter le minutage de `plan.md` (repère : environ 1 à 2 minutes par slide).
- Images dans `2-slides/assets/`, référencées en `assets/nom.jpg`. Toute image doit avoir son crédit dans `2-slides/assets/CREDITS.md`.

## Build

```bash
npm run build      # HTML + PDF dans 3-presentation/
npm run preview    # aperçu avec rechargement automatique
```

Après une modification des slides, lancer `npm run build` pour vérifier que tout compile.
