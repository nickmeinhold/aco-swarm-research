# Cartographer — incremental notes

## 2026-05-01 — Cycle 0 (initial sweep)

Empty workspace; no other agents have written yet. Did a wide-radius sweep across
all 9 territories listed in the brief. Published `territory.md v1`.

**Hottest finding (collision risk):**

- **AMRO / AMRO-S** — arXiv 2603.12933, OpenReview `ojUhmgIS7o`. "Efficient and
  Interpretable Multi-Agent LLM Routing via Ant Colony Optimization". They model
  agent routing as semantic-conditioned path selection with task-specific
  pheromone-specialist memory pools and adaptive decay. **This is the nearest
  prior art to Nick's project.** Crucially: they do **agent routing**, not
  **knowledge-graph search**, and pheromones are *learned routing memory* not
  *file-system marks*. So the differentiation is real, but the related-work
  section will live or die on this paragraph.

**Strongest white-space candidate:**

- ACO-on-biomedical-KGs is genuinely thin. Trent Leslie's Medium piece
  ("Unraveling Biomedical Mysteries: ACO in Knowledge Graphs", 2024) is one of
  the few public mentions. PLANTS et al. operate on *molecular* graphs.

**Wild-card I want to chase:**

- Connell's intermediate-disturbance hypothesis (1978) does *not* appear in the
  Byzantine-swarm or adversarial-MAS literature I've seen. Bridging IDH to
  Byzantine swarms (the "anteater") could be a self-contained paper. Dropping a
  pheromone for whoever takes adversarial.

**Surprises:**

1. Sakana AI Scientist v2 was published in *Nature* in 2025 — closer prior art for
   the *meta-loop* than I expected. Nick's framing ("colony researches its own
   ACO") needs to be careful here.
2. Bonabeau, Dorigo & Theraulaz "Swarm Intelligence: From Natural to Artificial
   Systems" (1999) is *still* the canonical text. 27 years old.
3. The Frontiers in AI 2025 survey (PMC12135685) explicitly demos LLM-driven ant
   foragers and bird flockers — claiming first-of-kind. Worth a careful read; might
   be either huge prior art or thin demo-ware.

**Pheromones dropped this cycle:**

- `pheromones/2026-05-01-0000-cartographer-to-llm-agent.md` — AMRO collision warning.
- `pheromones/2026-05-01-0000-cartographer-to-adversarial.md` — IDH bridge opportunity.
- `pheromones/2026-05-01-0000-cartographer-to-drug-discovery.md` — ACO+biomedical-KG
  is your white space; dig there hardest.

**Sources used this cycle (for citations later):**

- arXiv 2603.12933 (AMRO)
- arXiv 2105.03546 (stigmergic MARL)
- Frontiers AI 2025 / PMC12135685 (LLM swarm survey)
- Springer 10.1007/s10462-024-10885-1 (LBD active curriculum)
- ScienceDirect S1532046423001855 (Alzheimer LBD KG embedding)
- MDPI 15/16/8785 (hybrid LBD with LLMs)
- Springer 10.1007/s10910-023-01549-6 (augmented ACO virtual drug)
- Springer 11839088_22 (PLANTS)
- PMC2867149 (pharmACOphore)
- Nature s41598-018-34454-z (metabolic ACO)
- arXiv 2508.00622 (SwarmRaft)
- ScienceDirect S0951832025009809 (V-WMSR vigilance)
- Roxburgh et al. 2004 IDH formalisation
- arXiv 1812.05433 (Lenia)
- Royal Society 10.1098/rsfs.2018.0029 (Adamatzky fungal computer)
- sakana.ai/ai-scientist-nature/ (AI Scientist v2 in Nature)
- arXiv 2409.18659v2 (EDGAR drug-repurposing KG)
- Nature s41597-023-02757-0 (OREGANO KG)
- Heylighen "Stigmergy as a generic mechanism for coordination"
- DTIC ADA441283 (Parunak / DoD stigmergy assessment)

## 2026-05-01 — Cycle 1 (after first wave of agent findings)

Read: `aco-classical.md`, `drug-discovery.md`, `llm-multiagent.md`, `viz.md` (stub),
`wildcard.md` (stub), and 4 cross-agent pheromones.

**Big update**: prior-art picture has shifted significantly. **ACO-ToT (arXiv
2501.19278, Jan 2025)** is closer prior art than AMRO — five fine-tuned Llama-70B
agents walk a Tree-of-Thought graph with literal pheromones, GSM8K +28.6%. Plus
SwarmSys, ReEvo, CodeCRDT, GPTSwarm all in-band. The "LLM-as-ant" idea is
demonstrably in the air — multiple groups arrived at it 2024-26.

Published `territory.md v2` with a 5-paper **prior-art collision register at the
top**, surviving novelty list, and per-section updates.

**Convergent signals (multiple agents, independently):**
1. **Anteater × Connell IDH** — confirmed absent by both me and llm-multiagent.
2. **ACO + biomedical KGs** — confirmed thin by both me and drug-discovery.
3. **File-system substrate** — confirmed novel by llm-multiagent's deep sweep.

**Surviving novelty surface (post-collision):**
filesystem-substrate, heterogeneous compute caste, anteater × IDH, dual-objective
meta-loop, viz-as-fitness, KG-hole-finding-as-foraging.

**Pheromones dropped this cycle:**
- `2026-05-01-0100-cartographer-to-all-PRIORART-UPDATE.md` — broadcast
- `2026-05-01-0100-cartographer-to-meta-loop.md` — GEPA + Sakana anchors
- `2026-05-01-0100-cartographer-to-viz.md` — Picbreeder + AgentSociety + gaze IGA

**Bullshit-flag candidate**: SwarmSys "GPT-4o swarm ≈ GPT-5 single-agent perf"
is a load-bearing claim with no released code. Cite cautiously; could be
overclaim.

**Worth chasing next cycle**: meta-loop / DSPy / GEPA agent hasn't started; will
seed if still empty next cycle. Same for adversarial, kg-holes, alife.

## 2026-05-01 — Cycle 2 (after second wave: adversarial + alife + kg-holes + viz + wildcard all wrote)

Read all 8 specialist findings + 30+ pheromones. Published `territory.md v3` —
major restructure. Three NOVEL constructs have crystallised; prior-art register
expanded; IDH justification needs caveat per aco-classical's Fox-2013 flag.

**Three NOVEL constructs (now §A of territory.md):**

- **A1. Frustration pheromone φ on non-edges** (kg-holes). LLM-ant queries
  desired-next-node; if not a neighbour, deposit pheromone on the *missing edge*.
  Operationalises Burt 1992 structural holes directly. Apparently absent from
  ACO canon (anti-pheromone exists but only on real edges).
- **A2. Six-anteater taxonomy + Pineda antifragility metric** (adversarial).
  Eraser/Forger/Predator/Flooder/Infector/Mirage. Each isolates a robustness axis.
  *File stigmergy is a worse attack surface than in-memory MARL* (Prompt Infection
  arXiv 2410.07283).
- **A3. Stigmergic human-AI cohabitation** (viz). Human gaze (WebGazer.js) is a
  pheromone deposit on the *same* substrate. Human as ant-with-high-bandwidth-
  sensors, not external oracle.

**Major caveat from aco-classical**: Connell 1978 IDH is *contested* (Fox 2013).
Posted REDIRECT pheromone advising reframe to MMAS pheromone re-initialisation
(Stützle & Hoos 2000) as primary justification. Anteater = "MMAS re-init dressed
for the gallery" — ties novelty to proven ACO prior art.

**Wildcard delivered 7 imports**, each a concrete design-change candidate:
mycorrhizal markets (reputation-weighted deposits) | quorum sensing (per-agent
threshold distribution) | jazz comping (motif/completion pheromones) | octopus
(capped queen↔micro bandwidth) | compost succession (time-varying agent-class
composition) | soccer (triadic coupling + Bielsa press) | desire paths (gaze
paves edge promotion).

**Pheromones dropped this cycle:**
- `REDIRECT-2026-05-01-cartographer-IDH-reframe.md` (broadcast — pivot framing)
- `2026-05-01-0200-cartographer-to-aco-classical-and-kg-holes.md` (verify A1
  against deep ACO canon; it's our most defensible novelty)

**Bullshit-flag updates:**
- SwarmSys "GPT-4o ≈ GPT-5" — still no code released. Caveat on cite.
- Trent Leslie Medium ACO-on-SPOKE — *blog, not implemented* (kg-holes confirmed).
- IDH itself — Fox 2013 critique is genuine; reframe required.

**What's still missing**: meta-loop / DSPy agent never started. Engram (Nick's
prior work) hasn't surfaced. Termite-mound templating + linguistic-drift-as-
pheromone are wildcard's next-cycle targets.
