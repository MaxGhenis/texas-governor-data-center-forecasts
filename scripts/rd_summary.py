"""Per-run discontinuity summaries of the raw answers, by model.

For every pooled run and every question answered at all six cells, take the run's own answer at each
cell (the probability for a yes/no question, the median for a quantity) and report:

- jump: the answer at 50.5% minus the answer at 49.5%, the cutoff contrast in the raw answers;
- fit_jump: the gap at 50% between least-squares lines through the three cells on each side;
- total: the answer at 56% minus the answer at 44%;
- within: total minus jump, the part of the 44%-to-56% change that the margin carries rather than who
  wins.

Averages are over runs, overall and by model. The runs are those `i86 simulate` pooled (the keys of
`per_run` in outputs/summary.json). These are model forecasts under stated scenarios, not
observations, and they use medians and probabilities, not the simulator's means.

    .venv/bin/python scripts/rd_summary.py [--root DIR]
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from i86 import graph as graph_mod  # noqa: E402
from i86.graph import cell_label  # noqa: E402
from i86.response import parse  # noqa: E402

LEFT, RIGHT = (0.44, 0.47, 0.495), (0.505, 0.53, 0.56)
MEASURES = ("jump", "fit_jump", "total", "within")


def family(meta: dict, label: str) -> str:
    """'Opus' or 'Sol' from the served model, else from the run's label."""
    served = str(meta.get("model_served") or "").lower()
    for text in (served, label.lower()):
        if "opus" in text or "claude" in text:
            return "Opus"
        if "sol" in text or "gpt" in text:
            return "Sol"
    return "other"


def line_at(xs: tuple[float, ...], ys: list[float], x0: float) -> float:
    """Least-squares line through (xs, ys), evaluated at x0."""
    mx, my = statistics.fmean(xs), statistics.fmean(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    return my + slope * (x0 - mx)


def point(graph, node, value) -> float:
    """A run's answer at one cell: the probability, or the median of a quantity."""
    if node.kind == "binary":
        return float(value)
    return float(value[list(graph.quantiles).index(0.5)])


def measures(graph, node, vals: dict) -> dict | None:
    cells = LEFT + RIGHT
    if any(cell_label(c) not in vals for c in cells):
        return None
    y = {c: point(graph, node, vals[cell_label(c)]) for c in cells}
    jump = y[0.505] - y[0.495]
    fit = line_at(RIGHT, [y[c] for c in RIGHT], 0.5) - line_at(LEFT, [y[c] for c in LEFT], 0.5)
    total = y[0.56] - y[0.44]
    return {"jump": jump, "fit_jump": fit, "total": total, "within": total - jump,
            **{f"at_{c * 100:g}": y[c] for c in cells}}


def fmt(node, x: float) -> str:
    if node.kind == "binary":
        return f"{x * 100:+.1f} pts"
    if abs(x) >= 100 or node.integer or node.unit == "MW":
        return f"{x:+,.0f}"
    return f"{x:+.2f}"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=ROOT, help="the directory holding runs/ and outputs/")
    args = ap.parse_args(argv)
    g = graph_mod.load()
    summary = json.loads((args.root / "outputs" / "summary.json").read_text())
    labels = sorted(summary["per_run"])
    rows, by = [], {}
    for label in labels:
        run = args.root / "runs" / label
        meta = json.loads((run / "meta.json").read_text())
        fc = parse(g, json.loads((run / "response.json").read_text()))
        fam = family(meta, label)
        for node in g.forecast_nodes():
            if node.kind not in {"binary", "quantity"}:
                continue
            m = measures(g, node, fc.values.get(node.id, {}))
            if m is None:
                continue
            rows.append({"run": label, "model": fam, "question": node.id, **m})
            for group in ("All", fam):
                by.setdefault((node.id, group), []).append(m)
    out = args.root / "outputs"
    with open(out / "rd.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    groups = ["All", *sorted({r["model"] for r in rows})]
    counts = {grp: len({r["run"] for r in rows if grp == "All" or r["model"] == grp}) for grp in groups}
    lines = [
        "# Cutoff contrasts in the raw answers",
        "",
        "Each run's own answers at the six cells: the probability for yes/no questions, the median for "
        "quantities. 'Jump' is the answer at 50.5% minus the answer at 49.5%. 'Fitted jump' is the gap at "
        "50% between least-squares lines through the three cells on each side. 'Total' is the answer at "
        "56% minus the answer at 44%, and 'within sides' is total minus jump: the part of that change the "
        "margin carries rather than who wins. Each cell gives the mean over runs, with the range across "
        "runs in brackets. These are model forecasts under stated scenarios, not observations.",
        "",
        "Runs: " + ", ".join(f"{grp} {counts[grp]}" for grp in groups) + ".",
        "",
    ]
    for module, title in g.modules.items():
        nodes = [n for n in g.forecast_nodes() if n.module == module and (n.id, "All") in by]
        if not nodes:
            continue
        lines += [f"## {title}", "", "| Question | Runs | Jump | Fitted jump | Total (44% to 56%) | Within sides |",
                  "|---|---|---|---|---|---|"]
        for node in nodes:
            for grp in groups:
                ms = by.get((node.id, grp))
                if not ms:
                    continue
                cells = []
                for key in MEASURES:
                    xs = [m[key] for m in ms]
                    cells.append(f"{fmt(node, statistics.fmean(xs))} [{fmt(node, min(xs))}, {fmt(node, max(xs))}]")
                lines.append(f"| `{node.id}` | {grp} ({len(ms)}) | " + " | ".join(cells) + " |")
        lines.append("")
    (out / "rd.md").write_text("\n".join(lines))
    print(f"wrote {out / 'rd.md'} and {out / 'rd.csv'} from {len(labels)} run(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
