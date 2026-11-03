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
| `2026-11-03-pooled/` | 20:54Z 11/03 | the above plus `outputs/` from `i86 simulate --accept-suspect sol-2 --accept-prior opus-3 --accept-prior sol-1 --accept-prior sol-2 --accept-prior sol-3 --accept-prior sol-4 --accept-prior sol-6` (seed 0, 20,000 draws), and `scripts/rd_summary.py` |
| `2026-11-03-codex-sessions/` | 21:50Z 11/03 | the above, unchanged, plus each Sol run's `codex-sessions/`: the session logs of its main thread and its three sub-agents, and their audit from `scripts/audit_codex_sessions.py` |

The pooled run accepts two kinds of flag after a reader checked each one. sol-2's one suspect call runs
`python3 -I -c` to fetch and parse the Comptroller's public list of registered data centers
(comptroller.texas.gov/taxes/data-centers/data-center-lists.php); it reads no local file. opus-3's
prior context says "none" and adds that nothing in its context mentions these questions; sol-1, 2, 3,
4 and 6 quote only their work directory's name, which repeats the brief's subject.

Each Sol run's main thread spawned three sub-agents, and its transcript omits their calls.
`scripts/audit_codex_sessions.py` audits all 24 Sol threads from the lanes' session logs. It finds no
violations and three more suspect calls, all from sub-agents and all aimed at the same Comptroller
list. sol-3's `texas_baselines` helper ran a `python -` heredoc, which stopped at once with the
shell's error "can't create temp file for here document", then a `python -c` fetch; sol-6's
`texas_policy` helper ran a `python3 -c` fetch. A reader checked all three: each only fetches and
parses that public page, and none reads a local file. Both fetches, like sol-2's, failed to resolve
the host name, so no call returned any data. Had `audit` seen these calls, the pooled run would have
needed `--accept-suspect sol-3 --accept-suspect sol-6` as well; the reader accepts both, so the
pooled outputs stand.

`2026-11-03-dispatch/SHA256SUMS.ots` holds the proof as `ots upgrade` completed it, with
attestations from four calendars; the earliest sits in Bitcoin block 974415, mined at 17:20:45Z on
11/03, before any run started. The pending proof it replaced stamped the same manifest.

To check a manifest, run `shasum -a 256 -c prereg/<folder>/SHA256SUMS` from the repository root; it
lists any file whose bytes have changed. `ots verify prereg/<folder>/SHA256SUMS.ots` checks the proof
against a Bitcoin node once the calendars have anchored it (`ots upgrade` fetches the attestation).
