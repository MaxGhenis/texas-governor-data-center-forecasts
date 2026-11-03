# Texas governor's race and data center construction: conditional forecasts

Texas elects a governor on November 3, 2026: Greg Abbott, the Republican incumbent, against Gina
Hinojosa, the Democrat. This repository asks AI forecasters, each working alone with web search before
polls close, what the result does to data center construction in Texas and across the country. Each
forecaster answers every question at six values of Hinojosa's certified two-party share, and a causal
map pools the answers.

## Design

**Cells.** Forecasters answer at Hinojosa shares of 44%, 47% and 49.5%, where Abbott wins, and 50.5%,
53% and 56%, where Hinojosa wins. Three cells on each side give each side a line through three points.
The 49.5% and 50.5% cells differ by one point of vote share but also in who governs, so their contrast,
the cutoff effect, is the forecasters' estimate of what a bare Hinojosa win changes. The gap between
the "Abbott wins" and "Hinojosa wins" columns mixes that with what a larger margin says about Texas
voters.

**Questions.** `graph/graph.yaml` defines 13 questions, 68 answers in all.

- The vote: Hinojosa's share (a cumulative distribution), turnout, and James Talarico's share in the
  same-day US Senate race.
- What the state does: ERCOT resuming approvals for data center Large Loads by mid-2027 (it paused them
  in August 2026), a special session on data centers, a cut to the data center sales tax exemptions,
  and a law adding limits on building or connecting data centers, the last three by the end of 2027.
- Texas construction: MW with ERCOT's Approval to Energize at the end of 2027 and of 2028, and data
  center projects the Comptroller registers with 2027 effective dates.
- Nationwide: Census private construction spending on data centers in 2027 and 2028, and a statewide
  moratorium in another state by the end of 2027.

Forecasters answer every question but the vote share and turnout at all six cells. Each question names
its public resolution source in the map.

**The placebo.** The governor's result cannot cause the result of the Senate race on the same ballot.
Hinojosa at 49.5% and at 50.5% describe nearly the same electorate, so a forecaster's Senate answers
should differ across that line by about what one point of the governor's vote implies, with no extra
jump for who won. The prompt does not say so. The map does not mark the Senate question `continuous`,
so the simulator does not hold it fixed across the cutoff, and the report shows whatever jump the
forecasters gave.

**Forecasters.** Claude Opus 5.5 and GPT-6.1 Sol, in equal numbers where lanes allow, each running
alone in an empty directory on a Subfleet lane with a read-only sandbox. Runs of one model share its
training and often its answers, so the results appear by model as well as pooled.

**Headline measures.** Fixed after dispatch and before anyone read an answer (only format checks had
run); the commit that added this paragraph records when. For each policy and construction question
the write-up reports:

1. the cutoff effect: the pooled mean at 50.5% minus the pooled mean at 49.5% (`outputs/summary.md`);
2. the same contrast in each run's raw answers, and the fitted jump, the gap at 50% between lines
   through the three cells on each side (`outputs/rd.md`);
3. the change from 44% to 56%, and its within-sides part, the change that the margin carries beyond
   who wins;
4. each of these for Opus and for Sol separately, with the range across runs.

For the placebo it reports Talarico's fitted jump, by model. A forecaster who adds nothing for who
won the governor's race gives a fitted jump near zero. Answers that fail `check` stay out, and fresh
runs under new labels replace them until 23:00Z.

**Pooling.** `src/i86/simulate.py` runs a Monte Carlo through the map for each forecaster. A draw takes
Hinojosa's share from that forecaster's own distribution, or fixes it at a cell, and interpolates each
answer between the cells on the same side of 50%, never mixing a winning cell with a losing one. Each
condition (Abbott wins, Hinojosa wins, each narrow band, each cutoff cell) gets its own simulation, and
the pooled summary weights every forecaster's conditional distribution equally, whatever that
forecaster thinks Hinojosa's chances are. The two cutoff simulations share random numbers.

## Timing

Texas polls close at 7 p.m. local time: 01:00 UTC on November 4 in most of the state, an hour later in
El Paso and Hudspeth counties. Every run must finish before then. `scripts/deadline_guard.py` cancels
any run not started by 23:00Z and kills any still going at 00:50Z, and `abandon` marks each one. The
prompt bars vote counts and results and asks a forecaster to note any it comes across. `prereg/` holds
SHA-256 hashes of the map, prompt, context, runs and outputs, stamped with OpenTimestamps.
`scripts/seal.py --now` collects, checks, audits and stamps the answers once every run has finished;
a launchd copy of it does the same from 23:20Z if no one has.

## Run it

```bash
uv venv --python 3.13
uv pip install -e ".[dev]"
.venv/bin/i86 prompt                     # regenerate prompts/forecaster.md from the map and context/
.venv/bin/pytest -q
```

```bash
.venv/bin/i86 dispatch subfleet opus-1 --tier standard -m opus      # Claude Opus 5.5
.venv/bin/i86 dispatch subfleet sol-1 --tier hard                    # GPT-6.1 Sol
.venv/bin/i86 collect        # once every run has finished, copy answers and transcripts into runs/
.venv/bin/i86 abandon LABEL  # mark a run that will never finish; final
.venv/bin/i86 check          # parse and validate every response
.venv/bin/i86 audit          # check each transcript's tool calls
.venv/bin/i86 simulate       # pool the accepted runs into outputs/
.venv/bin/i86 prereg         # hash everything into prereg/SHA256SUMS and timestamp it
```

The audit's tests compare its shell model with macOS's shells and BSD tools, so the suite assumes macOS
with ripgrep and poppler from Homebrew. The GitHub workflow runs only on request.

## Independence

Every forecaster gets the same prompt, byte for byte; its SHA-256 is in `prompts/forecaster.md.sha256`
and in each run's `meta.json`, and `simulate` pools only runs made with the current prompt. Forecasters
work in empty directories outside the repository, and the prompt tells them not to read local files.
No answer enters the repository until every run has finished. `audit` flags tool calls that reach
outside a run's work directory; a run with a suspect call, or whose `prior_context` mentions these
questions, stays out of the pool until a reader checks it and passes `--accept-suspect` or
`--accept-prior`. The source repository's README describes the audit in full.

Codex ran every Sol run here with its proactive multi-agent mode on, and each run's main thread
spawned three sub-agents. They saw the same brief and searched the web from the same work directory
and read-only sandbox. `codex exec --json`, which `transcript.jsonl` records, carries only the main
thread, so `audit` never sees the sub-agents' calls.
`scripts/audit_codex_sessions.py` finds every thread behind a Codex run in its lane's session logs,
keeps the logs in `runs/<label>/codex-sessions/`, audits each thread as `audit` audits a transcript,
and flags any tool or item it cannot read. `i86 prereg` hashes those folders too.

## Files

- `graph/graph.yaml`: the map: questions, cells and resolution criteria.
- `context/brief.md`: the facts every forecaster gets, with sources.
- `prompts/forecaster.md`: the generated prompt; `schemas/template.json`: the response template.
- `runs/<label>/`: each run's prompt as sent, metadata, verbatim answer, transcript, parsed response and
  audit. For a Codex run, `codex-sessions/` keeps the session log of every thread, sub-agents
  included, and their audit.
- `scripts/`: `rd_summary.py` writes the raw-answer contrasts in `outputs/rd.*`; `seal.py` and
  `deadline_guard.py` seal the answers and enforce the deadline; `audit_codex_sessions.py` audits a
  Codex run's sub-agents.
- `outputs/`: pooled summaries (`summary.md`, `summary.json`, `nodes.csv`, `runs.csv`) and `plots/`.
- `prereg/`: hashes and timestamps.
- `src/i86/`: map loading, response checks, samplers, simulator, pooling, report, runners and audit.
- `tests/`: the source repository's tests. Most run on its DC Initiative 86 map, kept as
  `tests/fixtures/i86_graph.yaml`; the prompt test runs on this map. Test responses carry the label MOCK.

## What the numbers are

They are model forecasts under stated scenarios. They are not observations, and the cutoff contrast is
not an observed causal estimate. The questions resolve against public records from mid-2027 to mid-2029.
Quantity tails beyond the 5th and 95th percentiles extend the neighbouring slope, so means of heavy
right tails run low.

## Provenance

Forked from [MaxGhenis/dc-i86-llm-forecast](https://github.com/MaxGhenis/dc-i86-llm-forecast) at
c6dc25b, forecasts of DC's Initiative 86 on the same ballot day. The package keeps that repository's
name, `i86`, and its ballot-measure vocabulary: `fail` cells are Abbott wins, `pass` cells Hinojosa
wins, and `passes` in a condition means Hinojosa wins.

## License

MIT. See [LICENSE](LICENSE).
