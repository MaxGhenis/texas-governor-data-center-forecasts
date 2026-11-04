"""Draw the election-night thread's quantities chart from the pooled means in outputs/summary.json.

    python3 social/make_quantity_chart.py
    rsvg-convert -z 2.5 -b white social/images/thread-quantities.svg -o social/images/thread-quantities.png

Each row shows four pooled means, as in social/images/thread-chart.svg: if Abbott wins, if Hinojosa
wins, at a Hinojosa share of 49.5% and at 50.5%. Each panel has its own axis from zero. The right
column gives the change from 49.5% to 50.5%.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NODES = json.loads((ROOT / "outputs" / "summary.json").read_text())["nodes"]
OUT = ROOT / "social" / "images" / "thread-quantities.svg"

ABBOTT, HINOJOSA = "#eb6834", "#2a78d6"
INK, MUTED, GRID, PAPER = "#0b0b0b", "#52514e", "#e6e5e1", "#fcfcfb"
LABEL_X, X0, X1, CHANGE_X = 128, 140, 600, 682
TITLE = "What the forecasters expect for data center growth"
FOOTER = ("Six runs each of Claude Opus 5.5 and GPT-6.1 Sol made these forecasts on Nov 3, 2026.",
          "Each dot marks the average of the 12 runs' forecasts.")

# (header, axis maximum, ticks, rows of (label, node))
PANELS = [
    ("Texas: megawatts of large power users that ERCOT has approved to switch on", 30000,
     [0, 10000, 20000, 30000],
     [("End of 2027", "ercot_approved_mw_2027"), ("End of 2028", "ercot_approved_mw_2028")]),
    ("Texas: data center projects the Comptroller registers for sales tax breaks", 70,
     [0, 20, 40, 60],
     [("Effective in 2027", "comptroller_new_projects_2027")]),
    ("Nationwide: private construction spending on data centers ($ billion)", 175,
     [0, 50, 100, 150],
     [("2027", "us_dc_spending_2027"), ("2028", "us_dc_spending_2028")]),
]


def means(node: str) -> dict:
    n = NODES[node]
    return {"abbott": n["N"]["mean"], "hinojosa": n["Y"]["mean"],
            "loss": n["cutoff_fail"]["mean"], "win": n["cutoff_pass"]["mean"]}


def change(node: str) -> float:
    m = means(node)
    return 100 * (m["win"] / m["loss"] - 1)


def signed(pct: float) -> str:
    return f"{pct:+.1f}%".replace("-", "−")


def dot(x, y, color, filled):
    if filled:
        return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{color}" stroke="{PAPER}" stroke-width="2"/>'
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{PAPER}" stroke="{color}" stroke-width="2"/>'


def svg() -> str:
    out = []
    y = 84
    for header, top, ticks, rows in PANELS:
        sx = lambda v, top=top: X0 + (X1 - X0) * v / top
        out.append(f'<text x="16" y="{y}" font-size="12" font-weight="600" fill="{INK}">{header}</text>')
        grid_top, y = y + 10, y + 20
        body = []
        for label, node in rows:
            m = means(node)
            body.append(f'<text x="{LABEL_X}" y="{y + 12}" font-size="12" fill="{INK}" text-anchor="end">{label}</text>')
            body.append(f'<g><title>{label}: {m["abbott"]:,.1f} if Abbott wins, {m["hinojosa"]:,.1f} if Hinojosa wins</title>'
                        f'<line x1="{sx(m["abbott"]):.1f}" x2="{sx(m["hinojosa"]):.1f}" y1="{y}" y2="{y}" stroke="{MUTED}" stroke-width="2"/>'
                        f'{dot(sx(m["abbott"]), y, ABBOTT, True)}{dot(sx(m["hinojosa"]), y, HINOJOSA, True)}</g>')
            body.append(f'<g><title>{label}: {m["loss"]:,.1f} at 49.5%, {m["win"]:,.1f} at 50.5%</title>'
                        f'<line x1="{sx(m["loss"]):.1f}" x2="{sx(m["win"]):.1f}" y1="{y + 16}" y2="{y + 16}" stroke="{MUTED}" stroke-width="1.5"/>'
                        f'{dot(sx(m["loss"]), y + 16, ABBOTT, False)}{dot(sx(m["win"]), y + 16, HINOJOSA, False)}</g>')
            body.append(f'<text x="{CHANGE_X}" y="{y + 20}" font-size="12" fill="{INK}" text-anchor="middle">{signed(change(node))}</text>')
            y += 40
        grid_bottom = y - 14
        for t in ticks:
            out.append(f'<line x1="{sx(t):.1f}" x2="{sx(t):.1f}" y1="{grid_top}" y2="{grid_bottom}" stroke="{GRID}"/>')
            out.append(f'<text x="{sx(t):.1f}" y="{grid_bottom + 14}" font-size="11" fill="{MUTED}" text-anchor="middle">{t:,}</text>')
        out += body
        y = grid_bottom + 44
    height = y + 18
    head = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 {height}" width="760" height="{height}" '
        f'font-family="Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif" role="img" aria-label="{TITLE}">',
        f'<rect width="100%" height="100%" fill="{PAPER}"/>',
        f'<text x="16" y="24" font-size="15" font-weight="600" fill="{INK}">{TITLE}</text>',
        dot(22, 46, ABBOTT, True), f'<text x="32" y="50" font-size="12" fill="{INK}">If Abbott wins</text>',
        dot(132, 46, HINOJOSA, True), f'<text x="142" y="50" font-size="12" fill="{INK}">If Hinojosa wins</text>',
        dot(257, 46, ABBOTT, False), f'<text x="267" y="50" font-size="12" fill="{INK}">After a one-point Hinojosa loss</text>',
        dot(470, 46, HINOJOSA, False), f'<text x="480" y="50" font-size="12" fill="{INK}">After a one-point Hinojosa win</text>',
        f'<text x="{CHANGE_X}" y="80" font-size="11" fill="{MUTED}" text-anchor="middle">From a one-point loss</text>',
        f'<text x="{CHANGE_X}" y="93" font-size="11" fill="{MUTED}" text-anchor="middle">to a one-point win</text>',
    ]
    foot = [f'<text x="16" y="{y - 4 + 14 * i}" font-size="11" fill="{MUTED}">{line}</text>'
            for i, line in enumerate(FOOTER)]
    return "\n".join(head + out + foot + ["</svg>"]) + "\n"


if __name__ == "__main__":
    OUT.write_text(svg())
    for _, _, _, rows in PANELS:
        for label, node in rows:
            m = means(node)
            print(f"{node}: abbott {m['abbott']:,.1f} hinojosa {m['hinojosa']:,.1f} "
                  f"49.5% {m['loss']:,.1f} 50.5% {m['win']:,.1f} change {change(node):+.2f}%")
