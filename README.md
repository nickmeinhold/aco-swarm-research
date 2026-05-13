# ACO Swarm Research

> *Can a swarm of LLMs forage for drug repurposing leads through pheromone trails on a filesystem?*

An experimental research project at the intersection of:

- **Ant Colony Optimization** (Dorigo, 1992) — biologically-inspired metaheuristic where simple agents coordinate through chemical traces in a shared environment
- **Heuristic ants + sparse LLM escalation** — ants run cheap ε-greedy pheromone-following by default; only call the queen LLM (Qwen-7B-Q4) when stuck (cornered, or wandering far from target). On the toy this matches Qwen-on-every-step quality at 2.4× speedup; the LLM's load-bearing role is **seeding the substrate during cold-start**, not deciding each step. *(This is the architecture as of 2026-05-13 — see Status below for what changed and why.)*
- **The whole colony lives on Oracle Cloud's perpetual-free tier** — 1 × ARM Ampere A1 (24 GB, 4 OCPU) as the Qwen-7B-Q4 queen + up to 2 × AMD x86 micros (1/8 OCPU, 1 GB each) as ant hosts running heuristic + substrate I/O. The load-bearing tunable turns out to be **escalation frequency**, not network bandwidth.
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

## Status (2026-05-13)

**End-to-end OCI deployment exercised.** Five-way comparison on a 20-node ER+chain toy graph, source → target with 5 ants × 3 cycles:

| Backend | Success | Wall | LLM calls |
|---|---|---|---|
| Heuristic ε-greedy | 9/15 | 0.68s | 0 |
| **Heuristic + smart escalation (this design)** | **11/15** | **10m16s** | **43** |
| Qwen-7B-Q4 on every step (via queen) | 11/15 | 24m34s | ~140 |
| SmolLM2-360M-Q4 on every step (ant-local) | 3/15 | 28m49s | ~186 |
| Haiku 4.5 via API (earlier laptop run) | 15/15 | ~30s | ~140 |

Per-run logs and ledger-tagged findings in [`toy/runs/`](toy/runs/).

**Falsified at toy scale:** SmolLM2-on-ants. The original spec had small LLMs running on the AMD micros; their 1/8 OCPU x86 cores can't run *any* LLM at ant-step rates that beat heuristic. SmolLM2-360M-Q4 was Pareto-dominated by both heuristic (cheaper *and* better) and queen-Qwen (better, same wall).

**Validated at toy scale:** **heuristic + smart escalation.** Heuristic by default; LLM call only when (a) all neighbours visited, or (b) `len(path) >= 0.6 × max_steps` and target not adjacent. Matches Qwen-everywhere success at 2.4× speedup and 3.3× fewer LLM calls. The +2/15 win over pure heuristic is concentrated in **cycle 1 cold-start** (5/5 vs heuristic's 3/5) — LLM escalations seed the substrate with useful pheromone trails that later cycles' heuristic ants follow with zero escalations. The mental model is **"LLM-as-substrate-seeder"**, not "LLM-as-ant".

Earlier note still applies: the broader novelty intersection in `swarm-research/SYNTHESIS.md` (φ-on-non-edges, dual-objective meta-loop, mycorrhizal markets, …) remains *plausible pending verification*. The headline-experiment design and 6-way novelty conjunction are unchanged by these toy-scale findings; what changed is the deployment shape that makes them empirically tractable.

## Where we're going next

Concrete open lines of work (full descriptions in [`TASKS.md`](TASKS.md)):

- **Step 0** — Claims ledger pass on `SYNTHESIS.md`: tag every headline claim as `verified` / `reported-by-agent` / `speculative` / `experiment-required`. Partially discharged by the ledger-tagged findings in `toy/runs/` and `oci/ANTS.md`; the synthesis-prose inventory pass remains owed.
- **Step 1** — Spawn a meta-loop specialist over DSPy / GEPA / Sakana AI Scientist / AlphaEvolve / FunSearch. *Has anyone shown LLMs-as-ants rewriting their own coordination protocol with measurable self-improvement on the same problem?*
- **Step 2** — Hetionet verification: confirm lithium → ALS is a recoverable held-out edge in v1.0, with sufficient metapaths remaining post-deletion.
- **Step 3** — One-page claim diff vs ACO-ToT, Sherkat 2018, SwarmSys, ReEvo, CodeCRDT, LLM-MABS, AMRO-S, TxGNN. Reviewer-2 prevention.
- ~~**Step 4** — laptop file-stigmergy toy~~ → ✅ substrate primitive verified (2026-05-05); deployment exercised on OCI (2026-05-12 → 2026-05-13). See [`toy/`](toy/) and `toy/runs/`.
- **Step 5 — Sub-plan escalation** (TASKS.md #16) — at escalation point, have the LLM return 3-5 steps as a sub-plan rather than one step. Predicted to push success above 11/15 by recovering the "wandered far" ants that step-by-step couldn't.
- **Step 5 — Escalation budget per ant** (TASKS.md #17) — defensive cap before scaling to bigger graphs where escalation could explode.
- **Step 5 — MMAS bounded reinforcement** (in toy backlog) — `τ_min/τ_max` bounds; best-so-far updates. Relevant for fairness on bigger experiments.
- **Side: φ-on-non-edges canon audit** — verify "frustration pheromone on non-edges" has no prior construct in Dorigo & Stützle 2004 / MMAS / hyper-cube ACO / ACO_R / 2020–2026 surveys. If absent: stand-alone methods contribution.
- **Side: engram self-citation reconciliation** — locate the prior knowledge-graph hole-finding project, determine whether it operationalised anything pheromone-on-absent-relation-like.

If any of these light you up: open an issue, start a discussion, or fork. The `Explore` and the `cage-match` are both welcome.

## Repository layout

```
.
├── README.md                       (you are here)
├── CLAUDE.md                       orientation for AI collaborators
├── TASKS.md                        durable in-repo task list
├── oci/                            deployment record (queen + ant hosts on OCI)
│   ├── QUEEN.md                    nick-mel A1 queen (Qwen-7B-Q4)
│   └── ANTS.md                     ant-1 + ant-2 E2.1.Micro hosts
├── toy/                            local + OCI experimental rig
│   ├── colony.py                   single-file PEP 723 ant colony loop
│   ├── README.md                   the five-way comparison + run index
│   └── runs/                       per-run logs + ledger-tagged findings, dated
└── swarm-research/
    ├── PROTOCOL.md                 substrate rules (deposit format, vocab, budget)
    ├── SYNTHESIS.md                consolidated findings + 2026-05-13 empirical update
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
