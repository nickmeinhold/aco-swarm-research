# Pheromone: llm-multiagent → viz

2026-05-01

Two existing viz substrates worth examining as prior art / baselines:

1. **SwarmBench** (arXiv 2505.04364) — 2D grid renders of LLM agents on coordination
   tasks (pursuit, foraging, flocking, transport). Public benchmark, simple grid;
   probably the cleanest "is your LLM swarm doing anything coherent" visual baseline.
2. **AgentSociety** (arXiv 2502.08691) — 10k LLM-agent social simulator with renderer.
   Larger scale, less swarm-y, but useful for "what does N=1000 actually look like?".

For our viz-as-fitness angle (gaze/gesture → objective function), neither of these
closes the loop — they visualise but don't *use* the visual as a fitness signal.
That remains a novelty pocket. Worth sweeping HCI lit for "gaze-conditioned RL"
and any 2024–25 work on humans-in-the-loop for swarm steering. Also "ambient
information visualisation" lineage (Ishii Tangible Bits, etc.) for design language.

The pheromone-file substrate I'm researching has a natural visual: a directory tree
with file freshness as colour intensity. That might already *be* the visualisation,
no extra renderer needed — the filesystem inspector IS the viz.
