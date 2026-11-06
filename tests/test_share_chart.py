"""blog/images/forecasts-by-share.svg must match a fresh run of blog/make_share_chart.py, and every dot must sit
inside its panel."""
import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("share_chart", ROOT / "blog" / "make_share_chart.py")
chart = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chart)


def test_committed_svg_matches_the_chart_script():
    assert chart.OUT.read_text() == chart.svg()


def test_every_dot_falls_inside_its_panel():
    for i, (_, node, top, _, scale, _) in enumerate(chart.PANELS):
        for s in chart.ABBOTT_CELLS + chart.HINOJOSA_CELLS + [chart.COUNT]:
            assert 0 <= chart.mean(s, node, scale) <= top, (node, s)
    cx = [float(x) for x in re.findall(r'<circle cx="([\d.]+)"', chart.svg())]
    assert cx and all(16 <= x <= 760 for x in cx)
