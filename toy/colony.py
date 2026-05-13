# /// script
# requires-python = ">=3.12"
# dependencies = ["anthropic>=0.39", "httpx>=0.27"]
# ///
"""
ACO laptop toy — minimal file-based stigmergy substrate test.

Task #5 (TASKS.md): does file-based persistent stigmergy behave qualitatively
differently from in-memory pheromone matrices? This is the smallest viable
demonstration: synthetic KG, 5 ants × 3 cycles, file-based deposits with
mtime-decoupled (timestamp-in-payload) decay, async-concurrent ants per cycle.

Run:
  uv run colony.py                # LLM ants (Haiku 4.5) — needs ANTHROPIC_API_KEY
  uv run colony.py --mock         # heuristic ants, no API calls
  uv run colony.py --reset --mock # wipe substrate, then run mock
"""

import argparse
import asyncio
import hashlib
import json
import math
import random
import shutil
import time
from pathlib import Path

# --- Substrate config ---
ROOT = Path(__file__).parent / "data" / "pheromones"
TAU = 60.0  # decay time-constant in seconds; strength = quality * exp(-age/TAU)


def edge_key(a: str, b: str) -> str:
    a, b = sorted([a, b])
    return f"{a}__{b}"


# --- Knowledge graph (synthetic ER + chain backbone for connectivity) ---
def make_kg(n_nodes: int = 20, avg_degree: int = 4, seed: int = 42):
    rng = random.Random(seed)
    nodes = [f"n{i}" for i in range(n_nodes)]
    adj: dict[str, set[str]] = {n: set() for n in nodes}
    # Backbone — guarantees source can reach target
    for i in range(n_nodes - 1):
        adj[nodes[i]].add(nodes[i + 1])
        adj[nodes[i + 1]].add(nodes[i])
    # Random extra edges
    extra = max(0, (n_nodes * avg_degree) // 2 - (n_nodes - 1))
    for _ in range(extra):
        a, b = rng.sample(nodes, 2)
        adj[a].add(b)
        adj[b].add(a)
    return {n: sorted(adj[n]) for n in nodes}


# --- Substrate primitives ---
def deposit(edge: str, agent_id: str, quality: float) -> Path:
    """Write a deposit file. The file IS the pheromone — its existence + payload encode strength."""
    d = ROOT / edge
    d.mkdir(parents=True, exist_ok=True)
    sig = hashlib.sha256(f"{agent_id}|{edge}|{quality}".encode()).hexdigest()[:12]
    ts_ns = time.time_ns()
    payload = {
        "agent": agent_id,
        "edge": edge,
        "quality": quality,
        "ts": ts_ns / 1e9,
        "sig": sig,
    }
    # ts_ns prefix gives natural sort + collision-resistant filenames under concurrency
    f = d / f"{ts_ns}-{agent_id}-{int(quality * 1000):04d}.dep"
    f.write_text(json.dumps(payload))
    return f


def strength(edge: str, now: float | None = None) -> float:
    """Decay-weighted sum across all deposits on this edge."""
    d = ROOT / edge
    if not d.exists():
        return 0.0
    if now is None:
        now = time.time()
    total = 0.0
    for f in d.iterdir():
        if not f.name.endswith(".dep"):
            continue
        try:
            payload = json.loads(f.read_text())
            age = now - payload["ts"]
            total += payload["quality"] * math.exp(-age / TAU)
        except Exception:
            continue
    return total


def evaporate(max_age_sec: float = 600.0) -> int:
    """Delete deposits older than max_age (effectively zero strength). Returns count removed."""
    if not ROOT.exists():
        return 0
    now = time.time()
    removed = 0
    for edge_dir in ROOT.iterdir():
        if not edge_dir.is_dir():
            continue
        for f in edge_dir.iterdir():
            if not f.name.endswith(".dep"):
                continue
            try:
                payload = json.loads(f.read_text())
                if now - payload["ts"] > max_age_sec:
                    f.unlink()
                    removed += 1
            except Exception:
                f.unlink()
                removed += 1
    return removed


# --- LLM backends ---
class QueenClient:
    """LLM backend pointed at an ollama HTTP API (e.g. the OCI queen via private VCN).

    Holds the httpx.AsyncClient and the model name so llm_step can stay polymorphic:
    isinstance(client, QueenClient) → ollama; otherwise → AsyncAnthropic.
    """

    def __init__(self, base_url: str, model: str):
        import httpx
        self.http = httpx.AsyncClient(timeout=120.0)
        self.base_url = base_url.rstrip("/")
        self.model = model


# --- Ant policies ---
SYS_PROMPT = """\
You are a foraging ant in a swarm. You walk on a graph and follow pheromone trails left by other ants.

You will be told:
- Your current node
- The target node you are trying to reach
- Your path so far (to avoid pointless loops)
- Your neighbours and the pheromone strength on each edge to them

Strong pheromone (high number) means other ants found that edge useful. Weak/zero means unexplored. Balance exploitation (follow strong trails) with exploration (try unmarked edges sometimes), and avoid revisiting nodes in your path unless cornered.

Reply with EXACTLY one word: the name of the neighbour to walk to. No reasoning, no preamble.\
"""


async def llm_step(client, current, target, neighbours_with_str, path):
    msg = (
        f"Current: {current}\n"
        f"Target: {target}\n"
        f"Path so far: {' -> '.join(path)}\n"
        f"Neighbours and pheromone strengths:\n"
        + "\n".join(f"  {n}: {s:.3f}" for n, s in neighbours_with_str)
    )
    if isinstance(client, QueenClient):
        r = await client.http.post(
            f"{client.base_url}/api/chat",
            json={
                "model": client.model,
                "stream": False,
                "messages": [
                    {"role": "system", "content": SYS_PROMPT},
                    {"role": "user", "content": msg},
                ],
                "options": {"num_predict": 20},
            },
        )
        r.raise_for_status()
        text = r.json()["message"]["content"]
        return text.strip().split()[0].strip(".,;:!?")
    resp = await client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=20,
        system=[{"type": "text", "text": SYS_PROMPT, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": msg}],
    )
    return resp.content[0].text.strip().split()[0].strip(".,;:!?")


def heuristic_step(current, target, neighbours_with_str, path):
    """Mock ant for substrate plumbing tests — epsilon-greedy on pheromone."""
    visited = set(path)
    options = [(n, s) for n, s in neighbours_with_str if n not in visited]
    if not options:
        options = list(neighbours_with_str)
    if random.random() < 0.2:
        return random.choice(options)[0]
    return max(options, key=lambda x: x[1] + random.random() * 0.05)[0]


async def run_ant(ant_id, kg, source, target, max_steps, client, mock, escalate):
    """Walk an ant from source toward target.

    Modes:
      - mock=True: heuristic ε-greedy every step. No LLM.
      - mock=False, escalate=False, client set: LLM every step (run 1 shape).
      - mock=False, escalate=True, client set: heuristic by default; escalate
        to LLM only when cornered (all neighbours visited). TASKS.md #15.
    """
    path = [source]
    current = source
    escalations = 0
    for _ in range(max_steps):
        if current == target:
            break
        nbrs = kg[current]
        if not nbrs:
            break
        # Visited-filter: hide revisited neighbours from the LLM unless cornered.
        # Soft instructions ("avoid revisiting") are unreliable on smaller models
        # (Qwen-7B-Q4 produced n12→n3→n12→n3 loops in 2026-05-12-oci-run-1). Only
        # relax the filter when every neighbour has been seen — "cornered" mode.
        visited = set(path)
        nbrs_unvisited = [n for n in nbrs if n not in visited]
        cornered = not nbrs_unvisited
        nbrs_visible = nbrs if cornered else nbrs_unvisited
        nbrs_str = [(n, strength(edge_key(current, n))) for n in nbrs_visible]
        try:
            if mock or client is None:
                nxt = heuristic_step(current, target, nbrs_str, path)
            elif escalate and not cornered:
                # Heuristic-on-ant: cheap default decision, save the LLM for stuck cases.
                nxt = heuristic_step(current, target, nbrs_str, path)
            else:
                # All-LLM (escalate=False) OR escalation-on-cornered: defer to the LLM.
                nxt = await llm_step(client, current, target, nbrs_str, path)
                escalations += 1
            if nxt not in nbrs_visible:
                # LLM returned a node outside what we showed it (hallucination or a
                # filtered visited revisit). Fall back to highest pheromone among
                # what was visible — keeps the filter honest.
                nxt = max(nbrs_str, key=lambda x: x[1])[0]
        except Exception as e:
            print(f"  ant {ant_id} step error: {e}")
            break
        path.append(nxt)
        current = nxt
    success = current == target
    quality = (1.0 / len(path)) if success else 0.0  # shorter winning path => higher quality
    if success:
        for a, b in zip(path, path[1:]):
            deposit(edge_key(a, b), ant_id, quality)
    return {"ant": ant_id, "path": path, "success": success, "quality": quality, "escalations": escalations}


# --- Colony loop ---
async def run_cycle(cycle_n, n_ants, kg, source, target, max_steps, client, mock, escalate):
    print(f"\n=== Cycle {cycle_n} ===")
    tasks = [
        run_ant(f"a{i}", kg, source, target, max_steps, client, mock, escalate)
        for i in range(n_ants)
    ]
    results = await asyncio.gather(*tasks)
    for r in results:
        marker = "OK  " if r["success"] else "FAIL"
        esc = f" esc={r['escalations']}" if r.get('escalations') else ""
        print(f"  [{marker}] {r['ant']} q={r['quality']:.3f} len={len(r['path']):2d}{esc} path={'->'.join(r['path'])}")
    n_ok = sum(1 for r in results if r["success"])
    n_esc = sum(r.get("escalations", 0) for r in results)
    print(f"  Cycle {cycle_n}: {n_ok}/{n_ants} reached target  ({n_esc} escalations)")
    return results


def show_top_edges(kg, k=8):
    edges = []
    for n, nbrs in kg.items():
        for m in nbrs:
            if n < m:
                e = edge_key(n, m)
                s = strength(e)
                if s > 0:
                    n_dep = sum(1 for f in (ROOT / e).iterdir() if f.name.endswith(".dep"))
                    edges.append((e, s, n_dep))
    edges.sort(key=lambda x: -x[1])
    if edges:
        print("  Top pheromone edges:")
        for e, s, n_dep in edges[:k]:
            print(f"    {e}: strength={s:.3f}  deposits={n_dep}")
    else:
        print("  (no pheromone yet)")


async def main():
    p = argparse.ArgumentParser()
    p.add_argument("--mock", action="store_true", help="heuristic ants (no API calls)")
    p.add_argument("--queen", action="store_true", help="ollama-on-queen ants (private VCN)")
    p.add_argument("--queen-url", default="http://10.0.0.4:11434",
                   help="ollama HTTP base URL (default: queen private IP)")
    p.add_argument("--queen-model", default="qwen2.5:7b-instruct-q4_K_M")
    p.add_argument("--escalate", action="store_true",
                   help="heuristic by default, escalate to LLM only when cornered (TASKS.md #15)")
    p.add_argument("--reset", action="store_true", help="wipe substrate before run")
    p.add_argument("--ants", type=int, default=5)
    p.add_argument("--cycles", type=int, default=3)
    p.add_argument("--nodes", type=int, default=20)
    p.add_argument("--max-steps", type=int, default=12)
    args = p.parse_args()

    if args.reset and ROOT.exists():
        shutil.rmtree(ROOT)
    ROOT.mkdir(parents=True, exist_ok=True)

    kg = make_kg(n_nodes=args.nodes, avg_degree=4)
    source, target = "n0", f"n{args.nodes - 1}"
    print(f"KG: {args.nodes} nodes, source={source}, target={target}")
    print(f"  source ({source}) neighbours: {kg[source]}")
    print(f"  target ({target}) neighbours: {kg[target]}")
    print(f"  TAU={TAU}s, ants/cycle={args.ants}, cycles={args.cycles}, max_steps={args.max_steps}, mock={args.mock}")

    client = None
    if args.queen:
        client = QueenClient(args.queen_url, args.queen_model)
        print(f"  backend: queen @ {args.queen_url} model={args.queen_model}")
    elif not args.mock:
        from anthropic import AsyncAnthropic
        client = AsyncAnthropic()
        print("  backend: Anthropic Haiku 4.5")
    else:
        print("  backend: mock (heuristic ε-greedy)")

    all_results = []
    for c in range(1, args.cycles + 1):
        results = await run_cycle(c, args.ants, kg, source, target, args.max_steps, client, args.mock, args.escalate)
        all_results.append(results)
        removed = evaporate(max_age_sec=600)
        if removed:
            print(f"  evaporator: removed {removed} stale deposits")
        show_top_edges(kg)

    n_total_ok = sum(r["success"] for cycle in all_results for r in cycle)
    n_total = args.cycles * args.ants
    n_dep_files = sum(1 for _ in ROOT.glob("*/*.dep"))
    n_esc = sum(r.get("escalations", 0) for cycle in all_results for r in cycle)
    esc_str = f", {n_esc} LLM escalations" if args.escalate else ""
    print(f"\n=== Summary: {n_total_ok}/{n_total} successful, {n_dep_files} deposit files on disk{esc_str} ===")


if __name__ == "__main__":
    asyncio.run(main())
