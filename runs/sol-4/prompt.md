# Forecasting brief: the 2026 Texas governor's race and data center construction

You are one of several forecasters working independently on the same questions. Your forecasts will be
pooled with the others' and logged before Texas polls close on 2026-11-03. Forecast with what is
known as of 2026-11-03, before any results. Research the questions yourself with web search, reason from
base rates and current facts, and give your own numbers.

## Rules

1. Work from public sources and this brief. Polls, prediction markets, campaign statements, filings and
   published analyses are all fair game. Do not read local files, other than this brief, on the machine
   you run on.
2. Do not use vote counts or results of the 2026-11-03 election, even partial ones; turnout figures
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

## The questions

The governor's race sets the cells. Every other question, on the Senate race, on what the state does about data centers, and on data center construction in Texas and nationwide, is forecast at each cell. Read every question before forecasting any, so your answers cohere.

## The vote

### `dem_share`: Gina Hinojosa's certified share of the two-party vote for governor.

- Answer each with: cumulative probabilities at `le_38`, `le_40`, `le_42`, `le_44`, `le_45`, `le_46`, `le_47`, `le_48`, `le_49`, `le_50`, `le_51`, `le_52`, `le_53`, `le_54`, `le_55`, `le_56`, `le_58`, `le_60`, `le_62`.
- Forecasts: one forecast (`all`).
- Resolution: The official canvass of the 2026-11-03 general election for governor, as the Texas Secretary of State publishes it: Hinojosa's votes divided by Hinojosa's votes plus Greg Abbott's. Votes for other candidates are left out.

### `turnout`: Votes for Hinojosa plus votes for Abbott.

- Answer each with: quantity in votes (Hinojosa plus Abbott), bounds [5e+06, 1.4e+07], a whole number; give p05, p25, p50, p75, p95.
- Forecasts: one forecast (`all`).
- Resolution: The official canvass, as for dem_share.

### `senate_dem_share`: James Talarico's certified share of the two-party vote for US Senate in Texas.

- Answer each with: quantity in percent of the two-party vote, bounds [30, 70]; give p05, p25, p50, p75, p95.
- Forecasts: `dem_44.0`, `dem_47.0`, `dem_49.5`, `dem_50.5`, `dem_53.0`, `dem_56.0`.
- Resolution: The official canvass of the 2026-11-03 general election for US Senate, as the Texas Secretary of State publishes it: Talarico's votes divided by Talarico's votes plus Ken Paxton's, as a percent.

## What the state does about data centers

### `ercot_pause_lifted`: By 2027-06-30, ERCOT resumes approving new data center Large Loads to energize.

- Answer each with: probability.
- Forecasts: `dem_44.0`, `dem_47.0`, `dem_49.5`, `dem_50.5`, `dem_53.0`, `dem_56.0`.
- Resolution: Between 2026-11-04 and 2027-06-30, ERCOT resumes giving Approval to Energize to data center Large Loads (75 MW or more) that were not energized when it paused those approvals on 2026-08-03, as an ERCOT market notice, board or TAC presentation, or Large Load Interconnection Status Update shows. Approvals only for loads that pass the verification and audit count; approvals only in emergencies do not. Sources: ERCOT market notices and Large Load reports (ercot.com); PUCT filings.

### `special_session_data_centers`: The governor calls a special session that takes up data centers, by 2027-12-31.

- Answer each with: probability.
- Forecasts: `dem_44.0`, `dem_47.0`, `dem_49.5`, `dem_50.5`, `dem_53.0`, `dem_56.0`.
- Resolution: Between 2026-11-04 and 2027-12-31, the governor issues a proclamation convening a special session of the Legislature, or adding to one, that names data centers or large electric loads among its subjects. Abbott serves until his successor takes office in January 2027, so his calls count. Sources: the governor's proclamations (gov.texas.gov); the Texas Register; Texas Legislature Online.

### `tax_exemption_cut`: By 2027-12-31, Texas enacts a law that repeals or narrows its data center sales tax exemptions.

- Answer each with: probability.
- Forecasts: `dem_44.0`, `dem_47.0`, `dem_49.5`, `dem_50.5`, `dem_53.0`, `dem_56.0`.
- Resolution: Between 2026-11-04 and 2027-12-31, a bill becomes law (signed, left unsigned past the deadline, or passed over a veto) that does at least one of these to the exemptions for qualifying data centers and qualifying large data center projects (Tax Code sections 151.359 and 151.3595): repeals either; closes either to new certifications; shortens either's exemption period; takes electricity out of either; or narrows the purchases either covers. A law that only adds reporting, audits or clawbacks does not count. Sources: Texas Legislature Online; the Tax Code; the Comptroller's data center pages.

### `restriction_law`: By 2027-12-31, Texas enacts a law that adds limits on building or connecting data centers.

- Answer each with: probability.
- Forecasts: `dem_44.0`, `dem_47.0`, `dem_49.5`, `dem_50.5`, `dem_53.0`, `dem_56.0`.
- Resolution: Between 2026-11-04 and 2027-12-31, a bill becomes law that, for data centers or for electric loads of 75 MW or more, adds at least one of: a moratorium or pause on new interconnections or energizations; a state or local approval, siting or zoning requirement; a limit, fee or permit on water use; an interconnection fee or required payment toward grid costs beyond those in Senate Bill 6 (2025); or a cap on power use. Laws that only require reporting or studies, and changes to the sales tax exemptions alone, do not count. Sources: Texas Legislature Online; the Texas statutes.

## Data center construction in Texas

### `ercot_approved_mw_2027`: Large Load MW with ERCOT's Approval to Energize, at the end of 2027.

- Answer each with: quantity in MW, bounds [3000, 150000]; give p05, p25, p50, p75, p95.
- Forecasts: `dem_44.0`, `dem_47.0`, `dem_49.5`, `dem_50.5`, `dem_53.0`, `dem_56.0`.
- Resolution: The MW of Large Loads (75 MW or more, all project types) that have received Approval to Energize, Observed Energized and Approved to Energize but Not Operational together, in the last Large Load Interconnection Status Update ERCOT publishes in 2027, or the report that replaces it. The March 13, 2026 update gave 9,042 MW.
- Report a baseline (current value, date, source).

### `ercot_approved_mw_2028`: Large Load MW with ERCOT's Approval to Energize, at the end of 2028.

- Answer each with: quantity in MW, bounds [3000, 200000]; give p05, p25, p50, p75, p95.
- Forecasts: `dem_44.0`, `dem_47.0`, `dem_49.5`, `dem_50.5`, `dem_53.0`, `dem_56.0`.
- Resolution: As for ercot_approved_mw_2027, in the last update ERCOT publishes in 2028.
- Report a baseline (current value, date, source).

### `comptroller_new_projects_2027`: Data center projects the Comptroller registers for the sales tax exemptions with an effective date in 2027.

- Answer each with: quantity in projects, bounds [0, 400], a whole number; give p05, p25, p50, p75, p95.
- Forecasts: `dem_44.0`, `dem_47.0`, `dem_49.5`, `dem_50.5`, `dem_53.0`, `dem_56.0`.
- Resolution: Entries on the Texas Comptroller's lists of Registered Qualifying Data Center Projects and Registered Qualifying Large Data Center Projects (comptroller.texas.gov/taxes/data-centers/data-center-lists.php) with an Effective Date from 2027-01-01 to 2027-12-31, counted on 2028-03-31. If the lists stop being published, the count the Comptroller reports for that period. Baseline: entries with an Effective Date in 2026 on the day you look.
- Report a baseline (current value, date, source).

## Data center construction nationwide

### `us_dc_spending_2027`: US private construction spending on data centers in 2027.

- Answer each with: quantity in billions of current dollars, bounds [10, 400]; give p05, p25, p50, p75, p95.
- Forecasts: `dem_44.0`, `dem_47.0`, `dem_49.5`, `dem_50.5`, `dem_53.0`, `dem_56.0`.
- Resolution: The annual value of private construction put in place for data centers in calendar 2027, in the Census Bureau's Construction Spending tables (the 'Data center' line of the private series), as first published in the release of July 2028.
- Report a baseline (current value, date, source).

### `us_dc_spending_2028`: US private construction spending on data centers in 2028.

- Answer each with: quantity in billions of current dollars, bounds [10, 600]; give p05, p25, p50, p75, p95.
- Forecasts: `dem_44.0`, `dem_47.0`, `dem_49.5`, `dem_50.5`, `dem_53.0`, `dem_56.0`.
- Resolution: As for us_dc_spending_2027, for calendar 2028, as first published in the release of July 2029.
- Report a baseline (current value, date, source).

### `other_state_moratorium`: A US state other than Texas enacts a statewide moratorium on new data centers by 2027-12-31.

- Answer each with: probability.
- Forecasts: `dem_44.0`, `dem_47.0`, `dem_49.5`, `dem_50.5`, `dem_53.0`, `dem_56.0`.
- Resolution: Between 2026-11-04 and 2027-12-31, a state other than Texas enacts a law, or its governor or a statewide agency issues an order, that for a period bars new data centers, or new connections or approvals for data centers, across the state. Moratoria by counties, cities or single utilities do not count. Sources: state legislative records; governors' orders; news.

## Context

### The election

- Texas votes on 2026-11-03. Governor Greg Abbott (Republican) faces Gina Hinojosa (Democrat).
- The same ballot carries the US Senate race between James Talarico (Democrat) and Ken Paxton
  (Republican), who beat Senator John Cornyn in the Republican runoff on 2026-05-26.
- Polls close at 7 p.m. local time: 01:00 UTC on 2026-11-04 in most of the state, and an hour later in
  El Paso and Hudspeth counties, which keep Mountain time.
- The governor elected takes office in January 2027. The 90th Legislature's regular session opens on
  2027-01-12 and runs 140 days, to 2027-05-31.

### Data centers and the grid

- On 2026-08-03 Governor Abbott directed the Public Utility Commission and ERCOT to complete "a
  comprehensive verification and audit" of all data centers advancing through the interconnection
  process before allowing those loads to proceed. ERCOT then paused its Batch Zero study and stopped
  approving data centers and crypto mining facilities of 75 MW or more to energize, until the
  verification and audit and a community impact review are complete. ERCOT is to file both reports with
  the Commission by 2026-12-10. Source: ERCOT Board of Directors, Item 14, Batch Zero Update,
  2026-09-14
  (https://www.ercot.com/files/docs/2026/09/11/14-Batch-Zero-Update.pdf).
- In that update, ERCOT had conditionally classified 204 Large Load projects (66.4 GW) as base load and
  158 (127.9 GW) as studied load in Batch Zero, its one-time study of Large Loads (75 MW or more) that
  seek to connect.
- ERCOT's Large Load Interconnection Status Update of 2026-03-13 reported 9,042 MW of Large Loads with
  Approval to Energize
  (https://www.ercot.com/files/docs/2026/03/12/March-TAC-Report.pdf).
- Senate Bill 6 (89th Legislature, 2025) set standards for connecting large loads in ERCOT, with a
  default threshold of 75 MW, covering cost allocation, backup generation, financial commitments and
  curtailment during shortages
  (https://capitol.texas.gov/tlodocs/89R/analysis/html/SB00006F.htm).

### Sales tax exemptions

- The Comptroller certifies qualifying data centers (at least 100,000 square feet, 20 jobs and $200
  million of investment over five years) and qualifying large data center projects (at least 250,000
  square feet, 40 jobs and $500 million). Their qualifying purchases, including electricity necessary
  and essential to their operation, are exempt from the 6.25% state sales tax for 10 or 15 years (data
  centers) or 20 years (large projects) (https://comptroller.texas.gov/taxes/data-centers/). The
  Comptroller lists both kinds of registered projects with their effective dates
  (https://comptroller.texas.gov/taxes/data-centers/data-center-lists.php).

### Construction statistics

- The Census Bureau's monthly Construction Spending release reports data center construction in its
  private construction table (https://www.census.gov/construction/c30/c30index.html).

## Response template

```json
{
 "forecaster": {
  "model": null,
  "prior_context": null,
  "notes": null
 },
 "research_summary": null,
 "nodes": {
  "dem_share": {
   "forecasts": {
    "all": {
     "le_38": null,
     "le_40": null,
     "le_42": null,
     "le_44": null,
     "le_45": null,
     "le_46": null,
     "le_47": null,
     "le_48": null,
     "le_49": null,
     "le_50": null,
     "le_51": null,
     "le_52": null,
     "le_53": null,
     "le_54": null,
     "le_55": null,
     "le_56": null,
     "le_58": null,
     "le_60": null,
     "le_62": null
    }
   },
   "reasoning": null,
   "sources": []
  },
  "turnout": {
   "forecasts": {
    "all": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    }
   },
   "reasoning": null,
   "sources": []
  },
  "senate_dem_share": {
   "forecasts": {
    "dem_44.0": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    },
    "dem_47.0": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    },
    "dem_49.5": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    },
    "dem_50.5": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    },
    "dem_53.0": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    },
    "dem_56.0": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    }
   },
   "reasoning": null,
   "sources": []
  },
  "ercot_pause_lifted": {
   "forecasts": {
    "dem_44.0": {
     "p": null
    },
    "dem_47.0": {
     "p": null
    },
    "dem_49.5": {
     "p": null
    },
    "dem_50.5": {
     "p": null
    },
    "dem_53.0": {
     "p": null
    },
    "dem_56.0": {
     "p": null
    }
   },
   "reasoning": null,
   "sources": []
  },
  "special_session_data_centers": {
   "forecasts": {
    "dem_44.0": {
     "p": null
    },
    "dem_47.0": {
     "p": null
    },
    "dem_49.5": {
     "p": null
    },
    "dem_50.5": {
     "p": null
    },
    "dem_53.0": {
     "p": null
    },
    "dem_56.0": {
     "p": null
    }
   },
   "reasoning": null,
   "sources": []
  },
  "tax_exemption_cut": {
   "forecasts": {
    "dem_44.0": {
     "p": null
    },
    "dem_47.0": {
     "p": null
    },
    "dem_49.5": {
     "p": null
    },
    "dem_50.5": {
     "p": null
    },
    "dem_53.0": {
     "p": null
    },
    "dem_56.0": {
     "p": null
    }
   },
   "reasoning": null,
   "sources": []
  },
  "restriction_law": {
   "forecasts": {
    "dem_44.0": {
     "p": null
    },
    "dem_47.0": {
     "p": null
    },
    "dem_49.5": {
     "p": null
    },
    "dem_50.5": {
     "p": null
    },
    "dem_53.0": {
     "p": null
    },
    "dem_56.0": {
     "p": null
    }
   },
   "reasoning": null,
   "sources": []
  },
  "ercot_approved_mw_2027": {
   "baseline": {
    "value": null,
    "as_of": null,
    "source": null
   },
   "forecasts": {
    "dem_44.0": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    },
    "dem_47.0": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    },
    "dem_49.5": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    },
    "dem_50.5": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    },
    "dem_53.0": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    },
    "dem_56.0": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    }
   },
   "reasoning": null,
   "sources": []
  },
  "ercot_approved_mw_2028": {
   "baseline": {
    "value": null,
    "as_of": null,
    "source": null
   },
   "forecasts": {
    "dem_44.0": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    },
    "dem_47.0": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    },
    "dem_49.5": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    },
    "dem_50.5": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    },
    "dem_53.0": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    },
    "dem_56.0": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    }
   },
   "reasoning": null,
   "sources": []
  },
  "comptroller_new_projects_2027": {
   "baseline": {
    "value": null,
    "as_of": null,
    "source": null
   },
   "forecasts": {
    "dem_44.0": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    },
    "dem_47.0": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    },
    "dem_49.5": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    },
    "dem_50.5": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    },
    "dem_53.0": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    },
    "dem_56.0": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    }
   },
   "reasoning": null,
   "sources": []
  },
  "us_dc_spending_2027": {
   "baseline": {
    "value": null,
    "as_of": null,
    "source": null
   },
   "forecasts": {
    "dem_44.0": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    },
    "dem_47.0": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    },
    "dem_49.5": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    },
    "dem_50.5": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    },
    "dem_53.0": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    },
    "dem_56.0": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    }
   },
   "reasoning": null,
   "sources": []
  },
  "us_dc_spending_2028": {
   "baseline": {
    "value": null,
    "as_of": null,
    "source": null
   },
   "forecasts": {
    "dem_44.0": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    },
    "dem_47.0": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    },
    "dem_49.5": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    },
    "dem_50.5": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    },
    "dem_53.0": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    },
    "dem_56.0": {
     "p05": null,
     "p25": null,
     "p50": null,
     "p75": null,
     "p95": null
    }
   },
   "reasoning": null,
   "sources": []
  },
  "other_state_moratorium": {
   "forecasts": {
    "dem_44.0": {
     "p": null
    },
    "dem_47.0": {
     "p": null
    },
    "dem_49.5": {
     "p": null
    },
    "dem_50.5": {
     "p": null
    },
    "dem_53.0": {
     "p": null
    },
    "dem_56.0": {
     "p": null
    }
   },
   "reasoning": null,
   "sources": []
  }
 }
}
```
