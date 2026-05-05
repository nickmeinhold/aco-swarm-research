# Open Tasks

Source-of-truth for the project's active task list. The live `TaskList` in any given Claude Code session, the `pending-tasks.json` snapshot in `~/.claude/projects/-Users-nick-git-experiments-aco/memory/`, and the `next-session-prompt.md` in `~/.claude/consolidation/<latest>/` are all *transient mirrors*. This file is the durable, in-repo, authoritative list.

When a task is started, mark it `[in-progress]`. When finished, move it to a "Completed" section at the bottom or remove it; either is fine, but keep the file in sync.

---

## Step 0 — gates everything else

### #7 Add Claims Ledger to `swarm-research/SYNTHESIS.md`

Status: pending — load-bearing prerequisite for Steps 1-4.

Walk every headline claim in `swarm-research/SYNTHESIS.md` and tag each one of:
- `verified` — first-principles checked or independently confirmed against primary source
- `reported-by-agent` — relayed from a `findings/*.md` agent report, not independently verified
- `speculative` — design intuition / wildcard composition / novelty hypothesis
- `experiment-required` — only resolvable by running the toy or the demo

Then demote the language inline. Examples from the next-session prompt:
- "Confirmed novelty intersection" → "**Plausible** novelty intersection (pending verification — see ledger)"
- "DWPC is mathematically equivalent to ACO pheromone" → "DWPC is **reported as** mathematically equivalent (verify against Himmelstein 2017 directly)"
- "The swarm validated the substrate primitive" → "demonstrated coordination at small N (9 agents, single shared dir, no concurrency stress); **production substrate unverified**"
- "Mycorrhizal markets solves substrate attack surface" → "**proposes** a reputation-weighted defense worth testing (reputation systems have their own attack surfaces — Sybil, slow-burn defection)"
- "Frustration pheromone φ on non-edges (possibly stand-alone ACO methods contribution)" → keep `possibly` but tag `experiment-required` and link to Task #3

Standing rule (write into the ledger header): every new claim added to project docs lands with a ledger tag in the same commit. This is the upstream discipline — Step 0 because it's cheap, prerequisite, and changes the semantic ground every later step stands on. No agent. No build. Just the file, and a tag per claim.

Carnot's prescription against "premature crystallization" — the failure mode where agent reports → architecture → novelty claim → project identity in nine minutes with zero verification gates.

---

## Step 1 — parallel with Step 2

### #1 Spawn meta-loop specialist agent (DSPy / GEPA / Sakana)

Status: pending. Use `Explore` subagent type (read-only research).

Cartographer flagged a coverage gap: novelty #4 ("dual-objective meta-loop, colony researches its own coordination protocol") rests only on ReEvo (NeurIPS 2024 arXiv 2402.01145) + Sakana AI Scientist as cited siblings. Until a specialist passes over DSPy (Khattab et al.), GEPA (if it exists in 2026 — search), Sakana AI Scientist v1+v2, AlphaEvolve / FunSearch (DeepMind LLM-evolves-code), and 2024–2026 self-improving LLM literature, that claim is structurally weakest.

Brief the specialist with the same protocol the original 9 used (`swarm-research/PROTOCOL.md`).

**Load-bearing question**: has anyone shown LLMs-as-ants rewriting their own *coordination* protocol (not just heuristic functions), with measurable self-improvement on the same problem?

Output: `swarm-research/findings/meta-loop.md` plus a 400-word report.

---

## Step 2 — parallel with Step 1

### #3 Confirm Hetionet has recoverable lithium → ALS demo case

Status: pending. Hands-on, not delegate-able.

Single Cypher query against `neo4j.het.io`. Confirm:
- (a) the lithium → ALS edge exists
- (b) is deletable for held-out evaluation
- (c) sufficient metapaths remain for swarm-recovery to be plausible
- (d) it's actually one of Project Rephetio's 700 recovered indications, not a novel-but-unconfirmed case

If any of those fail, fall back to: sildenafil → PAH, metformin → cancer, carbamazepine → trigeminal neuralgia, or Swanson fish-oil → Raynaud's — with the same verification.

Output: a one-paragraph "demo target locked" note appended to SYNTHESIS.md (with appropriate ledger tag per Step 0).

---

## Step 3 — depends on Step 0 + Step 1

### #4 Write one-page claim diff vs nearest prior art

Status: pending. Reviewer-2 prevention.

For each of: ACO-ToT (arXiv 2501.19278), Sherkat 2018 quantum-ACO link prediction, ACM 2024 (DOI 10.1145/3675888.3676123), SwarmSys (arXiv 2510.10047), ReEvo (NeurIPS 2024 arXiv 2402.01145), CodeCRDT (arXiv 2510.18893), LLM-MABS (arXiv 2510.01285), AMRO-S (arXiv 2603.12933), TxGNN (Huang & Zitnik *Nat Med* 2024 DOI 10.1038/s41591-024-03233-x) — write three sentences:

1. What they do
2. What we add over them
3. Why our addition is non-trivial

This is the scaffold of the related-work section and the document that prevents an over-claim. Consumes outputs from Step 0 (claims ledger) and Step 1 (meta-loop coverage).

---

## Step 4 — after Steps 0-3 OR in parallel when context allows

### #5 Build 10-ant local file-stigmergy toy (laptop, no OCI)

Status: **in-progress** (initial substrate plumbing verified 2026-05-05). **Prerequisite for OCI deployment, not a substitute.**

First-run findings (see [`toy/README.md`](toy/README.md)):
- Substrate primitives (deposit / decay-weighted strength / evaporator) work cleanly at small N. 5 async-concurrent ants per cycle produced 118 readable deposit files with no corruption.
- LLM ants (Haiku 4.5 via Anthropic API) reached target 15/15 across 3 cycles on a 20-node synthetic ER graph.
- **`experiment-required` finding**: swarm converged on a suboptimal 10-hop path over a 5-hop alternative — classical Ant System premature-convergence pathology. Confirms the project spec's reliance on **MMAS** ([Stützle & Hoos 2000](https://doi.org/10.1016/S0167-739X%2800%2900043-1)) for bounded reinforcement.

Remaining for full Task #5 closure:

aco-classical's load-bearing open question: *does file-based persistent stigmergy behave qualitatively differently from in-memory pheromone matrices?*

Build the minimal toy on the laptop:
- 10 LLM-ants (Haiku or local Qwen2.5-3B)
- ~1000-node knowledge graph
- File-based pheromone substrate with `mtime` as strength
- Cron evaporator
- Signed deposits (`agent_id + claimed_quality + signature`)
- Per-agent budget (mass-conserved, Flow-Lenia style)

**Measure**:
- Convergence behaviour
- Race-condition incidence under concurrent writes
- Whether file-substrate noise helps or hurts vs equivalent in-memory matrix

**Outcome decides** whether OCI Free Tier deployment (1 × ARM Ampere A1 + 4 × AMD x86 micros) is the natural next step or whether the substrate primitive needs a redesign first.

---

## Side tasks — pick up when context allows, in parallel with main sequence

### #2 Verify φ-on-non-edges absence in deep ACO canon

Status: pending.

`kg-holes` flagged "frustration pheromone on non-edges" as NOVEL pending confirmation; cartographer flags this as **possibly a stand-alone ACO methods contribution** separable from the KG application.

Before publishing that claim, audit:
- Dorigo & Stützle's *Ant Colony Optimization* (MIT Press 2004) — chapter on variants
- MMAS (Stützle & Hoos 2000)
- Hyper-cube ACO (Blum & Dorigo 2004)
- Continuous-domain ACO_R (Socha & Dorigo 2008)
- Any 2020-2026 ACO survey

For any prior construct that deposits pheromone on absent / phantom edges (as distinct from anti-pheromone, which marks bad existing edges — Robinson 2005 *Nature*).

- If absent: write a one-page methods-contribution claim (separable paper).
- If present: rescope the novelty claim accordingly.

### #6 Reconcile engram prior-work as self-citation

Status: pending. Prevents reviewer surprise.

Cartographer flagged that Nick's prior **engram** project (knowledge graph that found missing nodes) may constitute self-prior-art. Before publishing:

1. Locate engram repo / notes
2. Characterise what it built
3. Determine whether it operationalised anything like φ-on-non-edges or pheromone-on-absent-relations

Outcomes:
- If yes: this work cites engram as direct prior art and frames itself as ACO-formalisation of an empirical finding.
- If no: separate contribution; note the lineage.

See also: `~/.claude/projects/-Users-nick-git-experiments-aco/memory/project_engram_callback.md`.

---

*Numbering note: the `#N` IDs follow the order in which tasks were created in the previous session's TaskList (which differs from the Step ordering above — Step 0 is `#7` because it was created last, after the other six were already enumerated). The Step ordering reflects execution sequence; the `#N` IDs are stable identifiers for cross-reference.*
