# `ant-1`, `ant-2` — the ant hosts

The SmolLM2-360M (intended) inference hosts for the ACO swarm, deployed on Oracle Cloud Free Tier alongside the queen `nick-mel`. This file is a durable record of the ants' deployment shape so a fresh instance can pick up cold. Companion to `oci/QUEEN.md`.

## Current state (2026-05-06)

Both instances `RUNNING` as of 2026-05-06 16:37:45 AEST. Image: `Canonical-Ubuntu-22.04-2026.04.30-1`. SSH user `ubuntu`, key `~/.ssh/id_ed25519` (same key as the queen).

| Host | Public IP | Private IP | Shape | OCID |
|---|---|---|---|---|
| ant-1 | 130.162.196.243 | 10.0.0.107 | `VM.Standard.E2.1.Micro` (1/8 OCPU, 1 GB, x86_64) | `ocid1.instance.oc1.ap-melbourne-1.anwwkljr2htpxkqc42ct5irnmalxqn4rd5nphicqgzzyxqiadheo3lkkzc7a` |
| ant-2 | 169.224.226.141 | 10.0.0.58 | `VM.Standard.E2.1.Micro` (1/8 OCPU, 1 GB, x86_64) | `ocid1.instance.oc1.ap-melbourne-1.anwwkljr2htpxkqcjqvuiichi2ne3qcw6xxqbb66wl6dmlf2o6qqd46oqgga` |

- **Region / AD**: `ap-melbourne-1` / `MNVQ:AP-MELBOURNE-1-AD-1` (single-AD region)
- **VCN / subnet**: `xdeca-vcn` / `xdeca-subnet` (10.0.0.0/24) — same subnet as queen at 10.0.0.4
- **Cloud-init**: included a 6-hourly keep-alive cron lifted from `~/git/experiments/imagineering-infra/scripts/oci-retry-provision.sh` to defend against idle-reclamation
- **Ollama / model**: not yet installed. The intended ant model is SmolLM2-360M; install pending Task #6 prerequisites.

OCI tenancy is the `[MELBOURNE]` profile in `~/.oci/config`. Tenancy OCID is in `~/.claude/projects/-Users-nick-git-experiments-aco/memory/reference_oci_melbourne_instance.md`.

## How to use

```bash
# SSH to either ant
ssh ubuntu@130.162.196.243   # ant-1
ssh ubuntu@169.224.226.141   # ant-2

# Listing instances in the tenancy
oci --profile MELBOURNE compute instance list \
  --compartment-id <tenancy-ocid> \
  --output table --query 'data[*].{name:"display-name",ip:"primary-private-ip",state:"lifecycle-state"}'
```

## Findings — 2026-05-06 provisioning event

These are the load-bearing observations from the provisioning run. Both are tagged per the project's claims-ledger convention (see `TASKS.md` Step 0 — `verified` / `reported-by-agent` / `speculative` / `experiment-required`).

### Finding 1 — free-tier quota caps ant count at 2

**Tag: `verified`** (live `oci limits resource-availability get` call, 2026-05-06).

```bash
oci --profile MELBOURNE limits resource-availability get \
  --compartment-id <tenancy-ocid> \
  --service-name compute \
  --limit-name standard-e2-micro-core-count \
  --availability-domain MNVQ:AP-MELBOURNE-1-AD-1
# returned: available: 2, used: 0   (pre-provision)
```

The deployment topology described in `swarm-research/SYNTHESIS.md`, root `CLAUDE.md`, and project memory `project_aco_swarm.md` ("1 queen + 4 AMD x86 micros") was inherited from generic OCI free-tier folklore, not verified against this tenancy's actual quota. Free tier is 2 × E2.1.Micro per tenancy in `ap-melbourne-1`; Melbourne is single-AD, so AD-spreading isn't a workaround.

**Implication:** the "4 micros" claim is `experiment-required` against quota. Demote to "1 queen + N micros, N ≤ 2 on current OCI free tier in this tenancy" in the next pass over those documents. Architectures that depend on 4+ ants need to flex to 2, or motivate a paid-tier ask.

### Finding 2 — same-subnet ≠ intra-subnet reachability (resolved 2026-05-06)

**Tag (ICMP fact): `verified`** — ICMP from each ant to queen 10.0.0.4 returned 100% packet loss; root cause is the subnet security list permitting only ICMP type-3 from 10.0.0.0/16 (path-MTU only), not echo-request.

**Tag (TCP/11434 ant→queen): `verified` working** as of 2026-05-06. Cold call (model load + inference) **10.22s**; warm call **1.09s**; same numbers from both ants. Resolution required two changes — see Finding 3.

**Tag (architecture implication): `verified`** — same-subnet placement does NOT imply intra-subnet reachability. OCI's default-deny posture on the security list combines with the default Ubuntu host iptables (`REJECT --reject-with icmp-host-prohibited` trailing rule) to require *two* rules per service exposed on the private VCN. The "ant → queen private IP" path is now sound; any future ant-hosted service will hit the same wall.

### Finding 3 — two-blocker network on the OCI default Ubuntu image

**Tag: `verified`** (Finding 2's resolution surfaced it).

To expose a service on the OCI private VCN between two instances, you need:

1. **Subnet security list ingress rule** scoped to the source CIDR + destination port (stateful TCP).
2. **Host iptables ACCEPT rule** scoped to the same CIDR + port, inserted **before** the trailing `REJECT --reject-with icmp-host-prohibited` rule that ships in the default OCI Ubuntu chain. Persist with `netfilter-persistent save`.

Diagnostic: after fixing only (1), `nc` returns `No route to host` rather than timing out. That message is the ICMP-host-prohibited reject from layer (2) — it's diagnostic gold, not a routing issue.

**Implication for ant-hosted services:** ant-1 and ant-2 run the same default Ubuntu 22.04 image. When SmolLM2-360M lands on the ants and the queen (or a peer ant) needs to call it, both rules will need to be re-added per service. Pre-empting this in the cloud-init for the ant SmolLM2 deployment is worth considering.

## What's *not* set up yet

- **No ollama on ants.** Pending Task #6 prerequisites and the SmolLM2-360M install.
- **No file-substrate scaffolding on ants.** `data/pheromones/` etc. land after Task #5 closes.
- ~~**No verified intra-subnet ant→queen path**~~ — **resolved 2026-05-06**, see Findings 2 & 3 above.
- **No paid-tier ask.** With the 2-micro cap, the "4 ants" target is unreachable on free tier (Finding 1 above).
- **No reverse path queen→ant verified.** When ants host SmolLM2, the queen calling them on the private VCN will need the same two-rule pattern (SL + ant-side iptables) — see Finding 3.

## Connections

- Companion: `oci/QUEEN.md`
- Cross-links to memory: `feedback_oci_quota_vs_spec.md`, `feedback_oci_intra_subnet_reachability.md`, `reference_oci_melbourne_instance.md`
- Tasks: relevant to Task #6 (laptop toy → OCI deployment gate)
