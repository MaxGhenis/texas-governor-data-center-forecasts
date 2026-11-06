"""The arithmetic behind the blog post's numbers (blog/post_numbers.py).

Invariants, for every input:
- `line_at` matches a reference regression, and its residuals sum to zero and stay orthogonal to the shares;
- a line through the runs' average at each share equals the average of the runs' lines;
- the 49.5%-to-50.5% contrast equals the jump at 50%, plus half a point of each side's slope, plus the
  50.5% value's distance above its line, minus the 49.5% value's distance above its line;
- points on one line per side give back those lines, so the two-share and three-share jumps agree.

Differential checks: the chart's fit and the fit script's stored jumps agree with `line_at`.

Regression checks pin forecast figures the post takes from exact_by_share.json and the fit script, so a
re-pool that moves one past its rounding fails here until someone changes this table, and the post with it.
They compare the data with this table and never read the post, so a typo in the post still passes. Names
that start with MOCK_ mark random inputs, not forecasts.
"""
import csv
import importlib.util
import math
import statistics
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "blog" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


numbers = load("post_numbers")
chart = load("make_share_chart")

LOSS, WIN = numbers.LOSS, numbers.WIN
RUNS = sorted(numbers.DATA["by_share"]["0.495"]["ercot_pause_lifted"]["by_run"])
with (ROOT / "outputs" / "rd.csv").open() as f:
    RD_ROWS = list(csv.DictReader(f))

MOCK_Y = st.floats(min_value=-1e5, max_value=1e5, allow_nan=False, allow_infinity=False)
MOCK_THREE = st.lists(MOCK_Y, min_size=3, max_size=3)

# (node, group, scale, measure, decimal places, the figure as the post cites it)
POST_FIGURES = [
    ("ercot_pause_lifted", "all", 100, "loss", 0, 79),
    ("ercot_pause_lifted", "all", 100, "win", 0, 64),
    ("ercot_pause_lifted", "all", 100, "jump", 0, -15),
    ("ercot_pause_lifted", "all", 100, "contrast", 0, -16),
    ("ercot_pause_lifted", "all", 100, "total", 0, -30),
    ("ercot_pause_lifted", "all", 100, "at_count", 0, 59),
    ("ercot_pause_lifted", "opus", 100, "jump", 0, -22),
    ("ercot_pause_lifted", "sol", 100, "jump", 0, -8),
    ("special_session_data_centers", "all", 100, "loss", 0, 31),
    ("special_session_data_centers", "all", 100, "win", 0, 47),
    ("special_session_data_centers", "all", 100, "jump", 0, 16),
    ("special_session_data_centers", "all", 100, "contrast", 0, 17),
    ("special_session_data_centers", "all", 100, "total", 0, 27),
    ("special_session_data_centers", "all", 100, "at_count", 0, 50),
    ("ercot_approved_mw_2028", "all", 1, "loss", -2, 26900),
    ("ercot_approved_mw_2028", "all", 1, "win", -2, 24400),
    ("ercot_approved_mw_2028", "all", 1, "jump", -2, -2500),
    ("ercot_approved_mw_2028", "all", 1, "contrast", -2, -2800),
    ("ercot_approved_mw_2028", "all", 1, "at_count", -2, 22800),
    ("senate_dem_share", "all", 1, "at_count", 1, 55.5),
    ("ercot_approved_mw_2028", "opus", 1, "share", 2, 0.54),
    ("ercot_approved_mw_2028", "sol", 1, "share", 2, 0.25),
    ("comptroller_new_projects_2027", "all", 1, "loss", 0, 58),
    ("comptroller_new_projects_2027", "all", 1, "win", 0, 52),
    ("comptroller_new_projects_2027", "all", 1, "jump", 1, -5.4),
    ("comptroller_new_projects_2027", "all", 1, "contrast", 1, -6.2),
    ("comptroller_new_projects_2027", "all", 1, "at_count", 0, 48),
    ("restriction_law", "all", 100, "loss", 0, 77),
    ("restriction_law", "all", 100, "win", 0, 79),
    ("restriction_law", "all", 100, "at_count", 0, 82),
    ("tax_exemption_cut", "all", 100, "loss", 0, 77),
    ("tax_exemption_cut", "all", 100, "win", 0, 77),
    ("other_state_moratorium", "all", 100, "loss", 0, 66),
    ("other_state_moratorium", "all", 100, "win", 0, 67),
    ("other_state_moratorium", "all", 100, "at_56", 0, 73),
    ("us_dc_spending_2028", "all", 1, "loss", 1, 155.1),
    ("us_dc_spending_2028", "all", 1, "win", 1, 154.3),
    ("us_dc_spending_2028", "all", 1, "at_56", 1, 146.9),
    # The chart labels its ring at the count's share with this figure.
    ("us_dc_spending_2028", "all", 1, "at_count", 0, 150),
]
HEADLINES = [
    ("ercot_pause_lifted", 100),
    ("special_session_data_centers", 100),
    ("ercot_approved_mw_2028", 1),
    ("comptroller_new_projects_2027", 1),
]


def close(a: float, b: float, scale: float = 1.0) -> bool:
    return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-9 * max(1.0, abs(scale)))


def biggest(values) -> float:
    return max(abs(v) for v in values)


@settings(deadline=None)
@given(MOCK_THREE, st.floats(min_value=0.4, max_value=0.6))
def test_line_at_matches_a_reference_regression(ys, share):
    slope, intercept = statistics.linear_regression(LOSS, ys)
    assert close(numbers.line_at(LOSS, ys, share), intercept + slope * share, biggest(ys) / 0.03)


@settings(deadline=None)
@given(MOCK_THREE)
def test_residuals_sum_to_zero_and_stay_orthogonal_to_the_shares(ys):
    residuals = [y - numbers.line_at(WIN, ys, x) for x, y in zip(WIN, ys)]
    assert close(math.fsum(residuals), 0.0, biggest(ys))
    assert close(math.fsum(r * x for r, x in zip(residuals, WIN)), 0.0, biggest(ys))


@settings(deadline=None)
@given(st.lists(MOCK_THREE, min_size=1, max_size=12))
def test_the_line_through_the_average_equals_the_average_of_the_lines(runs):
    pooled = [statistics.fmean(r[i] for r in runs) for i in range(3)]
    lines = [numbers.line_at(WIN, r, 0.5) for r in runs]
    assert close(numbers.line_at(WIN, pooled, 0.5), statistics.fmean(lines), biggest(pooled + lines))


@settings(deadline=None)
@given(MOCK_THREE, MOCK_THREE)
def test_the_contrast_splits_into_the_jump_the_slopes_and_the_misses(loss, win):
    jump = numbers.line_at(WIN, win, 0.5) - numbers.line_at(LOSS, loss, 0.5)
    slopes = 0.005 * (statistics.linear_regression(WIN, win).slope + statistics.linear_regression(LOSS, loss).slope)
    misses = (win[0] - numbers.line_at(WIN, win, WIN[0])) - (loss[2] - numbers.line_at(LOSS, loss, LOSS[2]))
    assert close(win[0] - loss[2], jump + slopes + misses, biggest(loss + win))


@settings(deadline=None)
@given(MOCK_Y, MOCK_Y, MOCK_Y, MOCK_Y)
def test_points_on_one_line_per_side_give_back_those_lines(a_loss, b_loss, a_win, b_win):
    loss = [a_loss + b_loss * (s - 0.5) for s in LOSS]
    win = [a_win + b_win * (s - 0.5) for s in WIN]
    jump = numbers.line_at(WIN, win, 0.5) - numbers.line_at(LOSS, loss, 0.5)
    near = numbers.line_at(WIN[:2], win[:2], 0.5) - numbers.line_at(LOSS[1:], loss[1:], 0.5)
    scale = biggest((a_loss, b_loss, a_win, b_win))
    assert close(jump, a_win - a_loss, scale)
    assert close(near, jump, scale)


@pytest.mark.parametrize("group,size", [("all", 12), ("opus", 6), ("sol", 6)])
@pytest.mark.parametrize("node,scale,unit", numbers.QUESTIONS)
def test_the_pooled_measures_equal_the_average_run_measures(node, scale, unit, group, size):
    pooled = numbers.measures(node, group, scale)
    per_run = [numbers.measures(node, r, scale) for r in RUNS if group == "all" or r.startswith(group)]
    assert len(per_run) == size
    for key in ("loss", "win", "jump", "contrast", "total", "at_56", "at_count"):
        assert close(pooled[key], statistics.fmean(m[key] for m in per_run), pooled["loss"])


@pytest.mark.parametrize("spec", chart.PANELS, ids=[p[1] for p in chart.PANELS])
def test_the_chart_and_the_numbers_read_the_same_lines_at_50(spec):
    _, node, _, _, scale, _ = spec
    m = numbers.measures(node, "all", scale)
    assert close(chart.fit_at(chart.ABBOTT_CELLS, node, scale, 0.5), m["loss"], m["loss"])
    assert close(chart.fit_at(chart.HINOJOSA_CELLS, node, scale, 0.5), m["win"], m["win"])


@pytest.mark.parametrize("row", RD_ROWS, ids=[f"{r['run']}-{r['question']}" for r in RD_ROWS])
def test_line_at_reproduces_the_fit_scripts_stored_jumps(row):
    loss = [float(row[f"at_{s:g}"]) for s in (44, 47, 49.5)]
    win = [float(row[f"at_{s:g}"]) for s in (50.5, 53, 56)]
    jump = numbers.line_at(WIN, win, 0.5) - numbers.line_at(LOSS, loss, 0.5)
    assert close(jump, float(row["fit_jump"]), biggest(loss + win))


@pytest.mark.parametrize("node,group,scale,measure,digits,figure", POST_FIGURES)
def test_the_post_cites_this_figure(node, group, scale, measure, digits, figure):
    assert round(numbers.measures(node, group, scale)[measure], digits) == figure


@pytest.mark.parametrize("node,scale,model,low,high", [
    ("ercot_pause_lifted", 100, "opus", 37, 49),
    ("ercot_pause_lifted", 100, "sol", 62, 80),
    ("special_session_data_centers", 100, "opus", 26, 46),
    ("special_session_data_centers", 100, "sol", 59, 65),
    ("us_dc_spending_2028", 1, "opus", 97, 149),
    ("us_dc_spending_2028", 1, "sol", 165, 189),
])
def test_the_post_cites_this_range_across_a_models_runs_at_the_count(node, scale, model, low, high):
    at_count = [numbers.value(numbers.DATA["count_share"], node, r, scale) for r in RUNS if r.startswith(model)]
    assert len(at_count) == 6
    assert numbers.count_range(node, model, scale) == (min(at_count), max(at_count))
    assert (round(min(at_count)), round(max(at_count))) == (low, high)


def test_the_post_cites_this_range_of_slope_ratios():
    ratios = [r for node in numbers.SLOPE_QUESTIONS for r in numbers.slope_ratios(node)]
    assert len(ratios) == 6
    assert (round(min(ratios), 1), round(max(ratios), 1)) == (3.3, 4.3)


def test_the_slope_ratios_divide_the_models_average_lines():
    for node in numbers.SLOPE_QUESTIONS:
        for cells, ratio in zip((LOSS, WIN), numbers.slope_ratios(node)):
            per_run = {m: statistics.fmean(statistics.linear_regression(
                cells, [numbers.value(s, node, r, 1) for s in cells]).slope for r in RUNS if r.startswith(m))
                for m in ("opus", "sol")}
            assert close(ratio, per_run["sol"] / per_run["opus"], ratio)


@pytest.mark.parametrize("key,group,digits,figure", [
    ("p_win", "all", 2, 0.26),
    ("p_above_53", "all", 2, 0.04),
])
def test_the_post_cites_this_chance(key, group, digits, figure):
    assert round(numbers.vote(key, group), digits) == figure


@pytest.mark.parametrize("model,low,high", [("opus", 0.20, 0.35), ("sol", 0.21, 0.33)])
def test_the_post_cites_this_range_of_chances_of_a_win(model, low, high):
    wins = [numbers.vote("p_win", r) for r in numbers.runs(model)]
    assert len(wins) == 6
    assert (round(min(wins), 2), round(max(wins), 2)) == (low, high)


def test_the_counts_percentages_and_votes_give_the_same_share():
    count, share = numbers.DATA["count"], numbers.DATA["count_share"]
    assert round(count["hinojosa"] / (count["hinojosa"] + count["abbott"]), 3) == share
    assert round(count["hinojosa_votes"] / (count["hinojosa_votes"] + count["abbott_votes"]), 3) == share


@pytest.mark.parametrize("node,fraction", [
    ("ercot_pause_lifted", 1 / 2),
    ("special_session_data_centers", 3 / 5),
    ("ercot_approved_mw_2028", 1 / 3),
    ("comptroller_new_projects_2027", 3 / 10),
])
def test_the_post_cites_this_fraction_of_the_total_at_50(node, fraction):
    assert abs(numbers.measures(node, "all", 1)["share"] - fraction) < 0.02


@pytest.mark.parametrize("node,scale", HEADLINES)
def test_all_twelve_jumps_share_a_sign_and_the_contrast_exceeds_the_jump(node, scale):
    m = numbers.measures(node, "all", scale)
    assert all(numbers.measures(node, r, scale)["jump"] * m["jump"] > 0 for r in RUNS)
    assert abs(m["contrast"]) > abs(m["jump"])


@pytest.mark.parametrize("question,digits,figure", [
    ("ercot_approved_mw_2028", -2, -2700),
    ("comptroller_new_projects_2027", 1, -6.0),
])
def test_the_post_cites_this_figure_from_the_fit_script(question, digits, figure):
    jumps = [float(r["fit_jump"]) for r in RD_ROWS if r["question"] == question]
    assert len(jumps) == 12
    assert round(statistics.fmean(jumps), digits) == figure


def test_the_senate_lines_differ_by_less_than_the_post_says():
    jumps = [float(r["fit_jump"]) for r in RD_ROWS if r["question"] == "senate_dem_share"]
    assert len(jumps) == 12
    assert biggest(jumps) < 0.07
