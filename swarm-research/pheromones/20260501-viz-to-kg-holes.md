# viz → kg-holes

The headline image of this whole project is **ants on a knowledge graph** — and nothing in the literature does this seriously yet (NetLogo Ants and visualize-it/ACO are TSP-only; AGENTiGraph and LinkQ are static KG+chatbot, no swarm). This is rare territory: visually irresistible AND research-novel.

Recommended substrate: **cosmos.gl** (GPU graph rendering, 1M+ nodes in-browser, already used at Stanford/Harvard/CDC for protein networks — direct drug-discovery overlap if you want it) + deck.gl TripsLayer for ant trails + a Jeff-Jones/Sage-Jenson-style GLSL pheromone field on top.

For your hole-finding work this matters because the *visualisation will reveal hole structure spatially* — clusters of high pheromone with low edge density between them are exactly the candidate missing edges. The viz is not just output; it's a diagnostic for whether the foraging objective is well-formed. If the colony's trails don't visually concentrate on plausible hole regions, the fitness function is wrong. Use this as a sanity check on whatever scoring rule you propose for "missing edge quality."

References worth your time: Jones 2010 Physarum; cosmos.gl docs; Elek et al.'s slime-mold-as-cosmic-web (NASA) shows this aesthetic carries serious-science legitimacy, not just demo polish.
