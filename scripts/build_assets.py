"""Build the profile's self-contained SVG artwork. Run with Python 3."""

from html import escape
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / "assets"
PALETTES = {
    "dark": dict(bg="#0c1722", fg="#edf5f2", muted="#a4b8b8", line="#29414b", accent="#77e5bb", soft="#132f32"),
    "light": dict(bg="#f1f7f4", fg="#122e35", muted="#4c686c", line="#c6dbd4", accent="#087756", soft="#deeee6"),
}


def svg(name, width, height, title, description, content, css=""):
    document = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title>
<desc id="desc">{escape(description)}</desc>
<style>
text{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}}
.mono{{font-family:ui-monospace,SFMono-Regular,Consolas,monospace}}
{css}
@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}.cursor{{display:none}}}}
</style>
{content}
</svg>\n'''
    (ASSETS / name).write_text(document)
    if "@keyframes" in css:
        still = document.replace('</style>', '*{animation:none!important}.cursor{display:none!important}</style>')
        (ASSETS / name.replace('.svg', '-still.svg')).write_text(still)


def text(x, y, value, size, fill, extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" {extra}>{escape(value)}</text>'


def hero(theme, mobile):
    p = PALETTES[theme]
    w, h = (440, 500) if mobile else (960, 360)
    x = 28 if mobile else 48
    court = '''<g fill="none" stroke="{accent}" stroke-width="1.5" opacity=".35">
<path d="M40 30H270V330H40Z M40 180H270 M62 30V330 M248 30V330 M40 108H270 M40 252H270 M155 30V108 M155 252V330"/>
<path d="M22 180H288" stroke-dasharray="2 4"/>
</g>'''.format(**p)
    court_transform = "translate(197 264) rotate(-22) scale(.64)" if mobile else "translate(615 -4) rotate(18 155 180)"
    arc = "M248 434Q260 284 397 335" if mobile else "M610 264Q676 44 903 166"
    # The resting shuttle is visible when reduced motion is enabled.
    end = (397, 335) if mobile else (903, 166)
    shuttle = f'''<g transform="translate({end[0]} {end[1]})"><g class="shuttle" fill="{p['fg']}" stroke="{p['bg']}" stroke-width="1">
<path d="M-6 0L-24-19L-12-26L0-29L10-26L6 0Z"/>
<path d="M-3-1L-12-25M1-1L0-28M4-1L9-25" stroke="{p['accent']}"/>
<path d="M-6 0H6V5A6 6 0 0 1-6 5Z" fill="{p['accent']}"/>
</g></g>'''
    animation = "@keyframes shuttle{0%,100%{transform:translate(-149px,99px) rotate(-48deg);opacity:0}8%{opacity:1}32%{transform:translate(-123px,-2px) rotate(-20deg)}60%{transform:translate(-59px,-26px) rotate(35deg)}85%{transform:translate(0,0) rotate(70deg);opacity:1}94%{opacity:0}}" if mobile else "@keyframes shuttle{0%,100%{transform:translate(-293px,98px) rotate(-48deg);opacity:0}8%{opacity:1}32%{transform:translate(-228px,-46px) rotate(-20deg)}60%{transform:translate(-126px,-49px) rotate(35deg)}85%{transform:translate(0,0) rotate(70deg);opacity:1}94%{opacity:0}}"
    title_y = 137 if mobile else 155
    name_size = 55 if mobile else 76
    body = f'<rect width="{w}" height="{h}" rx="20" fill="{p["bg"]}"/>'
    body += f'<g transform="{court_transform}">{court}</g>'
    body += f'<path d="{arc}" fill="none" stroke="{p["accent"]}" stroke-width="2" stroke-dasharray="3 8" opacity=".55" class="arc"/>{shuttle}'
    body += f'<circle cx="{x + 4}" cy="54" r="4" fill="{p["accent"]}"/>'
    body += text(x + 19, 59, "CANADA / FULL STACK DEVELOPER", 11 if mobile else 12, p["muted"], 'class="mono" letter-spacing="1.2"')
    body += text(x - 2, title_y, "Divy Dantu", name_size, p["fg"], 'font-weight="750" letter-spacing="-2.5" class="name"')
    body += text(x, title_y + 42, "Building useful things for the web.", 19 if mobile else 23, p["muted"], 'class="intro"')
    line_y = 231 if mobile else 267
    body += f'<path d="M{x} {line_y}H{w-x}" stroke="{p["line"]}"/>'
    body += text(x, line_y + 37, "</>", 15, p["accent"], 'class="mono"')
    body += '<defs><clipPath id="typing"><rect class="typing" x="0" y="0" width="270" height="40"/></clipPath></defs>'
    body += f'<g transform="translate({x+39} {line_y+17})" clip-path="url(#typing)">{text(0,20,"Code. Ship. Hit the court.",14,p["fg"], 'class="mono"')}</g>'
    body += f'<path class="cursor" d="M{x+39} {line_y+21}v18" stroke="{p["accent"]}" stroke-width="2"/>'
    css = f'''.name{{animation:appear .8s ease-out both}}.intro{{animation:appear .8s .15s ease-out both}}
@keyframes appear{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:translateY(0)}}}}
.shuttle{{animation:shuttle 7s ease-in-out infinite}}{animation}
.arc{{animation:flow 2s linear infinite}}@keyframes flow{{to{{stroke-dashoffset:-22}}}}
.typing{{animation:type 9s steps(25,end) infinite}}@keyframes type{{0%,8%{{width:0}}45%,88%,100%{{width:270px}}}}
.cursor{{animation:caret 9s steps(25,end) infinite,blink 1s step-end infinite}}@keyframes caret{{0%,8%{{transform:translateX(0)}}45%,88%,100%{{transform:translateX(211px)}}}}@keyframes blink{{50%{{opacity:0}}}}'''
    svg(f'hero-{theme}{"-mobile" if mobile else ""}.svg', w, h, "Divy Dantu — Full stack developer in Canada", "Building useful things for the web. A shuttlecock arcs across a badminton court. Code. Ship. Hit the court.", body, css)


def workflow(theme, mobile):
    p = PALETTES[theme]
    w, h = (440, 362) if mobile else (960, 170)
    labels = [("Book a court", "Find a time to play"), ("Invite players", "Bring everyone together"), ("Play together", "Get on the court"), ("Split costs", "Keep balances clear")]
    body = f'<rect width="{w}" height="{h}" rx="16" fill="{p["bg"]}"/>'
    path = "M42 48V300" if mobile else "M123 57H837"
    body += f'<path d="{path}" fill="none" stroke="{p["line"]}" stroke-width="2"/>'
    body += f'<path class="flow" d="{path}" fill="none" stroke="{p["accent"]}" stroke-width="2" stroke-dasharray="4 12"/>'
    for i, (label, caption) in enumerate(labels):
        cx, cy = (42, 48+i*84) if mobile else (123+i*238, 57)
        body += f'<circle class="step s{i}" cx="{cx}" cy="{cy}" r="20" fill="{p["soft"]}" stroke="{p["accent"]}"/>'
        body += text(cx, cy+5, f"0{i+1}", 12, p["accent"], 'text-anchor="middle" class="mono"')
        tx, ty = (82, cy-1) if mobile else (cx, 106)
        anchor = '' if mobile else 'text-anchor="middle"'
        body += text(tx, ty, label, 18, p["fg"], f'font-weight="600" {anchor}')
        body += text(tx, ty+24, caption, 13, p["muted"], anchor)
    css = '.flow{animation:flow 1.8s linear infinite}@keyframes flow{to{stroke-dashoffset:-32}}.step{animation:step 8s ease-in-out infinite}.s1{animation-delay:2s}.s2{animation-delay:4s}.s3{animation-delay:6s}@keyframes step{0%,24%{stroke-width:3}25%,100%{stroke-width:1}}'
    svg(f'badminton-{theme}{"-mobile" if mobile else ""}.svg',w,h,"Badminton Bookings workflow","Book a court, invite players, play together, and split costs.",body,css)


def stack(theme, mobile):
    p = PALETTES[theme]
    w, h = (440, 118) if mobile else (960, 62)
    names = [("TS", "TypeScript"), ("N", "Next.js"), ("JS", "JavaScript"), ("Py", "Python"), ("J", "Java")]
    body = ''
    for i, (mark, label) in enumerate(names):
        x, y = ((i % 3)*148, (i//3)*62) if mobile else (i*194, 0)
        bw = 144 if mobile else 184
        body += f'<g class="tech t{i}" transform="translate({x} {y})"><rect width="{bw}" height="50" rx="9" fill="{p["bg"]}"/><rect x="10" y="11" width="28" height="28" rx="5" fill="{p["soft"]}"/>'
        body += text(24,30,mark,12,p["accent"],'text-anchor="middle" font-weight="700" class="mono"')
        body += text(47,30,label,13 if mobile else 15,p["fg"],'font-weight="550"') + '</g>'
    css = '.tech{animation:in .7s ease-out both}.t1{animation-delay:.1s}.t2{animation-delay:.2s}.t3{animation-delay:.3s}.t4{animation-delay:.4s}@keyframes in{from{opacity:0}to{opacity:1}}'
    svg(f'stack-{theme}{"-mobile" if mobile else ""}.svg',w,h,"Tech I work with","TypeScript, Next.js, JavaScript, Python, and Java.",body,css)


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    for theme in PALETTES:
        for mobile in (False, True):
            hero(theme, mobile)
            workflow(theme, mobile)
            stack(theme, mobile)
    for filename, label, mark in (("website", "Portfolio", "↗"), ("linkedin", "LinkedIn", "in"), ("email", "Email", "@")):
        body = '<rect width="120" height="36" rx="7" fill="#132f32"/>'
        body += text(18,23,mark,14,"#77e5bb",'text-anchor="middle" font-weight="600"')
        body += text(37,23,label,13,"#edf5f2",'font-weight="550"')
        svg(f'{filename}.svg',120,36,label,f'Visit my {label.lower()}' if filename != "email" else "Email Divy Dantu",body)
