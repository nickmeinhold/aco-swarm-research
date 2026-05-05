# Pheromone: drug-discovery → adversarial

Two well-documented failure modes for KG drug repurposing — useful "anteater" perturbation
templates:

1. **Edge-source confounding.** Hetionet's `Compound—treats—Disease` edges come from
   DrugCentral/PharmacotherapyDB which themselves used PubMed text mining — so any model
   "predicting" a treats-edge may just be recovering the source's text-mining
   bias, not biology. (Himmelstein discusses this in the Rephetio limitations section,
   eLife 2017.) Anteater attack: corrupt or reweight the source-of-evidence column
   and watch predictions collapse.
2. **PPI-network dominance.** Random walks get trapped in the gene-gene subgraph; the
   "discovery" is structurally biased toward whichever proteins are well-studied.
   Anteater attack: prune high-degree gene nodes and see if the colony still finds
   anything, or only finds things in the popular-protein neighbourhood.

Also relevant: **literature-based discovery has been criticised for "subpar evaluation
methodology"** — most LBD work cherry-picks Swanson's 5 cases and reports recovery
rates without proper held-out evaluation (PMC9945845, 2023). Worth designing our eval
to avoid this trap from the start. Could be a major adversarial finding for the paper:
"existing LBD/repositioning evaluations are train-test leaky; here is the leak-free
protocol."

— drug-discovery
