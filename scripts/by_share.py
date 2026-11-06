"""Pool the registered answers at fixed Hinojosa shares, the way `i86 simulate` pools its two cutoff cells.

    .venv/bin/python scripts/by_share.py

Writes outputs/after-the-vote/by_share.json: for each question, the pooled mean at each of the six cells
and at Hinojosa's two-party share in the NBC News count that COUNT records. Between cells on one side
of 50%, the simulator interpolates each answer linearly. The script also gives each run's chance of a
Hinojosa win and of a share above 53% and above the count's share, from that run's own share
distribution. It runs the stamped runs
through the stamped simulator and first checks that the 49.5% and 50.5% cells reproduce
outputs/summary.json.
"""
import json
from pathlib import Path

import numpy as np

from i86 import cli, graph as graph_mod
from i86.simulate import simulate
from i86.summarize import run_seed, values

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "after-the-vote" / "by_share.json"

# The flags of the stamped pooled run (prereg/README.md).
ACCEPT_SUSPECT = {"sol-2", "sol-3", "sol-6"}
ACCEPT_PRIOR = {"opus-3", "sol-1", "sol-2", "sol-3", "sol-4", "sol-6"}
N = 20000
# NBC News's count at 3:34 p.m. ET on November 5 (nbcnews.com/politics/2026-elections/texas-governor-results).
COUNT = {"as_of": "2026-11-05T15:34-05:00", "hinojosa": 52.8, "abbott": 45.7, "hinojosa_votes": 5230929,
         "abbott_votes": 4524955, "expected_vote_in": 0.99}
COUNT_SHARE = round(COUNT["hinojosa"] / (COUNT["hinojosa"] + COUNT["abbott"]), 3)
SHARES = [0.44, 0.47, 0.495, 0.505, 0.53, COUNT_SHARE, 0.56]
NODES = ["ercot_pause_lifted", "special_session_data_centers", "tax_exemption_cut", "restriction_law",
         "ercot_approved_mw_2027", "ercot_approved_mw_2028", "comptroller_new_projects_2027",
         "us_dc_spending_2027", "us_dc_spending_2028", "other_state_moratorium", "senate_dem_share"]


def pooled(per_run: dict, key: str) -> dict:
    by_model = {m: [v[key] for r, v in per_run.items() if r.startswith(m)] for m in ("opus", "sol")}
    return {"all": float(np.mean([v[key] for v in per_run.values()])),
            **{m: float(np.mean(xs)) for m, xs in by_model.items()},
            "by_run": {r: v[key] for r, v in per_run.items()}}


def compute() -> dict:
    g = graph_mod.load()
    runs = cli.accepted_runs(g, cli._prompt_sha(), False, ACCEPT_PRIOR, ACCEPT_SUSPECT)
    summary = json.loads((ROOT / "outputs" / "summary.json").read_text())
    if sorted(runs) != sorted(summary["runs"]):
        raise ValueError(f"accepted runs {sorted(runs)} differ from outputs/summary.json")

    out = {"count": COUNT, "count_share": COUNT_SHARE, "runs": sorted(runs), "by_share": {}, "vote": {}}
    for share in SHARES:
        per_run = {}
        for rid, fc in sorted(runs.items()):
            d = simulate(g, fc, N, [*run_seed(0, rid), 1], fixed_share=share, continuous_share=0.5)
            per_run[rid] = {k: float(np.mean(values(d, k))) for k in NODES}
        out["by_share"][str(share)] = {k: pooled(per_run, k) for k in NODES}

    for share, cond in [(0.495, "cutoff_fail"), (0.505, "cutoff_pass")]:
        for k in NODES:
            mine = out["by_share"][str(share)][k]["all"]
            theirs = summary["nodes"][k][cond].get("mean", summary["nodes"][k][cond].get("p"))
            if abs(mine - theirs) > 1e-9 * max(1.0, abs(theirs)):
                raise ValueError(f"{k} at {share}: {mine} here, {theirs} in outputs/summary.json")

    per_run = {}
    for rid, fc in sorted(runs.items()):
        share = simulate(g, fc, N, run_seed(0, rid))["dem_share"]
        per_run[rid] = {"p_win": float(np.mean(share > 0.5)), "p_above_53": float(np.mean(share > 0.53)),
                        "p_above_count": float(np.mean(share > COUNT_SHARE)), "mean": float(np.mean(share)),
                        "p95": float(np.quantile(share, 0.95)), "p99": float(np.quantile(share, 0.99))}
    out["vote"] = {k: pooled(per_run, k) for k in next(iter(per_run.values()))}
    return out


def main() -> None:
    out = compute()
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1) + "\n")
    for k in NODES:
        print(k, "  ".join(f"{s}:{out['by_share'][str(s)][k]['all']:.4g}" for s in SHARES))
    print({k: round(v["all"], 4) for k, v in out["vote"].items()})


if __name__ == "__main__":
    main()
