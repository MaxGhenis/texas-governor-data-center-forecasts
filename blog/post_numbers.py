"""Print the forecast figures the blog post cites, from outputs/after-the-vote/exact_by_share.json.

    python3 blog/post_numbers.py

It leaves out the figures from outside sources; the design, timing and audit figures; the Senate lines
and the fit script's 2,700 megawatts and 6.0 projects, which come from outputs/rd.csv; and the counts of
forecasters citing each reason.

For each question, overall and by model, it reads the pooled forecast at each of the six shares the
forecasters answered at, exact rather than drawn (scripts/exact_by_share.py), and prints the measures
below. On each side of 50%, a least-squares line through that side's three shares, read at 50%, gives
the forecast after a bare loss (44%, 47%, 49.5%) or a bare win (50.5%, 53%, 56%). The jump is the
second minus the first.

Before the first dispatch, the README named the contrast between the 49.5% and 50.5% cells as the
forecasters' estimate of what a bare win changes (237b4e6), and that contrast in the pooled forecasts
appears here as "contrast". Also before it, 756af19 added scripts/rd_summary.py, which fits lines to
each run's raw answers, with medians for quantities. It first wrote outputs/rd.md at 20:52Z, after the
last run finished (f36db37). After dispatch and format checks, and before anyone read an answer, the
README's headline measures listed both (82a311c). Fitting lines through the pooled forecasts, with
means for quantities, as the post does, is a choice made after the vote.

"Total" is the forecast at 56% minus the forecast at 44%, and "share" is jump / total (nan when a run's
total is zero). "2-share" is the jump from lines through the two shares nearest 50% on each side.
"Runs" counts the runs whose own jump has the pooled jump's sign. The ranges give the lowest and
highest of each model's runs at the count's share, and the slope ratios divide the Sol runs' average
slope on each side of 50% by the Opus runs'. These are model forecasts under stated scenarios, not
observations.
"""
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "outputs" / "after-the-vote" / "exact_by_share.json").read_text())
LOSS, WIN = (0.44, 0.47, 0.495), (0.505, 0.53, 0.56)
# (node, scale from stored value to printed units, unit)
QUESTIONS = [
    ("ercot_pause_lifted", 100, "pts"),
    ("special_session_data_centers", 100, "pts"),
    ("ercot_approved_mw_2028", 1, "MW"),
    ("comptroller_new_projects_2027", 1, "projects"),
    ("restriction_law", 100, "pts"),
    ("tax_exemption_cut", 100, "pts"),
    ("other_state_moratorium", 100, "pts"),
    ("us_dc_spending_2028", 1, "$bn"),
    ("ercot_approved_mw_2027", 1, "MW"),
    ("us_dc_spending_2027", 1, "$bn"),
]
# The quantities whose slopes the post compares across the two models.
SLOPE_QUESTIONS = ["ercot_approved_mw_2028", "comptroller_new_projects_2027", "us_dc_spending_2028"]


def value(share: float, node: str, group: str, scale: float) -> float:
    """Pooled forecast at one share for "all", "opus", "sol", or one run's label."""
    entry = DATA["by_share"][f"{share:g}"][node]
    return scale * (entry[group] if group in entry else entry["by_run"][group])


def runs(model: str | None = None) -> list:
    every = DATA["runs"]
    return [r for r in every if model is None or r.startswith(model)]


def line_at(cells: tuple, ys: list, share: float) -> float:
    """The least-squares line through (cells, ys), read at `share`."""
    mx, my = sum(cells) / len(cells), sum(ys) / len(ys)
    slope = sum((x - mx) * (y - my) for x, y in zip(cells, ys)) / sum((x - mx) ** 2 for x in cells)
    return my + slope * (share - mx)


def slope(cells: tuple, node: str, group: str) -> float:
    """The slope of the least-squares line through one side's three pooled forecasts."""
    return statistics.linear_regression(cells, [value(s, node, group, 1) for s in cells]).slope


def measures(node: str, group: str, scale: float) -> dict:
    y = {s: value(s, node, group, scale) for s in LOSS + WIN}
    loss = line_at(LOSS, [y[s] for s in LOSS], 0.5)
    win = line_at(WIN, [y[s] for s in WIN], 0.5)
    total = y[0.56] - y[0.44]
    near = line_at(WIN[:2], [y[s] for s in WIN[:2]], 0.5) - line_at(LOSS[1:], [y[s] for s in LOSS[1:]], 0.5)
    return {"loss": loss, "win": win, "jump": win - loss, "contrast": y[0.505] - y[0.495], "near": near,
            "total": total, "share": (win - loss) / total if total else float("nan"), "at_56": y[0.56],
            "at_count": value(DATA["count_share"], node, group, scale)}


def count_range(node: str, model: str, scale: float) -> tuple[float, float]:
    """The lowest and highest forecast among one model's runs at the count's share."""
    at_count = [value(DATA["count_share"], node, r, scale) for r in runs(model)]
    return min(at_count), max(at_count)


def slope_ratios(node: str) -> tuple[float, float]:
    """The Sol runs' average slope over the Opus runs', below 50% and above it."""
    return tuple(slope(cells, node, "sol") / slope(cells, node, "opus") for cells in (LOSS, WIN))


def vote(key: str, group: str = "all") -> float:
    entry = DATA["vote"][key]
    return entry[group] if group in entry else entry["by_run"][group]


def main() -> None:
    print(f"Runs: {len(runs())}; count share {DATA['count_share']:.1%}")
    print(f"Chance of a Hinojosa win {vote('p_win'):.1%}; of a share above 53% {vote('p_above_53'):.1%}; "
          f"above the count's {vote('p_above_count'):.1%}")
    for model in ("opus", "sol"):
        wins = [vote("p_win", r) for r in runs(model)]
        print(f"  {model} runs' chances of a win: {min(wins):.1%} to {max(wins):.1%}")
    print(f"{'question':32} {'group':5} {'bare loss':>10} {'bare win':>10} {'jump':>9} {'contrast':>9} "
          f"{'2-share':>9} {'total':>9} {'share':>6} {'at 56%':>9} {'at count':>9}")
    for node, scale, unit in QUESTIONS:
        for group in ("all", "opus", "sol"):
            m = measures(node, group, scale)
            print(f"{node[:32]:32} {group:5} {m['loss']:10.2f} {m['win']:10.2f} {m['jump']:9.2f} "
                  f"{m['contrast']:9.2f} {m['near']:9.2f} {m['total']:9.2f} {m['share']:6.3f} {m['at_56']:9.2f} "
                  f"{m['at_count']:9.2f}")
        pooled = measures(node, "all", scale)["jump"]
        same = sum(1 for r in runs() if measures(node, r, scale)["jump"] * pooled > 0)
        same_contrast = sum(1 for r in runs() if measures(node, r, scale)["contrast"] * pooled > 0)
        print(f"  {unit}; runs with the pooled jump's sign: {same} of {len(runs())} "
              f"(contrast: {same_contrast} of {len(runs())}); at the count, "
              + ", ".join(f"{model} runs {lo:.2f} to {hi:.2f}"
                          for model in ("opus", "sol") for lo, hi in [count_range(node, model, scale)]))
    print("Sol runs' slope over the Opus runs' (below 50%, above 50%): "
          + "; ".join(f"{node} {a:.3f}, {b:.3f}" for node in SLOPE_QUESTIONS for a, b in [slope_ratios(node)]))
    print(f"Talarico's mean share at the count's: {value(DATA['count_share'], 'senate_dem_share', 'all', 1):.2f}")


if __name__ == "__main__":
    main()
