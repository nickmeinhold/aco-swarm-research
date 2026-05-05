# Pheromone: aco-classical -> drug-discovery

Two existing ACO-in-drug-discovery threads you must engage with:

1. **PLANTS (Protein-Ligand ANT System)** — Korb et al. 2006/2007 — ACO is the *de facto* swarm-intelligence docking tool, free for academia. ACO ants navigate ligand conformation space; pheromone on conformational moves. If you propose anything ACO-flavoured for docking, PLANTS is the baseline.
2. **PLANTS extension to flexible docking** (Swarm Intel 2007, doi:10.1007/s11721-007-0006-9) — adds receptor flexibility.
3. **Recent (2024-2025)**: BACO for QSAR toxicity feature selection (MDPI Molecules 2025); CA-HACO-LF for drug-target interaction (Sci Rep 2025, doi:10.1038/s41598-025-19593-4); improved ACO for ADMET (PMC11693920, 2024).

White space (none of the above use LLMs):
- LLM ants reasoning about *why* a binding pose is good and depositing pheromone on chemically-meaningful substructures, not just conformations.
- Stigmergic exploration of a molecule-space KG (which molecules to synthesise next?) rather than docking-pose-space.

Engram-style framing: in a KG of (drug, target, mechanism, indication), a "missing edge" with high LLM-ant-pheromone is a drug-repurposing hypothesis. This is novel territory.
