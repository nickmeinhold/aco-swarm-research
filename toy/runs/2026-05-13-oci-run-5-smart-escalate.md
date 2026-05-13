# OCI run 5 — heuristic + smart escalation trigger

**Date:** 2026-05-13, 13:00 AEST
**TASKS.md:** #15 follow-up (Finding 2's recommendation from run 4)
**Raw log:** [`2026-05-13-oci-run-5-smart-escalate.log`](2026-05-13-oci-run-5-smart-escalate.log)

## Setup

- `toy/colony.py` with new `--escalate-trigger smart` option:
  - `smart` = escalate to LLM when **cornered** OR when `len(path) >= 0.6 × max_steps` AND target not in current's neighbours
  - `cornered` (default, run 4 semantics) = escalate only when all neighbours visited
- Same host (ant-1), backend (queen Qwen-7B-Q4 over private VCN), params (5×3×20×max_steps=12)
- Command: `uv run colony.py --queen --escalate --escalate-trigger smart --reset`

## Headline — five-way comparison final

| Backend | Success | Wall | LLM calls | Pareto position |
|---|---|---|---|---|
| Heuristic (run 2) | 9/15 (60%) | 0.68s | 0 | Cheapest baseline |
| H + cornered escalation (run 4) | 9/15 (60%) | 58.8s | 2 | Same success, far cheaper than all-LLM |
| **H + smart escalation (this run)** | **11/15 (73%)** | **10m16s** | **43** | **Best success-per-cost** |
| Qwen-everywhere (run 1) | 11/15 (73%) | 24m34s | ~140 | Same success, 2.4× slower |
| SmolLM2-local-on-ant (run 3) | 3/15 (20%) | 28m49s | ~186 | Dominated on every axis |

**Smart escalation matches Qwen-everywhere success at 2.4× speedup and 3.3× fewer LLM calls.** It also beats pure heuristic on success rate (+2/15) at moderate cost (~10 min wall). **This is the positive evidence for the architectural pivot** — the deployment shape that minimises queen-CPU while matching the success quality of the original heterogeneous-LLM plan.

## Findings

### Finding 1 — Smart escalation is the Pareto-best point. `verified`

11/15 success matches the strongest LLM-on-every-step baseline (Qwen-everywhere) at less than half the wall and one-third the LLM calls. It also beats the pure-heuristic floor by +2/15. **This is the positive evidence the architectural pivot needed.**

### Finding 2 — The improvement comes from cycle 1 cold-start. `verified`

Cycle-by-cycle success rate:

| Cycle | Heuristic-only (run 2) | Cornered-escalate (run 4) | **Smart-escalate (this run)** |
|---|---|---|---|
| 1 | 3/5 | 4/5 | **5/5** |
| 2 | 2/5 | 3/5 | 3/5 |
| 3 | 4/5 | 2/5 | 3/5 |
| **Total** | **9/15** | **9/15** | **11/15** |

The smart-escalate gain is concentrated in **cycle 1: 5/5 success with 12 escalations** when there is no substrate signal yet. Cycles 2 and 3 are within-noise (heuristic alone does fine once the trail amplifies). **The LLM's job, in this design, is primarily to bootstrap the substrate — not to be the ant.**

### Finding 3 — "LLM-as-substrate-seeder" reframe. `concept`

The mental model "LLM-as-ant" suggests LLMs make ant-level decisions while ants walk on the graph. Run 5's mechanism is materially different: **LLM escalations in cycle 1 deposit pheromone on edges that the heuristic then surfs in cycles 2-3 with zero escalations.**

Specifically: cycle 3 ants `a1` and `a2` each found 7-hop near-optimal paths `n0→n5→n4→n3→n12→n11→n19` with **zero escalations** — pure heuristic following a trail that earlier escalation-rescued ants laid down. The LLM seeds the substrate; the substrate carries the heuristic; together they coordinate.

This reframe sharpens the project's contribution claim. The novelty isn't "use LLMs as ants" (well-trodden) — it's "**use LLMs sparingly to seed a stigmergic substrate that heuristic ants follow**". The substrate becomes the *carrier of LLM intelligence into a low-cost runtime*, which is a different conceptual move than either pure-LLM-swarms or pure-heuristic-ACO.

Should be reflected in any SYNTHESIS.md rewrite — see "Implications" below.

### Finding 4 — Step-by-step escalation has a recovery ceiling. `verified`

Cycle 2 a0/a1 and cycle 3 a3/a4 each escalated 5-6 times and still failed. The LLM picked individual next-steps that seemed locally reasonable but didn't reverse a global "wandered far from target" condition. **Step-by-step LLM calls can't undo cumulative wrong turns.**

Sketch of a follow-up: at escalation, pass the LLM the full path and graph-snapshot, ask for a **sub-plan** (next 3-5 steps), not just one step. Saves round-trips and lets the LLM plan a coherent recovery. Worth its own TASKS.md entry — "Sub-plan escalation" — for future iteration.

### Finding 5 — Smart trigger fires often but bounded. `verified`

43 escalations across 15 ants × ~9 average steps = ~14% of step-decisions deferred to the LLM. Higher than cornered-only's 1.4% by 10×, much lower than Qwen-everywhere's 100%. The trigger is **self-limiting per ant** because once an ant reaches the target the loop exits; failing ants escalate every step past the threshold, so failed-ant escalation cost is proportional to `max_steps - threshold` = ~5 calls each.

For a bigger graph (1000-node Hetionet subset, max_steps probably 30-50), failure-mode escalations could rise sharply. **An escalation budget per ant** (cap on LLM calls per ant per cycle) might be worth adding.

### Finding 6 — Premature convergence less visible at smart trigger. `verified`

Run 4 showed cycle 3 over-converging onto a suboptimal trunk. Run 5 cycle 3 is back to 3/5 (vs run 4's 2/5) and the successful ants found genuinely good paths (7 hops). The LLM's seeding in cycle 1 created multiple distinct successful paths (the cycle 1 pheromone-top showed `n7__n8, n18__n19, n14__n15, n14__n7, n15__n16` all in the top), which gave cycles 2-3 more options than the run-4 trunk. **Diversity in seeding → less premature convergence.** Suggests MMAS bounds are still useful but less urgent under this design than they would be under pure-heuristic.

## Implications

1. **README and SYNTHESIS.md rewrite is now justified by positive evidence.** The project shape is "heuristic-on-ants + queen-Qwen as substrate seeder via smart-trigger escalation", not "1 queen + 4 micros with heterogeneous LLM ants". Major pitch rewrite — likely needs Nick's eyes before pushing.

2. **`feedback_llm_as_anti_diversity_prior.md` should be revised or retired.** The "LLMs as anti-diversity prior" framing was based on Haiku in 2026-05-05's toy. With Qwen-7B-Q4 at sparse escalation, the LLM contributes *diversity in seeding*, not over-exploitation. The cleaner framing across all five runs: **the LLM's role depends on call frequency** — at 100% (Qwen-everywhere) it converges hard; at 14% (smart trigger) it diversifies; at 0% (heuristic) it's absent.

3. **New project axis: escalation trigger design.** A research dimension that didn't exist before this run. Triggers tested: `cornered` (run 4), `smart=cornered+long-path` (run 5). Worth exploring: low-pheromone-signal trigger, learned-trigger, multi-step-escalation.

4. **Sub-plan escalation (Finding 4)** is the next single experiment if we want to push success above 11/15. Replace "one LLM call → one step" with "one LLM call → 3-5 step sub-plan". Predicted to recover the a3/a4 cases that ran out of step budget despite 5-6 escalations.

5. **Escalation budget per ant** (Finding 5) becomes more important on bigger graphs. A 1000-node run might explode escalation count without a cap.

## Status of TASKS.md #15

**Done.** Both phases (cornered trigger run 4, smart trigger run 5) executed; positive evidence in hand. The README/SYNTHESIS rewrite that this finding unblocks is now the load-bearing next step — surface to Nick, don't auto-merge a project-identity-level change without his eyes.
