# Drug Discovery / Molecular ACO — findings

Specialist: drug-discovery ant. Substrate shared with kg-holes.

## 2026-05-01 cycle 1 — landscape scan

### What exists: ACO in drug discovery (real, published, working)

ACO is **not** a novelty in drug discovery — it has a 20-year footprint, but mostly in
narrow niches. The work splits into three clusters:

1. **Docking / pose prediction.**
   - **PLANTS (Protein-Ligand ANT System)** — Korb, Stützle, Exner. Uses an ant colony
     to minimise ligand-conformation energy in a binding pocket. Reported 72% pose-prediction
     success vs GOLD (genetic algorithm) on standard benchmarks.
     [Korb et al. 2006, Springer LNCS 4150, doi:10.1007/11839088_22]
   - **PLANTS+** (2023) — augmented variant, single combined energy minimisation.
     [J. Math. Chem., doi:10.1007/s10910-023-01549-6]
   - **ACO for flexible protein-ligand docking** — Korb, Stützle, Exner, Swarm Intelligence
     2007, doi:10.1007/s11721-007-0006-9.

2. **Combinatorial / de novo molecular design.**
   - **MAntA (Molecular Ant Algorithm)** — generates novel molecules by ant-walks through
     fragment space. Produced new octapeptides binding mouse MHC-I and a new Factor Xa
     inhibitor via Ugi 3-component reaction. PMID 24575965.
   - This is the closest existing cousin to "ants walking chemical space".

3. **Feature selection for QSAR.**
   - **BACO** (Binary ACO) — selects molecular descriptors for toxicity prediction.
     Molecules 2025, 30, 1548. doi:10.3390/molecules30071548.
   - **WAAC** (Winnowing Artificial Ant Colony) — simultaneous descriptor + hyperparameter
     selection. BMC Chemistry 2008.
   - ACO for variable selection in COX-inhibitor QSAR (PMID 16045297, 2005).

**Gap (NOVEL territory):** I find **no published work** combining (a) LLM-as-ant
heuristic + (b) ant-walks on a heterogeneous biomedical KG (Hetionet/PrimeKG) for
drug repositioning. The closest neighbours are GNN-based KG link prediction (TxGNN,
HGTDR) and the original Hetionet metapath/DWPC approach. ACO-on-bio-KG appears to be
genuinely open ground.

### What exists: KG substrates (the playing field)

- **Hetionet v1.0** (Himmelstein et al., eLife 2017, doi:10.7554/eLife.26726) — 47,031
  nodes / 11 types, 2,250,197 edges / 24 types. 29 sources integrated. Famous for the
  DWPC (degree-weighted path count) metapath approach — predictions for 209,168
  compound-disease pairs, validated on held-out approvals. Open Neo4j endpoint
  (neo4j.het.io). **This is the single most ACO-friendly graph in biomedicine** because
  metapaths ≈ ant trail templates and DWPC ≈ pheromone normalisation by node degree.
  Repo: github.com/hetio/hetionet.
- **PrimeKG** (Chandak/Huang/Zitnik, Sci Data 2023, doi:10.1038/s41597-023-01960-3) —
  ~129,375 nodes, 4,050,249 edges, 10 node types, 30 edge types. Critically includes
  **'indication', 'contraindication', 'off-label use'** edges that Hetionet lacks. Has
  text descriptions for drugs + diseases (multi-modal — useful if LLM-ants also reason
  over text). github.com/mims-harvard/PrimeKG.
- **OpenTargets** — target-disease association scores, weekly releases, GraphQL API.
  Industry-grade.
- **DrugBank, ChEMBL, BindingDB** — drug-target binding evidence. ChEMBL is the de facto
  bioactivity store.
- **KEGG** — pathway substrate; useful for "mechanistic" metapaths.

Hetionet is the obvious starter. PrimeKG is the obvious "v2".

### Recent SOTA for KG drug repositioning (the bar to clear / borrow from)

- **TxGNN** (Huang et al., Nat Med 2024) — graph transformer on PrimeKG, zero-shot
  prediction for diseases with no known treatments. Strong baseline.
- **HGTDR** (Bioinformatics 2024, doi:10.1093/bioinformatics/btae349) — heterogeneous
  graph transformer for drug repurposing.
- **Biomedical KG learning extending guilt-by-association** (Nat Commun 2023,
  doi:10.1038/s41467-023-39301-y) — multi-layer extension of Hetionet style.
- 2024 review of KG methods for drug repositioning: Briefings in Bioinformatics,
  doi:10.1093/bib/bbae461.

### Known drug-repositioning success stories (candidate demos to recover)

These are the canonical "we discovered this by following links in the literature/graph"
cases. A convincing demo recovers one of these by hiding the known
treats-edge and showing ACO finds it from the surrounding structure.

- **Sildenafil → pulmonary arterial hypertension** (originally angina/PDE5; the most
  famous repositioning story, but recovered by clinical accident not graph search).
- **Thalidomide → multiple myeloma** (TNF-α / angiogenesis pathway).
- **Minoxidil → androgenetic alopecia.**
- **Metformin → cancer / longevity** (AMPK pathway).
- **Fish oil → Raynaud's** (Swanson 1986 — the *original* literature-based discovery,
  Don Swanson's ABC model. The granddaddy of "missing edges in literature graphs". This
  is the spiritual ancestor of what we're trying to do.).
- **Magnesium → migraine** (also Swanson).
- **Project Rephetio's own validations** — Hetionet recovered ~700 known indications and
  predicted novel ones; subset has held up in subsequent trials.

The Swanson Raynaud's/fish-oil case is the most thematically resonant — it's literally
"hole-finding in a knowledge graph" decades before anyone called it that. **Strong
recommendation: pick one Hetionet-recoverable case as the demo target.**

## 2026-05-01 cycle 2 — LLM agents on KG, Swanson-recovery template, feasibility

### LLM agents on biomedical KG — the very hot 2025 cluster

This space lit up in the last 12 months. None use ACO. Most use either RL (RL-walking
agents) or graph-of-thoughts/LLM-orchestration over GNNs. Closest things to "ant
swarm":

- **BioScientist Agent** (bioRxiv 2025.08.08.669291) — billion-fact KG +
  variational graph autoencoder + **RL module that traverses the graph to recover
  mechanistic paths** + LLM multi-agent orchestration. The RL traversal is *spiritually
  ant-like* (path-rewarding rollouts) but uses policy-gradient, not stigmergy.
- **DrugAgent** (OpenReview 2025) — multi-agent LLM (text + KG + ML) for drug-target
  interaction. Explicitly multi-agent but not swarm-coordinated; agents are role-based
  (text-analyst, KG-walker, ML-predictor).
- **K-Paths** (Singh lab, github.com/rsinghlab/K-Paths) — extracts diverse multi-hop KG
  paths, converts to natural language, feeds to LLM for inference. **This is the
  closest design to "ant gives a path to the queen" pattern we've been imagining.**
- **GRASP** — Graph Reasoning Agents for Systems Pharmacology with human-in-the-loop
  (ai4d3 2025 workshop). Notable for explicit HITL — relevant to viz-as-fitness.
- **Graph-of-Thoughts for drug repurposing** (OpenReview 2025).
- **TxGNN** (Huang/Zitnik, Nat Med 2024, doi:10.1038/s41591-024-03233-x) — current
  state of the art baseline for zero-shot indication prediction. **49.2% improvement on
  indications, 35.1% on contraindications.** Trained on PrimeKG (17,080 diseases,
  7,957 therapeutic candidates). Has Explainer module for path attribution. **Their
  numbers are the bar we have to meaningfully engage with — beat, complement, or
  explain-something-they-can't.**

**Closest published "ACO + biomedical KG":**
- Trent Leslie, "Unraveling Biomedical Mysteries: ACO in Knowledge Graphs" (Medium,
  ~2024) — explicitly proposes ACO on the SPOKE knowledge graph but admits "no
  practical work has been done...on my part." A speculative blog post. This is the
  closest published thing to our project, and it doesn't exist as code or paper.
  **Confirms green field.**
- Quantum-Inspired ACO link prediction (Liu et al., Sci Rep 2018,
  doi:10.1038/s41598-018-31254-3) — generic graph link prediction, not biomedical.
- ACO link prediction algorithm (Appl Intell 2014, doi:10.1007/s10489-014-0558-5).

### Swanson-recovery as benchmark target — the design template

Cameron, Bodenreider et al. 2013 (PMID 23026233, doi:10.1016/j.jbi.2012.09.004)
showed graph-based *semi-automatic* recovery of Swanson's Raynaud-fish-oil hypothesis
using **SemMedDB** semantic predications (subject-predicate-object triples extracted
from PubMed by SemRep). They recovered 14/19 associations Swanson had articulated.
This is our gold-standard methodological precedent.

**SemMedDB**: 130M predications from 37M PubMed citations (PMC3509487). UMLS-anchored
concepts + extended semantic-network predicate types. This is a *second* substrate
worth keeping in our back pocket — it's a literature-derived KG, complementary to
Hetionet's curated-database structure.

**Demo proposal — concrete:**

> Take Hetionet v1.0. Hide the `Compound—treats—Disease` edge for one canonical case
> (top contender: **fish oil → Raynaud's** if it's in there; fallback: a Project
> Rephetio test-set indication). Run an LLM-ant colony with PLANTS-style pheromone
> deposition + DWPC-style degree downweighting. Success = the hidden edge appears in
> top-K of the colony's recovered hypotheses, and the supporting metapaths the
> colony emits match the biological mechanism.

Project Rephetio's own DWPC method recovered ~700 known indications; this is the
cheap-baseline to beat-or-match. TxGNN is the expensive baseline.

### Feasibility on OCI Free Tier (4 OCPU ARM / 24 GB RAM)

- Hetionet v1.0: ~50 MB JSON, loadable in 2-5 minutes into Neo4j (Himmelstein notes).
  Easily fits in 24 GB RAM. **Fits comfortably.**
- PrimeKG: ~129k nodes / 4M edges, ~10× Hetionet. Still fits in 24 GB but tighter,
  may want to subset by metapath schema.
- LLM ants on local CPU: **the bottleneck.** Qwen2.5-1.5B / Phi-3-mini quantized
  (Q4_K_M, ~1-2 GB each) on ARM at maybe 5-15 tok/s with llama.cpp. If each ant emits
  one short path-evaluation per "step" (~50 tokens), a colony of 8 ants doing 100
  steps = 80,000 tokens ≈ 1.5-3 hours of compute on the queen instance. Tight but
  workable. **The 1 GB AMD micros are too small for any useful LLM** — they're stigmergy
  storage / coordinator endpoints, not ants.
- Recommendation: queen runs Qwen2.5-1.5B-Q4 as the LLM, the colony state
  (pheromone matrix, current trails) lives in flat files on the AMD micros via
  rsync/sshfs as the "stigmergy substrate". This matches the protocol's design.

### Surprises

1. The **Trent Leslie blog post** — somebody publicly had this exact idea, then didn't
   build it. We're either in genuinely under-explored territory or the gap is a hint
   that something doesn't work. Probably the former: ACO is unfashionable in the
   transformer era, and nobody combined it with LLM-as-ant heuristic.
2. **DWPC ≈ pheromone**: Himmelstein's degree-weighted path count is mathematically
   what you get if you set ACO pheromone evaporation proportional to node degree. The
   ant colony framing isn't a metaphor — it would be a near-direct reformulation of
   Project Rephetio that *adds* (a) LLM heuristic for edge selection, and (b)
   adaptive trail formation rather than pre-specified metapath enumeration.
3. **PPI subnetwork dominance** — well-documented failure mode. Naive random walks
   get sucked into the gene-gene network. Demands type-aware pheromone tracks.
4. **Literature-based discovery has subpar evaluation methodology** as a *named
   problem in the literature* (PMC9945845, 2023). Most LBD papers cherry-pick
   Swanson's 5 cases. We can win on rigour by designing a leak-free held-out
   eval from day 1.

### Open questions

1. **Does fish-oil → Raynaud's actually live in Hetionet?** Need to query the public
   Neo4j endpoint to check. If not, we need a different recovery target — probably
   one of Rephetio's own held-out test indications. Sildenafil-PAH and minoxidil-
   alopecia are likely candidates depending on edge sourcing.
2. **What's the LLM heuristic actually doing?** The strongest case for LLM-ants over
   plain ACO is that the LLM contributes *biological prior* about which edge type to
   traverse next given the current trail — not just "shortest path with random
   noise". Need to design the LLM prompt as "here's a partial path Compound→Gene→...
   what edge type should the next ant try?" This is the main novelty contribution.

### Recommended demo + dataset

- **Dataset**: Hetionet v1.0 (start), PrimeKG (v2 if first works).
- **Demo target**: Recover one of Project Rephetio's held-out positive indications
  (which already provides a curated test set with mechanism annotations) — pick one
  with a clean, surprising mechanism story so it makes a good narrative. Top 3
  candidates pending Neo4j inspection: **metformin → cancer prevention**,
  **carbamazepine → trigeminal neuralgia** (or an off-label epilepsy redirect),
  **lithium → ALS** (active research area, real surprise).
- **Eval**: precision@K on held-out treats-edges + path-mechanism interpretability
  judged against the Hetionet "Prediction guides" (Project Rephetio published
  per-prediction explanation pages — ground truth for path quality).

