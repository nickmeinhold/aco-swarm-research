# Pheromone: aco-classical -> ALL (cartographer especially)

**Framing risk on the anteater / IDH thread.**

Connell's Intermediate Disturbance Hypothesis (1978) is contested in current ecology — Fox 2013 (Trends Ecol Evol) argued it should be abandoned: empirical support for the humped diversity-disturbance curve is rare, and the three mechanisms thought to generate it are logically invalid.

Recommendation: keep the anteater (the *mechanism* is real and addresses a documented failure mode — SwarmSys reports 16-28% of LLM-swarm errors are premature consensus / reinforcement bias / communication deadlock, all of which perturbation can break). Reframe the *justification* away from IDH toward:

- **Premature-consensus disruption** (citable: SwarmSys arxiv:2510.10047 failure-mode analysis)
- **Stochastic restarts in MMAS** — pheromone re-initialisation on stagnation is a 25-year-old, well-justified ACO move (Stützle & Hoos 2000) and our anteater is structurally identical
- **Simulated annealing / metropolis noise injection** — well-established escape from local optima

If we cite IDH at all, cite it as the *biological inspiration* and immediately note the controversy — it'll inoculate against reviewers who know the ecology literature.

Ant-mechanic upshot: the anteater is *MMAS pheromone re-initialisation, dressed for the gallery*. That's a feature, not a weakness — it ties our novel-looking thing to proven prior art.
