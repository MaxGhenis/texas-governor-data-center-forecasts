"""Pool the registered answers at fixed Hinojosa shares exactly, with no random draws.

    .venv/bin/python scripts/exact_by_share.py

Writes outputs/after-the-vote/exact_by_share.json, laid out as scripts/by_share.py lays out
by_share.json, for the same runs, questions and shares. Every question in the map hangs on the vote
share alone, so at a fixed share each run's forecast follows from its own answers there:

- a yes/no question's forecast is the probability the simulator interpolates (`simulate.node_params`),
  the chance that one of its draws comes up yes;
- a quantity's forecast is the mean of the piecewise-linear inverse CDF through its interpolated
  quantiles and the simulator's tails (`dists.quantity_knots`), with each value rounded to a whole unit
  where the map counts whole units, as `dists.sample_quantity` rounds its draws.

The vote block gives each run's chance of a Hinojosa win, of a share above 53% and of a share above the
count's, from that run's share distribution (`dists.share_cdf_at`).

by_share.json estimates the same values from 20,000 draws per run and share. Before writing, the script
checks that every run's exact value lies within six standard errors of by_share.json's average, and that
each run's chance of a win equals the one in outputs/summary.json.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import by_share  # noqa: E402
from i86 import cli, dists, graph as graph_mod  # noqa: E402
from i86.simulate import node_params  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "after-the-vote" / "exact_by_share.json"
# The largest gap, in standard errors of by_share.json's averages, that the check allows.
MAX_Z = 6.0


def mean_rint(a, b):
    """The mean of rint(x) for x uniform on [a, b], a <= b, elementwise; rint(a) where a == b. Away from
    exact halves, which hold no probability, rint(x) = floor(x + 1/2), whose integral from 0 to y is F(y)
    below. Shifting by k = floor(a + 1/2) puts a - k + 1/2 in [0, 1), where F vanishes, so an interval
    inside one rounding step gives k exactly."""
    def F(y):
        f = np.floor(y)
        return f * (y - f) + f * (f - 1) / 2
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    k = np.floor(a + 0.5)
    wide = b - a > 0
    inner = (F(b - k + 0.5) - F(a - k + 0.5)) / np.where(wide, b - a, 1.0)
    return np.where(wide, k + inner, np.rint(a))


def quantity_moments(levels, q, lo: float, hi: float, integer: bool):
    """The mean and second moment of `dists.sample_quantity(levels, q, lo, hi, u, integer)` over a
    uniform u, for each row of quantiles q. The second moment leaves out rounding; it serves only the
    check against the draws."""
    probs, values = dists.quantity_knots(levels, q, lo, hi)
    dp = np.diff(probs)
    a, b = values[:, :-1], values[:, 1:]
    mean = (dp * (mean_rint(a, b) if integer else (a + b) / 2)).sum(1)
    second = (dp * (a * a + a * b + b * b) / 3).sum(1)
    return mean, second


def forecast(g, node, fc, share: float) -> tuple[float, float]:
    """One run's forecast of one question at one share, and its variance across the simulator's draws
    (about 1/12 more for a rounded quantity)."""
    params = node_params(g, node, fc, np.array([share]), None)
    if node.kind == "binary":
        p = float(params[0, 0])
        return p, p * (1 - p)
    assert node.kind == "quantity", node.kind
    mean, second = quantity_moments(g.quantiles, params, *node.bounds, node.integer)
    m = float(mean[0])
    return m, max(float(second[0]) - m * m, 0.0) + (1 / 12 if node.integer else 0.0)


def vote(g, fc) -> dict:
    """One run's chances of a Hinojosa share above 50%, above 53% and above the count's share."""
    cdf = np.asarray(fc.values["dem_share"]["all"], dtype=float)
    above = lambda x: 1 - float(dists.share_cdf_at(g.share_grid, cdf, g.share_floor, g.share_ceiling, x))
    return {"p_win": above(0.5), "p_above_53": above(0.53), "p_above_count": above(by_share.COUNT_SHARE)}


def z_score(exact: float, variance: float, drawn: float, n: int) -> float:
    if variance <= 0:
        return 0.0 if math.isclose(drawn, exact, rel_tol=1e-12, abs_tol=1e-12) else math.inf
    return (drawn - exact) / math.sqrt(variance / n)


def compute(check: bool = True) -> dict:
    g = graph_mod.load()
    runs = cli.accepted_runs(g, cli._prompt_sha(), False, by_share.ACCEPT_PRIOR, by_share.ACCEPT_SUSPECT)
    drawn = json.loads(by_share.OUT.read_text())
    summary = json.loads((ROOT / "outputs" / "summary.json").read_text())
    if sorted(runs) != drawn["runs"] or sorted(runs) != sorted(summary["runs"]):
        raise ValueError(f"accepted runs {sorted(runs)} differ from by_share.json or outputs/summary.json")

    out = {"count": by_share.COUNT, "count_share": by_share.COUNT_SHARE, "runs": sorted(runs), "by_share": {},
           "vote": {}}
    worst = 0.0
    for share in by_share.SHARES:
        per_run = {}
        for rid, fc in sorted(runs.items()):
            per_run[rid] = {}
            for k in by_share.NODES:
                value, variance = forecast(g, g.nodes[k], fc, share)
                per_run[rid][k] = value
                z = z_score(value, variance, drawn["by_share"][str(share)][k]["by_run"][rid], by_share.N)
                worst = max(worst, abs(z))
                if check and abs(z) > MAX_Z:
                    raise ValueError(f"{rid} {k} at {share}: exact {value}, by_share.json {z:.1f} standard errors away")
        out["by_share"][str(share)] = {k: by_share.pooled(per_run, k) for k in by_share.NODES}

    per_run = {rid: vote(g, fc) for rid, fc in sorted(runs.items())}
    for rid, chances in per_run.items():
        registered = summary["vote"]["by_run"][rid]["p_pass"]
        if check and not math.isclose(chances["p_win"], registered, rel_tol=1e-9, abs_tol=1e-12):
            raise ValueError(f"{rid}: chance of a win {chances['p_win']} here, {registered} in outputs/summary.json")
        for k, p in chances.items():
            z = z_score(p, p * (1 - p), drawn["vote"][k]["by_run"][rid], by_share.N)
            worst = max(worst, abs(z))
            if check and abs(z) > MAX_Z:
                raise ValueError(f"{rid} {k}: exact {p}, by_share.json {z:.1f} standard errors away")
    out["vote"] = {k: by_share.pooled(per_run, k) for k in next(iter(per_run.values()))}
    out["worst_z"] = worst
    return out


def main() -> None:
    out = compute()
    OUT.write_text(json.dumps(out, indent=1) + "\n")
    for k in by_share.NODES:
        print(k, "  ".join(f"{s}:{out['by_share'][str(s)][k]['all']:.4g}" for s in by_share.SHARES))
    print({k: round(v["all"], 4) for k, v in out["vote"].items()})
    print(f"largest gap from by_share.json's averages: {out['worst_z']:.2f} standard errors")


if __name__ == "__main__":
    main()
