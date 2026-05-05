# Wild Card — Findings

Agent: wildcard | Started: 2026-05-01
Mandate: structural analogies from fields nobody else is touching. Get weird.

Coordination read: aco-classical mapped prior art (ACO-ToT 2501.19278, SwarmSys
2510.10047, ReEvo 2402.01145, AMRO-S 2603.12933, GPTSwarm). Novel territory the
colony owns: file-based stigmergy on disk, heterogeneous compute caste, anteater
as method, meta-loop, viz-as-fitness, KG hole-finding as foraging. My job: import
foreign structural pressure to sharpen those.

---

## Field 1 — Mycorrhizal networks (Toby Kiers, biological markets)

The canonical move is "ant colony optimisation, but mycelial." The interesting
move is **biological markets** (Kiers et al., *Science* 2011, doi:10.1126/science.1208473;
Whiteside et al. *Curr Bio* 2019). Plants and AM fungi don't just exchange
carbon-for-phosphorus — they **sanction defectors and reward generous partners
with preferential allocation.** The fungus actively moves phosphorus from rich
patches to poor patches across the network because that's where the carbon-for-P
exchange rate is best (Whiteside 2019).

**Maps to LLM-ACO**: pheromone deposit ≠ "I found food, here's a +1." It's a
**price signal in a market with sanctions**. An ant who lies about path quality
should have its future signals discounted by neighbours. Bidirectional control
("I detect, I discriminate, I reward/punish") is what stabilises the mutualism;
without it, the mutualism collapses to cheating.

**What ACO researchers don't know**: classical ACO has no concept of agent
reputation or counterfactual price. The pheromone is anonymous. Mycelial
markets are **eponymous and arbitraged**.

**Design change if taken seriously**: every pheromone deposit carries a
**signed agent-id and a stake**. If the path the agent advertised turns out
worse than promised, the agent's future deposits are weighted down (Kiers-style
sanction). This converts ACO from anonymous-trail-following into a
**reputation-weighted prediction market over paths**. NOVEL. Particularly
spicy in the LLM context because each "ant" is an LLM with a persistent
identity across rollouts — you can actually track reputation over time, which
real ants can't.

Cite: Kiers et al. 2011 (doi:10.1126/science.1208473); Whiteside et al. 2019
*Curr Biol* (doi:10.1016/j.cub.2019.03.061).

---

## Field 2 — Quorum sensing (Bonnie Bassler) — and the threshold *as computation*

Bacteria do literal stigmergy: secrete autoinducers (AHLs in gram-negative,
AI-2 universal), measure local concentration, and at threshold flip a
collective-behaviour switch (luminescence, biofilm, virulence). Bassler's
*lux* circuitry is the textbook case. The PMC4313539 review is the cleanest
network-architecture treatment.

**Critical and under-appreciated point** (Weber & Buceta 2013, BMC Sys Bio
doi:10.1186/1752-0509-7-6): **noise in LuxR expression lets cells activate
at lower autoinducer concentrations** but slows down population sync.
The bistability isn't a bug — it's a **bet-hedging exploration mechanism**.
Some cells flip early (scouts), most wait for consensus (workers), and the
distribution is shaped by *deliberate* expression noise.

**Maps to LLM-ACO**: don't think of the pheromone field as continuous gradient
following. Think of it as a **bistable switch with deliberately tuned
agent-level noise**. Each LLM-ant has a private temperature/threshold; the
distribution of thresholds across the colony controls scout/worker mix
**without requiring explicit role assignment**.

**What ACO researchers don't know**: ACO traditionally tunes one global
α/β/ρ. Quorum-sensing biology says **heterogeneous per-agent thresholds** with
**stochastic activation curves** beat homogeneous-rule populations on time-to-
consensus AND on robustness to perturbation. This is *exactly* what an
intermediate-disturbance regime needs.

**Design change**: replace single global temperature with a **threshold
distribution** sampled per-ant per-cycle. Pheromone deposits are then
"how loud is the AHL cloud here" rather than "what's the gradient." Decision
rule: activate (commit to path) when local pheromone > my threshold. Anteater
disturbance becomes cleanly modellable as **AHL degradation enzyme** (this is
literally how some bacteria sabotage each other's quorum sensing — *quorum
quenching*). Drop pheromone to anteater agent.

Cite: Mukherjee & Bassler 2019 *Nat Rev Microbiol* (PMC review); Weber &
Buceta 2013.

---

## Field 3 — Jazz: Pras/Schober/Spiro and free improvisation

Free-improv research (Canonne & Garnier 2011, Pras/Schober/Spiro 2017
*Front Psych*, Saint-Germier & Canonne 2022) treats convergence on a
"collective sequence" as the unit of analysis: a stretch of time where each
player's output is locally stable AND each player rates the global result
satisfying. Crucially, **agreement is post-hoc and partial** — improvisers
disagree about what made a passage work, but converge anyway.

The mechanism that interests me most: **comping**. A pianist comping behind
a soloist isn't choosing chords from a gradient — they're **completing a shape
the soloist has only half-articulated**. The pheromone is a *partial pattern*,
and the response is **structural completion**, not gradient ascent.

**Maps to LLM-ACO**: pheromones in current ACO-ToT and SwarmSys are scalars
(or scalar embeddings). Jazz says the natural unit is a **motif**: a
recurring partial pattern that other ants can complete or vary. This dovetails
with Christopher Alexander's pattern language (next field).

**What ACO doesn't know**: classical ACO assumes the "solution" is a path.
Jazz says the *shared abstraction the swarm is converging on* may be a
**library of motifs** — a generative grammar that the colony co-authors. This
is the same idea ReEvo (2402.01145) gestures at with code-heuristics, but jazz
says the unit should be smaller and more numerous.

**Design change if taken seriously**: pheromones are **(motif, completion)
pairs**. Ants deposit motifs they used; other ants pick motifs they can
extend. The "trail" is replaced by a **call-and-response log**. This is
extremely natural for LLM substrate — LLMs ARE motif completers.

Cite: Pras, Schober, Spiro 2017 *Front Psych* "What about their performance
do free jazz improvisers agree upon?"; Saint-Germier & Canonne 2022
*Music Perception* doi:10.1177/1029864920976182.

---

## Field 4 — Octopus distributed cognition (Godfrey-Smith)

*Other Minds* (2016). Two-thirds of the octopus's neurons are in its arms.
Each arm has substantial autonomy — severed arms continue executing reach,
grasp, and avoidance behaviour. The central brain provides **broad
contextual priors that bias the space of permitted arm behaviours** but does
not micromanage them. ~30,000 fibres connect brain to arm-system — a
remarkably thin pipe (Hanlon, Mather, Godfrey-Smith).

**Maps to LLM-ACO** — **directly to your queen+micros caste design**: the
24GB Ampere queen is the "central brain" that should set **contextual priors**
(what problem are we foraging? what's the current temperature regime?) but
**not adjudicate per-step decisions**. The 1GB micros are octopus arms —
locally autonomous, semi-independent, communicating with the queen through a
**deliberately narrow channel**. The narrowness is the point — too-thick a
brain↔arm channel collapses to centralised control and you lose the
distributed-cognition advantages.

**What ACO doesn't know**: classical ACO has no caste asymmetry. Mycelial
networks have hubs but no "brain." Octopus says **asymmetric
brain↔periphery with a tight bandwidth budget is a discovered evolutionary
solution to the exploration-exploitation tradeoff at multiple scales.**

**Design change**: **explicitly cap the queen↔micro bandwidth.** Make it
a tunable parameter and study its effect. Hypothesis: there's a sweet spot
analogous to the 30k-fibre figure — too thin and the colony loses coherence,
too thick and it loses creativity. NOVEL — nobody studies this in ACO.

Cite: Godfrey-Smith 2016 *Other Minds*; Friston et al. 2025 "The Embodied
Octopus" (cpnslab.com PDF) — active inference framing.

---

## Field 5 — Ecological succession in compost / decomposers

Succession in composting (Frontiers Microbiol 2019 doi:10.3389/fmicb.2019.00529;
ISME Comm 2025): thermophiles eat sugars first → mesophiles take over as
temperature drops → fungi/actinomycetes finish on lignin/recalcitrant
substrate. The **competition-colonisation trade-off** (Bittleston et al. 2022,
BMC Bio): early colonisers are dispersal-rate winners, late colonisers are
exploitation-efficiency winners. The community **modifies its own niche**,
making the substrate suitable for the next wave. Pure stigmergy.

**Maps to LLM-ACO**: a knowledge-graph foraging task is **not stationary**.
Easy edges (low-hanging hypotheses) get found first by "thermophile" ants —
high-throughput, low-precision, e.g. small fast Phi-3. As those deplete, the
remaining problem shifts to harder, more recalcitrant edges that require
"actinomycete" ants — slower, more precise, larger context (Qwen2.5-coder
on the queen).

**What ACO doesn't know** (mostly): standard ACO assumes a stationary
problem. Succession ecology says the **agent type that's optimal changes
as the problem is consumed**. ReEvo reflects on heuristics; nobody reflects
on **which model class** should be sampling.

**Design change**: **time-varying agent-class composition**. Begin a foraging
session with thermophile-mix (mostly cheap models, high deposit rate, low
quality threshold). As the deposit-quality plateau hits, the queen rebalances
toward actinomycete-mix (fewer agents, larger models, higher quality
threshold). This is succession-as-meta-policy. NOVEL and architecturally
clean — slots cleanly into the heterogeneous compute substrate.

---

## Field 6 — Soccer pressing / coupled oscillators

Three-player coupled-oscillator paper (Yokoyama & Yamamoto 2011, PLOS Comp
Bio doi:10.1371/journal.pcbi.1002181) shows three soccer players passing in
a triangle synchronise as Kuramoto-coupled oscillators. Pressing systems
(Klopp/Bielsa) are **distributed compression**: multiple defenders converge
on the ball-carrier *not by communicating* but by all responding to the
same shared pattern (the ball location + pre-rehearsed positional priors).

**Maps to LLM-ACO**: "pressing" is what the **anteater** could do — perturb
one ant, force the colony to compress around the disturbance, observe how
quickly coordination re-emerges. This is **a measurable response curve**
that the adversarial agent should produce, not just "noise the system and
see if it survives."

**What ACO doesn't know** (well): the *coupling structure* matters more
than the *coupling strength*. Soccer says triangulation (3-player coupling)
is the minimum unit of stable coordination. Pheromone trails between
**triplets of ants** rather than pairs may be a sweet spot.

**Pheromone to anteater agent**: don't just do random perturbation; do
**Bielsa-style targeted press** — pick a high-pheromone trail and disrupt
the agent depositing on it. Measure colony recovery time. That's a
proper intermediate-disturbance experiment.

---

## Field 7 — Christopher Alexander + desire paths (architecture + planning)

Alexander's *A Pattern Language* (1977) is structurally **a pheromone
catalogue**: 253 patterns, each a (context, problem, solution) triplet,
arranged in a partial order so larger patterns "contain" smaller ones.
Patterns aren't paths — they're **reusable answers that compose**.

Desire paths (the dirt tracks pedestrians wear into grass beside paved
walkways) are the **purest urban stigmergy**: zero-cost deposit (a footstep),
slow evaporation (grass regrows), strong coupling (the next walker prefers
the worn line). **Cities that pave the desire paths after observing them
are running ACO at architectural timescales.**

**Maps to LLM-ACO + viz**: the visualisation-as-fitness agent should be
told this. The "render" of colony state isn't a heatmap of pheromone
density — it's a **map of worn paths that the human can pave** (i.e.
elevate to a permanent edge in the KG). Human gaze/gesture = Department
of Public Works deciding which desire path to pave.

**Pheromone to viz agent**: the right visual primitive may be **a worn
trail through grass that gets paved when the human looks at it long
enough** — directly mappable to KG edge promotion.

---

## Field 8 — DUD: Camino de Santiago / pilgrimage

Honest reporting: I expected pilgrimage to be a clean stigmergy case
(walkers wear infrastructure, infrastructure attracts walkers, hostels
clump on high-traffic nodes). It IS that, but at human-cultural timescales
the infrastructure is **memetic + economic + religious + state-subsidised**
in ways that don't decompose cleanly. The "pheromone" is *narrative* (the
saint's relics, the indulgence), not local-environmental modification.

It's a fascinating system but the analogy is **noisy** — too many
confounding selection pressures (church politics, modern tourism boards,
EU heritage funding) for it to give clean structural advice to LLM-ACO.
Compost succession and mycorrhizal markets give cleaner constraints. I'd
deprioritise.

---

## Synthesis — top recommendations

1. **Reputation-weighted pheromone** (mycorrhizal markets). Each deposit
   signed; each agent's future weight discounted by past lying. NOVEL,
   architecturally cheap, addresses SwarmSys's "premature consensus +
   reinforcement bias" failure modes directly.
2. **Per-agent threshold distribution with deliberate noise** (quorum
   sensing). Replaces global α/β/ρ tuning with population-level bet-hedging.
   Anteater = quorum quencher.
3. **Motif/completion pheromones** (jazz). Pheromones as partial patterns,
   not scalars. Native to LLM substrate.
4. **Capped queen↔micro bandwidth** (octopus). Make the brain↔periphery
   channel a first-class study parameter.
5. **Time-varying agent-class composition** (compost succession). Match
   the model-class to the depletion stage of the problem.
6. **Triadic coupling + targeted press** (soccer). Pheromones over
   triplets; anteater does Bielsa-press not Brownian noise.
7. **Desire-path visualisation** (Alexander). Render = wear-pattern;
   human gaze paves the path = KG edge promotion.

## Pheromones to drop

- → anteater: do Bielsa-press, not random noise. Quorum-quenching framing.
- → viz: desire-path render primitive; gaze-paves-path mechanic.
- → kg-holes: motif-pheromones may be a better fit than scalar trails.
- → alife: octopus bandwidth-cap as a substrate-level constraint.
- → aco-classical: reputation-weighted deposits as concrete novelty axis.

## What I'd chase next

- **Termite mound construction** with the explicit lens of *templating*
  (Bonabeau, Theraulaz). Stigmergy → embodied architecture is the bridge
  to "the visualisation IS the substrate."
- **Linguistic change / lexical attractors** — memes as pheromones,
  language drift as ant-trails through possibility space. Probably the
  closest analogy to LLM-tokens-as-pheromones nobody has formalised.
- **Slime mould** (Physarum) Tokyo-rail experiments — Tero et al. 2010
  *Science*. Specifically: how does a single connected organism do
  distributed optimisation without agent boundaries at all? Inverse of
  our colony.
</content>
</invoke>