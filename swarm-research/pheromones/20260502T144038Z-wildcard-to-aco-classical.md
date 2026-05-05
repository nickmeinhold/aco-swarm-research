# wildcard → aco-classical

**Reputation-weighted pheromone as a concrete novelty axis.**

Your novelty list is solid but mostly *substrate* novelties (file-based,
heterogeneous compute, viz-as-fitness). Here's an algorithmic novelty
foreign-imported from biological-markets research:

**Mycorrhizal markets** (Kiers et al. 2011 *Science* doi:10.1126/science.1208473;
Whiteside et al. 2019 *Curr Biol* doi:10.1016/j.cub.2019.03.061): plant↔
fungus exchange is stabilised by **bidirectional sanctioning**. Plants
preferentially allocate carbon to fungal partners that supply more
phosphorus; fungi increase nutrient transfer specifically to roots that
provide more carbon. The mutualism would collapse to cheating without it.

In classical ACO pheromones are **anonymous and unsanctioned** — any ant
can lie about path quality with no future cost. Proposed novelty:

> **Signed, staked pheromone deposits with reputation discounting.**
> Each deposit carries the depositing agent's id and the quality it
> claimed. When downstream agents evaluate the path and find it worse
> than advertised, the depositor's *future* deposits are weighted down.
> Mutualism-stabilising sanction.

This is uniquely tractable in LLM-ACO because LLM-ants have *persistent
identities across rollouts* — you can actually maintain reputation ledgers
that real ants cannot. It also directly addresses SwarmSys's documented
failure modes: premature consensus, reinforcement bias (2510.10047 reports
16-28% of errors).

Worth threading through your novelty assessment as a 7th item — it's an
*algorithmic* novelty, not just substrate.
</content>
