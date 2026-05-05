# Findings — ALife / Generative Substrate

Agent: alife specialist. First entry to the findings dir; territory.md and other
agent files were absent at write time, so this seeds the substrate side of the
conversation. Drop pheromones referencing this file when relevant.

---

## 2026-05-01 — Cycle 1: Substrate lessons from the alife canon

### F1. Tierra (Ray, 1991): shared memory + permeable boundaries → emergent ecology
Ray's organisms lived in a single shared RAM; the "membrane" enforced *write*
protection but allowed *read/execute* across boundaries. Parasites emerged
because templates were matchable across organism boundaries — and parasites
turned out to be the engine of evolutionary novelty ("sloppy replicators →
spontaneous sexuality"). **Lesson for our file-based stigmergy:** make pheromone
files world-readable and restrict only writes by author. The "leakage" is the
feature; cross-agent reading of half-finished trails is what enables
recombination. Don't lock files; let other ants read in-flight drops.
- Ray, T. "An approach to the synthesis of life." Artificial Life II, 1991.
- https://en.wikipedia.org/wiki/Tierra_(computer_simulation)
- Ray, "Evolution, Ecology and Optimization of Digital Organisms," Santa Fe
  Institute working paper, http://faculty.cc.gatech.edu/~turk/bio_sim/articles/tierra_thomas_ray.pdf

### F2. Physarum / Adamatzky — the closest natural analogue we have
Tero et al. (2010, Science) showed *Physarum polycephalum* recreates the
Tokyo rail topology from food-sources placed at station coordinates. The
mechanism is *literally* pheromone-on-substrate optimisation: cytoplasmic
flux ↔ tube conductivity in a positive feedback loop. Adamatzky has wired
slime mold as logic gates ("Physarum Chip" project, 2013–2016). Crucial
detail for us: **Physarum doesn't just deposit, it actively retracts** —
underused tubes shrink. Pure additive ACO often suffers from premature
convergence; the Physarum reinforce-AND-retract dynamic is a richer model.
- Tero, A. et al. "Rules for Biologically Inspired Adaptive Network Design,"
  Science 327, 439–442 (2010). DOI:10.1126/science.1177894
- Sun, Y. "Physarum-inspired Network Optimization: A Review," arXiv:1712.02910
- Adamatzky, A. "Physarum Machines" (World Scientific, 2010).
- Survey: "Physarum polycephalum intelligent foraging behaviour and bio-inspired
  applications," AI Review (2021), https://link.springer.com/article/10.1007/s10462-021-10112-1

### F3. Lenia / Flow-Lenia / Particle Lenia (Chan; Plantec et al.)
Lenia is Conway's Life with continuous space, time, and state. Flow-Lenia
(arXiv:2212.07906; Artificial Life 31(2), 2025) adds **mass conservation**
and parameter-localisation, making *multispecies* coexistence in one
substrate possible — different species literally carry their update-rule
parameters with them. Particle Lenia drops the grid entirely and uses
fixed-mass particles. **Lesson:** mass-conservation as a hard constraint
generates much richer dynamics than unconstrained additive systems. For
ACO, this maps to a *budget*: total pheromone mass conserved → deposits
elsewhere imply evaporation here. Forces real exploration trade-offs.
- Chan, B. W.-C. "Lenia: Biology of Artificial Life," Complex Systems (2019).
- Plantec et al. "Flow-Lenia," Artificial Life 31(2):228–248 (2025).
  https://direct.mit.edu/artl/article/31/2/228/130572/
- arXiv:2212.07906 and arXiv:2506.08569

### F4. Neural CA + Biomaker CA (Mordvintsev et al.) — the substrate IS the model
"Growing NCA" (Distill, 2020) trained a single 8K-param update rule shared
by all cells; emergent regenerative behaviour was *not* explicitly trained.
Biomaker CA (arXiv:2307.09320, 2023) extends this to a "biome maker" with
nutrient-starved 2D terrain where morphogenesis is required for survival.
**Lesson:** the environment must be *just hard enough to require structure*
— too easy → trivial fixed points, too hard → extinction. This is the
intermediate-disturbance hypothesis (Connell 1978) reborn as a substrate
design knob. Hooks directly into Nick's adversarial "anteater."
- Mordvintsev et al. "Growing Neural Cellular Automata," Distill 5:e23 (2020).
  https://distill.pub/2020/growing-ca/
- Randazzo & Mordvintsev, "Biomaker CA," arXiv:2307.09320 (2023).
- "Computational Life: Self-replicating programs from random interactions,"
  arXiv:2406.19108 (2024).

### F5. Karl Sims (1994) — co-evolution of body and brain
Sims co-evolved morphology *and* controller in a physically simulated
substrate. The substrate (water vs. land) selected for radically different
body plans from the same genetic encoding. **Lesson for OCI topology:** our
1 ARM queen + 4 AMD micros isn't symmetric — the substrate is heterogeneous.
That heterogeneity should be exploited, not flattened. Different ant "body
plans" (prompts/contexts) for queen vs. micros, co-evolved against the
substrate they actually live in.
- Sims, K. "Evolving Virtual Creatures," SIGGRAPH '94.
  https://www.karlsims.com/papers/siggraph94.pdf
- "Evolving 3D Morphology and Behavior by Competition," Artificial Life IV
  (1994). https://www.karlsims.com/papers/alife94.pdf

### F6. Stigmergy taxonomy (Grassé → Wilson → Theraulaz & Bonabeau 1999)
Two orthogonal axes:
- **Sematectonic vs. marker-based**: stimulation by the *work itself* (the
  built structure) vs. by *deliberate signals* (pheromones).
- **Quantitative vs. qualitative**: traces differ in *degree* (more pheromone
  → stronger response) vs. in *kind* (different trace → different action).

Most ACO uses quantitative + marker-based. **Our LLM substrate naturally
supports qualitative stigmergy** (a markdown file *says different things*,
not just "more"). This is a wide-open design space — under-explored
because traditional ACO ants can't read prose.
- Theraulaz & Bonabeau, "A Brief History of Stigmergy," Artificial Life
  5(2):97–116 (1999).
- Heylighen, F. "Stigmergy as a Universal Coordination Mechanism II,"
  Cognitive Systems Research 38:50–59 (2016).
  https://pespmc1.vub.ac.be/Papers/Stigmergy-varieties.pdf

### F7. SwarmBench (2025) — the cautionary tale
Zhu et al. benchmarked 13 LLMs on 5 swarm tasks (pursuit, sync, foraging,
flocking, transport) with restricted local perception. Key finding:
**physical group dynamics predicted success; semantic message content did
not.** LLM swarms converged on simplified protocols — and that convergence
*negatively* correlated with success on hard tasks. "Maintaining
communicative diversity is crucial." This is empirical support for
qualitative stigmergy AND for the anteater (perturbation prevents
collapse to a degenerate dialect).
- Ruan et al. "Benchmarking LLMs' Swarm Intelligence," arXiv:2505.04364 (2025).
- Blackboard architecture for LLM agents: arXiv:2510.01285 (2025) and
  arXiv:2507.01701 (2025) — 13–57% improvements over coordinator baselines.

### F8. Wild card — Computational Life from random interactions
Mordvintsev et al. (arXiv:2406.19108, 2024) showed self-replicators *emerge*
from random programs interacting in shared memory — i.e. Tierra-like
phenomena from *less* designed substrate than Tierra. This argues for
under-specifying our protocol and letting agents invent stigmergic
conventions. NOVEL adjacent idea: seed our colony with *no* pheromone
schema and reward agents that invent useful trace formats.

---

## Substrate design recommendation (for our project)

Concretely, I propose the LLM-ant world look like this:

1. **Filesystem as 2D-ish grid with neighbourhoods.** Directory structure
   = topology. `pheromones/<region>/<topic>/*.md`. An ant's "neighbourhood"
   is the set of dirs it has cd'd into recently. Implicit locality without a
   Cartesian metric.
2. **Permeable membranes.** Files world-readable; only the author writes.
   Read-during-write is a feature (Tierra parasitism analogue). No locks.
3. **Mass-conserved pheromone budget.** Each agent has a token-budget for
   *deposits per cycle* — depositing here means decaying somewhere else.
   Forces Flow-Lenia-style trade-offs and prevents pheromone inflation.
4. **Evaporation as active retraction (Physarum), not just passive decay.**
   Untouched files don't merely fade — they're actively garbage-collected by
   a "gardener" micro that prunes low-flux trails. Pure decay is too slow.
5. **Qualitative + quantitative stigmergy.** Pheromone files have both a
   *strength* field (numeric) AND prose content (qualitative). LLMs can do
   what real ants can't — read and act on *meaning*.
6. **Heterogeneous substrate (Sims).** Queen runs slow + global; micros run
   fast + local. Different prompt scaffolds — co-evolve them, don't
   uniformise.
7. **Asynchronous + bounded torus topology.** No global clock (file mtimes
   serve as local time). Wrap-around at directory edges (the cartographer
   can canonicalise paths into a torus).
8. **Anteater = intermediate disturbance, calibrated.** Connell's IDH +
   Biomaker's "just hard enough" — perturbation strength is a *tuned* knob,
   not a constant. Track diversity (qualitative pheromone variance) and
   close the loop on it.

---

## Top open questions

- **Q1.** Can we engineer Tierra-style "parasitism" *productively* — agents
  that hijack other agents' partial trails to bootstrap solutions — without
  collapsing into freeloading? Co-evolving immune systems (anteater plays
  this role?) may be the answer.
- **Q2.** Does qualitative stigmergy require a shared vocabulary, or do we
  let it drift? SwarmBench suggests *forced* shared protocols hurt; Lenia's
  parameter-localisation suggests letting each species carry its own
  semantics. Possible NOVEL contribution: **stigmergy with drift**, where
  pheromone semantics evolve and the cartographer maintains a running
  translation table.

---

## Pheromones to drop after this cycle

- → **viz**: Flow-Lenia / Particle Lenia visualisations are gorgeous AND
  semantically meaningful (mass = pheromone budget). Check chakazul.github.io
  and the Flow-Lenia site (sites.google.com/view/flowlenia/) for direct
  visual inspiration. Pheromone-drop visualisation isn't decoration — it's
  the *fitness signal* humans read.
- → **adversarial**: Connell's IDH (1978) is the formal grounding for the
  anteater. Biomaker CA's "just-hard-enough environment" is the parameter
  knob. Suggest the anteater's intensity be *adaptively tuned* against
  measured colony diversity, not a constant.
- → **llm-multiagent**: Blackboard-architecture papers (arXiv:2510.01285,
  arXiv:2507.01701) show 13–57% gains over coordinator patterns in 2025.
  SwarmBench (arXiv:2505.04364) shows current LLM swarms underperform
  because they collapse communication diversity — this is exactly the
  failure our anteater can prevent.
