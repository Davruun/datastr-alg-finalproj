"""
run_example.py
--------------
Fast & Easy demo of BFS exploration vs DFS exploration

Run from the project root with:
    python3 run_example.py

What to watch for
-----------------
BFS  — pages are visited layer by layer. All direct links from
       "Data science" come first (~200 pages), then their links,
       then those links' links. The visited set stays wide and close
       to the starting topic.

DFS  — immediately dives into the FIRST link it finds and follows
       that chain as deep as possible before backtracking. Within
       the first 20 pages you'll likely be far from "Data science" —
       possibly in history, philosophy, or something surprising.
"""

from src import BFSFrontier, DFSFrontier, WikiScraper, WikiExplorer

SCRAPER   = WikiScraper(delay=0.3)
START     = "Cat"
MAX_PAGES = 20   

# ── BFS ──────────────────────────────────────────────────────────────────────
print("=" * 60)
print("BFS EXPLORATION  (Queue / FIFO / layer-by-layer)")
print("=" * 60)

bfs_explorer = WikiExplorer(
    BFSFrontier(),
    scraper=SCRAPER,
    max_pages=MAX_PAGES,
    verbose=True,
)
bfs_graph = bfs_explorer.explore(START)

print(f"\nBFS result: {bfs_graph}")
print(f"Pages visited: {sorted(bfs_graph.visited)}\n")

# ── DFS ──────────────────────────────────────────────────────────────────────
print("=" * 60)
print("DFS EXPLORATION  (Stack / LIFO / deep-dive)")
print("=" * 60)

dfs_explorer = WikiExplorer(
    DFSFrontier(),
    scraper=SCRAPER,
    max_pages=MAX_PAGES,
    verbose=True,
)
dfs_graph = dfs_explorer.explore(START)

print(f"\nDFS result: {dfs_graph}")
print(f"Pages visited: {sorted(dfs_graph.visited)}\n")

# ── Comparison ────────────────────────────────────────────────────────────────
print("=" * 60)
print("COMPARISON")
print("=" * 60)

bfs_only = bfs_graph.visited - dfs_graph.visited
dfs_only = dfs_graph.visited - bfs_graph.visited
shared   = bfs_graph.visited & dfs_graph.visited

print(f"Pages visited by BOTH   : {len(shared)}")
print(f"Pages visited by BFS only: {len(bfs_only)}  → {sorted(bfs_only)[:5]} ...")
print(f"Pages visited by DFS only: {len(dfs_only)}  → {sorted(dfs_only)[:5]} ...")
print()
print(f"Notice: BFS stays close to '{START}' (mostly nearby topics).")
print( "        DFS wanders far — its unique pages will look unrelated.")
