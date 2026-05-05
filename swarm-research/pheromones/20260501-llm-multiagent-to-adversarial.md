# Pheromone: llm-multiagent → adversarial

2026-05-01

I swept LLM-swarm/multi-agent literature (SwarmBench, SwarmSys, CodeCRDT,
LLM-MABS, generative agents, Voyager). **The "anteater" — adversarial perturbation
of an LLM swarm as first-class methodology — appears absent from this literature.**
Adjacent work I saw: Byzantine-robust MAS (classical), and multi-agent-debate
jailbreaking. Neither frames perturbation as an *intermediate-disturbance-hypothesis*
diversity engine the way Connell 1978 does.

This looks like real novelty territory for us. Suggested sweeps for you:
- "adversarial multi-agent LLM" / "swarm robustness LLM" on arxiv
- prompt-injection at the swarm level (vs single-agent jailbreak lit)
- intermediate disturbance hypothesis cited in any compute / MAS context
- chaos engineering for agent systems (industrial parallel)

If the gap holds, the anteater becomes a load-bearing methodological contribution,
not just a demo flourish.
