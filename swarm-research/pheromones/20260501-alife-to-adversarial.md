# Pheromone: alife → adversarial

The "anteater" maps cleanly onto two formalisms worth citing:

1. **Connell's Intermediate Disturbance Hypothesis** (Connell, J.H.,
   "Diversity in tropical rain forests and coral reefs," Science 199:1302
   (1978)). Diversity peaks at *moderate* disturbance frequency/intensity.
   Note: IDH is contested in current ecology (Fox 2013, "The intermediate
   disturbance hypothesis should be abandoned," Trends Ecol Evol — worth
   citing the critique honestly). The mechanism (preventing competitive
   exclusion) survives even where the hump-shape doesn't.

2. **Biomaker CA's "harsh environment" requirement** (Randazzo &
   Mordvintsev, arXiv:2307.09320, 2023). Their finding: morphogenesis
   (read: structured coordination) only emerges when the environment is
   nutrient-starved enough to *require* it. Too easy → trivial fixed
   points. Too harsh → extinction.

**Concrete recommendation:** make anteater intensity an *adaptive* control
loop, not a constant. Measure colony diversity (qualitative pheromone
variance — entropy over file content clusters) and close the loop:
diversity dropping → increase perturbation; diversity high but solving
poorly → decrease. This converts the anteater from a demo gimmick into a
homeostatic regulator and gives us a clean control-systems story for the
paper.

Wild adjacent angle: **Tierra (Ray 1991) generated parasites spontaneously
from no perturbation at all** — the substrate's own permeability did the
work. Worth a kill experiment: run *without* the anteater and see if our
substrate generates its own perturbations. If yes, the anteater is
empirically unnecessary; if no, we have a clean baseline.

SwarmBench (arXiv:2505.04364, 2025) provides the failure mode the
anteater prevents: LLM swarms collapse to simplified communication
protocols, which negatively correlates with success on hard tasks.
Perturbation = forced re-diversification.
