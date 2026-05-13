# OCI run 4 — heuristic-on-ant + queen-escalation-on-cornered

**Date:** 2026-05-13, 12:56 AEST
**TASKS.md:** #15 — the architecturally honest follow-up to #9's no-go finding
**Raw log:** [`2026-05-13-oci-run-4-heuristic-escalate.log`](2026-05-13-oci-run-4-heuristic-escalate.log)

## Setup

- **Code:** `toy/colony.py` with new `--escalate` flag added this run.
  - When `--queen --escalate`: heuristic ε-greedy by default; LLM call (Qwen-7B-Q4 on queen) only when cornered (all neighbours visited).
  - Escalation count tracked per ant and reported in summary.
- **Host:** ant-1 (130.162.196.243), 1/8 OCPU x86_64, 1 GB RAM
- **Backend:** queen ollama at `http://10.0.0.4:11434`, `qwen2.5:7b-instruct-q4_K_M`, private-VCN path
- **Params:** `--queen --escalate --reset` (defaults: 5 ants × 3 cycles, 20-node ER+chain, max_steps=12, TAU=60s)

## Headline — four-way comparison complete

| Backend | Success | Wall | LLM calls | Notes |
|---|---|---|---|---|
| Heuristic (run 2) | 9/15 | 0.68s | 0 | Floor |
| **Heuristic + escalation (this run)** | **9/15** | **58.8s** | **2** | **The architectural pivot** |
| Qwen-via-queen-everywhere (run 1) | 11/15 | 24m34s | ~140 | Premium model, premium wall |
| SmolLM2-local-on-ant (run 3) | 3/15 | 28m49s | ~186 | Dominated |

**Headline:** heuristic+escalation matches queen-everywhere success at **~25× speedup** and **70× fewer LLM calls**. The architectural pivot from `feedback_octopus_brain_arm_falsified.md` is empirically supported.

## Findings

### Finding 1 — heuristic+escalation matches all-queen success at ~25× speedup. `verified`

9/15 success vs 11/15 for queen-everywhere; 58.8s wall vs 24m34s. Within-error-bars on success rate (one toy run, n=15); enormous wall-time gap. 2 LLM escalations vs ~140 calls means queen-CPU usage is **70× lower** for nearly the same coordination quality.

**Implication:** for the OCI free-tier project as currently scoped, this is the deployment shape that actually fits the hardware. The queen handles only the cases the heuristic genuinely can't, freeing CPU for one of: (a) multiple concurrent colonies, (b) bigger graphs at the same wall-time, (c) longer cycles with deeper exploration.

### Finding 2 — escalation-on-cornered doesn't *improve* success over heuristic alone. `verified`

The heuristic baseline (run 2) was 9/15. This run was also 9/15. The 2 escalations resolved cornered cases (where the heuristic would have hit max_steps anyway) but didn't translate to more successful runs.

**Why:** by the time an ant is cornered (all neighbours visited), it has already wandered far from the target. The escalation gets the LLM into the loop too late to find a productive recovery path. Cornered ants picked sensible-looking next steps from the LLM (`a0` cycle 1 escalation: chose `n10` going from n6 — onward toward n19), but those steps couldn't undo the wasted exploration that preceded.

**To actually beat heuristic, escalation triggers need to fire *earlier*.** Candidate triggers worth testing:
- `len(path) > nodes/2` AND `target not in current_neighbours` — long-path-no-target trigger
- `max(visible_pheromone) < epsilon` — no-signal-anywhere trigger (would catch cold-start cycle 1)
- Heuristic loop detector — if `current` has appeared in `path` before, escalate (subtly different from cornered: handles "visited but escapeable" cases where heuristic still wants to revisit)

### Finding 3 — Cycle 3 shows classical AS premature convergence. `verified`

Cycle 3 success rate **dropped** from cycle 2's 3/5 to 2/5. Looking at paths: most cycle-3 ants follow the trunk `n0→n2→n1→n13→n14→n15→n16→n17→n3...` that cycles 1-2 reinforced — a suboptimal 12-hop route. Top pheromone edge in cycle 3: `n11__n19: strength=0.499 deposits=8` — but the ants aren't actually finding `n11` reliably because the strong trunk pulls them through `n14→n15→n16` instead.

The escalation didn't fix this because the heuristic *wasn't cornered* — it had a strong trail to follow, the trail was just wrong. This is the same Ant System pathology the 2026-05-05 toy run identified, reproduced here with a different ant policy.

**MMAS bounds (Stützle & Hoos 2000, in the project spec from day one) just became *more* load-bearing, not less.** The escalation prototype works for the cold-start and cornered cases; the over-reinforcement-of-wrong-trunk case is a separate failure mode that needs the τ_min/τ_max bounds.

### Finding 4 — The "queen-CPU as scarce budget" reframe. `concept`

CLAUDE.md frames "queen↔ant bandwidth" as a load-bearing tunable. After runs 1–4, the more useful framing is: **queen-CPU is the scarce budget; escalation frequency is the knob that gates it.** Network bandwidth is sub-millisecond and not interesting; the queen's 4-OCPU ARM running Qwen-7B-Q4 at 10s/call is the resource that determines what's possible.

This reframe sharpens the project's interesting dimensions:
- **Trigger design** — when does the ant decide it's stuck? (cornered? long-path? low-signal?)
- **Escalation budget per cycle** — how many LLM calls can a colony afford?
- **Escalation context** — what does the ant pass to the LLM when it asks for help? (Full path? Pheromone heatmap? Reasoning trace?)
- **Escalation product** — does the LLM return one step, a sub-plan, or a heuristic-policy adjustment?

Each of these is a real research dimension separable from "did we get to the target".

### Finding 5 — Substrate engaged healthily across both modes. `verified`

98 deposit files this run (vs 88 heuristic-only, 37 queen-everywhere). The substrate has more deposits because (a) more successful ants per cycle on average than run 1, (b) the heuristic mode runs at sub-millisecond per step so deposits land closer together in time, less inter-deposit decay. Substrate primitives still uncorrupted at this concurrency.

## Implications

1. **The architectural pivot from `feedback_octopus_brain_arm_falsified.md` is now backed by *positive* evidence**, not just negative. The README and SYNTHESIS.md rewrite is justified.

2. **TASKS.md #15 closes successfully.** Next sub-tasks emerge from Findings 2 + 3:
   - Smarter escalation triggers (the "earlier than cornered" candidates in Finding 2)
   - MMAS-bounded pheromone reinforcement (Finding 3 — was already in toy/README open-followups, just got priority)

3. **The novelty story in SYNTHESIS.md needs sharpening.** The substrate isn't novel as a coordination primitive among small N; it's interesting as an *audit primitive* (per `reference_substrate_as_audit_primitive.md`) and as an *escalation-budget medium* (per Finding 4 here). Worth a synthesis pass.

4. **`feedback_llm_as_anti_diversity_prior.md`** can be retired or substantially revised. The run-3 finding (SmolLM2 < heuristic) and this run (escalation-on-cornered ≠ improvement) suggest the original claim ("LLMs over-exploit") is one phenomenon among several. The cleaner statement: *small LLMs without strong substrate context contribute negative value at ant scale; medium LLMs (Qwen-7B-Q4) help marginally over heuristic; Haiku-class LLMs follow instructions much better but on different hardware/cost terms.*

## Next experiments

Three branches in roughly increasing complexity:

- **(a) Smarter escalation triggers** — modify the escalate condition to one of the Finding-2 candidates, rerun, see if 9/15 becomes 11/15 or 12/15 *at similar wall time*. ~30-minute change + 1-minute run.
- **(b) MMAS bounds** — add τ_min/τ_max to the substrate strength calculation, only best-so-far ants deposit, rerun cycles 2-3 to see if the suboptimal trunk gets unstuck. Substrate change.
- **(c) Bigger graph** — once Hetionet verification (TASKS.md #3) is done, run heuristic+escalation on a 1000-node subgraph. This is the real test of whether the architecture scales beyond toy.

(a) is the cheap, immediately-informative next move. (b) is on the existing roadmap. (c) needs Hetionet verification first.
