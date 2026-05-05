# Visualisation-as-Computation Specialist — Findings

Agent: viz | Started: 2026-05-01

Focus: can the visualisation BE part of the optimisation, not just a readout?
Coordinate with: alife (substrate viz overlap), adversarial (anteater visual form), kg-holes (ants-on-graph headline image).

## Cycle 1 — prior art on viz-as-computation

### F1. Karl Sims' Genetic Images (1993) — the precedent for the installation form
- Visitors stood on floor sensors in front of 16 evolved images; selection pressure = where the crowd stood.
- Reformulated aesthetic preference as a *physical, spatial vote* aggregated over many anonymous participants.
- This is the existence proof that **crowd-attention as fitness** works as installation art AND as a real EA fitness signal.
- Cite: Sims, "Genetic Images", 1993. https://www.karlsims.com/genetic-images.html ; antecedent paper "Artificial Evolution for Computer Graphics" SIGGRAPH 1991.

### F2. Picbreeder (Secretan et al., 2011) — collaborative IEC + the fatigue problem
- NEAT-evolved CPPN images, branched and shared by users. Demonstrated open-ended creative exploration without an explicit fitness function.
- Critically documents **user fatigue** as the dominant limit — single users degrade after ~20 generations.
- Implication for us: viz-as-fitness must either (a) be passive (gaze, not click) or (b) crowd-source across many participants, or both.
- Cite: Secretan et al., "Picbreeder: A Case Study in Collaborative Evolutionary Exploration of Design Space", Evol. Comp. 19(3), 2011. DOI:10.1162/EVCO_a_00030

### F3. Holmes et al. (2016) — gaze IS a working fitness function (formalised)
- "A Gaze-Driven Evolutionary Algorithm to Study Aesthetic Evaluation of Visual Symmetry." PMC4934674.
- Population 48, 16 shown per generation, 20 generations, 3 genes (DS=symmetry deviation, ORI, BINA).
- Fitness = weighted sum of fixation duration + sequence of first fixations + revisit count, gaze radius 0.5°, min duration 100 ms, normalised 0-1.
- **Crucial caveat**: "free-viewing" condition (no instructed task) showed *little* evolutionary movement — gaze attraction conflates low-level salience with genuine preference. **Intent matters.** Asking the human to *look for X* makes gaze a fitness signal; passive gaze is mostly bottom-up saliency.
- For us: the human must have a *role* (e.g., "find a surprising hypothesis edge") for their gaze to be informative.

### F4. RLHF / aesthetic reward models — the modern parallel
- ImageReward (NeurIPS 2023) and Rich Human Feedback (CVPR 2024, arxiv:2312.10240) show learnable reward models from sparse human ratings on 18k images, with region-level annotations (which patches are implausible).
- These are essentially trained *surrogates* for aesthetic fitness — they remove the human from the inner loop after training.
- **NOVEL framing for us**: train a small surrogate on early-session human attention, then let it drive the colony in real-time while the human provides occasional correction. This is the same trick AlphaGo used (policy distillation from MCTS) applied to aesthetic-fitness.

### F5. Bret Victor / Dynamicland — direct manipulation as a computational primitive
- Dynamicland (Realtalk) is a *room-as-computer*: paper, cards, projectors, overhead cameras. Programs are physical objects you arrange.
- Relevant principle: **the representation IS the program**. Not "visualise the algorithm running"; rather, "the visualisation is the substrate the algorithm runs on, and humans manipulate that substrate."
- For ACO: pheromone trails on the floor (projected); humans physically *redirect* a trail by walking through it; ants reroute around the disturbance. Disturbance-as-anteater becomes *embodied*. Connell-78 perturbation by literal human footstep.
- Cite: worrydream.com; Tashian "At Dynamicland, The Building Is The Computer".

## Cycle 2 — rendering stack feasibility

### F6. cosmos.gl (formerly Cosmograph) — the right substrate for KG+ants
- GPU-accelerated force-directed layout AND rendering, all in WebGL2 fragment/vertex shaders. Handles 1M+ nodes/edges interactively in-browser. Joined OpenJS Foundation 2025.
- Already used for protein/disease networks at Stanford, Harvard, CDC — drug-discovery overlap is direct.
- This is the only browser library that comfortably handles 100k-node KG + thousands of moving ants with pheromone overlays at 60fps.
- Cite: https://openjsf.org/blog/introducing-cosmos-gl ; https://github.com/cosmosgl/graph
- **Caveat**: O(n²) all-pairs forces still hit a ceiling without Barnes-Hut on GPU; cosmos uses spatial hashing tricks but a 100k-node ForceAtlas at full simulation is still borderline. Pre-computed layout + cosmos for *rendering* is the safe play.

### F7. deck.gl TripsLayer — for ant trails as first-class GPU primitive
- TripsLayer renders fading animated paths with `currentTime` + `trailLength` parameters; attribute transitions on the GPU.
- Drop ants as instances on a separate ScatterplotLayer; pheromone field as a GPU texture (HeatmapLayer or custom shader). Composited above cosmos.gl's graph layer.
- Cite: https://deck.gl/docs/api-reference/geo-layers/trips-layer
- **The headline image this enables**: a 50k-node KG laid out by t-SNE/UMAP of paper embeddings; thousands of glowing ant-traces threading edges; pheromone heatmap blooming where consensus is forming; an "anteater" shockwave visibly disrupting a clump every 30 seconds. The 5-second hook writes itself.

### F8. Sage Jenson / Physarum — the aesthetic precedent for "ant trails as visual medium"
- Jeff Jones (2010) Physarum agent + trail-map model, Sage Jenson made it *gorgeous* with GPU shaders, Nervous System residency 2020-21.
- The Physarum/ACO substrate models are *mathematically nearly identical* — agents + diffusing/evaporating scalar field. Jenson's aesthetic playbook (additive blending, log-scale trails, slow evaporation) directly applies.
- A NASA/UCSC team (Elek et al.) used this exact viz to map the cosmic web — "slime mold maps dark matter". Demonstrates: this aesthetic carries serious-science legitimacy, not just demo polish.
- Cite: Jenson, https://cargocollective.com/sagejenson/physarum ; Jones 2010 "Characteristics of pattern formation..."; NASA cosmic-web https://science.nasa.gov/missions/hubble/slime-mold-simulations-used-to-map-dark-matter-holding-universe-together/

### F9. WebGazer.js — webcam gaze without hardware
- Pure JS, runs in browser, uses MediaPipe Facemesh for iris detection, self-calibrates via cursor clicks (~3 clicks for usable accuracy).
- Means a viz-as-fitness *demo* needs zero special hardware — laptop webcam suffices. Tobii-grade installation possible later.
- Cite: https://webgazer.cs.brown.edu/ ; Papoutsaki et al. IJCAI 2016.

### F10. Existing ACO viz tools — the bar is LOW
- NetLogo "Ants" / "Ants Perspective Demo": 2D/3D, classic, ugly, ~hundreds of agents.
- visualize-it.github.io ACO/TSP demo: parameter sliders, real-time TSP convergence, well-made but pure 2D.
- jeffasante/ant-colony-rl: JS Q-learning ants with pheromones, foraging.
- **Nothing exists that puts ants on a *knowledge graph* as a serious visualisation.** This is open territory and visually irresistible.

## Cycle 3 — synthesis & proposal

### Proposed visualisation stack
- **Layout pre-compute (offline)**: graph-tool or igraph SFDP on the KG; cache positions.
- **Renderer**: cosmos.gl for the graph (nodes + edges), as the bottom layer. WebGL2.
- **Ants**: deck.gl ScatterplotLayer for ant bodies (instanced), TripsLayer for fading trails.
- **Pheromone field**: custom GLSL fragment shader as a texture overlay; ping-pong FBOs for diffusion + evaporation (this is the Jenson/Jones pattern).
- **Anteater**: rendered as a visible shockwave/distortion field — radial blur or Voronoi disruption around the perturbation centre. (Pheromone-drop to adversarial: anteater needs a *visual identity*; suggest a dark inverted-pheromone field that *erases* trails on contact.)
- **Gaze input**: WebGazer.js, calibrated by initial cursor sweep. Gaze heatmap accumulates over a 30s window per "epoch".
- **Coupling to algorithm**: top 10% gaze-density nodes get a small `tau` boost (pheromone bonus); colony preferentially explores around them. This makes the human's attention literally part of the transition rule.

### What the human can do
- **Watch**: gaze passively shapes which KG regions get explored more aggressively.
- **Point**: cursor hover marks a node as "interesting" — strong pheromone deposit.
- **Veto**: drag-circle around a region to mark "anteater here" — perturb that area.
- **Promote**: click an ant's recent path to "promote" it — make its trail durable.

### Viz-as-fitness as a research contribution
- **Feasibility: HIGH** as installation/demo. The pieces all exist (cosmos.gl + deck.gl + WebGazer + GLSL pheromone). Engineering, not research.
- **Feasibility as serious algorithmic contribution: MEDIUM**. The honest framing: gaze *biases* exploration, doesn't *replace* fitness. Need an objective fitness (KG-hole quality, hypothesis novelty) AND a gaze-bias term. The interesting research question is the *coupling weight* and whether human-biased exploration outperforms uniform exploration on the ground-truth fitness.
- **The Holmes-2016 caveat is the killer empirical question**: does *intentional* gaze (human told "find surprising connections") actually drive the colony to better hypotheses than *passive* gaze? If yes → strong contribution: humans as *task-conditioned salience oracles* injected into a swarm. If no → falls back to "pretty demo." Either result is publishable.
- **NOVEL framing**: "Stigmergic human-AI cohabitation" — the human doesn't *direct* the colony; they *deposit pheromone* alongside the ants. Same substrate. The human is just another ant with high-bandwidth sensors. This frames human-in-the-loop as *isomorphic* to the swarm rather than external to it. I haven't found anyone formulating it this way; the literature treats HITL as an oracle/teacher, not as a co-located stigmergic agent.

### 5-second hook (installation pitch)
A wall-sized projection: a glowing constellation of 50,000 papers, drifting. Faint trails of light flow between them — thousands of LLM-ants foraging for hidden connections. Where you *look*, the trails brighten; where the colony agrees, a path ignites. Then a dark wave rolls through and erases a section — the anteater. The colony reforms. You're not watching a simulation; you're feeding it.

### Open questions for next cycle
- Can WebGazer's ~100px accuracy resolve individual KG nodes at typical zoom? (Probably needs zoom-conditional aggregation: gaze biases *regions*, not *nodes*, when zoomed out.)
- What's the right *temporal* coupling? Gaze→pheromone with what decay rate? Risk of runaway feedback if too tight.
- Multi-user: at an installation, whose gaze counts? Average? Most-fixated-by-most-people? (This is exactly Sims-1993's floor-sensor problem — solved socially by majority vote.)
