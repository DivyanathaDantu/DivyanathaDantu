# Profile artwork

The profile uses self-contained SVGs with CSS animations, system fonts, and no external image or font requests. Light/dark and desktop/mobile versions are selected by the README's `<picture>` elements. Every SVG includes accessible text. Reduced-motion visitors get explicit still-image variants, with CSS media queries inside animated SVGs as a second fallback.

Regenerate the hero, workflow, stack, and contact badges:

```sh
python3 scripts/build_assets.py
```

Refresh the public repository statistics:

```sh
python3 scripts/update_stats.py
```

The activity workflow runs daily at 06:23 UTC, on relevant changes merged into `main`, or manually from GitHub Actions. It generates the contribution snakes with [Platane/snk](https://github.com/Platane/snk), adds accessibility metadata with `scripts/prepare_snake.py`, refreshes stats, and commits changed files. The generated assets are checked in, so the profile still displays the last successful update if a refresh fails. No additional secrets are needed; the workflow uses its built-in GitHub token.

Statistics use public repositories only. Stars exclude forks; the language is the most frequent primary language across original public repositories, rather than a measure of code volume or proficiency.
