# `toy/` — minimal file-based stigmergy substrate test

**Task #5** from [`TASKS.md`](../TASKS.md): does file-based persistent stigmergy behave qualitatively differently from in-memory pheromone matrices?

This is the smallest viable demonstration:

- Synthetic ER+chain knowledge graph, ~20 nodes
- 5 ants × 3 cycles, async-concurrent within a cycle
- File-based pheromone deposits — each deposit is a `.dep` JSON file with `(agent_id, edge, quality, timestamp, signature)`
- Decay-weighted strength: `strength(edge) = Σᵢ qualityᵢ · exp(-(now - tsᵢ) / TAU)`
- Two ant policies behind a flag: `--mock` heuristic ε-greedy, default LLM (Haiku 4.5 via Anthropic API with cached system prompt)
- Per-edge `evaporator()` deletes deposits older than `max_age_sec` (default 600s)

## Run

```bash
# heuristic ants — substrate plumbing test, no API calls
uv run colony.py --mock --reset

# Haiku 4.5 ants (default LLM backend)
export ANTHROPIC_API_KEY=...    # or: $(gcloud secrets versions access latest --secret=ANTHROPIC_API_KEY --project=adventures-in-tech-world-0)
uv run colony.py --reset

# ollama backend (any HTTP-compatible ollama instance)
# - From ant-1 against queen via private VCN (10.0.0.4:11434, OCI deployment):
uv run colony.py --queen --reset
# - Against a local ollama with a different model:
uv run colony.py --queen --queen-url http://localhost:11434 --queen-model smollm2:360m-instruct-q4_K_M --reset

# tweak
uv run colony.py --ants 8 --cycles 5 --nodes 30 --max-steps 15
```

## First-run findings (2026-05-05)

**Substrate primitive works at small N**: 5 async-concurrent ants per cycle produced no corruption (118 readable deposit files), strength reads via decay-weighted sum behave correctly, evaporator does its job.

**Convergence is visible** but the *first* convergence target is *not necessarily optimal* — running with Haiku ants on a 20-node graph, the swarm locked onto a suboptimal 10-hop path (`n0→n1→n2→n3→n4→n5→n6→n10→n11→n19`) over the 5-hop alternative (`n0→n1→n2→n18→n19`) that some ants found in early cycles. More ants happened to lay pheromone on the longer route first, and the positive-feedback loop reinforced it.

This is the classical [Ant System](https://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms) premature-convergence pathology that **MMAS** ([Stützle & Hoos 2000](https://doi.org/10.1016/S0167-739X%2800%2900043-1)) was specifically designed to prevent: bounded `[τ_min, τ_max]` reinforcement, only best-so-far ants deposit, and pheromone trail re-initialisation when entropy collapses.

**Tag: `experiment-required`** — this is the kind of result `SYNTHESIS.md`'s claims ledger (Task #7) should reference once it lands.

## Status

Initial substrate primitive verified 2026-05-05. OCI deployment exercised 2026-05-12. See [`runs/`](runs/) for per-run findings (raw logs + ledger-tagged analysis).

Open follow-ups (in rough priority):

- [x] ~~Swap Haiku for local Qwen2.5-7B (via ollama on the `nick-mel` queen)~~ — done 2026-05-12, see `runs/2026-05-12-oci-run-1.md`. Found ~10s per ant-step call (vs 1.09s smoke-test prediction); queen CPU is the bottleneck.
- [x] ~~Visited-filter hardening for soft-instruction failures~~ — done 2026-05-12, see `runs/2026-05-12-oci-run-2-mock.md` for the mock-baseline comparison.
- [ ] SmolLM2-360M on ants — in progress 2026-05-12. Cold-call timing on 1/8-OCPU x86 suggests ant-step prompt-eval at ~10 tps; full results pending in `runs/2026-05-12-oci-run-3-smollm2.md`.
- [ ] Implement MMAS-style bounded reinforcement + best-so-far update; re-run on same graph
- [ ] Stress-test concurrency: 50+ ants writing simultaneously, look for corruption
- [ ] Compare against an in-memory pheromone matrix on the same KG to answer the load-bearing Task #5 question quantitatively
- [ ] Try a real KG (Hetionet subset, 1000+ nodes) once Task #3 (Hetionet verification) lands

## File structure

```
toy/
├── colony.py        # single-file PEP 723 script: KG, substrate, ants, colony loop
├── data/
│   └── pheromones/  # the substrate (gitignored — runtime artifact)
├── runs/            # per-run logs + ledger-tagged findings, dated
│   ├── 2026-05-12-oci-run-1.{log,md}        # Qwen-7B-Q4 via queen private VCN
│   ├── 2026-05-12-oci-run-2-mock.{log,md}   # heuristic ε-greedy on ant-1
│   └── 2026-05-12-oci-run-3-smollm2.{log,md} # SmolLM2-360M Q4 local on ant-1
├── README.md        # this file
└── .gitignore
```
