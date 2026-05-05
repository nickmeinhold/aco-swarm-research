# ACO Swarm Research

> *Can a swarm of LLMs forage for drug repurposing leads through pheromone trails on a filesystem?*

An experimental research project at the intersection of:

- **Ant Colony Optimization** (Dorigo, 1992) — biologically-inspired metaheuristic where simple agents coordinate through chemical traces in a shared environment
- **LLM-as-ant agents** — small local models (Qwen2.5-7B Q4 "queen", SmolLM2-360M "micros") acting as foragers, not oracles
- **The whole colony lives on Oracle Cloud's perpetual-free tier** — 1 × ARM Ampere A1 (24GB RAM, 4 OCPU) as the queen + 4 × AMD x86 micros (1GB each) as the ant fleet, no credit card expiring on you. Heterogeneous compute is a feature: the queen↔micro bandwidth cap is the "octopus brain ↔ arm" tunable knob the experiment is designed around.
- **File-based stigmergy** — the substrate is the OS itself: directory = topology, `mtime` = pheromone strength, `touch`/`rm` = reinforce/evaporate
- **Knowledge-graph hole-finding** — depositing pheromone on *non-edges* the colony wishes existed, operationalising Burt's structural-holes theory
- **Drug repurposing as the demo target** — recovering held-out edges in [Hetionet](https://het.io) (lithium → ALS, sildenafil → PAH, …)
- **Adversarial perturbation as first-class methodology** — six "anteaters" (Eraser, Forger, Predator, Flooder, Infector, Mirage) each isolating one robustness axis
- **Humans-as-co-located-ants** — gaze and cursor as deposit signals on the same substrate, not external oracles

## The shape of the bet

There are crowded prior works on each leg individually (ACO for KG link prediction; LLM swarms; stigmergic multi-agent systems). The bet is that the **conjunction** is genuinely novel — and that file-based persistent stigmergy on heterogeneous compute is qualitatively different from the in-memory pheromone matrices everyone has tried.

We don't know yet. That's the experiment.

## The substrate is the project

The research **method** matches the research **subject**: this repo's `swarm-research/` directory was itself produced by a 9-agent stigmergic LLM swarm researching its own viability. The swarm self-corrected mid-flight (the cartographer broadcast a REDIRECT pheromone when the original Connell-IDH framing turned out to be contested in current ecology), which is the strongest evidence we have so far that file-based pheromone signals work as a coordination primitive at small N.

So the artifacts in `swarm-research/findings/` and `swarm-research/pheromones/` aren't a writeup of a swarm — they **are** a swarm's outputs, including its mistakes, redirects, and emergent compositions across agents that never talked directly.

## Status

Early-stage. The synthesis on disk (`swarm-research/SYNTHESIS.md`) reads more confidently than its evidence currently supports — this is documented as the project's first operating-discipline finding ("premature crystallization") and the next session's first task is a **claims ledger** that tags every headline claim as `verified` / `reported-by-agent` / `speculative` / `experiment-required`.

What this means for a reader: the questions are real, the substrate is built, the headline experiment is well-defined, and the prior-art reconnaissance is broad. The novelty intersection is *plausible pending verification*, not confirmed.

## Repository layout

```
.
├── README.md                       (you are here)
├── CLAUDE.md                       orientation for AI collaborators
└── swarm-research/
    ├── PROTOCOL.md                 substrate rules (deposit format, vocab, budget)
    ├── SYNTHESIS.md                consolidated findings (over-confident — see ledger TODO)
    ├── territory.md                cartographer's map of the research space
    ├── findings/                   9 specialist agent reports (one per leg of the bet)
    └── pheromones/                 raw deposit log (the swarm's actual coordination signal)
```

## Headline experiment (planned)

A 2D phase diagram across **anteater frequency × evaporation rate**, locating the optimum for [MMAS](https://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms#Max-min_ant_system) pheromone re-initialisation. Substrate: Hetionet v1.0 (47k nodes, 2.25M edges). Demo: recover held-out lithium → ALS edge from Project Rephetio's 700 indications. Baseline to beat: TxGNN ([Huang & Zitnik, *Nat Med* 2024](https://doi.org/10.1038/s41591-024-03233-x)).

## Headline visualisation (planned)

A wall-sized 50k-paper constellation rendered in [cosmos.gl](https://cosmograph.app/) + [deck.gl](https://deck.gl/) with GLSL ping-pong FBO for the pheromone field (Sage Jenson / Jones 2010 model — the same maths used to [map dark matter filaments](https://www.nature.com/articles/s41550-019-0967-9)). Glowing ant traces forge connections; your gaze brightens trails; an anteater wave erases a section; the colony reforms.

You're not watching it; you're feeding it.

## Collaboration shape

This project is a Nick + Claude collaboration. The swarm in `swarm-research/` is composed of specialist Claude subagents coordinating through the file substrate. The project's operating-discipline lessons (premature crystallization, synthesis-to-disk, appetite-vs-guardrails) are themselves part of the research output — captured as feedback in the auto-memory system and surfaced here as evidence that the human-AI research loop has its own failure modes worth documenting.

## Acknowledgements

Standing on shoulders: Dorigo & Stützle on ACO; Himmelstein et al. on Hetionet & DWPC; Burt on structural holes; Robinson on anti-pheromone; Kiers on mycorrhizal markets; Pineda et al. on antifragility; ReEvo / Sakana AI Scientist on self-improving LLM systems; the cartographer's REDIRECT pheromone, which saved us from a contested-IDH framing before adversarial committed.

---

*If any of this lights you up, open an issue or just fork and run — the substrate is meant to be touched.*
