"""outputs/after-the-vote/by_share.json must match a fresh run of scripts/by_share.py."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("by_share", ROOT / "scripts" / "by_share.py")
by_share = importlib.util.module_from_spec(spec)
spec.loader.exec_module(by_share)


def test_committed_json_matches_a_fresh_run():
    assert json.loads(by_share.OUT.read_text()) == by_share.compute()


def test_quantities_interpolate_linearly_between_53_and_56():
    cells = json.loads(by_share.OUT.read_text())["by_share"]
    w = (0.56 - by_share.COUNT_SHARE) / (0.56 - 0.53)
    for node in ["ercot_approved_mw_2027", "ercot_approved_mw_2028", "comptroller_new_projects_2027",
                 "us_dc_spending_2027", "us_dc_spending_2028", "senate_dem_share"]:
        line = w * cells["0.53"][node]["all"] + (1 - w) * cells["0.56"][node]["all"]
        # The simulator rounds each draw of an integer count, so the project count lands within 1e-4.
        assert abs(cells[str(by_share.COUNT_SHARE)][node]["all"] - line) <= 1e-4 * abs(line), node
