# `nick-mel` — the queen

The Qwen2.5-7B Q4 inference host for the ACO swarm, deployed on Oracle Cloud Free Tier. This file is a durable record of the queen's deployment shape so a fresh instance can pick up cold.

## Current state (2026-05-05)

| Component | State |
|-----------|-------|
| Instance | `nick-mel`, `VM.Standard.A1.Flex`, 4 OCPU / 24 GB RAM (full free A1 quota) |
| Region / AD | `ap-melbourne-1` / `MNVQ:AP-MELBOURNE-1-AD-1` |
| Public IP | `130.162.192.233` |
| Private IP | `10.0.0.4` |
| OS | Ubuntu 24.04.4 LTS (aarch64), kernel 6.17.0-1010-oracle |
| Disk | 48 GB (~3.8 GB used after install) |
| Memory | 23 GB free of 24 GB (idle) |
| ollama | v0.23.0, systemd-managed, `active` |
| Loaded model | `qwen2.5:7b-instruct-q4_K_M` (4.7 GB) |
| Smoke-test latency | ~10s wall for one short inference (first call, includes model load) |

OCI tenancy is the `[MELBOURNE]` profile in `~/.oci/config`. Tenancy OCID is in the project memory at `~/.claude/projects/-Users-nick-git-experiments-aco/memory/reference_oci_melbourne_instance.md`.

## How to use

```bash
# SSH
ssh ubuntu@130.162.192.233

# Inference (CLI)
ssh ubuntu@130.162.192.233 'ollama run qwen2.5:7b-instruct-q4_K_M "your prompt"'

# Inference (HTTP via local Ollama API on the queen)
ssh -L 11434:localhost:11434 ubuntu@130.162.192.233    # tunnel
curl http://localhost:11434/api/generate -d '{"model":"qwen2.5:7b-instruct-q4_K_M","prompt":"hi","stream":false}'
```

## What's *not* set up yet (deliberately)

- **No public network exposure of port 11434.** Ollama is bound to localhost only on the queen — access via SSH tunnel or local-network only. This is the right default; don't open 11434 to the public internet.
- **No file-substrate scaffolding on the queen yet.** `data/pheromones/` and friends will go up only after Task #5 (laptop toy) closes — Task #5 is the gate per `TASKS.md`.
- **No 4 × AMD x86 micros provisioned yet.** The full project spec calls for 4 micros as ant hosts. They'll be provisioned when the laptop toy answers the "does file-stigmergy work qualitatively differently" question.
- **No keep-alive cron.** Account is presumably PAYG; if it isn't, idle reclamation is a risk — see `~/git/experiments/imagineering-infra/scripts/oci-retry-provision.sh` for the keep-alive pattern.

## Architectural notes

**Queen↔ant bandwidth is a load-bearing tunable**, not an incidental constraint. Inference latency on this CPU-only ARM A1 is ~10s/short-completion for 7B Q4. That sets the practical ant-step rate. The "octopus brain ↔ arm" hypothesis (`SYNTHESIS.md` substrate spec) is that giving ants their own small models (SmolLM2-360M on micros) for routine decisions, and only escalating to the queen for hard reasoning, is the right shape — measurable once micros are up.

**Why ollama and not llama.cpp directly**: ollama gives us a uniform HTTP API across queen and any future host (local Mac for development), with built-in model management and concurrency handling. The cost is one extra layer over `llama.cpp`; the benefit is operational uniformity. Reasonable trade for now.
