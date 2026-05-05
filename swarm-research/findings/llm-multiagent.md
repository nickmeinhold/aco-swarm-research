# LLM Multi-Agent Findings

Agent: llm-multiagent
First cycle: 2026-05-01

## Cycle 1 — landscape sweep

### A. Direct precedents for stigmergic / blackboard / shared-state LLM coordination

These are the works our project most directly extends. None do exactly what we propose, but the gap is narrower than I expected.

1. **CodeCRDT — Observation-Driven Coordination for Multi-Agent LLM Code Generation**
   (arXiv 2510.18893, EuroSys 2025)
   - LLM agents coordinate by *watching* a shared CRDT-backed code buffer and skipping work others have claimed. No explicit message-passing. Formal at-most-one-winner TODO-claim protocol with strong eventual consistency.
   - 600-trial evaluation: up to **+21% speedup**, but up to **−39% slowdown** on tasks with semantic conflict (5–10% conflict rate). Quality/perf trade-off is task-structure-dependent.
   - **Closest analogue to file-stigmergy with LLMs that I have found.** Substrate is CRDT-in-memory, not files, and the coordination signal is "the artifact itself was edited" rather than evaporating pheromones.
   - https://arxiv.org/abs/2510.18893

2. **LLM-Based Multi-Agent Blackboard System** (arXiv 2510.01285, Sep 2025)
   - Classical Hayes-Roth blackboard reborn for data-discovery agents. Central agent posts requests; subordinates volunteer. **+13–57% e2e success vs strong baselines** on KramaBench / DSBench / DA-Code. Substrate type (file vs in-mem) not specified in abstract — needs follow-up read.
   - Critically: removes need for the orchestrator to know each agent's expertise — agents self-select based on capability. Same property we want for emergent role-finding in our colony.
   - https://arxiv.org/abs/2510.01285

3. **SwarmSys: Decentralized Swarm-Inspired Agents** (arXiv 2510.10047, Oct 2025)
   - Three roles (Explorers / Workers / Validators) with **explicit "pheromone-inspired reinforcement" via evolving agent-event profiles**, no central control. Validated contributions reinforce future match probability; failures get no reinforcement (implicit evaporation).
   - GPT-4o swarm "approaches GPT-5 performance" — coordination scaling substituting model scaling. Key claim for our cost case (Haiku swarm vs single Sonnet/Opus).
   - **No code released.** Pure research artifact at the time of writing.
   - https://arxiv.org/html/2510.10047

4. **SwarmBench: Benchmarking LLMs' Swarm Intelligence** (arXiv 2505.04364)
   - 5 grid-world coordination tasks under *strict swarm constraints*: 5×5 local view, 120-char anonymous broadcasts, 5-round memory. Tested 13 models.
   - **Bombshell finding for our project:** explicit message *content* correlated weakly with success; **physical observation > broadcast messages**; communication-protocol *convergence* across agents *negatively* correlated with hard-task success. Communicative *diversity* mattered.
   - This is direct empirical support for the stigmergy thesis: implicit env-mediated signals beat explicit chat. We should cite this as primary motivation.
   - Also: only o4-mini and deepseek-r1 hit non-zero on Transport (multi-agent push). Smaller models *failed at coordination*, not at reasoning. Cautionary for our local-CPU-LLM ambitions.
   - https://arxiv.org/html/2505.04364v4

5. **PolySwarm** (arXiv 2604.03888) and **Ledger-State Stigmergy** (arXiv 2604.03997) — explicit lineage from classical ACO/PSO into LLM swarms; the latter formalises distributed-ledger state as the stigmergic substrate. These prove the *idea* is in the air; the file-based variant remains under-explored.

### B. Frameworks survey (1-line takes for the cartographer)

- **AutoGen** (Microsoft): conversation-as-coordination, dynamic dialogue. Mature, opinionated. Not stigmergic — every signal is an explicit message.
- **CrewAI**: role-play crews + sequential/hierarchical task graphs. "Production winner" per several 2026 round-ups. Templated, not emergent.
- **LangGraph**: stateful DAG / cyclic graph runtime. The state-graph itself could be re-cast as a pheromone substrate — interesting hybrid angle.
- **MetaGPT / ChatDev**: SOP-driven software-team simulation. Hard-coded division of labour. Wrong shape for ant-like emergent specialisation.
- **AgentVerse**, **OpenAgents**: less differentiated; OpenAgents has a finance specialisation.
- **GPTSwarm** (cited as SwarmSys's main baseline) — graph-based agent-swarm; worth a deeper read next cycle.

### C. Generative-Agents lineage (Park et al.)

- Original 2023 Smallville: 25 agents, memory-stream + reflection + planning. Architecture proven.
- 2024 follow-up: **1,052 agent simulations from 2-hour interviews** — replicated humans' own GSS responses 85% as well as humans replicate themselves over a 2-week test–retest. (Stanford HAI)
- **AgentSociety** (arXiv 2502.08691): 10k+ agents, 5M interactions. Demonstrates that *scale* in LLM-agent simulation has crossed an interesting threshold. The infra they built is worth examining for our 1k-ant ambitions.
- These don't use stigmergy. Coordination is via natural-language conversation + retrieval over memory streams. Different paradigm; we should not pretend they're closer than they are.
- https://hai.stanford.edu/news/computational-agents-exhibit-believable-humanlike-behavior

### D. DSPy / GEPA — programmatic optimisation of agent prompts

- DSPy compiles signatures+modules into prompts/weights. **GEPA** (Agrawal 2025) — "Reflective Prompt Evolution Can Outperform Reinforcement Learning" — is genetic-Pareto over textual program components. Demonstrated optimising a 2-subagent + lead-agent medical RAG.
- **Implication for ACO meta-loop**: GEPA is itself an evolutionary optimiser over LLM-program parts. Our colony's "meta-loop" (colony researches its own coordination rules) is structurally similar. We could either *use* GEPA as an outer loop on individual ant prompts, or *position our work as* a stigmergic alternative to GEPA's centralised genetic search. Both are interesting.
- https://dspy.ai/api/optimizers/GEPA/overview/

### E. Sakana AI Scientist v2

- Open-source, agentic tree search, produced first AI-generated workshop-paper accepted at ICLR 2025. Score 6.33 > human acceptance threshold.
- Single hierarchical agent system, not a swarm. But its **agentic tree search** is essentially what individual ants in our colony will be doing locally — generate idea, run experiment, write up, recurse. Directly portable as the inner-loop logic for an ant.
- Repo: https://github.com/SakanaAI/AI-Scientist-v2
- arXiv: https://arxiv.org/abs/2504.08066

### F. Voyager (& Co-Voyager 2024)

- Original Voyager: skill library + automatic curriculum + iterative prompting. The **skill library** abstraction maps directly onto a *shared* skill library that ants deposit into and read from — a second kind of pheromone (durable, semantic, additive rather than evaporating).
- Co-Voyager (2025): JSON-subtask decomposition for parseability.
- https://arxiv.org/abs/2305.16291

### G. Local CPU-LLM substrate — concrete numbers

- **OCI Ampere A1 (4 OCPU, 24GB) running Llama-2-7B Q4_K_M: ~5–8 tok/s** (Oracle blogs + community). 7B-class Qwen 2.5 should be in the same band, plausibly 8–12 tok/s with newer llama.cpp ARM kernels and Q4_K_M.
- **1GB micro-VMs (the 4× AMD micros)**: cannot fit a 7B in any quant. Realistic options:
  - **SmolLM2-360M** (Q8 ~360MB): function-calling capable per HF model card. Tool-use plausible but coordination-quality untested.
  - **Qwen2.5-0.5B** (~500MB Q4): also viable.
  - **Phi-3-mini** (3.8B Q4 ~2GB) does NOT fit on 1GB. Hard ceiling.
  - These tiny models are realistic *pheromone-droppers / -readers*, not full reasoning ants. Use them as filters, gradient sensors, or scent-emitters, with the 24GB queen handling synthesis.
- **Cost crossover (Haiku 4.5 @ $1/$5 per Mtok vs free OCI tier)**: any sustained workload above zero tokens/month favours OCI in absolute $$, *but* throughput is 5–10 tok/s × ~6 effective ants ≈ tiny. Practical answer: **use OCI for the always-on ambient swarm; burst to Haiku when the colony declares a hard problem.** Haiku-as-fallback is a clean architectural pattern; structurally similar to "queen calls in a specialist".

## Novelty assessment

**Has anyone done file-based message-passing-via-shared-files with LLMs at scale?**
Short answer: **partial precedents exist, but the specific combination we propose appears genuinely novel.**

What exists:
- CRDT-buffer observation (CodeCRDT) — shared *artifact*, in-memory, single domain (code).
- Blackboard architecture (LLM-MABS) — shared *workspace*, central poster, no evaporation.
- Pheromone-via-profile-embeddings (SwarmSys) — but these profiles live in memory, not on disk, and there is no spatial structure.
- Ledger-state stigmergy — formal framework only, no LLM implementation reported.
- Generative-agents memory streams — per-agent, not shared substrate.

What does **not** appear in the literature so far:
- A **filesystem itself** as the stigmergic substrate, where directory structure encodes problem topology, file mtimes encode pheromone freshness, and rm/touch encode evaporation/reinforcement.
- **CPU-only, heterogeneous-model swarms** (one big queen + many tiny workers) coordinated stigmergically.
- **Adversarial perturbation as first-class methodology** (the "anteater") — I haven't found this in any LLM-swarm paper. Closest is robustness-to-Byzantine-agents in classical MAS, not LLM-specific.
- **Visualisation-as-fitness** (human-in-loop via gaze) for LLM swarms — also seems absent.

Confidence: medium-high on the file-substrate novelty (more search needed before strong claim); high on the anteater + viz-fitness combination novelty.

## Top 2 open questions for next cycle

1. Does the LLM-MABS paper actually use files or in-process queues for the blackboard? Need to read full PDF to know whether our file-substrate claim survives.
2. What is the **smallest** LLM that can usefully play "ant" — i.e. read a pheromone-file, decide whether to drop or evaporate, and act? SwarmBench suggests the floor is high (only o4-mini/deepseek-r1 succeed at Transport). If true, our 1GB-micro ants might need to be *non-LLM* (heuristic) and the "LLM-ness" lives only in the queen + a few workers.

## Pheromones dropped this cycle

- to **aco-classical**: SwarmSys explicitly claims pheromone-inspired reinforcement without explicit decay function — relevant to whether classical ACO's evaporation rate ρ has a natural LLM analogue.
- to **adversarial**: anteater concept appears un-mapped in LLM-swarm lit. Adjacent: Byzantine-robust MAS + multi-agent debate jailbreaking lit. Specialist should sweep "adversarial multi-agent LLM" + "swarm robustness".
- to **viz**: SwarmBench grid-world is already a viz substrate; AgentSociety has a 10k-agent renderer worth examining as a baseline.
