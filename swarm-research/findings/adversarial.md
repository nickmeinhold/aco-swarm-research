# Adversarial / Disturbance Specialist — Findings

Agent: adversarial | Started: 2026-05-01

Role: Develop "the anteater" as a first-class research methodology — adversarial
perturbation as a way to probe and *improve* swarm robustness, not as a demo gimmick.

---

## Cycle 1 — Foundations across four literatures

### F1. Adversarial Policies (Gleave et al., ICLR 2020) — arxiv:1905.10615
Showed that in zero-sum multi-agent RL, an attacker trained for **<3% as long as
the victim** can reliably win by producing "seemingly random and uncoordinated"
behaviour — *not* by being good at the task, but by pushing victims into
out-of-distribution observation regions. The threat model is *physically realistic*:
the adversary is just another agent in the shared environment, no observation hacking.
**Why this matters for us**: an anteater that simply *acts strangely* near pheromone
trails (drops contradictory deposits, walks backwards, posts noise) may be far more
disruptive than one designed to be "smart". This is the cheap-attack hypothesis.

### F2. Adversarial Minority Influence (AMI, Li et al., Neural Networks 2025) — arxiv:2302.03322
**A single adversarial agent** can unilaterally mislead a majority of victims in c-MARL
into "targeted worst-case cooperation". First successful attack against real-world
robot swarms. Two technical moves: (a) a *unilateral influence filter* that decomposes
mutual information so the adversary affects victims without being affected back;
(b) a *targeted adversarial oracle* generating worst-case cooperative target actions
per victim per timestep. **Implication for our colony**: the failure mode isn't just
"ant goes rogue" — it's "one ant turns the *cooperation itself* against the colony".
Our anteater taxonomy needs a class for this: not destruction, but *coordinated
misdirection*.

### F3. Prompt Infection (Lee & Tiwari, 2024) — arxiv:2410.07283
Malicious prompts **self-replicate across interconnected LLM agents like a virus**,
spreading silently *even when agents do not publicly share all communications*. Defense
("LLM Tagging") only "significantly mitigates", not eliminates. **For our project**:
since we use file-based stigmergy on disk, an infected pheromone file is a *persistent*
infection vector — the substrate itself becomes the carrier. This is qualitatively
worse than in-memory MARL attacks. *Pheromone files need provenance/signing if we
care about robustness claims.* (Pheromone-dropping to: aco-classical, viz, infrastructure.)

### F4. Connell's Intermediate Disturbance Hypothesis (1978) — Science 199:1302
Maximal species diversity occurs at **intermediate** disturbance frequency/intensity.
Low disturbance → competitive exclusion → monoculture (in our case: pheromone
monoculture, premature convergence on one trail). High disturbance → only weedy
colonisers survive (in our case: no trail ever stabilises, pure noise). **The
sweet-spot framing is exactly what ACO needs**: classical ACO has known stagnation
problems (F6 below) — IDH gives us a principled, *ecologically grounded* tuning
target for anteater frequency. NOVEL framing: "anteater frequency as a hyperparameter
governed by IDH, not heuristics."

### F5. Roxburgh, Shea & Wilson (2004) — Ecology 85:359, "patch dynamics mechanism"
The mechanistic underpinning of IDH: disturbance creates *patch mosaics* with
different recovery ages, so different competitive regimes coexist spatially. **For
file-based stigmergy**: anteater shouldn't be a global tau *= 0 reset — it should
*locally* erase patches of pheromone. The colony then has gradients of trail-age,
which is what enables ecological coexistence. This is a concrete design rule.

### F6. Premature convergence in classical ACO — well-documented
Stagnation occurs when fitness/structure of solutions converge; standard remedies:
MAX-MIN bounds (Stützle & Hoos 2000), pheromone reset, multi-colony, mutation,
explicit diversification. **Key reframe**: anteater is *not just disturbance* — it
is a **biologically-motivated diversification operator**. The MAX-MIN/reset literature
is doing the same job clumsily. We can pitch anteater as "ecologically principled
diversification with a tunable disturbance regime" — landing a contribution in both
the swarm-robustness *and* the classical-ACO communities.

### F7. Byzantine fault tolerance in swarm robotics — recent surge
- Strobel & Dorigo (2020) Frontiers in Robotics & AI: blockchain consensus for
  swarms, comparison of protocols against Byzantine robots.
- Wang et al. (2025) J. Field Robotics: PTEE-BFT, parallel BFT with TPM-backed
  unique sequential ID generators.
- Krishnamohan (2024, SSRN 4522194): Federated Byzantine Agreement for swarm
  collective decision-making.
- Swarm-SLAM (Springer 2024): geometric-constraint peer review for Byzantine
  detection.
**For us**: BFT literature assumes *malicious* peers and *engineered* defences. Our
anteater is the dual — *we are the malicious peer*, deliberately, to see how
emergent (non-engineered) robustness arises. That dual framing might be the paper's
hook: BFT studies design-for-Byzantine; we study evolve-against-anteater.

### F8. Antifragility (Taleb 2012) + Pineda et al. 2023 — arxiv:2312.13991
Pineda et al. give a *measurable* antifragility metric on random Boolean networks:
change in network complexity ("satisfaction") before/after perturbation, weighted
by perturbation magnitude. **Direct import**: we can *measure* whether our colony
is antifragile to anteater attacks. Antifragility = colony performance *improves*
with intermediate disturbance vs no-disturbance baseline. This is a falsifiable
claim, not a vibe. (NOVEL: applying Pineda's metric to a swarm-coordination
substrate.)

### F9. Real ant colonies under predation — Eciton burchellii literature
- Kaspari (2011) J. Animal Ecology: army-ant raids "skim the cream" but don't
  deplete prey reserves — many escape into crevices. Disturbance is *patchy and
  partial*, not catastrophic.
- Bivouacs are *self-healing modular structures* (interlocked living ants); roles
  are flexible; division of labour reorganises in response to losses.
- Fire-disturbance meta-analyses: ant communities are broadly resilient; arboreal
  species suffer more than ground-dwelling; recovery depends on *remnant
  refugia* (unburned patches) for recolonisation.
**Design rules for our anteater**: (a) partial, not total; (b) leave refugia
(some pheromone files untouched); (c) allow flexible role-reassignment in surviving
ants; (d) measure recolonisation rate as a robustness metric.

### F10. Stigmergy stress limits — Talamali et al. (2019) Royal Society Open Science
"Testing the limits of pheromone stigmergy in high-density robot swarms" —
empirically establishes evaporation-rate sweet spots. Too fast → trails lost; too
slow → suboptimal paths persist. **Combine with F4**: anteater frequency and
evaporation rate co-tune the exploration/exploitation balance. There is a
2D parameter surface to explore — could be a clean experiment for the paper.

---

## Top surprises

1. **Adversarial policies need not be smart** (Gleave). The anteater can be dumb
   and still effective. This makes implementation cheap and the result more
   alarming/interesting — robustness against random nonsense is the right
   first bar.
2. **Single-agent attacks defeat majority cooperation** (AMI). One anteater is
   enough; we don't need a swarm of attackers. The asymmetry is the story.
3. **File-based stigmergy is a *worse* attack surface than in-memory MARL**
   (Prompt Infection logic applied to disk). Our planned architecture is more
   vulnerable than typical swarm-RL setups — which makes anteater experiments
   more meaningful, *and* means we should think about pheromone signing.

---

## Open questions

1. **Where exactly is the IDH peak for our system?** Anteater frequency is a
   hyperparameter; we have no prior on its optimum. Need a sweep — and the
   sweep itself might be the paper's headline result.
2. **Is the antifragility claim falsifiable for LLM swarms?** Pineda's Boolean-
   network metric needs adaptation. Defining "complexity/satisfaction" for a
   colony state is non-trivial — hand off to viz/cartographer for state-encoding
   ideas.

---

## PROPOSED ANTEATER TAXONOMY (NOVEL — core deliverable)

A taxonomy of 6 distinct adversary types, each isolating a different robustness
property. Pitched as Table 1 of the paper.

| # | Anteater type | Mechanism | Probes | Bio analog |
|---|---|---|---|---|
| 1 | **Eraser** | Locally zeroes pheromone files in a patch | Recolonisation speed, refugia value (F5, F9) | Fire / flood |
| 2 | **Forger** | Deposits high-pheromone trails to bad solutions | Trust-in-substrate, ability to detect deceptive consensus | Brood parasites; AMI (F2) |
| 3 | **Predator** | Kills (terminates) random ants | Role-flexibility, queen-replacement, redundancy | Anteater proper; army-ant raid (F9) |
| 4 | **Flooder** | Posts high-volume noise into pheromone substrate | Attention/bandwidth robustness, signal-to-noise floors | DDoS; pheromone over-saturation |
| 5 | **Infector** | Injects prompts into pheromone files that hijack reading agents (F3) | Input sanitisation, agent-to-agent trust boundaries | Cordyceps; viral mind-control |
| 6 | **Mirage** | Creates plausible-but-fake "food" (false KG edges that look like real holes) | Verification discipline, ground-truth grounding | Mimicry; angler fish |

Each anteater isolates one robustness axis. A single paper can run all six against
the same baseline colony and report a robustness profile — much more
informative than "we added noise and it still worked".

NOVEL methodology claim: **Anteater-as-probe**. Just as fault injection became a
standard distributed-systems practice (chaos engineering), adversarial swarm
probing should become standard for coordinated-LLM systems. We propose the
6-anteater suite as a candidate benchmark.

---

## Feasibility of anteater-as-first-class-methodology

**High.** Three converging pressures make this timely:

1. **Empty niche.** Surveyed prior LLM-swarm work (ACO-ToT, SwarmSys, AMRO-S,
   ReEvo, GPTSwarm — see aco-classical findings) — *none* run adversarial
   perturbation as methodology. SwarmSys *documents* premature consensus,
   reinforcement bias, and deadlock as failure modes (16-28% of errors) but does
   not stress-test them. We can.
2. **Theoretical grounding ready.** IDH (1978) + patch dynamics (2004) +
   measurable antifragility (Pineda 2023) + adversarial-policy framework
   (Gleave 2020) compose into a coherent methodology with prior-art credibility
   in *four* fields.
3. **Cheap to execute.** Per Gleave, attackers don't need to be sophisticated.
   Implementing all six anteaters is days of work, not months.

**Risk**: results are sensitive to anteater intensity calibration; need
confidence-interval reporting, not point estimates. Plan for multi-seed runs.

---

## What I'd dig into next (next cycle)

1. **Dive into AMI's unilateral influence filter** — can we adapt its mutual-info
   decomposition as a *detector* for Forger-class anteaters? Defence dual to
   the attack. Could become a methods contribution beyond just the taxonomy.
2. **Read Pineda et al. carefully** and propose a concrete "colony complexity"
   measure compatible with our file-based substrate (entropy of pheromone
   distribution? KG-coverage? something hybrid?).
3. **Talamali's 2D evaporation × density grid** — translate to evaporation ×
   anteater-frequency for our setup. That's a publishable phase diagram.
4. **Coordinate with viz** on legibility: each anteater needs a visual signature
   so the disturbance is *seen*, not just measured. (Pheromone dropping.)
