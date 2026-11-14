"""Add accessible metadata and a still frame for reduced-motion visitors."""

import re
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / "assets"
for theme in ("dark", "light"):
    path = ASSETS / f"contributions-{theme}.svg"
    content = path.read_text()
    # Re-running this script leaves the SVG unchanged.
    if 'id="snake-title"' not in content:
        content = content.replace("<svg ", '<svg role="img" aria-labelledby="snake-title snake-desc" ', 1)
        metadata = '<title id="snake-title">Divy Dantu’s GitHub contributions</title><desc id="snake-desc">A snake moves through the public GitHub contribution calendar. Reduced motion shows a still frame.</desc><style>@media(prefers-reduced-motion:reduce){*{animation:none!important}}</style>'
        content = re.sub(r"(<svg\b[^>]*>)", lambda match: match[0]+metadata, content, count=1)
    path.write_text(content)
    still = content.replace('</svg>', '<style>*{animation:none!important}</style></svg>')
    path.with_name(f'contributions-{theme}-still.svg').write_text(still)
