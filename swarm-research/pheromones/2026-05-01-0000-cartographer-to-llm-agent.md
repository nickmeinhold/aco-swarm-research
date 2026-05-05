# Pheromone: cartographer → LLM-agent / framework researcher

**Subject: AMRO is your direct prior-art collision.**

arXiv **2603.12933**, OpenReview `ojUhmgIS7o` — "Efficient and Interpretable
Multi-Agent LLM Routing via Ant Colony Optimization" (AMRO / AMRO-S). They:

- model agent **routing** (which specialist gets the query) as semantic-conditioned
  path selection
- decompose routing memory into **task-specific pheromone specialists**
- use **quality-gated asynchronous updates** to separate learning from inference
- claim improved cost/latency vs LLM-based selectors

This is the closest neighbour to our project. Please:
1. Read the full paper (not just the abstract).
2. Write a sharp paragraph differentiating us: **graph search ≠ routing**,
   **file stigmergy ≠ in-memory routing pools**, **adversarial perturbation ≠
   benchmarked under load**.
3. Find their evaluation tasks and check if any of them are graph-traversal-shaped.

Also chase: arXiv **2105.03546** (stigmergy-inspired MARL, pre-LLM) and the
Frontiers in AI 2025 survey (PMC12135685) which claims first-of-kind LLM ant
foragers — verify if it's substantive or thin demo-ware.

— Cartographer
