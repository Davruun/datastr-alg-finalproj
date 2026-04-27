"""
mindmap.py
----------
WikiMindmap: builds a knowledge distance map centred on one Wikipedia article.

Given a centre page A and a list of target pages [B, C, D, …], it:
  1. Runs BFS shortest-path from A to each target
  2. Records the hop-distance and the full path for each pair
  3. Assembles a combined graph of all discovered paths
  4. Provides a radial visualisation where distance from A = visual distance

This answers the question: "How far is everything from what I care about?"
"""

from __future__ import annotations
from collections import deque
from dataclasses import dataclass, field

try:
    import networkx as nx
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    _VIZ_AVAILABLE = True
except ImportError:
    _VIZ_AVAILABLE = False

from .scraper import WikiScraper


@dataclass
class PathResult:
    """Result of a single centre → target BFS search."""
    center: str
    target: str
    path: list[str] | None         # None if not found within max_pages
    hops: int | None = field(init=False)

    def __post_init__(self) -> None:
        self.hops = len(self.path) - 1 if self.path else None

    @property
    def found(self) -> bool:
        return self.path is not None

    def __str__(self) -> str:
        if not self.found:
            return f"{self.center!r} → {self.target!r}  [NOT FOUND]"
        return (
            f"{self.center!r} → {self.target!r}  "
            f"({self.hops} hop{'s' if self.hops != 1 else ''})  "
            f"{'  →  '.join(self.path)}"
        )


class WikiMindmap:
    """
    Builds a knowledge distance map from one centre Wikipedia article.
    """

    def __init__(
        self,
        center: str,
        scraper: WikiScraper | None = None,
        max_pages: int = 300,
        verbose: bool = True,
    ) -> None:
        self.center    = center
        self.scraper   = scraper or WikiScraper()
        self.max_pages = max_pages
        self.verbose   = verbose
        self.results:  list[PathResult] = []

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------

    def build(self, targets: list[str]) -> "WikiMindmap":
        """
        Run BFS from `center` to each page in `targets`.
        """
        self.results = []
        for target in targets:
            if self.verbose:
                print(f"\n── Searching: {self.center!r}  →  {target!r} ──")
            path = self._bfs(self.center, target)
            result = PathResult(center=self.center, target=target, path=path)
            self.results.append(result)
            if self.verbose:
                status = f"{result.hops} hops" if result.found else "NOT FOUND"
                print(f"   Result: {status}")
        return self

    def _bfs(self, start: str, target: str) -> list[str] | None:
        """Internal BFS that returns the shortest path or None."""
        if start == target:
            return [start]

        visited: set[str] = set()
        parent_map: dict[str, str | None] = {start: None}
        queue: deque[str] = deque([start])
        pages_checked = 0

        while queue and pages_checked < self.max_pages:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            pages_checked += 1

            if self.verbose:
                print(f"  [{pages_checked:>4}/{self.max_pages}] {current}")

            for link in self.scraper.get_links(current):
                if link not in parent_map:
                    parent_map[link] = current
                    if link == target:
                        return self._reconstruct(parent_map, target)
                    queue.append(link)

        return None

    @staticmethod
    def _reconstruct(parent_map: dict[str, str | None], target: str) -> list[str]:
        path: list[str] = []
        cur: str | None = target
        while cur is not None:
            path.append(cur)
            cur = parent_map.get(cur)
        path.reverse()
        return path

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def summary(self) -> None:
        """Print a sorted distance table for all targets."""
        if not self.results:
            print("No results yet — call build() first.")
            return

        found    = [r for r in self.results if r.found]
        notfound = [r for r in self.results if not r.found]
        found.sort(key=lambda r: r.hops)

        print(f"\n{'='*60}")
        print(f"Knowledge distance from: '{self.center}'")
        print(f"{'='*60}")
        print(f"{'Target':<40} {'Hops':>5}  Path")
        print(f"{'-'*60}")
        for r in found:
            path_str = " → ".join(r.path) if r.path else ""
            print(f"{r.target:<40} {r.hops:>5}  {path_str}")
        for r in notfound:
            print(f"{r.target:<40} {'–':>5}  (not found within {self.max_pages} pages)")
        print(f"{'='*60}\n")

    # ------------------------------------------------------------------
    # Visualise
    # ------------------------------------------------------------------

    def visualize(
        self,
        figsize: tuple[int, int] = (14, 10),
        save_path: str | None = None,
    ) -> None:
        """
        Draw a radial knowledge-distance map.

        The centre page sits in the middle.  Each target is positioned
        along a ring whose radius is proportional to its hop distance
        from the centre.  Intermediate pages on each path are shown
        as smaller nodes along the route.
        """
        if not _VIZ_AVAILABLE:
            raise ImportError("matplotlib and networkx are required for visualize().")
        if not self.results:
            print("No results yet — call build() first.")
            return

        G = nx.DiGraph()
        node_roles: dict[str, str] = {self.center: "center"}

        # Build a combined directed graph of all shortest paths
        for r in self.results:
            if not r.found or r.path is None:
                continue
            node_roles.setdefault(r.target, "target")
            for i, page in enumerate(r.path):
                node_roles.setdefault(page, "intermediate")
                if i < len(r.path) - 1:
                    G.add_edge(page, r.path[i + 1])

        # Layout: spring with center pinned
        pos = nx.spring_layout(G, seed=42, k=1.5)
        pos[self.center] = (0, 0)  # force centre to origin

        # Node colours by role
        color_map = {"center": "#e74c3c", "target": "#2ecc71", "intermediate": "#4DB8FF"}
        node_colors = [color_map.get(node_roles.get(n, "intermediate"), "#aaa") for n in G.nodes()]
        node_sizes  = [
            2000 if node_roles.get(n) == "center"
            else 900 if node_roles.get(n) == "target"
            else 300
            for n in G.nodes()
        ]

        fig, ax = plt.subplots(figsize=figsize)

        nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=node_sizes, alpha=0.9)
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#888", arrows=True,
                               arrowsize=15, width=1.2, alpha=0.7,
                               connectionstyle="arc3,rad=0.05")

        # Only label centre and targets to keep the plot readable
        label_nodes = {n: n for n in G.nodes() if node_roles.get(n) in ("center", "target")}
        nx.draw_networkx_labels(G, pos, labels=label_nodes, ax=ax, font_size=8, font_weight="bold")

        # Hop-distance annotations on target nodes
        found = [r for r in self.results if r.found]
        for r in found:
            if r.target in pos:
                x, y = pos[r.target]
                ax.annotate(
                    f"{r.hops} hop{'s' if r.hops != 1 else ''}",
                    xy=(x, y), xytext=(x, y + 0.08),
                    ha="center", fontsize=7, color="#155724",
                )

        # Legend
        patches = [
            mpatches.Patch(color="#e74c3c", label=f"Centre: {self.center}"),
            mpatches.Patch(color="#2ecc71", label="Target pages"),
            mpatches.Patch(color="#4DB8FF", label="Intermediate pages"),
        ]
        ax.legend(handles=patches, loc="upper left", fontsize=9)
        ax.set_title(
            f"Knowledge distance map — centre: '{self.center}'",
            fontsize=14, pad=15,
        )
        ax.axis("off")
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=150)
            print(f"Saved to {save_path}")
        plt.show()

    # ------------------------------------------------------------------
    # Convenience accessors
    # ------------------------------------------------------------------

    def distances(self) -> dict[str, int | None]:
        """Return {target: hops} for all results (None if not found)."""
        return {r.target: r.hops for r in self.results}

    def closest(self) -> PathResult | None:
        """Return the PathResult with the fewest hops."""
        found = [r for r in self.results if r.found]
        return min(found, key=lambda r: r.hops) if found else None

    def farthest(self) -> PathResult | None:
        """Return the PathResult with the most hops."""
        found = [r for r in self.results if r.found]
        return max(found, key=lambda r: r.hops) if found else None
