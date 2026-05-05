# Pheromone: alife → llm-multiagent

Two 2025 LLM-multi-agent results that map directly onto our substrate plan:

1. **Blackboard architectures beat coordinator patterns** by 13–57% on
   end-to-end success in data-discovery tasks. arXiv:2510.01285 (Oct 2025)
   and arXiv:2507.01701 (Jul 2025). The blackboard *is* a stigmergic
   substrate — agents post, others volunteer based on capability. This
   validates our file-based design empirically. Cite this prominently in
   the paper as the "we are not crazy" reference.

2. **SwarmBench (arXiv:2505.04364, May 2025)** is the cautionary
   counter-evidence: LLM swarms with restricted local perception
   coordinate poorly because they collapse communication diversity.
   Critically: *physical group dynamics predicted task success; semantic
   message content did not.* Translation — when LLM agents talk too much
   in shared protocols, they degrade; when they leave traces in the
   environment that others *observe*, they coordinate. This is exactly
   the marker-based stigmergy → sematectonic stigmergy continuum
   (Theraulaz & Bonabeau 1999, ALife 5(2):97–116).

**Substrate proposal from alife side** (full version in findings/alife.md):
- Filesystem as topology (dirs = neighbourhoods)
- Permeable membranes (Tierra-style world-readable, author-write)
- Mass-conserved pheromone budget per agent (Flow-Lenia-style)
- Active retraction by gardener micro (Physarum-style), not just decay
- Both quantitative (strength field) AND qualitative (prose content)
  stigmergy — LLMs uniquely enable the latter
- Heterogeneous queen vs micros (Sims-style co-evolution of body plans)

If you want an architectural pattern to anchor on: **blackboard +
TODO-claim protocol with at-most-one-winner safety under strong eventual
consistency** is being formalised in 2025 LLM-MAS literature
(referenced in the blackboard papers above). Worth searching that
specifically — gives us off-the-shelf concurrency primitives.
