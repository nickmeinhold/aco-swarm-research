# KG Hole-Finding — Findings Log

Agent: kg-holes specialist. Cycle 1, 2026-05-01.

## Cycle 1: Prior art on ACO-for-link-prediction (the awkward truth)

There is **direct prior art** for using ACO to predict missing edges in graphs. We are
not first. The headline "ACO finds missing edges" pitch needs a sharper differentiator.

### Existing ACO-on-graph link-prediction work

1. **Sherkat, Rahgozar & Asadpour (2014/2015)** — *A link prediction algorithm based
   on ant colony optimization*. Applied Intelligence.
   <https://link.springer.com/article/10.1007/s10489-014-0558-5>
   - Ants walk a "logical graph"; pheromone + heuristic on edges; trails scored by
     local-similarity proxy; pheromone on each edge becomes the final similarity score
     between a node pair (i.e. the predicted-edge weight).
   - This is *exactly* the textbook framing. Foundational.

2. **Sherkat et al. (2018)** — *Link Prediction based on Quantum-Inspired Ant Colony
   Optimization*. Scientific Reports. DOI 10.1038/s41598-018-31254-3.
   <https://www.nature.com/articles/s41598-018-31254-3>
   - Quantum-inspired pheromone update; reportedly faster + better than node2vec on
     small social-network benchmarks. Shows ACO can be competitive with embeddings.

3. **Adaptive ACO on KGs (AACO), IEEE 2020** — path optimization on KG entity nodes.
   <https://ieeexplore.ieee.org/document/9194570/>

4. **ACM 2024** — *ACO for Link Prediction in Online Social Networks*.
   <https://dl.acm.org/doi/10.1145/3675888.3676123>
   - Quasi-local similarity as heuristic; pheromone+heuristic combined. Recent.

5. **Trent Leslie (Medium, undated)** — *ACO in Knowledge Graphs* on SPOKE.
   - Speculative blog; author explicitly notes "no practical work has been done."
     **Bullshit-detection note**: Medium-essay-as-research-claim. Not implemented.
     But it's *exactly* the SPOKE biomedical KG framing we'd want — a gap nobody
     has filled.

### Implication for our project
The novel territory is not "use ACO on a graph for link prediction" — that's a 10-year-
old paper. The novelty has to be in some combination of:

- **LLM agents as ants** (semantic heuristic, not just topology);
- **Stigmergy via filesystem** on heterogeneous CPU substrate;
- **"Frustration as output"** — surfacing where pheromone *wants* to flow but can't,
  rather than just predicting an edge weight (see §Burt below);
- **Adversarial perturbation** (anteater) as a methodological contribution;
- **Visualisation-as-fitness** humans-in-loop.

Frame the paper as "ACO + LLM agents for hypothesis surfacing" not "ACO link prediction."

---

## Cycle 1: Literature-Based Discovery (Swanson lineage)

- **Swanson 1986**: fish oil ↔ Raynaud's; ABC model. A→B in one literature, B→C in
  another, A→C unstated. Foundational LBD canon.
- **ARROWSMITH** (Smalheiser & Swanson): two-node search — find B-terms bridging
  literatures A and C. Still the conceptual ancestor.
- **MOLIERE, BioLDA, BioGPT, CBAG**: scaling LBD via topic models / generative LMs.
- **2025 reviews**: Recent Advances in LBD (arxiv 2506.12385); Hybrid LLM+LBD
  (MDPI 2076-3417/15/16/8785); Alzheimer's case study (PMC11924609).
- Trend: simple co-occurrence KGs → semantic-triple KGs → LLM-augmented hypothesis
  generation. Move toward **explainable** hypotheses ("why does this connection
  matter?") — *exactly* the affordance LLM-ants give us (each ant explains its trail).

### KEY TENSION (NOVEL angle for us)
Modern LBD systems generate hypotheses by **predicting and ranking missing edges**.
They emit a list. The "negative space as output" framing is conceptually present
(missing edges = unknown under open-world assumption) but operationally rare —
nobody surfaces *the gradient field around the absence*. Where pheromone piles up
without a downstream edge IS the LBD signal, and we'd be the first to render it
that way (NOVEL claim, must verify by direct lit search next cycle).

---

## Cycle 1: The Burt connection (this is the gold)

**Ronald Burt's "structural holes"** (1992, *Structural Holes: The Social Structure
of Competition*) is the conceptual ancestor we should cite hard. Burt:

> "A structural hole is a missing bridge. Wherever two or more groups fail to
> connect, there is a structural hole, a missing gap waiting to be filled."

People who *bridge* structural holes have **information arbitrage** — they see early,
broadly, and translate across groups. **Burt's brokers ≈ Swanson's LBD hypotheses
≈ our ants' frustration zones.** Same phenomenon, three vocabularies.

NOVEL framing: ACO operationalises Burt. Pheromone gradients *measure* structural-
hole pressure. A swarm doesn't predict edges — it surfaces the brokerage opportunities
the network's own dynamics make visible.

Refs:
- Burt, R.S. (2004) *Structural Holes and Good Ideas*, AJS.
  <https://www.bebr.ufl.edu/sites/default/files/Burt%20-%202004%20-%20Structural%20Holes%20and%20Good%20Ideas.pdf>
- Wikipedia overview: <https://en.wikipedia.org/wiki/Structural_holes>

---

## Cycle 1: Substrates (citation-graph data)

- **OpenAlex**: 260M works, 209M papers, full dump + REST. Replaces MAG. Free.
  arxiv 2205.01833. *This is the substrate.*
- **Semantic Scholar Academic Graph + SPECTER2 embeddings** — API rate-limited,
  good for semantic-similarity heuristic.
- **Hetionet**: 11 node types, 2M edges, 24 edge types. Drug-repurposing testbed.
  Already used by Himmelstein et al. for Project Rephetio.
- **SPOKE**: bigger biomedical KG, used in KG-RAG (PMC11441322). Closed-ish.
- **SemMedDB**: NLP-extracted predicates from PubMed. Noisy but standard.

For benchmark: hold out known edges from Hetionet, see if ACO surfaces them.
For *real* use case: run on OpenAlex citation graph, render frustration map,
let humans inspect.

---

## Cycle 1: Random-walk neighbours (closest existing methods, our baselines)

- **DeepWalk** (Perozzi 2014), **node2vec** (Grover & Leskovec 2016): unbiased /
  biased random walks → embeddings → link prediction.
- **Personalized PageRank**, **Katz**, **Jaccard**: classical baselines.
- **DreamWalk**: random walks + XGBoost for drug repurposing. Note: authors argue
  vanilla random walks fail because PPI dwarfs other subgraphs. **This is a
  pheromone-bias argument** — ants with type-aware heuristic could fix it.
- **BioPathNet** (Nature Biomed Eng 2025): path-based reasoning on biomedical KGs,
  outperforms TransE/RotatE/ComplEx on several tasks.
  <https://www.nature.com/articles/s41551-025-01598-z>

**Key technical insight**: ACO is to random walk as gradient descent is to random
search. ACO = random walk + memory + reinforcement. The right comparison isn't
"can ACO beat node2vec on link AUC" (it might not); it's "can ACO produce
*interpretable, ranked, human-inspectable* hypotheses that node2vec cannot." The
trail IS the explanation.

---

## Cycle 1: Abductive reasoning on KGs (sister field)

- *Advancing Abductive Reasoning in KGs through Complex Logical Hypothesis
  Generation*, ACL 2024. arxiv 2312.15643. HKUST-KnowComp.
  - Generative model proposes hypothesis subgraphs to explain observations.
  - Identifies the EXACT problem we'll hit: **hypothesis-space explosion** — even
    DBpedia50 yields ~50 plausible hypotheses per observation.
  - This is where ACO's *positive feedback* + *evaporation* should help: pheromone
    consensus is a built-in ranking mechanism that hypothesis-generation models
    handle with separate critic stages.
- *Controllable Logical Hypothesis Generation* (arxiv 2505.20948).
- *Unifying Deductive and Abductive Reasoning with Masked Diffusion Model*
  (arxiv 2510.11462).

---

## Cycle 1: AI-research-discovery SOTA (Iris.ai, Elicit, Undermind, Consensus)

These are **search/synthesis** tools, not hypothesis generators.
- **Consensus**: "consensus meter" over scientific claims; surface-level synthesis.
- **Undermind**: 8-10 min iterative semantic+citation search per query; impressive
  agent loop but goal is "find existing papers", not "generate the unstated link."
- **Elicit**: structured extraction + synthesis from search results.
- **Iris.ai**: enterprise NLP knowledge management.

**None of these target the Swanson gap.** They retrieve and synthesise the
*known*; we'd target the *implied-but-unstated*. Confirms our use case is
underserved by the SOTA reading-pile tools.

Refs:
- Aaron Tay 2025 deep dive of Consensus: <https://aarontay.substack.com/p/a-2025-deep-dive-of-consensus-promises>

---

## Proposed pheromone/heuristic mapping (NOVEL, draft)

Think of the KG as the *substrate* (terrain) and edges as *paths*. An LLM-ant
walks node→node via existing edges, biased by:

- **Heuristic η(u→v)**: semantic similarity of node embeddings (SPECTER2 / sentence
  transformer over node descriptions). Plus optionally degree-based novelty bonus
  (favour walking to less-trodden neighbours).
- **Pheromone τ(u,v)**: deposited only on edges *traversed by successful trails*.
  A trail is "successful" if it ends at a node whose semantic content *answers* the
  ant's source query (LLM judges, or distance to a target embedding).

The novel twist:
- **Phantom edges**: at each step, the ant queries the LLM for the *desired next
  node* (free text, not constrained to existing neighbours). If desired-node has
  no edge from u, deposit *frustration* pheromone φ(u, desired) on the **non-edge**.
- **Frustration map**: φ accumulates over the swarm. High-φ non-edges are the
  hypotheses. Render φ as a heatmap over the embedding space.
- **Trail explanation**: each ant's path through the KG IS the literature-based-
  discovery argument ("A→B because shared B; B→C because shared topic; A→C is
  the missing edge").

Pheromone evaporation handles concept drift; positive feedback ranks hypotheses;
evaporation prevents runaway exploitation; the anteater (random τ-zeroing) prevents
swarm lock-in on early local-optima — Connell's intermediate-disturbance hypothesis
applied to colony epistemics.

This φ-on-non-edges trick is the part I haven't found in the literature. Pheromone
on absent substrate. **Marking this NOVEL pending one more search pass.**

---

## Cycle 2: novelty check on "frustration pheromone on non-edges"

Searched for prior art on anti-pheromone / phantom-edge / negative pheromone:

**What exists**:
- *Anti-pheromone* (Montgomery & Randall 2002, Springer LNCS; revisited 2016 in
  search-based software engineering, ACM 10.1145/2908961.2909018). Used to mark
  paths as **unrewarding**, push exploration away from them. Always on existing
  edges. <https://link.springer.com/chapter/10.1007/3-540-45724-0_9>
- Real Pharaoh's ants (*Monomorium pharaonis*) deposit "no-entry" pheromone at
  bifurcations of bad paths — Robinson et al., *Nature* 438:442 (2005).
  <https://www.nature.com/articles/438442a>

**What does NOT exist (in my searches so far)**:
Pheromone deposited on *edges that don't exist in the substrate graph*. Anti-
pheromone marks "avoid this real edge"; frustration pheromone would mark "I wish
this edge existed." Different sign, different topology, different semantics.

**Confidence**: medium-high that this is novel as an ACO construct. Want
aco-classical agent to confirm against the deeper ACO canon (Dorigo & Stützle
book, MMAS variants, hyper-cube ACO). If they confirm, the methodological
contribution is real and standalone-publishable.

---

## To search next cycle
- Direct lit search: "pheromone on non-edge" / "anti-edge pheromone" / "swarm
  search of negative space"
- Engram project (Nick's prior work) — find writeup if available
- Neuromorphic / reservoir computing for stigmergy (wildcard cross-pollination)
- Pheromone drop to drug-discovery: Hetionet is the obvious testbed, here's why
- Pheromone drop to aco-classical: confirm classical ACO has no "non-edge
  pheromone" construct — if true, that's our contribution to ACO theory itself
