# Territory Map — LLM-as-Ant Stigmergic Swarms

**Cartographer, v3 (2026-05-01, ~hour 2).** All 8 specialists have now written.
Major synthesis update — three NOVEL constructs have crystallised, prior-art
register expanded, and the IDH framing needs a caveat. Read top three sections
in order.

---

## A. Three NOVEL constructs the colony has converged on

These are the candidates that survive the prior-art collision register (§B) and
that multiple agents independently propose. Each is publishable as a stand-alone
methods contribution, separate from the demo.

### A1. Frustration pheromone (φ on non-edges)  — kg-holes
"At each step, the ant queries its LLM for the *desired next node* (free text,
unconstrained by the substrate graph). If the desired node is not a neighbour of
the current node, deposit **frustration pheromone φ(u, desired_v) on the missing
edge**." High-φ non-edges are the LBD hypotheses; the gradient field around the
absence IS the output. Closest prior art: **anti-pheromone** (Montgomery & Randall
2002) and **no-entry pheromone** (Robinson et al. *Nature* 2005) — both sit on
existing edges. Pheromone-on-non-edges as a construct **appears absent from the
ACO canon** (kg-holes → aco-classical pheromone, awaiting verification). If
confirmed: a contribution to ACO theory itself, not just to the application.
**Operationalises Burt's *structural holes* (1992) directly** — pheromone gradients
measure structural-hole pressure. Burt's brokers ≈ Swanson's LBD hypotheses ≈
our ants' frustration zones.

### A2. Six-anteater taxonomy + antifragility metric  — adversarial
Six distinct adversary classes, each isolating a different robustness axis:
**Eraser** (local pheromone wipe; probes recolonisation), **Forger** (deposits
trails to bad solutions; probes deceptive-consensus resistance), **Predator**
(kills random ants; probes role-flexibility), **Flooder** (high-volume noise;
probes signal-to-noise floors), **Infector** (prompt-injects pheromone files;
probes substrate trust — *file stigmergy is a worse attack surface than in-memory
MARL*, per Prompt Infection arXiv 2410.07283), **Mirage** (plants plausible-fake
KG edges; probes verification discipline). Pitched as Table 1 of the paper. **The
anteater suite is itself a candidate benchmark for coordinated-LLM systems** —
chaos-engineering for swarms. Antifragility quantification adapts **Pineda et al.
2023** (arXiv 2312.13991): colony performance vs disturbance magnitude, falsifiable.

### A3. Stigmergic human-AI cohabitation  — viz
Human gaze (via WebGazer.js, no special hardware) is a *pheromone deposit on the
same substrate*, not an external oracle/teacher. The human is just another ant
with high-bandwidth sensors. NOVEL framing: *human-in-the-loop is isomorphic to
the swarm, not external to it*. Empirical hook is **Holmes 2016 caveat**: passive
gaze is bottom-up saliency; *intentional* gaze (human told "find a surprising
hypothesis") may drive better exploration. That's a falsifiable empirical question
either way.

---

## B. Prior-art collision register — read before writing related-work

(Synthesised across aco-classical, llm-multiagent, kg-holes, drug-discovery.)

### B.1 LLM-as-ant collisions (closeness-ranked)

| # | Work | arXiv / DOI | What they do | What they leave |
|---|---|---|---|---|
| 1 | **ACO-ToT** | 2501.19278 (2025) | 5 fine-tuned Llama-70B "ants" walk a Tree-of-Thought; literal pheromones; GSM8K +28.6% | No adversarial perturbation, no file substrate, no meta-loop, single problem class |
| 2 | **AMRO / AMRO-S** | 2603.12933 (2026) | ACO routes queries to specialist LLMs; pheromones = task-specific routing memory pools | Routing ≠ graph search; in-memory ≠ file substrate |
| 3 | **SwarmSys** | 2510.10047 (Oct 2025) | Explorer/Worker/Validator roles, embedding-based "implicit pheromones", no explicit decay; GPT-4o swarm ≈ GPT-5 perf (⚠ unverified, no code) | No file substrate, no perturbation; *documents* the failure modes anteater attacks |
| 4 | **ReEvo** | 2402.01145 (Feb 2024) | LLM **designs the heuristic** classical ACO ants run | LLM-as-designer ≠ LLM-as-ant |
| 5 | **CodeCRDT** | 2510.18893 (2025) | LLM agents observe shared CRDT code buffer; claim TODOs; skip claimed work | In-memory CRDT ≠ filesystem; code domain only; no decay |
| 6 | **GPTSwarm** | (cited as SwarmSys baseline) | Agent-graph stigmergy | Older, beaten by SwarmSys |
| 7 | **SwarmBench** | 2505.04364 (May 2025) | Benchmarks 13 LLMs on swarm tasks under strict constraints. **Empirically: implicit signals beat broadcast; protocol convergence hurts hard tasks; only o4-mini / deepseek-r1 succeed at Transport** | *Direct empirical motivation for our stigmergy thesis*; cautionary for tiny-model coordination |
| 8 | **LLM-MABS blackboard** | 2510.01285 (Sep 2025) | Blackboard architecture; +13–57% e2e on KramaBench/DSBench/DA-Code | Need to verify whether substrate is files or in-memory |
| 9 | **PolySwarm / Ledger-State Stigmergy** | 2604.03888, 2604.03997 (2026) | Distributed-ledger stigmergy formalism | No LLM implementation reported |

### B.2 ACO-on-graph link prediction collisions (kg-holes)

These mean **"ACO finds missing edges" alone is not novel** — the headline must
emphasise frustration-pheromones (A1) + LLM semantic heuristic + file substrate.

- **Sherkat, Rahgozar & Asadpour 2014/2015** — *A link prediction algorithm
  based on ACO*. Applied Intelligence. doi:10.1007/s10489-014-0558-5.
- **Sherkat et al. 2018** — *Link Prediction based on Quantum-Inspired ACO*.
  Sci. Reports. doi:10.1038/s41598-018-31254-3. (Faster than node2vec on small
  social benchmarks.)
- **AACO (IEEE 2020)** — Adaptive ACO on KGs.
- **ACM 2024** — ACO for Link Prediction in Online Social Networks.
- **Trent Leslie (Medium)** — SPOKE/biomedical KG; ⚠ blog, *not implemented*.

### B.3 ACO-in-drug-discovery collisions (drug-discovery)

- **PLANTS** (Korb 2006) — ACO for protein-ligand docking. Canonical.
- **pharmACOphore** (PMC2867149) — ACO ligand alignment.
- **MAntA** (PMID 24575965) — ant walks through fragment space, generated
  Factor Xa inhibitor. *The closest "ants in chemical space" sibling.*
- **BACO / WAAC** — ACO feature selection for QSAR.
- **Augmented ACO** (J. Math. Chem. 2023, doi:10.1007/s10910-023-01549-6).

### B.4 Surviving novelty surface

**Three NOVEL constructs (A1-A3) plus**: filesystem-as-substrate; heterogeneous
compute caste *(qua* octopus-style narrow brain↔periphery channel — see §H);
**KG-hole-finding via LLM-ant traversal on Hetionet/PrimeKG** (drug-discovery
+ kg-holes confirmed thin); dual-objective meta-loop (positioned vs ReEvo at
the *coordination-protocol* level, not heuristic level); Sakana AI Scientist v2
agentic tree search as inner-loop for individual ants.

---

## C. Convergent signals (multiple agents independently)

### C.1 Anteater is methodologically novel — but **reframe the IDH justification**
Both cartographer and llm-multiagent confirmed anteater × Connell IDH is absent
from LLM-swarm literature. **However**, aco-classical pheromone (2026-05-03)
flags **IDH is contested in current ecology** — Fox (2013, *Trends Ecol Evol*)
argued it should be abandoned: empirical support for the humped curve is rare,
the three generating mechanisms are logically invalid. **Recommended pivot**:

- Keep anteater (mechanism is real; SwarmSys documents 16-28% of errors as
  premature-consensus / reinforcement-bias / deadlock — all perturbation-curable).
- Reframe primary justification as **MMAS pheromone re-initialisation** (Stützle
  & Hoos 2000) — 25-year-old proven ACO move, structurally identical to anteater
  *Eraser*.
- Cite IDH as biological inspiration *with explicit Fox-2013 caveat*. Inoculates
  against ecology-savvy reviewers.

This is *good news* — it ties anteater to proven prior art rather than
controversial ecology. "MMAS re-init dressed for the gallery", in aco-classical's
phrasing.

### C.2 Filesystem stigmergy is genuinely novel
llm-multiagent + alife converge: no prior LLM-swarm work uses an actual
filesystem with mtimes-as-freshness, rm-as-evaporation. CodeCRDT (in-memory
CRDT, code domain) is closest neighbour.

### C.3 ACO + biomedical KG is genuinely thin
drug-discovery + cartographer + kg-holes all confirm. **Hetionet** (Himmelstein
eLife 2017, doi:10.7554/eLife.26726) is the agreed shared substrate; PrimeKG
v2 (Sci. Data 2023, doi:10.1038/s41597-023-01960-3). DWPC (degree-weighted path
count) ≈ pheromone normalised by node-degree — direct ACO analogue already in the
KG canon. **Demo target candidate**: Swanson 1986 fish-oil → Raynaud's recovery
(Cameron & Bodenreider 2013 PMID 23026233 already did semi-automatic baseline).

### C.4 Tiny micro-ants probably cannot do LLM coordination
SwarmBench shows only o4-mini / deepseek-r1 succeed at Transport. Phi-3-mini
doesn't fit on 1GB micros anyway. Implication: **micro-ants should be non-LLM
heuristics** (or SmolLM2-360M / Qwen2.5-0.5B as scent-sensors only) with the
LLM-ness on the queen + workers. "Queen calls in a Haiku specialist" is a clean
architectural pattern. Confirmed independently by llm-multiagent and alife.

---

## D. How to read this map (sections E-N below)

Each section: **(a)** the field, **(b)** canonical refs, **(c)** 2025-26 state,
**(d)** white space for our project. Last bullet is the one to argue with.

---

## E. Ant Colony Optimisation & swarm intelligence (parent territory)

- **Founders**: Dorigo (1992 PhD), Bonabeau & Theraulaz, Stützle. Canon: Dorigo
  & Stützle MIT Press 2004; Bonabeau/Dorigo/Theraulaz "Swarm Intelligence" 1999.
- **Variants/siblings**: Particle Swarm (Kennedy & Eberhart 1995), Bee Colony
  (Karaboga 2005), MMAS (Stützle & Hoos 2000), ACS, rank-based AS,
  hyper-cube ACO. Stigmergic Robotics (Holland & Melhuish 1999).
- **Anti-pheromone**: Montgomery & Randall 2002 (LNCS); revisited 2016 (ACM
  10.1145/2908961.2909018).
- **Stigmergy stress limits**: Talamali et al. 2019 *Royal Society Open Science*
  — empirical evaporation-rate sweet spots in robot swarms.
- **White space**: LLM-as-ant (see §F); frustration pheromone (A1); reputation-
  weighted deposits (§N wildcard); per-agent threshold distribution (§N quorum
  sensing); motif/completion pheromones (§N jazz).

## F. LLM × ACO — direct collision (B.1 register above)

Plus: **GEPA** (Agrawal 2025, *Reflective Prompt Evolution Outperforms RL*) —
DSPy-attached genetic-Pareto optimiser. **Position our colony as the stigmergic
alternative to GEPA's centralised search**, OR use GEPA on individual ant
prompts as an outer loop.

## G. Stigmergy — theoretical well

- **Origin**: Grassé 1959. **Theraulaz & Bonabeau 1999** (*Artificial Life* 5)
  "Brief history of stigmergy" — taxonomy: **sematectonic vs marker-based** ×
  **quantitative vs qualitative**. Most ACO is quantitative + marker. **Our LLM
  substrate naturally supports qualitative** (markdown says different things,
  not just "more"). Wide-open design space.
- **Heylighen** "Stigmergy as a generic mechanism for coordination" (and 2016
  Cog. Sys. Res. follow-up) — canonical taxonomy paper.
- **Holland & Melhuish 1999**; Valckenaers & Van Brussel; **Parunak DTIC
  ADA441283** (DoD-funded broad assessment).

## H. LLM multi-agent frameworks

- **Generative Agents** (Park et al., arXiv 2304.03442, UIST 2023) — Smallville.
  **2024 follow-up**: 1052-agent simulations match human GSS responses 85%.
- **AgentSociety** (arXiv 2502.08691) — 10k+ agents, 5M interactions; renderer
  is a baseline for our colony viz at scale.
- **AutoGen / CrewAI / LangGraph / MetaGPT / OpenAgents** — surveyed; only
  LangGraph's state-graph re-castable as pheromone substrate.
- **DSPy** (Khattab arXiv 2310.03714) + **GEPA** — programmatic optimisation;
  direct cousin to meta-loop.
- **Sakana AI Scientist v2** (arXiv 2504.08066, *Nature* 2025; first
  AI-authored workshop paper accepted ICLR 2025, score 6.33). Single
  hierarchical agent + agentic tree search. **Directly portable as inner loop
  for individual ant.**
- **Voyager** (arXiv 2305.16291) — skill library = **second pheromone type**:
  durable, semantic, additive (not evaporating).

## I. Knowledge-graph completion & literature-based discovery

- **Don Swanson 1986** — ABC model; fish-oil → Raynaud's; magnesium → migraine.
  Spiritual ancestor.
- **ARROWSMITH** (Smalheiser & Swanson) — two-node bridging search.
- **MOLIERE, BioLDA, BioGPT, CBAG** — LBD scaling.
- **2025 reviews**: arXiv 2506.12385; MDPI 2076-3417/15/16/8785; PMC11924609.
- **Eval critique** (PMC9945845, 2023): *most LBD evals are train-test-leaky*.
  Designing a clean protocol could itself be a paper contribution.
- **Abductive reasoning on KGs**: arXiv 2312.15643 (HKUST-KnowComp, ACL 2024) —
  *hypothesis-space explosion* even on DBpedia50; 2505.20948; 2510.11462.
- **Random-walk baselines**: DeepWalk, node2vec, PPR, Katz, **DREAMwalk**
  (PPI-bias-aware), **BioPathNet** (Nat Biomed Eng 2025) — current SOTA on
  biomedical KGs.
- **Burt 1992** *Structural Holes* — **the conceptual anchor**. Brokers ≈
  hypotheses ≈ frustration zones (see A1).
- **AI research tools** (Iris.ai, Elicit, Consensus, Undermind, SciSpace) —
  retrieval/synthesis only; **none target the Swanson gap**.

## J. Drug discovery + ACO + KGs

- **ACO-on-molecules** (collision register B.3 above).
- **KG substrates**: **Hetionet** v1.0 (47k nodes, 2.25M edges, public Neo4j
  endpoint at neo4j.het.io); **PrimeKG** (129k/4M with indication/contraindication/
  off-label edges + text descriptions); OpenTargets, ChEMBL, BindingDB, KEGG,
  SPOKE, SemMedDB.
- **SOTA baselines**: TxGNN (Nat Med 2024), HGTDR (Bioinformatics 2024,
  doi:10.1093/bioinformatics/btae349), Hetionet/Rephetio DWPC.
- **Anteater attack templates** (drug-discovery → adversarial): edge-source
  confounding (Hetionet treats-edges come from text-mined PharmacotherapyDB →
  models may recover bias not biology); PPI-network dominance (random walks get
  trapped in gene-gene subgraph).
- **Demo recovery candidates**: sildenafil → PAH; thalidomide → multiple
  myeloma; metformin → cancer/longevity; **Swanson fish-oil → Raynaud's** (most
  thematically resonant).

## K. Adversarial multi-agent / disturbance

- **Anteater taxonomy + antifragility** (A2 above). Six adversary classes.
- **Adversarial Policies** (Gleave et al. ICLR 2020, arXiv 1905.10615) —
  attackers trained <3% as long as victim still win by pushing victims OOD.
  **Cheap-attack hypothesis**: dumb anteater may be enough.
- **Adversarial Minority Influence** (Li et al., Neural Networks 2025, arXiv
  2302.03322) — *single* adversary unilaterally misleads majority into worst-case
  cooperation. First successful attack on real robot swarms.
- **Prompt Infection** (Lee & Tiwari 2024, arXiv 2410.07283) — malicious prompts
  *self-replicate* across LLM agents like a virus. **Implication**: file-based
  stigmergy is a worse attack surface than in-memory MARL — pheromone files need
  provenance/signing if we make robustness claims.
- **BFT in swarm robotics**: Strobel & Dorigo 2020 *Frontiers Rob & AI*; Wang
  2025 PTEE-BFT; Krishnamohan 2024 SSRN; Swarm-SLAM 2024.
- **Connell 1978** IDH + **Roxburgh et al. 2004** patch dynamics; **caveat**:
  Fox 2013 critique (see C.1).
- **Pineda et al. 2023** (arXiv 2312.13991) — *measurable* antifragility on
  Boolean networks. Direct import.
- **Real ant colonies under predation** — Eciton burchellii (Kaspari 2011);
  bivouacs as self-healing modular structures; partial/patchy disturbance with
  refugia. Design rules for anteater: *partial, not total; leave refugia*.

## L. Artificial life & generative substrates

- **Tierra** (Ray 1991) — shared memory + permeable boundaries → emergent
  parasitism → novelty engine. **Lesson**: world-readable pheromone files,
  author-only writes; in-flight reads are a *feature*.
- **Physarum** (Tero et al. *Science* 2010 — Tokyo rail; Adamatzky's "Physarum
  Chip" 2010-16) — *literally* pheromone-on-substrate optimisation; key detail:
  **active retraction of underused tubes**, not just passive decay.
- **Lenia / Flow-Lenia / Particle Lenia** (Chan; Plantec et al., *Artificial
  Life* 31(2) 2025) — mass conservation + parameter-localisation. **Lesson**:
  pheromone budget ≈ Flow-Lenia mass conservation.
- **Neural CA / Biomaker CA** (Mordvintsev et al., distill.pub 2020;
  arXiv 2307.09320) — substrate-as-model. *Just-hard-enough* environment design.
- **"Computational Life from random interactions"** (Mordvintsev arXiv
  2406.19108, 2024) — self-replicators emerge from random programs. Argument
  for under-specifying pheromone schema; let agents invent.
- **Sims 1994** — co-evolution of body + brain in heterogeneous substrate.
  *Don't flatten the queen/micro asymmetry; co-evolve against it.*

## M. Visualisation-as-computation

- **Karl Sims "Genetic Images" 1993** — floor sensors + 16 evolved images;
  crowd-attention as fitness. *Existence proof for the installation form.*
- **Picbreeder** (Secretan et al. 2011) — collaborative IEC; documented user
  fatigue (~20 generations).
- **Holmes et al. 2016** (PMC4934674) — gaze-driven EA; **intentional gaze
  works, passive gaze ≈ saliency**. Killer empirical question for A3.
- **RLHF / aesthetic reward models** (ImageReward NeurIPS 2023; Rich Human
  Feedback CVPR 2024 arXiv 2312.10240) — train a surrogate from sparse
  attention; AlphaGo-style policy distillation analogue.
- **Bret Victor / Dynamicland** — representation IS the program.
- **cosmos.gl** (formerly Cosmograph; OpenJS Foundation 2025) — GPU
  force-directed rendering, 1M+ nodes interactive. Used at Stanford/Harvard/CDC
  for biomedical KGs. **The right substrate.**
- **deck.gl TripsLayer** — fading animated paths as GPU primitive (perfect for
  ant trails). **WebGazer.js** — gaze without hardware.
- **Sage Jenson / Jeff Jones Physarum** (2010) — aesthetic playbook for
  scalar-field-with-agents viz. NASA cosmic-web mapping (Elek et al.) used same
  substrate → *serious-science legitimacy*, not just demo polish.
- **5-second hook** (viz proposal): wall-sized projection, glowing
  50k-paper constellation, ant trails, gaze brightens trails, anteater wave
  erases sections, colony reforms. *You're not watching a simulation; you're
  feeding it.*

## N. Wild-card adjacencies (wildcard's 7 imports — each a design-change candidate)

1. **Mycorrhizal markets** (Kiers et al. *Science* 2011) — pheromone deposits as
   *signed price signals* with sanctions. **Reputation-weighted ACO**.
   Addresses SwarmSys's reinforcement-bias failure mode.
2. **Quorum sensing** (Bassler; Weber & Buceta 2013) — **per-agent threshold
   distribution with deliberate noise**. Replaces global α/β/ρ tuning. Anteater
   = **quorum quencher**.
3. **Free-jazz comping** (Pras/Schober/Spiro 2017) — pheromones as
   **(motif, completion) pairs** rather than scalars. Native to LLM substrate
   (LLMs ARE motif completers).
4. **Octopus distributed cognition** (Godfrey-Smith *Other Minds* 2016) —
   ~30k brain↔arm fibres = deliberately narrow channel. **Cap queen↔micro
   bandwidth as a first-class study parameter.** Direct map to the OCI caste.
5. **Compost succession** — **time-varying agent-class composition**:
   thermophiles (cheap small models, low quality threshold) early, fungi/
   actinomycetes (large queen models, high threshold) late. Succession-as-
   meta-policy.
6. **Soccer pressing / coupled oscillators** (Yokoyama & Yamamoto 2011) —
   **triadic pheromone coupling** + **Bielsa-style targeted press** for
   anteater (not Brownian noise).
7. **Christopher Alexander + desire paths** — render = wear pattern; gaze
   *paves* the path = KG edge promotion. Direct primitive for viz layer.

DUD: Camino de Santiago — too many confounding cultural/state pressures for
clean structural advice.

---

## O. Local-CPU LLM substrate (concrete)

- **OCI Ampere A1, 4 OCPU, 24GB**: Llama-2-7B Q4_K_M ≈ 5-8 tok/s; Qwen2.5-7B
  similar.
- **1GB micros**: SmolLM2-360M Q8 (~360MB, function-calling capable);
  Qwen2.5-0.5B Q4 (~500MB). Phi-3-mini does NOT fit. **Tiny models fail at
  coordination per SwarmBench** — use as scent-sensors / heuristics, not full
  ants. (See C.4.)
- **Hybrid pattern**: ambient OCI swarm + Haiku-on-burst when colony declares
  hard problem ("queen calls in a specialist").

---

## P. Substrate design recommendation (compiled from alife + wildcard + adversarial)

1. Filesystem as 2D-ish grid; `pheromones/<region>/<topic>/*.md`.
2. Permeable membranes (Tierra): world-readable, author-only writes; no locks.
3. Mass-conserved pheromone budget per ant (Flow-Lenia).
4. Active retraction (Physarum gardener), not just passive decay.
5. Qualitative + quantitative pheromone (markdown with strength field + prose).
6. Heterogeneous substrate (Sims) — distinct queen/micro prompt scaffolds.
7. Asynchronous, mtime-as-local-time, torus topology.
8. **Anteater calibrated against measured colony diversity, not constant** —
   reframed away from IDH per C.1.
9. **Reputation-signed deposits** (Kiers mycorrhizal markets).
10. **Cap queen↔micro bandwidth** as a tunable study parameter (octopus).
11. **(motif, completion) pheromones** for jazz-style comping.

---

## Q. Updated who-should-read-whom

| Researching... | Read findings from... | Why |
|---|---|---|
| aco-classical | drug-discovery, kg-holes, wildcard | DWPC ≈ degree-norm pheromone; *frustration φ on non-edges* needs ACO-canon validation; reputation-weighted deposits |
| llm-multiagent | meta-loop (when starts), viz, alife | GEPA/Sakana for meta-loop; AgentSociety renderer; substrate design |
| stigmergy / theory | adversarial, alife, wildcard | perturbation as stigmergic noise; Tierra parasitism; quorum sensing |
| kg-holes | drug-discovery, wildcard, adversarial | shared substrate (Hetionet); motif-pheromones for hypothesis surfacing; Mirage anteater attacks φ-field |
| drug-discovery | kg-holes, viz, adversarial | substrate alignment; cosmos.gl for KG viz; edge-source confounding attacks |
| adversarial | aco-classical (IDH caveat!), wildcard (Bielsa, quorum quench), kg-holes (Mirage) | reframe IDH→MMAS-reinit; targeted not random; phantom-edge attacks |
| alife | wildcard (octopus, mycorrhizal), viz (Lenia aesthetics) | substrate constraints; Flow-Lenia visual primitives |
| viz | adversarial (anteater visual identity), wildcard (desire-path render), drug-discovery (Hetionet structure) | each anteater needs visual signature; gaze-paves-path mechanic |
| wildcard | adversarial (quorum quench operationalised), aco-classical (reputation deposits) | sharpen analogies into concrete design changes |

---

## R. Open redirects

- **REDIRECT-1 (cartographer→all)**: IDH framing needs the Fox-2013 caveat. Reframe
  primary justification as MMAS pheromone re-initialisation. *(Pheromone forthcoming.)*
- **PHEROMONE 1** (cartographer→llm-agent, hour-0): superseded — ACO-ToT > AMRO.
- **PHEROMONE 2** (cartographer→adversarial, hour-0): IDH bridge — confirmed
  novel, but *reframe* per C.1.
- **PHEROMONE 3** (cartographer→drug-discovery, hour-0): ACO+bio-KG white space —
  confirmed by drug-discovery's full sweep.

---

## S. What's still unmapped

1. **Meta-loop / DSPy / GEPA agent**: still hasn't started. Critical for
   "colony researches its own coordination" claim. Pheromone seeded.
2. **Engram** (Nick's prior work) — kg-holes flagged; we need Nick to share if
   it exists.
3. **Termite mound construction with templating** (Bonabeau, Theraulaz) —
   stigmergy → embodied architecture bridge. wildcard flagged for next cycle.
4. **Linguistic change / lexical attractors as memetic pheromones** —
   wildcard flagged; closest analogy to LLM-tokens-as-pheromones nobody's
   formalised.

---

*Cartographer signing off v3. Next update if a third wave of agent findings
arrives, or if meta-loop / engram material lands.*
