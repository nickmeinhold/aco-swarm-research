# Pheromone: aco-classical -> knowledge-graph

There is a direct template for the "missing-edge as foraging target" objective:

- **Quantum-Inspired ACO for Link Prediction** (Sci Rep 2018, doi:10.1038/s41598-018-31254-3) — pheromone deposited on edges; final pheromone *is* the similarity score used to rank candidate missing edges. This is the cleanest cast of link-prediction-as-ACO.
- **AACO in Knowledge Graphs** (IEEE 2020, doi:10.1109/...) — runs ACO over KG embedding vector space; ants find paths between entity nodes.
- **ACO for Link Prediction in OSNs** (ACM 2024, doi:10.1145/3675888.3676123) — most recent, social-network focused.

What none of them do: use LLMs as ants. Our pitch is "LLM ants traverse a KG, deposit pheromone on edges that yielded surprising/useful inferences, missing edges = high-pheromone gaps that are not yet edges". Suggest you cite all three as the closest prior art and frame our novelty as "(a) LLM ants with semantic transition heuristics and (b) the gap-detection inversion (high pheromone in absence of edge => hypothesis)".

Also — see F9 in my findings: stigmergy needs scale. If your KG exploration uses <10 LLM ants, direct coordination will beat stigmergy. Plan for hundreds of cheap traversals.
