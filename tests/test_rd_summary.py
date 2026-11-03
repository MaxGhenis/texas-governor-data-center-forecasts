"""Invariants of scripts/rd_summary.py's discontinuity measures, on MOCK lines."""

import importlib.util
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

spec = importlib.util.spec_from_file_location("rd_summary", Path(__file__).parent.parent / "scripts" / "rd_summary.py")
rd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rd)

finite = st.floats(min_value=-1e4, max_value=1e4, allow_nan=False)


@settings(max_examples=200, deadline=None)
@given(a=finite, b=finite, slope_l=finite, slope_r=finite, x0=st.floats(min_value=0.3, max_value=0.7))
def test_a_line_through_three_points_returns_itself(a, b, slope_l, slope_r, x0):
    ys = [a + slope_l * x for x in rd.LEFT]
    assert abs(rd.line_at(rd.LEFT, ys, x0) - (a + slope_l * x0)) <= 1e-6 * (1 + abs(a) + abs(slope_l))


@settings(max_examples=200, deadline=None, suppress_health_check=[])
@given(level=st.floats(0.05, 0.6), step=st.floats(-0.3, 0.3), slope=st.floats(-1, 1))
def test_fitted_jump_recovers_a_step_on_a_common_slope(tx_graph, level, step, slope):
    """MOCK answers on one line with a step at 50%: the fitted jump is the step, and the parts add up."""
    node = tx_graph.nodes["tax_exemption_cut"]
    vals = {}
    for c in rd.LEFT + rd.RIGHT:
        vals[rd.cell_label(c)] = level + slope * (c - 0.5) + (step if c > 0.5 else 0.0)
    m = rd.measures(tx_graph, node, vals)
    assert abs(m["fit_jump"] - step) < 1e-9
    assert abs(m["jump"] - (step + slope * 0.01)) < 1e-9
    assert abs(m["total"] - m["jump"] - m["within"]) < 1e-12


def test_a_missing_cell_gives_no_measures(tx_graph):
    node = tx_graph.nodes["tax_exemption_cut"]
    vals = {rd.cell_label(c): 0.3 for c in rd.LEFT}
    assert rd.measures(tx_graph, node, vals) is None
