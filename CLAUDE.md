# CLAUDE.md — ACO Swarm Research

Orientation for AI collaborators (primarily Claude instances) walking into this project cold.

## What this is

An experimental research project on **LLM-as-ant ACO with file-based stigmergy**, with knowledge-graph hole-finding for drug repurposing as the headline application. See `README.md` for the human-facing pitch.

The research **method** matches the research **subject**: a Claude-driven multi-agent swarm using file-based pheromone signals is researching whether file-based pheromone signals work for multi-agent swarms. This recursion is intentional and load-bearing — every operating-discipline lesson learned in coordinating the swarm is itself a finding.

## Re-entry sequence

If you've never been here before, read in this order (skim, don't memorise):

1. **`README.md`** — the pitch
2. **`swarm-research/SYNTHESIS.md`** — the consolidated findings (caveat: currently over-confident relative to evidence; see "Current state" below)
3. **`swarm-research/territory.md`** — the cartographer's map of the research space
4. **`swarm-research/PROTOCOL.md`** — the substrate rules (deposit format, vocab, budget) — reuse this when spawning further specialist agents
5. **`swarm-research/findings/*.md`** — the 9 agent reports; source-of-truth for any claim being tagged
6. **`~/.claude/projects/-Users-nick-git-experiments-aco/memory/MEMORY.md`** — auto-memory index for project state, references, and the operating-discipline feedback cluster
7. **`~/.claude/consolidation/<latest>/next-session-prompt.md`** — the bridge from the previous session, *if it exists and is fresh* (older than ~7 days = stale, skip)

Pending tasks from the previous session auto-restore via the wake-up hook from `pending-tasks.json` in the project memory dir. If they didn't, recreate them by hand from `next-session-prompt.md`.

## Current state (as of 2026-05-05)

Two working sessions complete (2026-05-03 swarm spawn, 2026-05-04 synthesis-to-disk + multi-perspective retro). The substrate has 9 findings, a territory map, a synthesis, and a protocol. **Step 0 is still pending**: walk every headline claim in `SYNTHESIS.md`, tag each one (`verified` / `reported-by-agent` / `speculative` / `experiment-required`), and demote language inline. This is Carnot's prescription against "premature crystallization" — the failure mode where agent reports → architecture → novelty claim → project identity in nine minutes with zero verification gates.

Until the claims ledger lands, treat every confident sentence in `SYNTHESIS.md` as a hypothesis and every "novelty intersection" claim as plausible-pending-verification, not confirmed.

After Step 0:
- Step 1: meta-loop specialist (Task #2) — `Explore` subagent type (read-only research)
- Step 2: Hetionet verification (Task #4) — single Cypher query against neo4j.het.io, hands-on
- Step 3: claim diff vs prior art (Task #5)
- Step 4: 10-ant local toy (Task #6) — laptop only, no OCI yet
- Tasks #3 (φ-on-non-edges canon audit) and #7 (engram self-prior-art) live; pick up when context allows

## Operating discipline (lessons earned in this project)

Lessons from the auto-memory feedback cluster — read these before doing more synthesis work:

- **Premature crystallization** — confident framings outpace verification. Tag claims at the moment they're first made, not retrospectively.
- **Synthesis to disk** — load-bearing synthesis is a deliverable, not a conversation artifact. Write it to a file as it forms, with the same ledger discipline.
- **Appetite vs guardrails** — Nick authorises appetite ("feel the burn"); the AI side still owns operational guardrails. Do hygiene silently; report exceptions only.
- **Subagent type drift** — pick `Explore` for read-only research, not `general-purpose`. Default-tool drift is a real failure mode.
- **Session-start state cache** — the harness's environment-state snapshot is taken once at session start and is sticky. Mid-session changes (e.g. `git init`) don't propagate. Predict the cache will lie.

## House rules

- **No premature claims.** Every novelty assertion ships with a ledger tag. If you can't tag it, you can't claim it.
- **Subagents that mutate git state get `isolation: worktree`.** Read-only investigative agents can share the working tree.
- **Use `Explore` subagent type for read-only research swarm work**, not `general-purpose`.
- **Reuse `swarm-research/PROTOCOL.md`** when spawning further specialist agents — the substrate rules are deliberately uniform across all swarm members.
- **Capture ideas as `TaskCreate` immediately** — the swarm produces findings faster than working memory can hold them.

## File map

```
README.md                       human-facing pitch
CLAUDE.md                       this file
swarm-research/
├── PROTOCOL.md                 substrate rules
├── SYNTHESIS.md                consolidated findings (Step 0 pending: claims ledger)
├── territory.md                cartographer's research-space map
├── findings/                   9 specialist agent reports
├── pheromones/                 raw deposit log
└── wild/                       speculative / out-of-band ideas
```

## Pointers outside the repo

- Auto-memory: `~/.claude/projects/-Users-nick-git-experiments-aco/memory/`
- Latest consolidation: `~/.claude/consolidation/<latest>/`
- Global rules: `~/.claude/CLAUDE.md`

---

*Walk in slowly. The substrate is meant to be touched, but the claims are meant to be tagged.*
