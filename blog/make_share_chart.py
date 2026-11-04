"""Draw the blog post's chart of the pooled forecasts at each Hinojosa share, from outputs/after-the-vote/by_share.json.

    python3 blog/make_share_chart.py
    rsvg-convert -z 2 -b white blog/images/forecasts-by-share.svg -o blog/images/forecasts-by-share.png

Each panel shows one question's pooled mean at the six shares the forecasters answered at, joined on
each side of 50% as the simulator interpolates them, and marks the mean at Hinojosa's share in the
November 4 count. Each panel's axis starts at zero.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "outputs" / "after-the-vote" / "by_share.json").read_text())
OUT = ROOT / "blog" / "images" / "forecasts-by-share.svg"

ABBOTT, HINOJOSA = "#eb6834", "#2a78d6"
INK, MUTED, GRID, PAPER = "#0b0b0b", "#52514e", "#e6e5e1", "#fcfcfb"
TITLE = "What the forecasters expect at each Hinojosa share of the vote"
FOOTER = ("Six runs each of Claude Opus 5.5 and GPT-6.1 Sol forecast each question at six shares on Nov 3, 2026, before polls closed.",
          "Each dot marks the average of the 12 runs' forecasts; lines join the dots on each side of 50%.")
ABBOTT_CELLS, HINOJOSA_CELLS = [0.44, 0.47, 0.495], [0.505, 0.53, 0.56]
COUNT = DATA["count_share"]
COLUMNS = [16, 266, 516]
ROWS = [70, 252]
PLOT_LEFT, PLOT_RIGHT, PLOT_TOP, PLOT_HEIGHT = 46, 232, 38, 110

# (header lines, node, axis maximum, ticks, scale from stored value to axis units, label at the count)
PANELS = [
    (("ERCOT resumes approving data centers", "to energize by June 30, 2027"), "ercot_pause_lifted",
     100, [0, 50, 100], 100, lambda v: f"{v:.0f}%"),
    (("The governor calls a special session", "on data centers by the end of 2027"), "special_session_data_centers",
     100, [0, 50, 100], 100, lambda v: f"{v:.0f}%"),
    (("Texas enacts a law adding limits on", "data centers by the end of 2027"), "restriction_law",
     100, [0, 50, 100], 100, lambda v: f"{v:.0f}%"),
    (("Megawatts ERCOT has approved to", "energize, at the end of 2028"), "ercot_approved_mw_2028",
     30000, [0, 10000, 20000, 30000], 1, lambda v: f"{round(v, -2):,.0f}"),
    (("Projects the Comptroller registers for", "data center tax breaks, effective 2027"), "comptroller_new_projects_2027",
     70, [0, 20, 40, 60], 1, lambda v: f"{v:.0f}"),
    (("US private construction spending on", "data centers in 2028 ($ billion)"), "us_dc_spending_2028",
     175, [0, 50, 100, 150], 1, lambda v: f"{v:.0f}"),
]


def tick_label(t: float, top: float) -> str:
    return f"{t:.0f}%" if top == 100 else f"{t:,.0f}"


def mean(share: float, node: str, scale: float) -> float:
    return scale * DATA["by_share"][str(share)][node]["all"]


def dot(x, y, color, filled):
    if filled:
        return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{color}" stroke="{PAPER}" stroke-width="2"/>'
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{PAPER}" stroke="{color}" stroke-width="2"/>'


def panel(col_x: int, row_y: int, spec) -> list:
    (line1, line2), node, top, ticks, scale, fmt = spec
    x0, x1 = col_x + PLOT_LEFT, col_x + PLOT_RIGHT
    y_top, y_bottom = row_y + PLOT_TOP, row_y + PLOT_TOP + PLOT_HEIGHT
    sx = lambda s: x0 + (x1 - x0) * (s - 0.44) / 0.12
    sy = lambda v: y_bottom - (y_bottom - y_top) * v / top
    out = [f'<text x="{col_x}" y="{row_y + 12}" font-size="12" font-weight="600" fill="{INK}">{line1}</text>',
           f'<text x="{col_x}" y="{row_y + 26}" font-size="12" font-weight="600" fill="{INK}">{line2}</text>']
    for t in ticks:
        out.append(f'<line x1="{x0}" x2="{x1}" y1="{sy(t):.1f}" y2="{sy(t):.1f}" stroke="{GRID}"/>')
        out.append(f'<text x="{x0 - 6}" y="{sy(t) + 4:.1f}" font-size="11" fill="{MUTED}" text-anchor="end">{tick_label(t, top)}</text>')
    for s in [0.44, 0.47, 0.50, 0.53, 0.56]:
        out.append(f'<text x="{sx(s):.1f}" y="{y_bottom + 16}" font-size="11" fill="{MUTED}" text-anchor="middle">{s:.0%}</text>')
    out.append(f'<line x1="{sx(0.5):.1f}" x2="{sx(0.5):.1f}" y1="{y_top}" y2="{y_bottom}" stroke="{MUTED}" stroke-width="1"/>')
    out.append(f'<line x1="{sx(COUNT):.1f}" x2="{sx(COUNT):.1f}" y1="{y_top}" y2="{y_bottom}" stroke="{MUTED}" stroke-width="1" stroke-dasharray="3 3"/>')
    for cells, color in [(ABBOTT_CELLS, ABBOTT), (HINOJOSA_CELLS, HINOJOSA)]:
        points = " ".join(f"{sx(s):.1f},{sy(mean(s, node, scale)):.1f}" for s in cells)
        out.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="2"/>')
        for s in cells:
            v = mean(s, node, scale)
            out.append(f'<g><title>{s:.1%} Hinojosa share: {fmt(v)}</title>{dot(sx(s), sy(v), color, True)}</g>')
    v = mean(COUNT, node, scale)
    out.append(f'<g><title>{COUNT:.1%} Hinojosa share, in the Nov 4 count: {fmt(v)}</title>{dot(sx(COUNT), sy(v), HINOJOSA, False)}</g>')
    out.append(f'<text x="{sx(COUNT) + 8:.1f}" y="{sy(v) - 8:.1f}" font-size="12" font-weight="600" fill="{INK}">{fmt(v)}</text>')
    return out


def svg() -> str:
    body = []
    for i, spec in enumerate(PANELS):
        body += panel(COLUMNS[i % 3], ROWS[i // 3], spec)
    axis_y = ROWS[1] + PLOT_TOP + PLOT_HEIGHT + 32
    height = axis_y + 50
    head = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 {height}" width="760" height="{height}" '
        f'font-family="Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif" role="img" aria-label="{TITLE}">',
        f'<rect width="100%" height="100%" fill="{PAPER}"/>',
        f'<text x="16" y="24" font-size="15" font-weight="600" fill="{INK}">{TITLE}</text>',
        f'<line x1="16" x2="36" y1="46" y2="46" stroke="{ABBOTT}" stroke-width="2"/>', dot(26, 46, ABBOTT, True),
        f'<text x="42" y="50" font-size="12" fill="{INK}">Abbott wins</text>',
        f'<line x1="132" x2="152" y1="46" y2="46" stroke="{HINOJOSA}" stroke-width="2"/>', dot(142, 46, HINOJOSA, True),
        f'<text x="158" y="50" font-size="12" fill="{INK}">Hinojosa wins</text>',
        f'<line x1="264" x2="264" y1="38" y2="54" stroke="{MUTED}" stroke-width="1" stroke-dasharray="3 3"/>',
        dot(264, 46, HINOJOSA, False),
        f'<text x="274" y="50" font-size="12" fill="{INK}">At {COUNT:.1%}, Hinojosa\'s share in the Nov 4 count</text>',
    ]
    foot = [f'<text x="380" y="{axis_y}" font-size="11" fill="{MUTED}" text-anchor="middle">Hinojosa\'s share of the two-party vote for governor</text>']
    foot += [f'<text x="16" y="{axis_y + 22 + 14 * i}" font-size="11" fill="{MUTED}">{line}</text>'
             for i, line in enumerate(FOOTER)]
    return "\n".join(head + body + foot + ["</svg>"]) + "\n"


if __name__ == "__main__":
    OUT.write_text(svg())
    for (line1, line2), node, _, _, scale, fmt in PANELS:
        print(f"{node}: " + "  ".join(f"{s}: {fmt(mean(s, node, scale))}" for s in ABBOTT_CELLS + HINOJOSA_CELLS + [COUNT]))
