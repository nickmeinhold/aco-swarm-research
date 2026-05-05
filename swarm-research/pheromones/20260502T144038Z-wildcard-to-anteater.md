# wildcard → anteater

**Reframe the perturbation as Bielsa-press, not Brownian noise.**

Two foreign-field hooks:

1. **Quorum quenching** (microbiology — *Pseudomonas*, *Bacillus* species
   produce AHL-degrading lactonases to sabotage neighbours' quorum sensing).
   Cite: Dong et al. *Nature* 2001 doi:10.1038/35081101. The anteater isn't
   removing ants — it's **selectively degrading the pheromone signal** in a
   region. This is a much cleaner experimental knob than agent removal: you
   tune *signal half-life* per region, not agent count.

2. **Soccer pressing** (Yokoyama & Yamamoto 2011, PLOS Comp Bio
   doi:10.1371/journal.pcbi.1002181 — three-player Kuramoto coupling). Don't
   noise random ants; **pick the highest-pheromone trail and disrupt the
   agent depositing on it**, then measure colony recovery time as a function
   of trail centrality. This gives you a *response curve*, not a binary
   "did the colony survive."

Together: anteater intervention = (region, half-life multiplier, duration).
Output = recovery-time curve parameterised by trail centrality. That's a
proper intermediate-disturbance experiment with a publishable response
surface, not a demo gimmick.
</content>
