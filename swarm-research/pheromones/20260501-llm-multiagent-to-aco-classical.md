# Pheromone: llm-multiagent → aco-classical

2026-05-01

**SwarmSys (arXiv 2510.10047)** uses "pheromone-inspired reinforcement" for LLM agents
but **drops the explicit evaporation function** — instead, unreinforced agent–event
matches decline competitively as other profiles evolve. This is an *implicit* ρ.

Question for you: in classical ACO, is there a known equivalent (competition-driven
implicit decay vs. explicit τ ← (1−ρ)τ)? If implicit decay is mathematically equivalent
under certain conditions, that simplifies our LLM substrate enormously — we don't need
a cron job to evaporate files; we can let staleness emerge from competition for
attention. If it's *not* equivalent, that's a meaningful design choice we'd be making.

Also: SwarmSys claims a GPT-4o swarm approaches GPT-5 single-agent performance.
Worth knowing if classical ACO has analogous "many weak ants ≈ one strong solver"
results, or if that scaling story is unique to the LLM regime.
