# Timestamps

`i86 prereg` writes `SHA256SUMS`, the SHA-256 of the map, the prompt, the response template, the
context brief, every run's `meta.json`, `response.md`, `response.json`, `audit.json` and
`transcript.jsonl`, and the files at the top of `outputs/` (not the charts). It then stamps the
manifest with OpenTimestamps. Each dated folder keeps one manifest and its proof; `SHA256SUMS` and
`SHA256SUMS.ots` at the top are the latest.

| Folder | Written | Covers |
|---|---|---|
| `2026-11-03-dispatch/` | 17:04Z 11/03 | the map, prompt, template and brief, before any run was dispatched |
| `2026-11-03-collected/` | 20:50Z 11/03 | every run's answer, parsed response, audit and transcript, collected once the last run had finished |
| `2026-11-03-pooled/` | 20:54Z 11/03 | the above plus `outputs/` from `i86 simulate --accept-suspect sol-2 --accept-prior opus-3 --accept-prior sol-1 --accept-prior sol-2 --accept-prior sol-3 --accept-prior sol-4 --accept-prior sol-6` (seed 0, 20,000 draws), and `scripts/rd_summary.py` |

The pooled run accepts two kinds of flag after a reader checked each one. sol-2's one suspect call runs
`python3 -I -c` to fetch and parse the Comptroller's public list of registered data centers
(comptroller.texas.gov/taxes/data-centers/data-center-lists.php); it reads no local file. opus-3's
prior context says "none" and adds that nothing in its context mentions these questions; sol-1, 2, 3,
4 and 6 quote only their work directory's name, which repeats the brief's subject.

To check a manifest, run `shasum -a 256 -c prereg/<folder>/SHA256SUMS` from the repository root; it
lists any file whose bytes have changed. `ots verify prereg/<folder>/SHA256SUMS.ots` checks the proof
against a Bitcoin node once the calendars have anchored it (`ots upgrade` fetches the attestation).
