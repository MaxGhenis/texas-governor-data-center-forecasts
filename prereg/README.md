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

To check a manifest, run `shasum -a 256 -c prereg/<folder>/SHA256SUMS` from the repository root; it
lists any file whose bytes have changed. `ots verify prereg/<folder>/SHA256SUMS.ots` checks the proof
against a Bitcoin node once the calendars have anchored it (`ots upgrade` fetches the attestation).
