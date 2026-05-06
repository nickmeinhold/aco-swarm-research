# `nick-mel` — the queen

The Qwen2.5-7B Q4 inference host for the ACO swarm, deployed on Oracle Cloud Free Tier. This file is a durable record of the queen's deployment shape so a fresh instance can pick up cold.

## Current state (2026-05-06)

| Component | State |
|-----------|-------|
| Instance | `nick-mel`, `VM.Standard.A1.Flex`, 4 OCPU / 24 GB RAM (full free A1 quota) |
| Region / AD | `ap-melbourne-1` / `MNVQ:AP-MELBOURNE-1-AD-1` |
| Public IP | `130.162.192.233` |
| Private IP | `10.0.0.4` |
| OS | Ubuntu 24.04.4 LTS (aarch64), kernel 6.17.0-1010-oracle |
| Disk | 48 GB (~3.8 GB used after install) |
| Memory | 23 GB free of 24 GB (idle) |
| ollama | v0.23.0, systemd-managed, `active`, bound to `0.0.0.0:11434` (private-VCN reachable) |
| Loaded model | `qwen2.5:7b-instruct-q4_K_M` (4.7 GB) |
| Smoke-test latency | cold ~10.2s (model load + inference); warm ~1.1s — measured from ant-1 over private VCN, 2026-05-06 |

OCI tenancy is the `[MELBOURNE]` profile in `~/.oci/config`. Tenancy OCID is in the project memory at `~/.claude/projects/-Users-nick-git-experiments-aco/memory/reference_oci_melbourne_instance.md`.

## How to use

```bash
# SSH
ssh ubuntu@130.162.192.233

# Inference (CLI)
ssh ubuntu@130.162.192.233 'ollama run qwen2.5:7b-instruct-q4_K_M "your prompt"'

# Inference (HTTP from laptop) — SSH tunnel still works
ssh -L 11434:localhost:11434 ubuntu@130.162.192.233    # tunnel
curl http://localhost:11434/api/generate -d '{"model":"qwen2.5:7b-instruct-q4_K_M","prompt":"hi","stream":false}'

# Inference (HTTP from an ant host) — direct over private VCN, no tunnel needed
# (Run from ant-1 / ant-2; 11434 is not reachable from outside 10.0.0.0/24)
curl http://10.0.0.4:11434/api/chat -d '{"model":"qwen2.5:7b-instruct-q4_K_M","stream":false,"messages":[{"role":"user","content":"hi"}]}'
```

## Network exposure (2026-05-06)

Port 11434 is reachable from ants on the **private VCN only**, not the public internet.

| Layer | Configuration |
|-------|---------------|
| ollama bind | `OLLAMA_HOST=0.0.0.0:11434` via systemd drop-in `/etc/systemd/system/ollama.service.d/override.conf` (drop-in survives package upgrades, trivially reversible) |
| Subnet SL ingress | `10.0.0.0/24 → tcp/11434` stateful, on `ocid1.securitylist.oc1.ap-melbourne-1.aaaaaaaa6ryonwsisk6ovtkxrqs3klp3jizpgifmp5hsg3jfiwkhsg6wtn4a` |
| Queen host iptables | `iptables -I INPUT 5 -p tcp -s 10.0.0.0/24 --dport 11434 -m state --state NEW -j ACCEPT`, persisted via `netfilter-persistent save` |
| Public exposure | **None.** Verified from external: `nc 130.162.192.233 11434` times out. |

Both layers were required — see `feedback_oci_intra_subnet_reachability.md` for the two-blocker lesson. Smoke test from ant-1: cold 10.22s, warm 1.09s; ant-2 warm 1.09s. Original-unit backup at `/tmp/ollama-unit-before.txt` on the queen (ephemeral; consider migrating to `/etc/ollama/` or recreating from `systemctl cat ollama` if rollback ever needed).

## What's *not* set up yet (deliberately)

- **No file-substrate scaffolding on the queen yet.** `data/pheromones/` and friends will go up only after Task #5 (laptop toy) closes — Task #5 is the gate per `TASKS.md`.
- ~~**No 4 × AMD x86 micros provisioned yet.**~~ **Update 2026-05-06:** 2 × E2.1.Micro ant hosts (`ant-1`, `ant-2`) provisioned on the same VCN/subnet — see `oci/ANTS.md`. The "4 micros" target in the original spec is `experiment-required` against actual free-tier quota (cap is 2 per tenancy in `ap-melbourne-1`); see `feedback_oci_quota_vs_spec.md`. Intra-subnet ant→queen TCP/11434 reachability **verified 2026-05-06** — see `feedback_oci_intra_subnet_reachability.md`.
- **No keep-alive cron on the queen.** Account is presumably PAYG; if it isn't, idle reclamation is a risk — see `~/git/experiments/imagineering-infra/scripts/oci-retry-provision.sh` for the keep-alive pattern. (Ants got a keep-alive cron from cloud-init — see `oci/ANTS.md`.)

## Architectural notes

**Queen↔ant bandwidth is a load-bearing tunable**, not an incidental constraint. Inference latency on this CPU-only ARM A1 is ~10s/short-completion for 7B Q4. That sets the practical ant-step rate. The "octopus brain ↔ arm" hypothesis (`SYNTHESIS.md` substrate spec) is that giving ants their own small models (SmolLM2-360M on micros) for routine decisions, and only escalating to the queen for hard reasoning, is the right shape — measurable once micros are up.

**Why ollama and not llama.cpp directly**: ollama gives us a uniform HTTP API across queen and any future host (local Mac for development), with built-in model management and concurrency handling. The cost is one extra layer over `llama.cpp`; the benefit is operational uniformity. Reasonable trade for now.
