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

Status: **in-progress, partially scope-shifted to Step 5.** Initial substrate plumbing verified 2026-05-05; on 2026-05-06 the project jumped ahead to OCI provisioning (Step 5 below) before closing the laptop toy's remaining sub-items. The MMAS bounds, in-memory comparison, concurrency stress test, and Hetionet-subset-1000-nodes items remain owed — but several can now be done on OCI just as easily as locally (and OCI is cheaper per call). Decide when reopening: close as "superseded by Step 5" or keep open as the rigorous in-memory-vs-file-substrate comparison rig.

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

---

## Step 5 — OCI deployment (new 2026-05-06)

The 2026-05-06 session jumped past the laptop toy and provisioned the OCI deployment topology. See "Completed (2026-05-06)" below for what landed. The remaining OCI-side work, in roughly the order it unblocks the next thing:

### #8 Run existing toy on OCI via private VCN

Status: pending. **Highest-leverage next move.**

Take `toy/colony.py`, run it from ant-1 (130.162.196.243) with the LLM backend pointed at the queen's private IP `http://10.0.0.4:11434` instead of Haiku. Same 20-node ER+chain graph, same 5-ant × 3-cycle structure. Compares:

- Cold + warm latency profile vs the laptop-Haiku baseline
- Whether the Haiku-anti-diversity finding persists with Qwen-7B-Q4 (load-bearing for `feedback_llm_as_anti_diversity_prior.md`)
- Whether file-substrate behaviour changes with the slower ant-step rate (1.09s/step on Qwen vs ~1-2s on Haiku — not very different actually)

Output: a `toy/oci-run-N.md` log + a one-paragraph finding tagged with the ledger discipline.

### #9 Deploy SmolLM2-360M to ant-1 and ant-2

Status: **closed 2026-05-12 as no-go.** Empirically dominated; see `toy/runs/2026-05-12-oci-run-3-smollm2.md`.

ollama + `smollm2:360m-instruct-q4_K_M` was installed on ant-1 and a full toy run (5 ants × 3 cycles) executed. Result: **3/15 success, 28m49s wall** — worse than heuristic (9/15, 0.68s) AND slower than queen-Qwen (11/15, 24m34s). The 1/8-OCPU x86 hardware is too compute-poor to run *any* LLM at ant-step rates that beat the heuristic baseline. This isn't a tuning problem; the model size that would fit fast enough is below the size that contributes useful intelligence.

**Architectural revision unlocked by this finding:** the honest deployment for OCI free-tier hardware is **heuristic-on-ants + queen-Qwen for escalation-on-stuck**, not the "1 queen + 4 ant-LLMs" topology in `CLAUDE.md` / `SYNTHESIS.md`. See new task #15 (heuristic+escalation prototype) below.

Note: ant-2 was never touched — installing SmolLM2 there would just confirm the same finding on the same hardware. ant-1 still has ollama installed; if reusing for a different purpose (e.g. ant-side caching, substrate maintenance), the existing install is fine. Otherwise candidate for `systemctl disable --now ollama` to reclaim memory.

### #10 Substrate-distribution design note

Status: pending. Load-bearing for any multi-node file-substrate work.

The file-pheromone substrate currently lives on a single host. For the real deployment topology (queen + 2 ants writing/reading the same substrate), it needs to live somewhere all three can reach. Options:

- **NFS/sshfs over private VCN** — simple, single shared mount
- **rsync-cron** — eventual consistency, no shared mount, simpler ops
- **bind-mount with sshfs** — same as NFS but per-host
- **MinIO/S3-compatible blob store** — over-engineered for the scale
- **Symlink trick / git-style merge** — clever but probably broken
- **No shared substrate; each host writes locally + queen aggregates** — different model entirely

Write `swarm-research/SUBSTRATE-DISTRIBUTION.md` enumerating these with their bandwidth/latency/consistency profiles, pick one, document the bandwidth knob it exposes (the "octopus brain ↔ arm" tunable per CLAUDE.md). Decide before #8/#9 actually do multi-node writes.

### #11 Pre-empt two-blocker pattern in ant cloud-init template

Status: pending. Low priority but high payoff when reprovisioning.

The cloud-init currently used for ants installs base packages + a keep-alive cron. Extend it with an iptables ACCEPT rule for the expected service port BEFORE the trailing `REJECT --reject-with icmp-host-prohibited` rule, persisted via `netfilter-persistent save`. Means when SmolLM2 lands on an ant (or future re-provisioning happens) we don't repeat the diagnostic dance.

### #12 Verify reverse path queen → ant

Status: pending. Inverse of what was verified 2026-05-06.

When SmolLM2 is up on ant-1 (#9), the queen needs to TCP-reach `10.0.0.107:11434`. Repeat the two-rule pattern in the reverse direction: subnet SL ingress `10.0.0.4/32 → 11434` on each ant, plus ant-side iptables ACCEPT. Smoke-test from queen with `curl http://10.0.0.107:11434/api/chat -d '...'`. Capture cold/warm latency from queen perspective.

### #13 Queen keep-alive cron

Status: pending. Idle-reclamation defense.

Ants got the keep-alive cron from cloud-init (`/opt/keep-alive.sh` every 6h). Queen never got one — risk if the Melbourne tenancy is subject to idle reclamation (unclear). Install the same script on `nick-mel` via SSH; one-line crontab entry.

### #15 Prototype heuristic-on-ant + queen-escalation-on-stuck

Status: **completed 2026-05-13.** Two phases run; positive evidence captured.

- **Phase A (cornered-only trigger):** `toy/runs/2026-05-13-oci-run-4-heuristic-escalate.md` — matched queen-everywhere success (9/15) at 25× speedup and 70× fewer LLM calls. Did not improve on heuristic.
- **Phase B (smart trigger = cornered OR long-path-without-target):** `toy/runs/2026-05-13-oci-run-5-smart-escalate.md` — **11/15 success, 10m16s wall, 43 LLM escalations.** Matches Qwen-everywhere at 2.4× speedup; beats heuristic by +2/15. Cycle 1 went 5/5 (vs heuristic-alone 3/5) — the LLM's main role is **seeding the substrate**, not making each ant decision.
- Conceptual win: "LLM-as-substrate-seeder" reframe (see run 5 Finding 3). Suggests SYNTHESIS.md novelty story should be sharpened.

Follow-up tasks unlocked by these runs:

- **README + SYNTHESIS.md rewrite** to reflect the architectural pivot (project-identity-level — needs Nick's eyes)
- **Sub-plan escalation** (run 5 Finding 4) — LLM returns 3-5 steps not 1
- **Escalation budget per ant** (run 5 Finding 5) — prevent explosion on bigger graphs
- **MMAS bounds** (run 4 Finding 3) — was already in toy/README backlog; smart-trigger run 5 made it less urgent but still relevant for fairness on bigger experiments

### #16 Sub-plan escalation — LLM returns 3-5 steps not 1 (NEW 2026-05-13)

Status: pending — emerged from run 5 Finding 4.

When the smart trigger fires, the current design has the LLM return a single next-step. Cycle 2 a0/a1 and cycle 3 a3/a4 each escalated 5-6 times and still failed — step-by-step LLM picks couldn't undo cumulative wrong turns.

Replace: pass full path + neighbour structure to LLM, ask for the next 3-5 steps as a sub-plan. Validate steps against the graph; fall through to single-step heuristic for any invalid step. Saves LLM round-trips and lets the LLM plan a coherent recovery.

Acceptance: re-run smart-escalate on the same 20-node KG with sub-plan mode; success rate ≥ 11/15 and escalation count down.

### #17 Escalation budget per ant on bigger graphs (NEW 2026-05-13)

Status: pending — bigger-graph safety. Emerged from run 5 Finding 5.

On the 20-node toy, smart-trigger produced 43 escalations across 15 ants (~3 per ant). On a 1000-node Hetionet subset with max_steps probably 30-50, a failing ant could escalate 20-30 times. Need either (a) a hard cap per ant per cycle, (b) a budget shared across the colony, or (c) an exponential back-off on repeated escalations from the same ant.

Acceptance: rerun smart-escalate on a small graph with the cap, confirm success rate unchanged at small N; surface cap as a CLI flag for tuning.

### #14 Migrate ollama-unit backup off /tmp

Status: pending. Low-priority hygiene.

Backup of the queen's pre-rebind ollama systemd unit is at `/tmp/ollama-unit-before.txt` on the queen (created 2026-05-06 by the deployment subagent). Ephemeral — will vanish on reboot. Either recreate from `systemctl cat ollama.service` (the pre-rebind state is the base unit anyway, the override is in the drop-in), move to `/etc/ollama/backup/`, or just delete since the rebind is durable via drop-in.

---

## Step 6 — Validation of the architectural pivot (NEW 2026-05-13 evening)

The pivot from "1 queen + 4 ant-LLMs" to "heuristic + smart-escalation" is currently anchored on **n=1** toy run (run 5). Before treating it as settled, replicate and stress-test. Of these, **#18 is the single most-load-bearing** — without variance evidence, the +2/15 win could be noise.

### #18 Replicate run-5 across multiple seeds

Status: pending — **highest priority for next session.**

Same config as run 5 (`--queen --escalate --escalate-trigger smart --reset`, 5 ants × 3 cycles × 20 nodes, max_steps=12) but with `--seed` varied. Need to add a `--seed` CLI flag to `colony.py` first (currently `make_kg` uses seed=42 hardcoded; the heuristic uses global `random` module unseeded).

Acceptance: ≥5 runs at distinct seeds. Report success-rate distribution (mean ± stdev, median, range). If the +2/15 gain has stdev > 1.5, the architectural-pivot claim needs softening.

### #19 Bigger-graph test (50-100 nodes)

Status: pending — second priority after #18.

Generate a 50–100 node ER+chain graph (same `make_kg` template, scaled). Rerun all five backends at appropriate `max_steps` (probably 30-50). Tests whether the cycle-1 cold-start mechanism that drove run 5's +2/15 transfers to bigger graphs where the heuristic has more room to wander.

Predicted (`speculative`): smart-escalate continues to dominate, but the escalation count grows faster than linearly (more wandering ants per cycle). The escalation budget cap (#17) may become load-bearing before this scale.

### #20 Bandwidth-throttling experiment

Status: pending. **Falsifies or confirms** the README+SYNTHESIS+CLAUDE claim that "escalation frequency is the load-bearing tunable, not network bandwidth".

Use `tc qdisc add dev eth0 root tbf` on ant-1 to throttle ant→queen TCP at 10 kbps / 100 kbps / 1 Mbps / unthrottled. Rerun smart-escalate at each setting. If success and wall are invariant under throttling, the claim is solid. If they degrade meaningfully at low bandwidth, the framing needs revisiting.

This is the experiment most directly tied to the project-pitch rewrite. Doing it early gives the new framing real empirical anchor.

### #21 Cycle-1-only escalation test

Status: pending. Further evidence for the "LLM-as-substrate-seeder" mechanism reading.

Add a `--escalate-cycle-cap N` flag. With cap=1, the LLM is only consulted during cycle 1; cycles 2+ run pure heuristic. If the "seeder" reading is right, this should match run 5's 11/15 at lower queen-CPU cost. If it doesn't, the run-5 cycle-by-cycle breakdown was misleading.

---

## Step 7 — Algorithmic improvements (NEW 2026-05-13 evening)

Substrate / algorithm work that survives the pivot and may compose well with smart-escalation.

### #22 MMAS bounded reinforcement

Status: pending. Was in `toy/README.md` open-followups since 2026-05-05; now formal task.

Add τ_min and τ_max bounds to the substrate strength calculation; only best-so-far ants deposit. Addresses run 4 Finding 3 (classical AS premature convergence onto suboptimal trunk in cycle 3). MMAS reference: Stützle & Hoos 2000.

After landing, rerun smart-escalate to see if cycle 2-3 success improves (currently 3/5 each; could go to 4-5/5 if trunk-lock-in is reduced) and overall success climbs above 11/15.

### #23 Parameterize TAU and scale with call latency

Status: pending. Small change (~10 lines).

Run 3 Finding 3: hardcoded `TAU = 60.0` breaks at slow LLM calls — pheromones decay during a cycle if calls are slow. Make TAU a CLI flag (`--tau`); optionally auto-scale at startup based on a calibration call (`TAU = 5-10 × per-call wall`). Useful for any future experiment that varies model size or hardware.

### #24 Concurrency stress test at N=50+ ants

Status: pending. Substrate primitive stress test.

Push `--ants` from 5 to 50-100 (with `--mock` so ant policy isn't the variable). Look for deposit-file corruption, read-during-write inconsistencies, filesystem inode pressure. Substrate has been clean at N=5; we need to know where it breaks.

### #25 In-memory pheromone matrix comparison rig

Status: pending. **Closes the original Task #5 load-bearing question.**

Add `--in-memory` mode where pheromones live in a `dict[str, list[deposit]]` not on disk. Run heuristic + smart-escalate at both `--in-memory` and `--filesubstrate`. Compare success, wall, convergence shape. If file-substrate behaves qualitatively differently from in-memory matrices (more noise = more diversity? less noise = stronger convergence?), this is where it shows.

This was the original Task #5 question (2026-05-04) that the OCI runs partially side-stepped. Worth answering directly.

---

## Hygiene / cleanup (NEW 2026-05-13)

### #26 Decide ant-2 fate + ant-1 ollama cleanup

Status: pending. Memory-budget hygiene on free-tier ants.

- **ant-2** was provisioned 2026-05-06 with cloud-init keep-alive but never used. Options: (a) leave running for #19 bigger-graph experiments (will use both ants in parallel), (b) shut down to reclaim free-tier slot, (c) repurpose as second substrate replica.
- **ant-1** has ollama + `smollm2:360m` (725 MB) + `smollm2:360m-instruct-q4_K_M` (270 MB) installed but architecture says heuristic-only. Options: (a) `ollama rm` both models and `systemctl disable --now ollama` to reclaim 1 GB disk + free 487 MB RAM headroom, (b) keep installed for future paid-tier experiments.

Document the decision in `oci/ANTS.md`.

### #27 Revise `feedback_llm_as_anti_diversity_prior.md` memory entry

Status: pending. Memory hygiene post-pivot.

Entry was written 2026-05-06 based on Haiku ants over-converging on laptop toy. Run 5 (Qwen-7B-Q4 via sparse smart-escalation) showed LLMs contributing *diversity in seeding*, not over-exploitation. Revise to: **LLM effect depends on call frequency** — 100% (Qwen-everywhere) converges hard; 14% (smart trigger) diversifies; 0% (heuristic) is absent. Pointed at by run 5 Findings 3 + 7.

### #28 Capture python-print-block-buffering as a tripwire memory

Status: pending. Small.

Python `print()` block-buffers when stdout is piped (tee, ssh, redirection). For long-running scripts on remote hosts (our SSH-tee pattern during runs), the log appears empty until the process exits, making "is it stuck?" indistinguishable from "is it running?". Fix: `python -u`, or `PYTHONUNBUFFERED=1`, or `flush=True` on prints. Write as `feedback_python_print_buffering.md` — short, links to `feedback_pre_action_tripwires.md`.

---

## Completed (2026-05-06)

### OCI ant host provisioning + private-VCN smoke test

- 2 × `VM.Standard.E2.1.Micro` provisioned in `MNVQ:AP-MELBOURNE-1-AD-1`: `ant-1` (130.162.196.243 / 10.0.0.107) and `ant-2` (169.224.226.141 / 10.0.0.58). Same VCN/subnet (10.0.0.0/24) as queen at 10.0.0.4.
- Queen ollama rebound to `0.0.0.0:11434` via systemd drop-in (clean, reversible). Subnet SL ingress + queen iptables ACCEPT both added for `10.0.0.0/24 → tcp/11434`. Public exposure verified absent (`nc 130.162.192.233 11434` from external times out).
- Smoke test from ant-1 and ant-2 against `qwen2.5:7b-instruct-q4_K_M`: cold 10.22s, warm 1.09s. Both ants confirmed.
- Documented in: `oci/QUEEN.md`, `oci/ANTS.md`, `feedback_oci_quota_vs_spec.md`, `feedback_oci_intra_subnet_reachability.md`. Commits `92e4718` + `8d04ddb` on `main`.

### Findings landed in the claims ledger

Two new findings tagged at the moment they were first asserted (small worked example of Step 0 discipline applied to live claims):

- "1 queen + 4 AMD x86 micros" topology → `experiment-required` against free-tier quota; demoted to "1 queen + N micros, N≤2 on current free tier".
- "Same-subnet placement implies private-VCN reachability" → `experiment-required` until two-rule fix (cloud SL + host iptables) is applied; OCI default Ubuntu ships an iptables trailing REJECT that gates independently from the cloud security list.
