"""outputs/after-the-vote/exact_by_share.json must match a fresh run of scripts/exact_by_share.py, and its
exact values must agree with what the simulator draws.

Invariants, for every input:
- `mean_rint(a, b)`, the mean of rint(x) for x uniform on [a, b], lies between the rounded ends, moves by
  n when both ends move by a whole n, and matches a fine grid's average;
- `quantity_moments` gives the mean of `dists.sample_quantity` over a uniform u: exactly (to rounding
  error) on a grid that the quantile levels split evenly, and within the rounding steps' share of the
  grid for whole-unit quantities.

Differential checks: each run's exact value lies within six standard errors of by_share.json's average
of 20,000 draws, and the check stops the script when one does not; each run's chance of a win equals
outputs/summary.json's; and each run's yes/no forecasts at the six cells equal the stated answers that
scripts/rd_summary.py wrote to outputs/rd.csv. Names that start with MOCK_ mark random inputs, not
forecasts.
"""
import csv
import importlib.util
import json
import math
import statistics
from pathlib import Path

import numpy as np
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from i86 import dists

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("exact_by_share", ROOT / "scripts" / "exact_by_share.py")
exact = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exact)

COMMITTED = json.loads(exact.OUT.read_text())
DRAWN = json.loads(exact.by_share.OUT.read_text())
LEVELS = [0.05, 0.25, 0.5, 0.75, 0.95]
# Midpoints of a grid of this many cells on [0, 1]; the quantile levels fall on cell edges.
GRID = 20000
MOCK_END = st.floats(min_value=-1e3, max_value=1e3, allow_nan=False, allow_infinity=False)
MOCK_GAP = st.floats(min_value=0.0, max_value=200.0, allow_nan=False, allow_infinity=False)


def midpoints(a: float, b: float, n: int) -> np.ndarray:
    return a + (b - a) * (np.arange(n) + 0.5) / n


def test_committed_json_matches_a_fresh_run():
    assert COMMITTED == exact.compute()


def test_the_exact_values_sit_within_six_standard_errors_of_the_draws():
    assert 0 < COMMITTED["worst_z"] < exact.MAX_Z


def test_each_runs_chance_of_a_win_equals_the_registered_one():
    summary = json.loads((ROOT / "outputs" / "summary.json").read_text())
    for rid, p in COMMITTED["vote"]["p_win"]["by_run"].items():
        assert math.isclose(p, summary["vote"]["by_run"][rid]["p_pass"], rel_tol=1e-9, abs_tol=1e-12), rid


def test_the_check_stops_on_a_draw_far_from_the_exact_value(tmp_path, monkeypatch):
    drawn = json.loads(json.dumps(DRAWN))
    entry = drawn["by_share"]["0.53"]["ercot_pause_lifted"]["by_run"]
    rid = sorted(entry)[0]
    entry[rid] += 0.05  # about 14 standard errors for a probability near one half
    path = tmp_path / "by_share.json"
    path.write_text(json.dumps(drawn))
    monkeypatch.setattr(exact.by_share, "OUT", path)
    with pytest.raises(ValueError, match="standard errors"):
        exact.compute()
    assert exact.compute(check=False)["worst_z"] > exact.MAX_Z


def test_the_check_stops_on_a_chance_of_a_win_unlike_the_registered_one(tmp_path, monkeypatch):
    summary = json.loads((ROOT / "outputs" / "summary.json").read_text())
    rid = sorted(summary["vote"]["by_run"])[0]
    summary["vote"]["by_run"][rid]["p_pass"] += 0.01
    (tmp_path / "outputs").mkdir()
    (tmp_path / "outputs" / "summary.json").write_text(json.dumps(summary))
    monkeypatch.setattr(exact, "ROOT", tmp_path)
    with pytest.raises(ValueError, match="chance of a win"):
        exact.compute()


def test_yes_no_forecasts_at_the_cells_equal_the_stated_answers_in_rd_csv():
    with (ROOT / "outputs" / "rd.csv").open() as f:
        rows = [r for r in csv.DictReader(f) if r["question"] in exact.by_share.NODES]
    binary = {r["question"] for r in rows if 0 <= float(r["at_44"]) <= 1 and r["question"] != "senate_dem_share"}
    assert len(binary) == 5
    checked = 0
    for r in rows:
        if r["question"] not in binary:
            continue
        for share, column in [(0.44, "at_44"), (0.47, "at_47"), (0.495, "at_49.5"), (0.505, "at_50.5"),
                              (0.53, "at_53"), (0.56, "at_56")]:
            mine = COMMITTED["by_share"][f"{share:g}"][r["question"]]["by_run"][r["run"]]
            assert math.isclose(mine, float(r[column]), rel_tol=1e-12, abs_tol=1e-12), (r["run"], r["question"], share)
            checked += 1
    assert checked == 5 * 12 * 6


@pytest.mark.parametrize("share", [str(s) for s in exact.by_share.SHARES])
def test_the_pooled_values_average_the_runs(share):
    for node, entry in COMMITTED["by_share"][share].items():
        runs = entry["by_run"]
        assert math.isclose(entry["all"], statistics.fmean(runs.values()), rel_tol=1e-12, abs_tol=1e-12), node
        for model in ("opus", "sol"):
            mine = [v for r, v in runs.items() if r.startswith(model)]
            assert len(mine) == 6
            assert math.isclose(entry[model], statistics.fmean(mine), rel_tol=1e-12, abs_tol=1e-12), (node, model)


@settings(deadline=None)
@given(MOCK_END, MOCK_GAP)
def test_mean_rint_lies_between_the_rounded_ends(a, gap):
    b = a + gap
    m = float(exact.mean_rint(a, b))
    assert math.floor(a + 0.5) - 1e-9 <= m <= math.ceil(b - 0.5) + 1e-9 or (gap == 0 and m == np.rint(a))


@settings(deadline=None)
@given(MOCK_END, MOCK_GAP, st.integers(min_value=-1000, max_value=1000))
def test_mean_rint_moves_with_a_whole_shift(a, gap, n):
    b = a + gap
    if gap > 0 and (a + n) + gap == b + n:  # the shifted interval keeps its exact width
        shifted = float(exact.mean_rint(a + n, b + n))
        assert math.isclose(shifted, float(exact.mean_rint(a, b)) + n, rel_tol=0, abs_tol=1e-9 * (1 + abs(a) + abs(n)))


@settings(deadline=None)
@given(MOCK_END, st.floats(min_value=1e-3, max_value=200.0, allow_nan=False, allow_infinity=False))
def test_mean_rint_matches_a_fine_grid(a, gap):
    b = a + gap
    grid = float(np.mean(np.rint(midpoints(a, b, GRID))))
    assert abs(float(exact.mean_rint(a, b)) - grid) <= (gap + 2) / GRID + 1e-9


MOCK_QUANTILES = st.tuples(
    st.floats(min_value=-500, max_value=500, allow_nan=False, allow_infinity=False),
    st.lists(st.floats(min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False), min_size=4, max_size=4),
    st.floats(min_value=0.0, max_value=300.0, allow_nan=False, allow_infinity=False),
    st.floats(min_value=0.0, max_value=300.0, allow_nan=False, allow_infinity=False),
)


@settings(deadline=None)
@given(MOCK_QUANTILES)
def test_quantity_moments_give_the_mean_of_the_sampler(spec):
    start, steps, below, above = spec
    q = np.array([start + sum(steps[:i]) for i in range(5)])
    lo, hi = q[0] - below, q[-1] + above
    u = (np.arange(GRID) + 0.5) / GRID
    draws = dists.sample_quantity(LEVELS, q[None, :], lo, hi, u)
    mean, second = exact.quantity_moments(LEVELS, q[None, :], lo, hi, False)
    scale = 1 + float(np.max(np.abs(draws)))
    assert math.isclose(float(mean[0]), float(np.mean(draws)), rel_tol=0, abs_tol=1e-9 * scale)
    assert math.isclose(float(second[0]), float(np.mean(draws ** 2)), rel_tol=1e-6, abs_tol=1e-6 * scale)
    rounded = dists.sample_quantity(LEVELS, q[None, :], lo, hi, u, integer=True)
    whole, _ = exact.quantity_moments(LEVELS, q[None, :], lo, hi, True)
    spread = float(draws.max() - draws.min())
    assert abs(float(whole[0]) - float(np.mean(rounded))) <= (spread + 2) / GRID + 1e-9 * scale
