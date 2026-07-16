"""Generate dark_mode.svg / light_mode.svg profile cards. Stdlib only, run once by hand."""
import html
from datetime import date

BIRTHDAY = date(1995, 1, 17)
W = 56  # info column width in characters

INFO = [
    ("OS", "Fedora"),
    ("Uptime", None),  # computed
    ("Kernel", "Fullstack Developer"),
    ("IDE", "Neovim, Claude CLI"),
    None,
    ("Languages.Programming", "Go, Python, JavaScript"),
]

CONTACT = [
    ("Email", "barisopa1@hotmail.com"),
]

PALETTES = {
    "dark": {"bg": "#0d1117", "border": "#30363d", "h": "#58a6ff", "k": "#ffa657", "v": "#c9d1d9", "d": "#484f58"},
    "light": {"bg": "#ffffff", "border": "#d0d7de", "h": "#0969da", "k": "#953800", "v": "#24292f", "d": "#afb8c1"},
}


def age(b, t):
    years = t.year - b.year - ((t.month, t.day) < (b.month, b.day))
    months = (t.month - b.month - (t.day < b.day)) % 12
    if t.day >= b.day:
        days = t.day - b.day
    else:
        pm_year, pm = (t.year, t.month - 1) if t.month > 1 else (t.year - 1, 12)
        import calendar
        days = calendar.monthrange(pm_year, pm)[1] - b.day + t.day
    return years, months, days


def kv(key, val, width=W):
    dots = "." * max(width - len(key) - len(str(val)) - 3, 1)
    return [(f"{key}: ", "k"), (dots + " ", "d"), (str(val), "v")]


def rule(title):
    label = f"─ {title} "
    return [(label, "h"), ("─" * (W - len(label)), "d")]


def info_lines():
    y, m, d = age(BIRTHDAY, date.today())
    lines = [[("khroxx@github ", "h"), ("─" * (W - 14), "d")], []]
    for row in INFO:
        if row is None:
            lines.append([])
        elif row[0] == "Uptime":
            lines.append(kv("Uptime", f"{y} years, {m} months, {d} days"))
        else:
            lines.append(kv(*row))
    lines.append([])
    lines.append(rule("Contact"))
    for row in CONTACT:
        lines.append(kv(*row))
    return lines


def render(mode):
    p = PALETTES[mode]
    lines = info_lines()
    height = 45 + len(lines) * 21 + 20
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="460" height="{height}" viewBox="0 0 460 {height}" '
        'font-family="Consolas, Menlo, monospace" font-size="13px">',
        f'<rect x="0.5" y="0.5" width="459" height="{height - 1}" rx="10" fill="{p["bg"]}" stroke="{p["border"]}"/>',
    ]
    for i, segs in enumerate(lines):
        if not segs:
            continue
        spans = "".join(f'<tspan fill="{p[c]}">{html.escape(t)}</tspan>' for t, c in segs)
        out.append(f'<text x="25" y="{45 + i * 21}" xml:space="preserve">{spans}</text>')
    out.append("</svg>")
    return "\n".join(out)


def selfcheck():
    assert age(date(1995, 1, 17), date(2026, 7, 16)) == (31, 5, 29)
    assert len("".join(t for t, _ in kv("OS", "Fedora"))) == W


if __name__ == "__main__":
    selfcheck()
    for mode in PALETTES:
        with open(f"{mode}_mode.svg", "w", encoding="utf-8") as f:
            f.write(render(mode))
    print("wrote dark_mode.svg, light_mode.svg")
