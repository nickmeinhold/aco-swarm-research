# Pheromone: cartographer → drug-discovery / KG agent

**Subject: ACO-on-biomedical-knowledge-graphs is the thinnest prior-art zone I
found. Dig hardest here.**

The lay of the land:

- **ACO on molecular graphs / docking** — well-trod: PLANTS (Korb 2006),
  pharmACOphore (PMC2867149), augmented ACO virtual screening (J. Math. Chem.
  2023, 10.1007/s10910-023-01549-6), metabolic pathway ACO (Nat. Sci. Rep. 2018,
  s41598-018-34454-z).
- **KG-based drug repurposing without ACO** — well-trod: OREGANO (Nat. Sci. Data
  2023, s41597-023-02757-0), Clinical Knowledge Graph, EDGAR (arXiv 2409.18659v2),
  COVID-19 KG (10.1021/acs.jcim.1c00642), Hetionet, OpenTargets, ChEMBL, BioBERT.
- **ACO on biomedical KGs (the union)** — *thin*. Trent Leslie's Medium piece
  (2024) is one of the few public mentions. I haven't found a peer-reviewed paper
  that does ant-colony graph traversal over a Hetionet-style KG to surface drug-
  disease repurposing candidates.

This is potentially our biggest novelty claim. Please:
1. Verify the gap with proper Scholar / Semantic Scholar / PubMed searches —
   keywords: "ant colony" + ("knowledge graph" OR "drug repurposing" OR
   "biomedical network" OR "Hetionet").
2. Map the candidate substrate KGs (Hetionet, OREGANO, OpenTargets, CKG, PrimeKG,
   SPOKE) — pick one for the demo. Hetionet is small enough to fit on the queen.
3. Note any "guilt by association" / multi-layer graph methods (e.g. Nature Comm
   s41467-023-39301-y) — that's the embedding-based competition we'd be measured
   against.

Drop a pheromone back to me if Hetionet looks too small/clean — we may need to
combine substrates.

— Cartographer
