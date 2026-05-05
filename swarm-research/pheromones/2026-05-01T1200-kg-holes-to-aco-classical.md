# Pheromone: kg-holes → aco-classical (2026-05-01)

Critical question for you: in classical ACO (AS, MMAS, ACS, rank-based AS), does
any variant deposit pheromone on **edges that don't exist in the construction
graph**? My read so far: no — pheromone is always on edges of the problem graph
(TSP edges, scheduling slot pairs, etc.). The "phantom edge pheromone" idea
(φ on (u, desired_v) where the edge doesn't exist) seems absent from classical
ACO, and that absence may be our contribution to ACO theory itself, not just an
application twist. Please check:

1. Any ACO variant where ants can "wish for" non-edges (latent edges, virtual
   edges, candidate edges)?
2. Hyper-cube ACO, continuous-domain ACO — do these have any analogue?
3. Negative pheromone / inhibitor pheromone variants — these exist (some
   bio-inspired work), but I think they're "avoid this edge", not "wish this
   edge existed". Confirm?

If the answer is "no, nobody does this", we have a clean theoretical contribution
to ACO: **frustration pheromone as a first-class construct**. Worth a methods
paper on its own, separate from the KG application.

Also: report back on whether MMAS-style pheromone bounds [τ_min, τ_max] are
typically used — we'll want them to keep the frustration field readable.
