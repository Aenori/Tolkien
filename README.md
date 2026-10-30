# Conférence Tolkien

Sources de la présentation, en trois niveaux :

| Dossier            | Contenu                                         | Qui l'écrit         |
|--------------------|-------------------------------------------------|---------------------|
| `1-brief/`         | Cadre, plan, style, textes de fond, citations   | L'auteur            |
| `2-slides/`        | Slides Marp (`slides.md`), thème, images        | L'IA, relue par l'auteur |
| `3-presentation/`  | HTML et PDF générés                             | Le build            |

Les consignes pour l'IA sont dans `CLAUDE.md`.

## Démarrage

```bash
npm install
npm run preview    # aperçu en direct pendant l'écriture
npm run build      # génère 3-presentation/tolkien.html et tolkien.pdf
```

## Démarche

1. Remplir `1-brief/conference.md`, `plan.md` et `style.md`.
2. Rédiger les textes de fond dans `1-brief/textes/` et les citations dans `citations.md`.
3. Demander à l'IA de générer ou de mettre à jour `2-slides/slides.md`.
4. Relire, ajuster, lancer `npm run build`.

## Le jour J

- Ouvrir `3-presentation/tolkien.html` dans un navigateur, puis `F` pour le plein écran et `P` pour la vue présentateur (notes et minuteur).
- Le HTML a besoin du dossier `3-presentation/assets/` à côté de lui. Copier tout le dossier `3-presentation/`.
- `tolkien.pdf` sert de secours.
