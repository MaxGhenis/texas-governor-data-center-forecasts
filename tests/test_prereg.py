"""`i86 prereg` replaces the previous proof instead of leaving it beside a manifest it does not prove."""

import argparse

from i86 import cli, runners


def area(tmp_path, monkeypatch):
    """A MOCK repository root: map, prompt, template and brief, no runs or outputs, and a previous
    manifest with its proof."""
    for rel in ("graph/graph.yaml", "prompts/forecaster.md", "schemas/template.json", "context/brief.md"):
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_text(f"MOCK {rel}\n")
    prereg = tmp_path / "prereg"
    prereg.mkdir()
    (prereg / "SHA256SUMS").write_text("MOCK OLD MANIFEST\n")
    (prereg / "SHA256SUMS.ots").write_text("MOCK OLD PROOF\n")
    monkeypatch.setattr(cli, "ROOT", tmp_path)
    monkeypatch.setattr(cli, "PROMPT_PATH", tmp_path / "prompts" / "forecaster.md")
    monkeypatch.setattr(cli, "TEMPLATE_PATH", tmp_path / "schemas" / "template.json")
    monkeypatch.setattr(cli, "OUTPUTS", tmp_path / "outputs")
    monkeypatch.setattr(cli, "PREREG", prereg)
    monkeypatch.setattr(runners, "RUNS", tmp_path / "runs")
    return prereg


def test_a_new_manifest_gets_a_new_proof(tmp_path, monkeypatch):
    prereg = area(tmp_path, monkeypatch)
    calls = []

    def fake_run(cmd, **kwargs):
        calls.append((cmd, (prereg / "SHA256SUMS.ots").exists()))
        (prereg / "SHA256SUMS.ots").write_text("MOCK NEW PROOF\n")
        return argparse.Namespace(returncode=0, stdout="", stderr="")

    monkeypatch.setattr(cli.subprocess, "run", fake_run)
    assert cli.cmd_prereg(argparse.Namespace(no_stamp=False)) == 0
    [(cmd, old_proof_present)] = calls
    assert cmd[-2:] == ["stamp", str(prereg / "SHA256SUMS")]
    assert not old_proof_present
    assert (prereg / "SHA256SUMS.ots").read_text() == "MOCK NEW PROOF\n"
    assert "MOCK OLD MANIFEST" not in (prereg / "SHA256SUMS").read_text()


def test_hashing_without_a_stamp_drops_the_old_proof(tmp_path, monkeypatch):
    prereg = area(tmp_path, monkeypatch)
    monkeypatch.setattr(cli.subprocess, "run", lambda *a, **k: (_ for _ in ()).throw(AssertionError("no stamp")))
    assert cli.cmd_prereg(argparse.Namespace(no_stamp=True)) == 0
    assert not (prereg / "SHA256SUMS.ots").exists()
    assert "graph/graph.yaml" in (prereg / "SHA256SUMS").read_text()
