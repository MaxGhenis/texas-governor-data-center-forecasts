# Pooled forecasts

12 independent forecaster runs, 20,000 Monte Carlo draws each (seed 0). Each column weights every forecaster's own conditional forecast equally, whatever that forecaster thinks Hinojosa's chance of winning is. Quantities show the mean and the 5th–95th percentile range; yes/no questions show a probability.

'Abbott wins' and 'Hinojosa wins' differ for two reasons: what a Hinojosa governorship does, and what the result says about Texas voters. Their gap is not an effect. 'At 49.5%' and 'At 50.5%' fix Hinojosa's certified two-party share, with shared random numbers. Their difference, the cutoff effect, is the forecasters' estimate of what a bare Hinojosa win changes; it does not show what a Hinojosa governorship does in a typical world where she wins. 'Per Hinojosa ballot' averages, over forecasters, each one's cutoff effect times its chance that one ballot decides the race, in the question's unit (a probability for yes/no questions). Forecasters who expect a close race weigh more in it, so its sign can differ from the pooled cutoff effect. All are model forecasts under stated scenarios, not observations.

## Who wins

- P(Hinojosa wins): 26.4%
- P(Hinojosa wins with 50–53%): 22.4%; P(Abbott wins with Hinojosa at 47–50%): 44.8%
- Density of Hinojosa's two-party share at 50%: 12.79 per unit share
- Chance one ballot decides it: 1 in 1,582,439

| Run | Model | P(Hinojosa wins) | Mean Hinojosa share | 1 ballot decides | Same at every cell | Same at 49.5% and 50.5% | Suspect calls | Prior context | Flags |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| opus-1 | claude-opus-5-5 | 20% | 47.5% | 1 in 1,978,872 | 0% | 0% | 0 | none |  |
| opus-10 | claude-opus-5-5 | 20% | 47.8% | 1 in 1,745,204 | 0% | 0% | 0 | none |  |
| opus-3 | claude-opus-5-5 | 22% | 47.6% | 1 in 2,170,724 | 0% | 0% | 0 | none. The only extra context was the user's account email and generic agent inst |  |
| opus-4 | claude-opus-5-5 | 22% | 48.0% | 1 in 1,667,665 | 0% | 0% | 0 | none |  |
| opus-8 | claude-opus-5-5 | 24% | 48.0% | 1 in 1,841,691 | 0% | 0% | 0 | none |  |
| opus-9 | claude-opus-5-5 | 35% | 49.0% | 1 in 1,325,914 | 0% | 0% | 0 | none |  |
| sol-1 | gpt-6.1-sol | 21% | 48.4% | 1 in 1,572,997 | 0% | 0% | 0 | The environment context gives the workspace path "/Users/maxghenis/.cache/tx-gov |  |
| sol-2 | gpt-6.1-sol | 33% | 49.0% | 1 in 1,385,122 | 0% | 0% | 1 | Before research, the only relevant context outside the brief was the user-provid |  |
| sol-3 | gpt-6.1-sol | 31% | 48.8% | 1 in 1,467,196 | 0% | 36% | 2 | The environment context supplied cwd: "/Users/maxghenis/.cache/tx-gov-datacenter |  |
| sol-4 | gpt-6.1-sol | 30% | 48.9% | 1 in 1,294,156 | 0% | 0% | 0 | The environment supplied '<cwd>/Users/maxghenis/.cache/tx-gov-datacenter-forecas |  |
| sol-5 | gpt-6.1-sol | 32% | 48.9% | 1 in 1,428,786 | 0% | 0% | 0 | none |  |
| sol-6 | gpt-6.1-sol | 26% | 48.5% | 1 in 1,573,458 | 0% | 0% | 1 | The environment context contains the workspace path "/Users/maxghenis/.cache/tx- |  |

'Same at every cell' and 'Same at 49.5% and 50.5%' are the shares of a run's question-and-state groups whose answers are identical across cells; high values can mean copied answers. 'Suspect calls' counts tool calls the audit flagged for reading without excluding the run. 'Prior context' is what the forecaster reported seeing, before research, beyond the brief. 'late' runs were dispatched after other answers were in the repository; 'recovered' runs were reported lost by their supervisor, and their answer is the final message in the run's own transcript.

## The vote

| Question | Unit | Abbott wins | Hinojosa wins | Abbott narrowly (Hinojosa 47–50%) | Hinojosa narrowly (50–53%) | At 49.5% | At 50.5% | Cutoff effect | Per Hinojosa ballot | Effect by run |
|---|---|---|---|---|---|---|---|---|---|---|
| `turnout` Votes for Hinojosa plus votes for Abbott. | votes (Hinojosa plus Abbott) | 10,117,638 [8,832,172–11,405,248] | 10,119,311 [8,838,103–11,408,317] | 10,118,179 [8,835,709–11,409,242] | 10,121,015 [8,834,381–11,418,786] | 10,118,831 [8,836,311–11,411,729] | 10,118,831 [8,836,311–11,411,729] | +0.00 | – | opus-1 +0.00, opus-10 +0.00, opus-3 +0.00, opus-4 +0.00, opus-8 +0.00, opus-9 +0.00, sol-1 +0.00, sol-2 +0.00, sol-3 +0.00, sol-4 +0.00, sol-5 +0.00, sol-6 +0.00 |
| `senate_dem_share` James Talarico's certified share of the two-party vote for US Senate in Texas. | percent of the two-party vote | 49.7 [45.7–53.3] | 53.8 [50.8–57.2] | 50.8 [48.0–53.7] | 53.4 [50.7–56.1] | 51.8 [49.3–54.3] | 52.7 [50.3–55.3] | +0.91 | – | opus-1 +0.92, opus-10 +0.90, opus-3 +0.90, opus-4 +0.90, opus-8 +0.92, opus-9 +1.00, sol-1 +0.90, sol-2 +0.90, sol-3 +0.90, sol-4 +0.88, sol-5 +0.90, sol-6 +0.90 |

## What the state does about data centers

| Question | Unit | Abbott wins | Hinojosa wins | Abbott narrowly (Hinojosa 47–50%) | Hinojosa narrowly (50–53%) | At 49.5% | At 50.5% | Cutoff effect | Per Hinojosa ballot | Effect by run |
|---|---|---|---|---|---|---|---|---|---|---|
| `ercot_pause_lifted` By 2027-06-30, ERCOT resumes approving new data center Large Loads to energize. | probability | 82% | 62% | 81% | 62% | 80% | 64% | -16.0 pts | -9.7e-08 | opus-1 -22.0 pts, opus-10 -24.0 pts, opus-3 -20.7 pts, opus-4 -22.1 pts, opus-8 -23.3 pts, opus-9 -24.9 pts, sol-1 -9.7 pts, sol-2 -6.1 pts, sol-3 -13.0 pts, sol-4 -11.8 pts, sol-5 -5.9 pts, sol-6 -7.9 pts |
| `special_session_data_centers` The governor calls a special session that takes up data centers, by 2027-12-31. | probability | 27% | 48% | 29% | 48% | 30% | 47% | +16.7 pts | +1.1e-07 | opus-1 +14.1 pts, opus-10 +12.8 pts, opus-3 +4.9 pts, opus-4 +22.3 pts, opus-8 +15.8 pts, opus-9 +17.0 pts, sol-1 +18.8 pts, sol-2 +21.1 pts, sol-3 +21.1 pts, sol-4 +15.2 pts, sol-5 +19.1 pts, sol-6 +17.7 pts |
| `tax_exemption_cut` By 2027-12-31, Texas enacts a law that repeals or narrows its data center sales tax exemptions. | probability | 75% | 79% | 76% | 78% | 77% | 78% | +1.1 pts | +7.9e-09 | opus-1 +1.0 pts, opus-10 -3.0 pts, opus-3 -2.0 pts, opus-4 +2.0 pts, opus-8 +0.9 pts, opus-9 -2.0 pts, sol-1 +3.9 pts, sol-2 +3.2 pts, sol-3 +0.9 pts, sol-4 +3.1 pts, sol-5 +3.1 pts, sol-6 +2.1 pts |
| `restriction_law` By 2027-12-31, Texas enacts a law that adds limits on building or connecting data centers. | probability | 75% | 80% | 76% | 80% | 77% | 79% | +2.2 pts | +1.4e-08 | opus-1 +1.9 pts, opus-10 +2.0 pts, opus-3 +3.0 pts, opus-4 +2.0 pts, opus-8 +4.3 pts, opus-9 -2.1 pts, sol-1 +3.0 pts, sol-2 +3.3 pts, sol-3 +0.0 pts, sol-4 +4.2 pts, sol-5 +3.0 pts, sol-6 +2.1 pts |

## Data center construction in Texas

| Question | Unit | Abbott wins | Hinojosa wins | Abbott narrowly (Hinojosa 47–50%) | Hinojosa narrowly (50–53%) | At 49.5% | At 50.5% | Cutoff effect | Per Hinojosa ballot | Effect by run |
|---|---|---|---|---|---|---|---|---|---|---|
| `ercot_approved_mw_2027` Large Load MW with ERCOT's Approval to Energize, at the end of 2027. | MW | 18,137 [9,506–36,200] | 15,810 [9,088–31,614] | 17,915 [9,473–35,724] | 15,959 [9,118–31,998] | 17,634 [9,396–35,196] | 16,112 [9,143–32,514] | -1,522 | -0.001 | opus-1 -1,402, opus-10 -1,332, opus-3 -861, opus-4 -1,210, opus-8 -1,408, opus-9 -2,765, sol-1 -1,011, sol-2 -2,104, sol-3 -1,109, sol-4 -2,395, sol-5 -1,548, sol-6 -1,122 |
| `ercot_approved_mw_2028` Large Load MW with ERCOT's Approval to Energize, at the end of 2028. | MW | 27,822 [10,956–60,433] | 23,654 [9,902–52,567] | 27,519 [10,925–59,728] | 23,838 [9,929–53,034] | 27,024 [10,791–58,679] | 24,234 [10,037–54,008] | -2,789 | -0.0018 | opus-1 -2,569, opus-10 -2,268, opus-3 -2,009, opus-4 -2,075, opus-8 -2,322, opus-9 -4,487, sol-1 -2,022, sol-2 -3,880, sol-3 -2,157, sol-4 -3,972, sol-5 -3,511, sol-6 -2,202 |
| `comptroller_new_projects_2027` Data center projects the Comptroller registers for the sales tax exemptions with an effective date in 2027. | projects | 60.3 [11–119] | 50.3 [5.00–105] | 59.3 [10–118] | 50.9 [6.00–106] | 58.2 [9.00–116] | 52.0 [6.00–108] | -6.20 | -4e-06 | opus-1 -4.69, opus-10 -2.99, opus-3 -7.69, opus-4 -6.29, opus-8 -4.46, opus-9 -7.52, sol-1 -5.43, sol-2 -9.60, sol-3 -5.61, sol-4 -6.10, sol-5 -7.41, sol-6 -6.55 |

## Data center construction nationwide

| Question | Unit | Abbott wins | Hinojosa wins | Abbott narrowly (Hinojosa 47–50%) | Hinojosa narrowly (50–53%) | At 49.5% | At 50.5% | Cutoff effect | Per Hinojosa ballot | Effect by run |
|---|---|---|---|---|---|---|---|---|---|---|
| `us_dc_spending_2027` US private construction spending on data centers in 2027. | billions of current dollars | 125 [70.5–209] | 122 [68.4–205] | 124 [70.4–208] | 122 [68.6–205] | 124 [69.8–207] | 123 [69.0–206] | -1.12 | -6.8e-07 | opus-1 -1.84, opus-10 -1.00, opus-3 -2.00, opus-4 -1.00, opus-8 -1.00, opus-9 -1.62, sol-1 -1.16, sol-2 -1.00, sol-3 +0.00, sol-4 -1.00, sol-5 -0.78, sol-6 -1.00 |
| `us_dc_spending_2028` US private construction spending on data centers in 2028. | billions of current dollars | 157 [61.9–315] | 152 [59.5–306] | 156 [61.6–312] | 153 [59.8–307] | 155 [61.2–311] | 153 [60.3–309] | -1.63 | -1e-06 | opus-1 -2.84, opus-10 -1.15, opus-3 -2.63, opus-4 -1.00, opus-8 -1.85, opus-9 -3.23, sol-1 -2.37, sol-2 -1.37, sol-3 +0.00, sol-4 -1.00, sol-5 -1.16, sol-6 -1.00 |
| `other_state_moratorium` A US state other than Texas enacts a statewide moratorium on new data centers by 2027-12-31. | probability | 64% | 69% | 65% | 68% | 66% | 67% | +1.6 pts | +1e-08 | opus-1 +2.1 pts, opus-10 +2.0 pts, opus-3 +0.9 pts, opus-4 +1.0 pts, opus-8 +2.0 pts, opus-9 +2.8 pts, sol-1 +2.0 pts, sol-2 +1.0 pts, sol-3 +0.0 pts, sol-4 +2.0 pts, sol-5 +1.9 pts, sol-6 +1.1 pts |

For a question defined only under a condition (none in this map), a cell shows the probability given that condition, and the joint probability P(condition and event) in parentheses where the two differ. The conditional is each forecaster's own, from draws restricted to worlds where the condition holds and weighted by that forecaster's probability of it, so every forecaster that gives the condition any probability counts equally. The cutoff effect and the per-ballot figure use the joint. 'n/a' marks conditions where the question is undefined; '(k of n runs)' marks a cell to which only k forecasters contribute.

† Asked only at a bare loss and a bare win (49.5% and 50.5%; none in this map). The Abbott wins and Hinojosa wins columns apply those answers at every margin on their side. They still vary with the margin through upstream questions answered at every cell, but not through the question's own answers.

Quantity tails beyond the 5th and 95th percentiles continue the neighbouring segment's slope, so means of heavy right tails are understated.
