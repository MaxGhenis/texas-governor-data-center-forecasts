"""The thread's quantities chart stays in step with outputs/summary.json."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("make_quantity_chart", ROOT / "social" / "make_quantity_chart.py")
chart = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(chart)


def test_committed_svg_matches_summary():
    assert chart.OUT.read_text() == chart.svg(), "rerun social/make_quantity_chart.py and rsvg-convert"


def test_every_dot_falls_inside_its_axis():
    for header, top, ticks, rows in chart.PANELS:
        assert max(ticks) <= top
        for _, node in rows:
            assert all(0 <= v < top for v in chart.means(node).values()), (header, node)
