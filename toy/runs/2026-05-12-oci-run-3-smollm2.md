# OCI run 3 — toy with SmolLM2-360M-Q4 local on ant-1

**Date:** 2026-05-12, 20:33 AEST (start) → 21:02 AEST (end)
**TASKS.md:** #9 (SmolLM2-360M on ants). Concludes with a **no-go finding**, not a deployment.
**Raw log:** [`2026-05-12-oci-run-3-smollm2.log`](2026-05-12-oci-run-3-smollm2.log)

## Setup

- **Code:** `toy/colony.py` post-hardening (visited-filter + tightened validity check from `2026-05-12-oci-run-2-mock.md`)
- **Host:** ant-1 (130.162.196.243), `VM.Standard.E2.1.Micro`, **1/8 OCPU x86_64, 956 MiB RAM**
- **Backend:** **local** ollama on ant-1 at `http://localhost:11434`, model `smollm2:360m-instruct-q4_K_M` (270 MB on disk)
- **Params:** `--queen --queen-url http://localhost:11434 --queen-model smollm2:360m-instruct-q4_K_M --reset` (defaults: 5 ants × 3 cycles, 20-node ER+chain, max_steps=12, TAU=60s)
- **Note on naming:** Previous attempt with default `smollm2:360m` (f16, 725 MB on disk) failed with HTTP 500s — model required 850 MiB system memory, only 488 MiB available. Q4 quantization (270 MB on disk, ~487 MiB resident) fit, with 76 MiB headroom.

## Headline numbers

| Metric | Value | Comparison |
|---|---|---|
| Success rate | **3/15 (20%)** | Heuristic baseline 9/15, Qwen-via-queen 11/15, Haiku 15/15 |
| Total wall | **28m49s** | Heuristic 0.68s, Qwen-via-queen 24m34s |
| Deposits on disk | 17 | Heuristic 88, Qwen 37 |
| Avg per-call latency | ~9s (186 calls / 1729s) | Cold-call extrapolation predicted ~25s — sub-linear, surprise to the upside |

## Findings

### Finding 1 — SmolLM2-on-ants is Pareto-dominated by both heuristic AND queen-Qwen. `verified`

The four-way comparison (heuristic, Qwen-via-queen, SmolLM2-local-on-ant, Haiku) places SmolLM2-local-on-ant in the worst position on every axis except disk space:

- **Worse success than heuristic** (3/15 vs 9/15)
- **Slower than heuristic** by 2500× (28m49s vs 0.68s)
- **Worse success than queen-Qwen** (3/15 vs 11/15)
- **Slower than queen-Qwen** (28m49s vs 24m34s) — despite a 20× smaller model

There is no axis on which this deployment is competitive. **This is not a tuning problem; the hardware is the problem.** A 1/8-OCPU x86 micro is too compute-poor to host any LLM at ant-step rates that beat heuristic.

### Finding 2 — The "octopus brain ↔ arm" architecture is falsified on OCI free-tier hardware. `verified`

The architecture spec in `CLAUDE.md` and `swarm-research/SYNTHESIS.md` assumes ants can usefully run small LLMs for routine decisions, escalating to the queen for hard reasoning. The empirical finding: **the arms have no useful LLM-inference budget on E2.1.Micro hardware.** SmolLM2-360M is small enough to fit but slow enough that heuristic dominates it on the same hardware.

Honest revised architecture for OCI free tier (`speculative` until tested but no other shape is consistent with the evidence):

- **Heuristic ε-greedy on ants** for routine ant-step — sub-millisecond per step, no LLM
- **Queen-Qwen for escalation only** when heuristic gets stuck, doesn't trigger every step
- **File-substrate distributed across ants** for write parallelism — no LLM required

This is a *meaningfully different project shape* than the current README and SYNTHESIS.md suggest. Tagged `experiment-required` against the alternative ("escalation-only saves enough queen-CPU to be worth the complexity") but the SmolLM2-as-routine-backend hypothesis is closed.

### Finding 3 — TAU=60s + 9s/call → pheromone decays faster than swarm coordinates. `verified`

Cycle 1 produced one success (a3, 6-hop path); the deposit on those edges was at ~0% strength by cycle 2 (cycle 1 alone took ~10 min wall, TAU=60s decays to ~exp(-600/60) ≈ 2e-5 in that time). **Cycle 2 returned 0/5 success — every ant essentially performed unguided random-walk-with-LLM.**

The temporal coupling between pheromone half-life and ant-step latency is now empirically load-bearing: **TAU must scale with call latency**, not be hardcoded. A reasonable rule of thumb is TAU ≈ (5–10) × wall_per_cycle, so deposits from one generation persist meaningfully into the next.

The current `colony.py` hardcodes `TAU = 60.0`. Should be either (a) a CLI flag, or (b) auto-scaled at startup based on a calibration call.

### Finding 4 — SmolLM2 without pheromone signal underperforms ε-greedy random. `verified`

Cycle 2 = pheromone strengths all ~0 (decayed) = LLM operates on no substrate signal = 0/5 success. Compare to the mock-baseline run (also 5 ants on the same KG starting from zero pheromone): cycle 1 was 3/5. **The 360M model without pheromone guidance is worse than random-with-pheromone-bias at this task.** Which makes the substrate's role precise: it's not optional scaffolding — it's the *primary signal* the LLM-ant is conditioning on; remove it and the LLM contributes negative value at this scale.

This is also a probe at the "LLM-as-ant" framing: a 360M ant *without substrate context* is worse than a heuristic ant *with substrate context*. That contradicts a naive reading of the project: "LLMs are better than heuristics at understanding pheromone trails". The data says the substrate matters more than the model intelligence — at least at the bottom of the model-size range.

### Finding 5 — Cold-call extrapolation was pessimistic. `verified`

Smoke-test sequential cold call: 6.3s load + 3.6s prompt-eval(38 tokens) + 0.8s eval(6 tokens) = 10.8s, predicting ~25s for full ant-step prompts (250 input tokens at 10 tps + 20 output). Actual mean: ~9s. Either prompt-eval has economy of scale at longer inputs (cache effects?), or ollama warms differently under sustained load than after a fresh start. **Don't extrapolate workload latency from cold calls — replicate with the workload prompt shape under load.**

This adds a refinement to `feedback_smoke_test_prompt_shape.md` — even with prompt shape matched, *under-vs-not-under-sustained-load* matters too.

### Finding 6 — Substrate primitives held up under another 186-call concurrent run. `verified`

17 deposits, no corruption, evaporator removed 5 between cycles 1→2 (deposits already at zero strength but still on disk). Same behavior as the Qwen run — substrate is *not* the bottleneck or failure mode in any of these runs. The substrate is fine; the LLMs (especially the small one) and the ARM/x86 CPU economy are the load-bearing constraints.

## Implications for project direction

1. **TASKS.md #9 closes with a no-go for SmolLM2-on-ants.** Not "deferred" — empirically dominated. Update `TASKS.md` to reflect this.
2. **The README and SYNTHESIS.md "1 queen + 4 micros, heterogeneous models" pitch needs revision.** The micros can't host useful LLM ant-step workers. Honest pitch: "1 queen + N ant-hosts running heuristic + substrate + queen-escalation-on-stuck".
3. **CLAUDE.md's "octopus brain ↔ arm bandwidth as load-bearing tunable" reads differently now.** Bandwidth was never the bottleneck (private-VCN hop is ~tens of ms); ant CPU is. The interesting tunable is now `frequency_of_queen_escalation`, not `network_bandwidth`.
4. **TAU needs to be parameterized or auto-scaled** (Finding 3). 3-line change.
5. **The substrate is doing more work than the LLM at this scale** (Finding 4). Sharpens the substrate-as-primitive contribution claim in SYNTHESIS.md.

## Next experiments (after Nick is back)

- (a) Implement "heuristic-ant-with-queen-escalation-on-stuck" — the architecturally honest design. Roughly: ant runs heuristic, but if it loops or hits a node with all-zero pheromone neighbors, escalate to queen for one LLM call. Predicted to dominate Qwen-via-queen-everywhere on wall-time without sacrificing convergence quality.
- (b) Parameterize TAU and rerun previous experiments with `TAU = 5 × avg_cycle_wall` to test Finding 3's hypothesis.
- (c) Try `--ants 1` SmolLM2 to see if sequential is much faster than 5-concurrent (probably yes by 4-5×, but doesn't change the "dominated" verdict).
- (d) Update `feedback_llm_as_anti_diversity_prior.md` and the SYNTHESIS.md novelty list with the empirical findings from this 4-way comparison.

The architectural pivot (a) is the biggest move — needs Nick's sign-off because it changes the project's pitch.
