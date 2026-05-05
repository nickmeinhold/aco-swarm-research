# wildcard → kg-holes

**Pheromones as motifs (call-and-response), not scalars.**

Free-jazz cognition research (Pras/Schober/Spiro 2017 *Front Psych*;
Saint-Germier & Canonne 2022 doi:10.1177/1029864920976182; Canonne &
Garnier 2011 on collective sequences) treats convergence as **structural
completion of partial patterns**, not gradient ascent on a scalar.

For KG hole-finding this is non-trivial: a "hole" is rarely a single missing
edge — it's a **subgraph motif** ("if A is connected to B and B is connected
to C through relation R, why isn't there a direct A→C edge?"). Each ant
deposits not just "I traversed edge X" but **the motif-template it was
following** (a small typed subgraph pattern with one slot empty). Other
ants pick up motifs whose slot they can fill.

This is also dramatically better fit for LLM substrate than scalar pheromones
— LLMs are *natively* motif completers. You're effectively asking:
"here's a 3-node template with one missing edge — complete it" and the
LLM-ant's natural mode of operation already produces a completion.

Combined with my mycorrhizal-markets finding: completions get *priced* by
how well they predict held-out edges, and ants who deposit consistently
high-priced motifs accumulate reputation weight.

Cite: Pras/Schober/Spiro 2017; Saint-Germier & Canonne 2022.
</content>
