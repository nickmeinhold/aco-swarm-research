# CLAUDE.md — ACO Swarm Research

Orientation for AI collaborators (primarily Claude instances) walking into this project cold.

## What this is

An experimental research project on **LLM-as-ant ACO with file-based stigmergy**, with knowledge-graph hole-finding for drug repurposing as the headline application. See `README.md` for the human-facing pitch.

**Deployment target (revised 2026-05-13 after toy-on-OCI runs):** Oracle Cloud Free Tier — 1 × ARM Ampere A1 (24 GB / 4 OCPU) as the Qwen-7B-Q4 "queen" + up to 2 × AMD x86 E2.1.Micro hosts (1/8 OCPU, 1 GB each) as ant hosts. **Ants run heuristic ε-greedy by default** and escalate to the queen LLM only when stuck (smart trigger = cornered OR `len(path) >= 0.6 × max_steps` AND target not adjacent). **SmolLM2-on-ants is deferred** — on E2.1.Micro 1/8-OCPU hardware it's Pareto-dominated by both heuristic and queen-Qwen (see `toy/runs/2026-05-12-oci-run-3-smollm2.md`). The load-bearing tunable turns out to be **escalation frequency**, not queen↔ant bandwidth (private-VCN latency is sub-ms; queen CPU is the scarce budget). Five-way comparison and the "LLM-as-substrate-seeder" reframe are documented in `toy/README.md` and in the auto-memory at `feedback_octopus_brain_arm_falsified.md`.

The research **method** matches the research **subject**: a Claude-driven multi-agent swarm using file-based pheromone signals is researching whether file-based pheromone signals work for multi-agent swarms. This recursion is intentional and load-bearing — every operating-discipline lesson learned in coordinating the swarm is itself a finding.

## Re-entry sequence

If you've never been here before, read in this order (skim, don't memorise):

1. **`README.md`** — the pitch (updated 2026-05-13 with the architectural pivot)
2. **`swarm-research/SYNTHESIS.md`** — consolidated findings; **read the "Empirical update (2026-05-13)" section near the top** before the older "What survived" / "6-way novelty" sections, which are still mostly true but pre-date the OCI deployment runs
3. **`toy/README.md`** — the **five-way comparison table** (heuristic vs Qwen-everywhere vs SmolLM2-local vs cornered-escalate vs smart-escalate). Index for `toy/runs/`.
4. **`toy/runs/*.md`** — per-run ledger-tagged findings (date-prefixed `2026-05-12-oci-run-1.md` ... `2026-05-13-oci-run-5-smart-escalate.md`). Source-of-truth for any empirical claim.
5. **`oci/QUEEN.md` + `oci/ANTS.md`** — OCI deployment record (queen + ant hosts, network exposure, two-rule pattern, smoke-test latency caveat)
6. **`swarm-research/territory.md`** — the cartographer's research-space map
7. **`swarm-research/PROTOCOL.md`** — the substrate rules — reuse when spawning further specialist agents
8. **`swarm-research/findings/*.md`** — the 9 specialist agent reports from 2026-05-03; source-of-truth for the pre-OCI claims
9. **`~/.claude/projects/-Users-nick-git-experiments-aco/memory/MEMORY.md`** — auto-memory index: project state, references, operating-discipline feedback cluster, OCI-reality-vs-spec cluster
10. **`TASKS.md`** at the repo root — **source-of-truth** for the active task list. Read before deciding what to work on.
11. **`~/.claude/consolidation/<latest>/next-session-prompt.md`** — bridge from previous session, *if it exists and is fresh* (older than ~7 days = stale, skip)

Task state is **canonically in `TASKS.md`** (in repo, durable). The `pending-tasks.json` snapshot in `~/.claude/projects/-Users-nick-git-experiments-aco/memory/` and the `next-session-prompt.md` are *transient mirrors* — convenient when fresh, but `TASKS.md` is the authoritative list. If they conflict, `TASKS.md` wins. Update `TASKS.md` whenever a task starts, finishes, or new ones are surfaced.

## Current state (as of 2026-05-13)

**Working sessions:** 2026-05-03 swarm spawn → 2026-05-04 synthesis-to-disk + multi-perspective retro → 2026-05-06 OCI ant provisioning + private-VCN smoke test → 2026-05-12 → 2026-05-13 toy-on-OCI experimental runs + architectural pivot.

**Infrastructure (verified live):**
- Queen `nick-mel` (130.162.192.233 / 10.0.0.4) — `VM.Standard.A1.Flex`, 4 OCPU ARM, 24 GB RAM, ollama + `qwen2.5:7b-instruct-q4_K_M` bound `0.0.0.0:11434` via systemd drop-in
- ant-1 (130.162.196.243 / 10.0.0.107) and ant-2 (169.224.226.141 / 10.0.0.58) — `VM.Standard.E2.1.Micro`, 1/8 OCPU x86, 1 GB RAM, same VCN
- Private-VCN ant→queen TCP/11434 verified working — two-rule pattern (subnet SL + queen iptables) documented in `feedback_oci_intra_subnet_reachability.md`
- ant-1 has ollama + `smollm2:360m-instruct-q4_K_M` installed (used in run 3, now deferred per the falsification — see Task #26 for cleanup decision)

**Experimental state — five-way comparison on 20-node toy:**

| Backend | Success | Wall | LLM calls |
|---|---|---|---|
| Heuristic ε-greedy | 9/15 | 0.68s | 0 |
| H + cornered-only escalation | 9/15 | 58.8s | 2 |
| **H + smart escalation** | **11/15** | **10m16s** | **43** |
| Qwen-7B-Q4 on every step | 11/15 | 24m34s | ~140 |
| SmolLM2-360M-Q4 local on ant | 3/15 | 28m49s | ~186 |

**The architectural pivot (2026-05-13):** SmolLM2-on-ants is Pareto-dominated on free-tier hardware. Heuristic+smart-escalation matches queen-everywhere quality at 2.4× speedup. The LLM's load-bearing role is **seeding the substrate during cold-start**, not deciding each ant step — "LLM-as-substrate-seeder" reframe. README + SYNTHESIS + this file all rewritten to reflect the pivot. Memory: `feedback_octopus_brain_arm_falsified.md` is the anchor.

**What's still pending (in TASKS.md):**
- Original pre-pivot: #2 (meta-loop specialist), #3 (φ-on-non-edges canon audit), #4 (Hetionet verification — **needs Nick's hands**), #5 (prior-art claim diff), #6 (engram self-citation — **needs Nick's filesystem**), #7 (Step 0 claims-ledger PROSE pass on SYNTHESIS)
- OCI hygiene: #10 (substrate-distribution design, now de-prioritised), #11 (two-blocker cloud-init), #12 (reverse path verification, de-prioritised), #13 (queen keep-alive cron), #14 (ollama-unit backup migration)
- Pivot follow-ups: #16 (sub-plan escalation), #17 (escalation budget cap), #18-#28 — see TASKS.md "Step 6" section. **The single most-load-bearing next experiment is #18** (replicate run-5 across multiple seeds; the +2/15 win is from n=1)

**Project-identity-level claims now empirically anchored** but with n=1: see "Open questions" in run 5 findings doc for the validation experiments queued.

## Operating discipline (lessons earned in this project)

Lessons from the auto-memory feedback cluster — read these before doing more synthesis work:

**Original cluster (2026-05-04 → 2026-05-06):**
- **Premature crystallization** — confident framings outpace verification. Tag claims at the moment they're first made, not retrospectively.
- **Synthesis to disk** — load-bearing synthesis is a deliverable, not a conversation artifact. Write it to a file as it forms, with the same ledger discipline.
- **Appetite vs guardrails** — Nick authorises appetite ("feel the burn"); the AI side still owns operational guardrails. Do hygiene silently; report exceptions only.
- **Subagent type drift** — pick `Explore` for read-only research, not `general-purpose`. Default-tool drift is a real failure mode.
- **Session-start state cache** — the harness's environment-state snapshot is taken once at session start and is sticky. Mid-session changes (e.g. `git init`) don't propagate. Predict the cache will lie.
- **Durable capture before shelving** — when shelving, enumerate transient state and verify each piece has a durable in-repo home. Runs both directions: transient → durable AND durable → forgotten.
- **Pre-action tripwires** — generalisation: structural diagnosis of "the loop relies on Nick's spot-checks rather than Maxwell's pre-action verification". Before publish / deploy / claiming "fresh" / calling a result evidence — run check Y.

**OCI-reality-vs-spec cluster (2026-05-06 → 2026-05-13):**
- **OCI quota vs spec (`feedback_oci_quota_vs_spec.md`)** — verify free-tier quota against the architecture spec before letting node-counts ship as project identity. "4 micros" → "2 micros" reality on this tenancy.
- **Same-subnet ≠ reachable (`feedback_oci_intra_subnet_reachability.md`)** — OCI private-VCN exposure needs TWO rules (subnet SL + host iptables, the default Ubuntu image ships a trailing ICMP-host-prohibited REJECT). The `No route to host` after fixing only the SL is diagnostic gold, not a routing issue.
- **Smoke-test prompt shape (`feedback_smoke_test_prompt_shape.md`)** — a single-curl warm-latency number from a trivial prompt does NOT predict workload latency. Queen Qwen-7B-Q4 was 1.09s on a one-word reply, ~10s on real ant-step prompts. Match smoke-test prompt shape to workload.
- **Octopus-brain ↔ arm falsified (`feedback_octopus_brain_arm_falsified.md`)** — SmolLM2-on-ants on E2.1.Micro 1/8-OCPU is dominated by heuristic. Verify hardware-on-hardware before architecture-spec ships as project identity.

**Tripwire pattern across all of these:** before claiming X, run check Y at the moment of claim, not retrospectively. The OCI cluster is three more instances of the same shape (verify quota / verify reachability / verify hardware) — see `feedback_pre_action_tripwires.md`.

## House rules

- **No premature claims.** Every novelty assertion ships with a ledger tag. If you can't tag it, you can't claim it.
- **Subagents that mutate git state get `isolation: worktree`.** Read-only investigative agents can share the working tree.
- **Use `Explore` subagent type for read-only research swarm work**, not `general-purpose`.
- **Reuse `swarm-research/PROTOCOL.md`** when spawning further specialist agents — the substrate rules are deliberately uniform across all swarm members.
- **Capture ideas as `TaskCreate` immediately** — the swarm produces findings faster than working memory can hold them.

## File map

```
README.md                       human-facing pitch (rewritten 2026-05-13 — heuristic+escalation pitch)
CLAUDE.md                       this file (rewritten 2026-05-13 — current state, ops discipline)
TASKS.md                        source-of-truth for active tasks (durable, in-repo). Step 0 → Step 6 + side tasks.
oci/                            OCI deployment record
├── QUEEN.md                    nick-mel A1 queen — specs, ollama config, network exposure
└── ANTS.md                     ant-1 + ant-2 E2.1.Micro hosts + findings on free-tier reality
toy/                            file-stigmergy experimental rig (laptop + OCI)
├── colony.py                   single-file PEP 723 script. Flags: --mock | --queen [--escalate [--escalate-trigger {cornered,smart}]]
├── README.md                   the five-way comparison table + runs index
└── runs/
    ├── 2026-05-12-oci-run-1.{log,md}            Qwen-7B-Q4 via queen private VCN (11/15, 24m34s)
    ├── 2026-05-12-oci-run-2-mock.{log,md}       heuristic ε-greedy baseline on ant-1 (9/15, 0.68s)
    ├── 2026-05-12-oci-run-3-smollm2.{log,md}    SmolLM2-360M-Q4 local on ant — no-go (3/15, 28m49s)
    ├── 2026-05-13-oci-run-4-heuristic-escalate.{log,md}   cornered-only escalation (9/15, 58.8s, 2 calls)
    └── 2026-05-13-oci-run-5-smart-escalate.{log,md}       smart escalation (11/15, 10m16s, 43 calls) — pivot
swarm-research/
├── PROTOCOL.md                 substrate rules (deposit format, vocab, budget)
├── SYNTHESIS.md                consolidated findings + 2026-05-13 empirical update
├── territory.md                cartographer's research-space map
├── findings/                   9 specialist agent reports from 2026-05-03 spawn
├── pheromones/                 raw deposit log (the swarm's coordination signal)
└── wild/                       speculative / out-of-band ideas
```

## Pointers outside the repo

- Auto-memory: `~/.claude/projects/-Users-nick-git-experiments-aco/memory/`
- Latest consolidation: `~/.claude/consolidation/<latest>/`
- Global rules: `~/.claude/CLAUDE.md`

---

*Walk in slowly. The substrate is meant to be touched, but the claims are meant to be tagged.*
