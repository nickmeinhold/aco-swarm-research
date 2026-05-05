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

# Haiku 4.5 ants
export ANTHROPIC_API_KEY=...    # or: $(gcloud secrets versions access latest --secret=ANTHROPIC_API_KEY --project=adventures-in-tech-world-0)
uv run colony.py --reset

# tweak
uv run colony.py --ants 8 --cycles 5 --nodes 30 --max-steps 15
```

## First-run findings (2026-05-05)

**Substrate primitive works at small N**: 5 async-concurrent ants per cycle produced no corruption (118 readable deposit files), strength reads via decay-weighted sum behave correctly, evaporator does its job.

**Convergence is visible** but the *first* convergence target is *not necessarily optimal* — running with Haiku ants on a 20-node graph, the swarm locked onto a suboptimal 10-hop path (`n0→n1→n2→n3→n4→n5→n6→n10→n11→n19`) over the 5-hop alternative (`n0→n1→n2→n18→n19`) that some ants found in early cycles. More ants happened to lay pheromone on the longer route first, and the positive-feedback loop reinforced it.

This is the classical [Ant System](https://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms) premature-convergence pathology that **MMAS** ([Stützle & Hoos 2000](https://doi.org/10.1016/S0167-739X%2800%2900043-1)) was specifically designed to prevent: bounded `[τ_min, τ_max]` reinforcement, only best-so-far ants deposit, and pheromone trail re-initialisation when entropy collapses.

**Tag: `experiment-required`** — this is the kind of result `SYNTHESIS.md`'s claims ledger (Task #7) should reference once it lands.

## Status

Initial substrate primitive verified. Open follow-ups (in rough priority):

- [ ] Implement MMAS-style bounded reinforcement + best-so-far update; re-run on same graph
- [ ] Stress-test concurrency: 50+ ants writing simultaneously, look for corruption
- [ ] Compare against an in-memory pheromone matrix on the same KG to answer the load-bearing Task #5 question quantitatively
- [ ] Swap Haiku for local Qwen2.5-7B (via ollama on the `nick-mel` queen, since that's the project's deployment target)
- [ ] Try a real KG (Hetionet subset, 1000+ nodes) once Task #4 (Hetionet verification) lands

## File structure

```
toy/
├── colony.py        # single-file PEP 723 script: KG, substrate, ants, colony loop
├── data/
│   └── pheromones/  # the substrate (gitignored — runtime artifact)
├── README.md        # this file
└── .gitignore
```
