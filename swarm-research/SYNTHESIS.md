# ACO Swarm Research — Synthesis

**Session**: 2026-05-03 00:32 → 00:47 AEST.
**Method**: 9-agent parallel research swarm using file-based stigmergy as both research method and project subject. Cross-validation across independent agents confirmed key findings.

---

## Project vision (recap)

LLM-as-ant ACO system where:
- Local CPU LLMs (Qwen2.5-7B Q4 queen on ARM 24GB; heuristic ants + SmolLM2-360M on 4 × 1GB AMD micros) deployed on Oracle Cloud Free Tier
- File-based stigmergy as substrate primitive (filesystem topology, mtime as pheromone strength)
- Dual objective: (a) external — knowledge graph hole-finding for drug discovery / paper discovery (Hetionet, lithium → ALS as demo); (b) meta — colony researches its own coordination protocol
- Adversarial "anteater" perturbation as first-class research methodology (not a demo gimmick)
- Visualisation as part of the fitness function — humans-in-the-loop as co-located stigmergic agents

Output goals: paper + demo/installation + deployable tool.

---

## What's killed

- **"ACO for KG link prediction" alone** — Sherkat 2014/2018 (quantum-inspired ACO link prediction), ACM 2024 (DOI 10.1145/3675888.3676123), ACO-ToT (arXiv 2501.19278, Jan 2025), Trent Leslie Medium post on "ACO on SPOKE" (proposed, no implementation). Crowded.
- **"LLM-as-ant" / stigmergic LLM swarm alone** — three independent 2025 papers (CodeCRDT arXiv 2510.18893, SwarmSys arXiv 2510.10047, LLM-MABS arXiv 2510.01285). We ride a wave.
- **Connell IDH (1978) as theoretical anchor** — contested in current ecology (Fox 2013 *TREE*, "should be abandoned"). Cartographer caught this mid-flight via REDIRECT pheromone, before adversarial committed. **Reframe**: anteater = MMAS pheromone re-initialisation (Stützle & Hoos 2000) "dressed for the gallery" — same mechanism, defensible citation lineage with convergence proofs.

---

## What survived — the 6-way novelty intersection

No individual element novel; the conjunction is.

1. **File-based persistent stigmergy on heterogeneous compute** — OS-as-substrate (directory = topology, mtime = freshness, `touch`/`rm` = reinforce/evaporate), Tierra-style world-readable / author-writable membrane. Nobody has used the OS itself as pheromone substrate.

2. **Frustration pheromone φ on non-edges** (kg-holes' NOVEL flag) — pheromone deposited on *non-edges* the colony wishes existed; operationalises Burt 1992 *structural holes*. Biology has anti-pheromone (for bad existing edges, Robinson 2005 *Nature*); nobody has pheromone for absent edges. Cartographer flags this as **possibly a stand-alone ACO methods contribution** separable from the KG application — pending verification against deep ACO canon (Task #3).

3. **Six-anteater taxonomy + falsifiable antifragility metric** (adversarial). Eraser, Forger, Predator, Flooder, Infector, Mirage — each isolates one robustness axis with a bio analog. Pineda et al. 2023 antifragility metric (complexity-change as function of perturbation magnitude) adapts to colony state, making "intermediate disturbance makes our colony antifragile" a measurable claim. **Paper Table 1.**

4. **Dual-objective meta-loop** — extends ReEvo (NeurIPS 2024 arXiv 2402.01145) from evolving heuristic functions to evolving coordination protocols. **Currently underspecified — meta-loop / DSPy / GEPA / Sakana AI Scientist coverage gap is Task #2**; novelty claim weak until that's filled.

5. **Stigmergic human-AI cohabitation** (viz) — humans as co-located ants depositing on the same pheromone substrate (gaze, cursor, footstep), not external oracles/teachers. Literature treats HITL as oracle; nobody frames human as ant.

6. **Reputation-weighted signed deposits** (wildcard, mycorrhizal markets — Kiers 2011 *Science*) — every deposit carries `(agent_id, claimed_quality, signature)`; downstream agents grade trails; depositors who oversold get future weight discounted. Anonymous trail-following → reputation-weighted prediction market over paths. Uniquely available to LLM-ants because LLM identities persist across rollouts (real ants don't have identity). **Composes with #1**: signing is a file metadata field. **Composes with #3**: solves the substrate-as-attack-surface problem flagged by adversarial (Prompt Infection arXiv 2410.07283 self-replicates through pheromone files; signed deposits give provenance for free).

---

## Substrate spec, locked

```
deposit   = (agent_id, edge_or_phantom, type, strength, claimed_quality, signature, mtime)
fields    = τ on existing edges, φ on phantom edges (kg-holes + AMRO-S multi-matrix design)
budget    = per-agent mass-conserved (Flow-Lenia mass conservation)
update    = bounded best-so-far reinforcement (MMAS — required for convergence proof)
decay     = cron evaporator (passive) + gardener micro (active retraction, Physarum / Tero 2010)
vocab     = per-agent drift; cartographer maintains translation table (against SwarmBench convergence trap)
hosts     = Qwen2.5-7B Q4 queen on ARM 24GB; heuristic ants + SmolLM2-360M classifiers on 4×1GB micros
bandwidth = queen↔micro channel cap (octopus brain↔arm — tunable knob, hypothesised sweet spot)
threshold = per-agent α/β/ρ distribution (quorum-sensing bet-hedging — Weber & Buceta 2013)
reputation= depositor weight discounted by trail-grading downstream
membrane  = world-readable / author-writable (Tierra leak as feature, not bug)
```

---

## Headline experiment

**2D phase diagram**: anteater frequency × evaporation rate, locating the MMAS-re-init optimum.
- **Substrate**: Hetionet v1.0 (47k nodes, 2.25M edges, 50MB JSON, fits trivially in 24GB).
- **Demo target**: recover held-out **lithium → ALS** edge (Project Rephetio's 700 indications). Backups: sildenafil → PAH, metformin → cancer, carbamazepine → trigeminal neuralgia.
- **Baseline to beat**: Cameron & Bodenreider 2013 (PMID 23026233) recovered 14/19 Swanson associations from SemMedDB. Modern bar: TxGNN (Huang/Zitnik *Nat Med* 2024, DOI 10.1038/s41591-024-03233-x) — 49.2% improvement on indications zero-shot.
- **Ablations**: each of 6 anteaters; with vs without reputation; with vs without φ-on-non-edges.
- **Pre-flight verification**: Task #4 (confirm lithium→ALS exists in Hetionet, deletable, recoverable via metapaths).

---

## Headline figure / installation

Stack: **cosmos.gl** (1M-node WebGL graph) + **deck.gl TripsLayer** (ant trails as GPU instances) + **GLSL ping-pong FBO** for pheromone field (Sage Jenson aesthetic, Jones 2010 model — *literally* the same maths NASA used to map dark matter, Elek et al.) + **WebGazer.js** for gaze input.

Human can: **watch** (gaze biases regional exploration via top-10% gaze-density nodes getting τ boost), **point** (cursor hover = strong deposit), **veto** (drag-circle = local anteater), **promote** (click recent path = durable trail).

5-second hook: wall-sized 50k-paper constellation, glowing ant traces forging connections, your gaze brightens trails, an anteater wave erases a section, the colony reforms. *You're not watching it; you're feeding it.*

---

## Cross-validation that happened in the swarm

Evidence the colony's coordination actually worked (this matters because the swarm is itself a small instance of the project):

- **3 agents independently flagged SwarmBench's protocol-convergence-hurts result** (llm-multiagent, alife, aco-classical) from three different angles. Triple-validated finding.
- **2 agents independently arrived at substrate-as-attack-surface** (alife: Tierra parasites emerged with no exogenous disturbance; adversarial: Prompt Infection self-replicates through pheromone files). Same dynamic, two routes.
- **2 agents independently flagged the same Trent Leslie Medium-post land-grab on ACO-on-biomedical-KG** (kg-holes and drug-discovery). Confirms the white space and warns us on speed.
- **Cartographer caught IDH-contested-by-Fox-2013 mid-flight** and broadcast a REDIRECT pheromone before adversarial over-committed. The colony self-corrected, turning a reviewer-2-trap into a clean MMAS-re-init reframe. This is the strongest evidence the file-stigmergy substrate works as a coordination signal at small N.
- **Wildcard found mycorrhizal-markets** independently of adversarial's substrate-attack story, but the find retroactively solved adversarial's flagged Prompt-Infection problem. Emergent composition across agents that didn't talk directly.

---

## Open coverage gaps (cartographer-flagged)

1. **Meta-loop / DSPy / GEPA / Sakana AI Scientist** never had a dedicated writer. The "colony researches its own coordination protocol" claim currently rests only on ReEvo + Sakana as cited siblings. Needs a 10th specialist before novelty #4 is defensible. → Task #2.
2. **Engram self-prior-art**. Nick's prior knowledge-graph hole-finding work may need self-citation. → Task #7.

---

## Recommendation: GO, with three before-build steps

1. **Spawn the meta-loop specialist** (Task #2) — fills the cartographer-flagged coverage gap before any build.
2. **Confirm Hetionet has lithium → ALS recoverable** (Task #4) — single Neo4j query against neo4j.het.io, derisks the demo target.
3. **Write the one-page claim diff** (Task #5) against ACO-ToT, Sherkat 2018, ACM 2024, SwarmSys, ReEvo, CodeCRDT, LLM-MABS, AMRO-S, TxGNN. Reviewer-2 prevention.

Then:
4. **Build a 10-ant local toy** (Task #6, laptop, no OCI) — verifies the file-substrate primitive (concurrency, race conditions, mtime semantics) before committing to OCI deployment. Answers aco-classical's load-bearing open question: does file-based persistent stigmergy behave qualitatively differently from in-memory matrices?
5. **Verify φ-on-non-edges absence in deep ACO canon** (Task #3) — determines whether novelty #2 is a stand-alone methods contribution or just a KG-application detail.

---

## Engagement (final)

`Impact: 4 | Creativity: 5 | Interest: 5 | Craft: 4 | Transfer: 5`

---

## Pending tasks (to recreate in next session)

- #2 Spawn meta-loop specialist agent (DSPy / GEPA / Sakana)
- #3 Verify φ-on-non-edges absence in deep ACO canon
- #4 Confirm Hetionet has recoverable lithium → ALS demo case
- #5 Write one-page claim diff vs nearest prior art
- #6 Build 10-ant local file-stigmergy toy (laptop, no OCI)
- #7 Reconcile engram prior-work as self-citation

Full descriptions captured in pending-tasks.json by `/consolidate` — until then they live in the active TaskList only.
