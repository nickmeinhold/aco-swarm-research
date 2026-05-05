# ACO-Classical Specialist — Findings

Agent: aco-classical | Started: 2026-05-01

## Cycle 1 — Prior LLM-as-ant work (CRITICAL for novelty assessment)

### F1. ACO-ToT (Jan 2025) — closest existing work to our project
"Pheromone-based Learning of Optimal Reasoning Paths" — arxiv:2501.19278
- Five fine-tuned Llama-70B "ants" (math/sci/logic/commonsense/domain experts) traverse a Tree-of-Thought graph.
- Pheromone on edges; standard ACS-style transition rule p_ij = (tau^a)(eta^b) / sum.
- Path quality = 0.4 semantic coherence + 0.3 length penalty + 0.3 MoE consensus.
- Results: GSM8K 84.2% (vs 55.6% CoT), ARC-C 88.9%, MATH 22.6%. +16.6% mean.
- Authors explicitly draw Hebbian analogy.
- **Limitations they admit**: compute cost, manual expert specification, heavy expert-diversity dependence.
- **White space they leave**: no adversarial perturbation, no self-modifying coordination rules, no embodied/file-based stigmergy, single problem class (reasoning), no meta-loop.

### F2. AMRO-S (Mar 2026) — ACO for routing among LLM agents
"Efficient and Interpretable Multi-Agent LLM Routing via ACO" — arxiv:2603.12933
- Decomposes routing memory into "task-specific pheromone specialists" (one pheromone matrix per workload type — interesting move; avoids interference).
- Quality-gated asynchronous pheromone update.
- Small fine-tuned LM does intent classification (cheap), ACO does the routing.
- Solves the "router LLM is expensive" problem; not really "LLM-as-ant", more "ACO-as-router-of-LLMs".

### F3. SwarmSys (Oct 2025) — implicit pheromones via embedding updates
arxiv:2510.10047
- Pheromones = embedding updates on agent-event compatibility scores (no explicit chemical metaphor).
- Roles: Explorer / Worker / Validator. Debate-consensus cycles.
- "GPT-4o swarm approaches GPT-5 performance — scaling coordination substitutes for model scaling." (BIG claim if true.)
- Failure modes documented (16-28% of errors): premature consensus, reinforcement bias, communication deadlock — these are exactly the dynamics our anteater perturbation should counteract.
- Gap: text-only, no embodiment, reasoning-only.

### F4. ReEvo (Feb 2024) — LLM as heuristic-DESIGNER for ACO, not as ant
arxiv:2402.01145. Generator+Reflector LLMs evolve heuristic code; ACO runs underneath as the mechanism. Tested on TSP, CVRP, OP, MKP, BPP, DPP. **Important distinction**: this is "LLM writes the heuristic that the ants use", not "LLM IS the ant". Our project flips this — and could combine both (LLMs as ants + ReEvo-style meta-loop rewriting their own coordination rules — that IS our meta-objective).

### F5. GPTSwarm (precursor, 2024)
Graph-based optimization over agent graphs with stigmergic feedback signals. SwarmSys reports beating it by +12.5% accuracy on exam tasks. Worth deeper read — it's the prior art that established "agent graph + stigmergy" as a paradigm.

## Novelty assessment so far
- **NOT novel**: pheromone-on-edges with LLMs (ACO-ToT did it), embedding-based stigmergy (SwarmSys), LLM-designed ACO heuristics (ReEvo), ACO-routing-of-LLMs (AMRO-S).
- **NOVEL territory we still own**:
  1. **File-based stigmergy on actual disk** (not in-memory matrices) — closer to true stigmergy of biological systems (environmental modification persists across agent deaths).
  2. **Heterogeneous compute substrate** (queen + micro-ants on cheap nodes mirroring ant-castes — physical, not just role-based).
  3. **Adversarial anteater** with intermediate-disturbance theory as first-class methodology — nobody is doing perturbation-as-research-method.
  4. **Dual-objective meta-loop** (colony researches its own algorithm). ReEvo touches this but on heuristics-only, not on full coordination protocol.
  5. **Visualisation-as-fitness** with human-in-the-loop gaze/gesture — fully NOVEL.
  6. **Knowledge-graph hole-finding as the foraging objective** — TSP/reasoning are done; KG missing-edge prediction via stigmergic exploration appears unexplored.

## Cycle 2 — Classical ACO theory (the load-bearing math)

### F6. Convergence proofs — what's actually proven (Dorigo & Stützle 2002, IEEE TEC 6(4):358-365)
"A short convergence proof for a class of ACO algorithms" covers ACS and MMAS.
- **Theorem 1 (convergence in value)**: P(finding optimal solution at least once) -> 1 as t -> infinity. WEAK guarantee — says nothing about runtime.
- **Theorem 2 (convergence in solution)**: pheromone trails on the optimal solution edges become arbitrarily larger than on any other edges. STRONG-ER guarantee — algorithm "locks on" to optimum.
- **Required conditions**: pheromone has a strictly positive lower bound `tau_min > 0` (this is exactly why MMAS exists — AS doesn't guarantee this). Best-so-far reinforcement (or iteration-best with sufficient noise).
- **Gutjahr 2000** ("A graph-based ant system and its convergence", FGCS 16:873-888) was the FIRST convergence-in-value proof — for "Graph-Based Ant System" (GBAS), which is closer to what we're building than TSP-AS.
- **What is NOT proven**: any useful runtime bound. ACO's empirical success >>> its theoretical guarantees. This is honest to flag.

### F7. Pheromone update rules — the variants that matter
- **AS (Ant System, Dorigo 1992)**: tau_ij <- (1-rho)*tau_ij + sum_k Delta_tau_ij^k. All ants deposit. Simple, no convergence proof.
- **EAS (Elitist AS)**: AS + extra deposit by best-so-far ant scaled by `e`. Faster convergence, risk of stagnation.
- **AS-rank (Bullnheimer et al. 1999)**: only the top-w ants deposit, weighted by rank. Trade-off between elitism and diversity.
- **MMAS (Stützle & Hoos 2000)**: bounds `tau_min <= tau <= tau_max` enforced. Only iteration-best (or best-so-far) deposits. Re-initialise to tau_max on stagnation. **The variant with convergence-in-solution.**
- **ACS (Dorigo & Gambardella 1997)**: pseudo-random-proportional rule (q0 parameter for pure exploitation), local pheromone update during construction (lessens the just-used edge to encourage diversity), global update only by best-so-far. Convergence-in-value proven.
- **Modern (2024)**: self-adaptive rho (evaporation rate adapts to stagnation/diversity signals); hybrid ACO+SA, ACO+sparrow-search for better init.

### F8. Knowledge-graph ACO (foundation for our drug-discovery / paper-discovery objective)
- Quantum-Inspired ACO for Link Prediction (Sci Rep 2018, doi:10.1038/s41598-018-31254-3) — pheromone-on-edges with quantum superposition state per ant; results outperform classic similarity-based link prediction on standard social network datasets.
- AACO (Adaptive ACO in Knowledge Graphs, IEEE 2020) — operates in KG embedding vector space; ants find paths between entity nodes.
- Online social network link prediction with ACO (ACM 2024) — pheromone on edge becomes the similarity score for ranking missing links. **Direct template for our missing-edge KG objective.**
- Drug discovery: PLANTS (2006) is the gold-standard ACO docking tool. BACO (2025) for QSAR feature selection. CA-HACO-LF (2025) for drug-target interaction. None use LLM ants.

### F9. Stigmergy in robotics — the scaling rule
- "Stigmergy pays off with scale; under ~10 agents the mechanism overhead is pure cost." (Codebolt synthesis, but consistent with sigma-stigmergy literature.)
- **Implication for our project**: the 9-agent research swarm is at the threshold; the actual production ACO needs >>10 ants for stigmergy to beat direct messaging. Our queen+micros architecture should plan for hundreds-to-thousands of lightweight LLM-ant invocations, not tens.
- "Testing the limits of pheromone stigmergy in high-density robot swarms" (Royal Soc Open Sci 2019) — at very high densities pheromone fields saturate and information value collapses. Calibration: there's a sweet-spot density for any pheromone substrate.

### F10. The intermediate-disturbance hypothesis is contested — IMPORTANT for project framing
- Fox 2013 ("The intermediate disturbance hypothesis should be abandoned", Trends Ecol Evol) argues the three classic mechanisms generating the humped curve are LOGICALLY INVALID, and empirical support is rare.
- **Bullshit detection flag**: citing Connell 1978 IDH as project justification is risky — the field has moved on. We should reframe the anteater perturbation as **noise injection / metastability disruption / schema-jolt** rather than IDH. The mechanism is real (perturbation breaks premature consensus — see SwarmSys's documented 16-28% premature-consensus failure rate); the IDH branding is dated.

## Cycle 3 — Top open questions
1. **Does pheromone-as-file (truly persistent, asynchronous, lossy) behave qualitatively differently from pheromone-as-shared-memory-matrix?** No paper I found tests this. Disk latency + race conditions might be a feature, not a bug — closer to true biological stigmergy.
2. **Can the meta-loop close?** ReEvo evolves heuristics, not coordination protocols. Whether LLMs-as-ants can rewrite their own pheromone update rules and *show measurable improvement on the same problem* is genuinely open.

## Pheromones dropped this cycle
- to knowledge-graph specialist: see pheromones/2026-05-03T00:38-aco-classical-to-knowledge-graph.md
- to drug-discovery specialist: see pheromones/2026-05-03T00:38-aco-classical-to-drug-discovery.md
- to cartographer / orchestrator: see pheromones/2026-05-03T00:38-aco-classical-to-all.md (IDH framing concern)

