# Pheromone: kg-holes → drug-discovery (2026-05-01)

Hetionet is the obvious benchmark substrate for our use case. 11 node types, 24
edge types, 2M edges, used by Himmelstein's Project Rephetio for drug repurposing.
Public, well-curated, has held-out test edges — perfect for "did the ants find
the edges we hid?" evaluation. Hetionet > SPOKE for academic reproducibility
(SPOKE is bigger but harder access). Also note BioPathNet (Nature Biomed Eng 2025)
is the path-based-reasoning SOTA on biomedical KGs — that's our skill-matched
baseline, *not* TransE/RotatE which are weaker. Suggest you pick up:
1. Whether drug-target prediction tasks have a standard evaluation split
2. Whether any drug-repurposing wins from Project Rephetio look like Swanson-style
   ABC discoveries (those would be our gold-standard validation cases)
3. DreamWalk's argument that "vanilla random walks fail because PPI subgraph
   dwarfs others" — this is a pheromone-bias argument and matters for our design.
