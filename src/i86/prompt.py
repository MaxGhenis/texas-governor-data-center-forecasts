"""Build the forecaster prompt from the graph, the context files and the response template.

Every forecaster gets the same prompt, byte for byte; its SHA-256 is recorded with each run.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .graph import ROOT, Graph, Node
from .response import quantile_key, share_key, template

CONTEXT = ROOT / "context"

INSTRUCTIONS = """\
# Forecasting brief: the 2026 Texas governor's race and data center construction

You are one of several forecasters working independently on the same questions. Your forecasts will be
pooled with the others' and logged before Texas polls close on {election_date}. Forecast with what is
known as of {as_of}, before any results. Research the questions yourself with web search, reason from
base rates and current facts, and give your own numbers.

## Rules

1. Work from public sources and this brief. Polls, prediction markets, campaign statements, filings and
   published analyses are all fair game. Do not read local files, other than this brief, on the machine
   you run on.
2. Do not use vote counts or results of the {election_date} election, even partial ones; turnout figures
   from early voting are fine. If you come across a count anyway, say so in `forecaster.notes`.
3. Every number is an absolute level in the unit stated (votes, percent, MW, projects, dollars,
   probabilities), never a ratio or a change.
4. Each forecast is conditional on its scenario. A *cell* such as `dem_50.5` means: the official canvass
   gives Gina Hinojosa exactly that share of the two-party vote for governor (Hinojosa's votes divided by
   Hinojosa's plus Greg Abbott's). At 50.5% she wins; at 49.5% Abbott does. Everything else about the
   world is whatever you think is consistent with that result.
5. Every question but `dem_share` and `turnout` is asked at all six cells: 44%, 47%, 49.5%, 50.5%, 53%
   and 56%.
6. Quantities take five quantiles (p05, p25, p50, p75, p95): your 5th percentile, quartiles, median and
   95th percentile. Quantiles must not decrease and must lie within the stated bounds.
7. `dem_share` takes your cumulative probability that Hinojosa's certified two-party share is at or below
   each grid value (`le_50` is P(share <= 50%)). These must not decrease.
8. Where a question has a `baseline`, report the current value you found with its date and source.
9. Keep each question's `reasoning` to a few sentences: the base rate, the main mechanism, and what
   moves the forecast across cells. List the URLs you relied on in `sources`.
10. Before you research, record in `forecaster.prior_context` anything in your context other than this
    brief (system prompt, memory, instructions, earlier conversation) that mentions the Texas governor's
    race, data centers, or forecasts of these questions. Quote it, or write "none".

## Output

Your final message must be the completed template below as a single JSON object in one ```json fenced
block, with every null replaced. Put your model name in `forecaster.model` and a short summary of your
research in `research_summary`. Use exactly the template's keys: add none and rename none. Nothing
after the block.
"""


def _entries_text(graph: Graph, node: Node) -> str:
    entries = graph.entries(node)
    if [e.key for e in entries] == ["all"]:
        return "one forecast (`all`)"
    return ", ".join(f"`{e.key}`" for e in entries)


def _states_text(node: Node) -> list[str]:
    return [f"  - `{name}`: {cond.text}" for name, cond in node.states.items()]


def node_text(graph: Graph, node: Node) -> str:
    lines = [f"### `{node.id}`: {node.question}", ""]
    if node.kind == "derived":
        lines.append(f"- Computed, not forecast: true when `{node.rule.text}`.")
        if node.notes:
            lines.append(f"- {node.notes}")
        return "\n".join(lines)
    if node.kind == "binary":
        kind = "probability"
    elif node.kind == "quantity":
        kind = (f"quantity in {node.unit}, bounds [{node.bounds[0]:g}, {node.bounds[1]:g}]"
                + (", a whole number" if node.integer else "")
                + "; give " + ", ".join(quantile_key(q) for q in graph.quantiles))
    elif node.kind == "pmf":
        kind = "probability for each of " + ", ".join(f"`{x}`" for x in node.labels)
    elif node.kind == "categorical":
        kind = "probability for each option (they are exclusive and sum to 1)"
    else:
        kind = "cumulative probabilities at " + ", ".join(f"`{share_key(x)}`" for x in graph.share_grid)
    lines.append(f"- Answer each with: {kind}.")
    lines.append(f"- Forecasts: {_entries_text(graph, node)}.")
    if node.states:
        lines.append("- States:")
        lines += _states_text(node)
    if node.options:
        lines.append("- Options:")
        lines += [f"  - `{option}`: {text}" for option, text in node.options.items()]
    if node.exists_if is not None:
        lines.append(f"- Defined only if `{node.exists_if.text}`; void otherwise.")
    lines.append(f"- Resolution: {node.resolution}")
    if node.baseline:
        lines.append("- Report a baseline (current value, date, source).")
    if not node.scored:
        lines.append("- Not scored: no source can settle it, so it is logged as an anchor.")
    if node.notes:
        lines.append(f"- Note: {node.notes}")
    return "\n".join(lines)


def build(graph: Graph) -> str:
    sections = [INSTRUCTIONS.format(election_date=graph.election_date, as_of=graph.as_of)]
    sections.append("## The questions\n")
    sections.append(
        "The governor's race sets the cells. Every other question, on the Senate race, on what the state "
        "does about data centers, and on data center construction in Texas and nationwide, is forecast at "
        "each cell. Read every question before forecasting any, so your answers cohere.\n"
    )
    for module, title in graph.modules.items():
        sections.append(f"## {title}\n")
        for nid in graph.order:
            node = graph.nodes[nid]
            if node.module == module:
                sections.append(node_text(graph, node) + "\n")
    sections.append("## Context\n")
    sections.append((CONTEXT / "brief.md").read_text())
    sections.append("## Response template\n")
    sections.append("```json\n" + json.dumps(template(graph), indent=1) + "\n```\n")
    return "\n".join(sections)


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def write(graph: Graph, path: Path) -> str:
    text = build(graph)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return sha256(text)
