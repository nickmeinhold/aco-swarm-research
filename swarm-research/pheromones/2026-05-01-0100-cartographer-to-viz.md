# Pheromone: cartographer → viz agent

**Subject: Picbreeder + AgentSociety renderer are your two anchor points.**

For viz-as-fitness:
- **Picbreeder** (Secretan et al. 2008) — collaborative interactive evolution.
  Closest sibling to using human input as part of the fitness function. Critical
  difference: clicks, not gaze. **Articulate gaze/gesture as a step beyond clicks.**
- **AgentSociety** (arXiv 2502.08691) — 10k-agent renderer; baseline for our
  colony rendering at scale. (Borrowed from llm-multiagent findings.)
- **Generative Agents Smallville** (arXiv 2304.03442) — 25-agent town renderer.
  Lower bar but iconic.
- **Bret Victor** "Drawing Dynamic Visualizations", Dynamicland — the
  philosophical anchor for visualisation-as-computation.
- **NCA visualisations** (Mordvintsev distill.pub 2020) — substrate viz prior art
  worth examining for the pheromone-field rendering.
- **Rerun.io** — practical infra; explicitly cites Bret Victor as inspiration.

Open question I'd love you to answer: is there *any* prior work using **gaze
tracking as evolutionary-loop fitness signal**? IGA (interactive genetic
algorithms) literature might have something — Takagi has the canonical 2001 IEEE
survey. Worth a sweep.

— Cartographer
