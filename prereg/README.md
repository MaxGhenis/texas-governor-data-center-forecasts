# Timestamps

`i86 prereg` writes `SHA256SUMS`, the SHA-256 of the map, the prompt, the response template, the
context brief, every run's `meta.json`, `response.md`, `response.json`, `audit.json` and
`transcript.jsonl`, a Codex run's `codex-sessions/` folder, and the files at the top of `outputs/`
(not the charts). It then stamps the manifest with OpenTimestamps. Each dated folder keeps one
manifest and its proof; `SHA256SUMS` and `SHA256SUMS.ots` at the top are the latest.

| Folder | Written | Covers |
|---|---|---|
| `2026-11-03-dispatch/` | 17:04Z 11/03 | the map, prompt, template and brief, before the first dispatch |
| `2026-11-03-collected/` | 20:50Z 11/03 | every run's answer, parsed response, audit and transcript, collected once the last run had finished |
| `2026-11-03-pooled/` | 20:54Z 11/03 | the above plus `outputs/` from `i86 simulate --accept-suspect sol-2 --accept-prior opus-3 --accept-prior sol-1 --accept-prior sol-2 --accept-prior sol-3 --accept-prior sol-4 --accept-prior sol-6` (seed 0, 20,000 draws), and the fit outputs that `scripts/rd_summary.py` writes (`outputs/rd.csv`, `outputs/rd.md`) |
| `2026-11-03-codex-sessions/` | 21:50Z 11/03 | the above, unchanged, plus each Sol run's `codex-sessions/`: the session logs of its main thread and its three sub-agents, and their audit from `scripts/audit_codex_sessions.py` |
| `2026-11-03-repooled/` | 22:27Z 11/03 | the above with `outputs/` pooled again under the gate that reads the session audits, by the pooled folder's command plus `--accept-suspect sol-3 --accept-suspect sol-6`; only `outputs/summary.md` changed |

The pooled run accepts two kinds of flag after a reader checked each one. sol-2's one suspect call runs
`python3 -I -c` to fetch and parse the Comptroller's public list of registered data centers
(comptroller.texas.gov/taxes/data-centers/data-center-lists.php); it reads no local file. opus-3's
prior context says "none" and adds that nothing in its context mentions these questions; sol-1, 2, 3,
4 and 6 quote only their work directory's name, which repeats the brief's subject.

Each Sol run's main thread spawned three sub-agents, and its transcript omits their calls.
`scripts/audit_codex_sessions.py` audits all 24 Sol threads from the lanes' session logs. It finds no
violations and three more suspect calls, all from sub-agents and all aimed at the same Comptroller
list. sol-3's `texas_baselines` helper tried a `python -` heredoc, which the shell refused before
Python started ("can't create temp file for here document"), then ran a `python -c` that fetches
the page and prints its length and first 200 characters. sol-6's `texas_policy` helper ran a
`python3 -c` that fetches the page, counts its rows and prints those dated 2026. A reader checked
all three: none reads a local file. Both fetches, like sol-2's, failed to resolve the host name, so
no call returned any data.

`i86 simulate` now reads those audits too. It pools a Codex run only if its session audit passed,
and a suspect call in any of the run's threads keeps it out until a reader accepts it, so pooling
these runs takes `--accept-suspect sol-3 --accept-suspect sol-6` as well; the reader accepts both.
With those flags, every output matches the pooled folder's byte for byte except two cells of
`outputs/summary.md`: the Suspect calls of sol-3 (now 2) and sol-6 (now 1).
`2026-11-03-repooled/` stamps the result.

`2026-11-03-dispatch/SHA256SUMS.ots` holds the proof as `ots upgrade` completed it, with
attestations from four calendars; the earliest sits in Bitcoin block 974415, mined at 17:20:45Z on
11/03, before any run finished (the first finished at 18:09Z). The other proofs sit in later blocks,
all mined before Texas polls close at 01:00Z on 11/04: collected and pooled in block 974441
(21:28:20Z), codex-sessions in 974445 (22:00:55Z) and repooled in 974448 (22:36:36Z). Each upgraded
proof replaced a pending proof of the same manifest, and `SHA256SUMS.ots` at the top matches the
repooled one.

To check a manifest, run `shasum -a 256 -c prereg/<folder>/SHA256SUMS` from the repository root; it
lists any file whose bytes have changed. Against today's files, the pooled and codex-sessions
manifests flag `outputs/summary.md`, which the repooled run rewrote, and
`git show f36db37:outputs/summary.md` gives the bytes they hashed. The codex-sessions and repooled
manifests, and `SHA256SUMS` at the top, also hash the Sol runs' 24 session logs. Those logs carry the
lanes' account details and stay out of this repository, so `shasum -c` reports them missing.
`ots verify prereg/<folder>/SHA256SUMS.ots` checks the proof against a Bitcoin node once the
calendars have anchored it (`ots upgrade` fetches the attestation).
