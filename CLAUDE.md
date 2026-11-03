# CLAUDE.md

Independent agentic conditional forecasts of what the 2026 Texas governor's race does to data center
construction, in Texas and nationwide, pooled through the causal map in `graph/graph.yaml`. Read
`README.md` first.

- The repository is private. Publish nothing from it (the repository, posts, a blog) without Max's
  explicit OK.
- Logged runs are append-only. Never edit `runs/*/response.md`, `response.json` or `meta.json` after a
  run is collected; add a new run instead. Pre-registered hashes and timestamps live in `prereg/`.
- Changing `graph/graph.yaml`, `context/` or `src/i86/prompt.py` changes the prompt. Regenerate it with
  `.venv/bin/i86 prompt`, commit it, and never pool runs made with different prompt hashes.
- Never copy an answer into `runs/` while any run is still going; `i86 collect` enforces this. A run
  dispatched after answers are in `runs/` must be `--late`, and the report flags it.
- Every run must finish before Texas polls close (01:00Z on 2026-11-04). Kill and `abandon` any run
  still going at 00:50Z.
- Dispatch only on Subfleet lanes: Opus 5.5 with `--tier standard -m opus`, GPT-6.1 Sol with
  `--tier hard`. Never on the OpenAI API.
- The package keeps the name `i86` and the ballot-measure vocabulary of the map it was forked from:
  `fail` cells are Abbott wins, `pass` cells Hinojosa wins, and `passes` means Hinojosa wins.
- Tests: `.venv/bin/pytest -q` (at most 4 workers). Test responses are MOCK and must stay labelled.
  `tests/fixtures/i86_graph.yaml`, the DC I-86 map, is the fixture most tests exercise.
- The forecasts are model outputs under stated scenarios. Do not describe them as observations or the
  cutoff contrast as an observed causal effect.
