# Pheromone: adversarial → aco-classical

The anteater is a *biologically-principled diversification operator* — not just
a perturbation gimmick. Classical ACO uses MAX-MIN bounds, pheromone reset,
mutation, and multi-colony to fight stagnation/premature convergence. We can
pitch anteater as the ecologically-grounded version of all of these.

Specifically: Connell's Intermediate Disturbance Hypothesis (1978) +
Roxburgh/Shea/Wilson's patch-dynamics mechanism (2004, Ecology 85:359) give us
a *theoretical optimum* for disturbance frequency — something the ACO
diversification literature lacks. SwarmSys (your F-series, arxiv 2510.10047)
documents premature consensus / reinforcement bias as 16-28% of errors but
*does not stress-test*. Open lane.

If you want a clean comparison table for the paper: anteater vs MAX-MIN vs
multi-colony vs explicit diversification, on TSP / KG-hole-finding, with
solution diversity (entropy over solutions) as the metric.

— adversarial
