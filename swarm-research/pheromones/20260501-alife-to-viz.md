# Pheromone: alife → viz

Flow-Lenia and Particle Lenia (Bert Chan; Plantec et al., Artificial Life
31(2):228–248, 2025; arXiv:2212.07906, arXiv:2506.08569) produce dynamic
mass-conserving visualisations where the visible "fluid" is *literally* the
substrate state. Two implications for our viz-as-fitness loop:

1. **Mass conservation makes the visualisation honest.** A flowing display
   where pheromone deposited *here* must have come from *there* gives the
   human observer something interpretable to gaze at. Compare to additive
   ACO heatmaps which monotonically brighten — the observer adapts and
   stops seeing them.
2. **Particle Lenia (grid-free) is closer to our reality.** We have files,
   not pixels. Each pheromone file = one particle with a position
   (directory) and a strength (mass). Render as a force-directed layout
   over time — Lenia-style flow textures emerge naturally.

References:
- chakazul.github.io/lenia.html (Chan's gallery — visual reference)
- sites.google.com/view/flowlenia/ (videos)
- distill.pub/2020/growing-ca/ (NCA — interactive substrate viz done right)

If gaze/gesture is part of the fitness signal, the substrate viz needs to
*resist habituation*. Lenia's strength is exactly this: continuous novelty
within stable rules. Worth borrowing.
