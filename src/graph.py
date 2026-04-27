"""
graph.py
--------
Graph data structures for the Wikipedia knowledge network.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class WikiNode:
    """
    A node in the Wikipedia graph, corresponding to one article.
    """

    title: str
    parent: Optional[str] = field(default=None)
    depth: int = field(default=0)

    def __hash__(self) -> int:
        return hash(self.title)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, WikiNode):
            return self.title == other.title
        return NotImplemented

    def __repr__(self) -> str:
        return f"WikiNode(title={self.title!r}, depth={self.depth})"


class WikiGraph:
    """
    Stores the explored Wikipedia subgraph.
    """

    def __init__(self) -> None:
        self.adjacency: dict[str, list[str]] = {}
        self.visited: set[str] = set()
        self.parents: dict[str, Optional[str]] = {}

    # ------------------------------------------------------------------
    # Mutation helpers
    # ------------------------------------------------------------------

    def add_edge(self, source: str, target: str) -> None:
        """Record a directed edge source → target."""
        neighbors = self.adjacency.setdefault(source, [])
        if target not in neighbors:
            neighbors.append(target)

    def mark_visited(self, title: str, parent: Optional[str] = None) -> None:
        """Mark a page as visited and record how it was reached."""
        self.visited.add(title)
        if title not in self.parents:
            self.parents[title] = parent

    # ------------------------------------------------------------------
    # Query helpers
    # ------------------------------------------------------------------

    def is_visited(self, title: str) -> bool:
        return title in self.visited

    def neighbors(self, title: str) -> list[str]:
        return self.adjacency.get(title, [])

    def reconstruct_path(self, start: str, target: str) -> list[str]:
        """
        Walk the `parents` dict backwards from target to start.

        Returns an ordered list of page titles from start to target.
        Returns an empty list if the target is unreachable.
        """
        if target not in self.parents:
            return []
        path: list[str] = []
        current: Optional[str] = target
        while current is not None:
            path.append(current)
            current = self.parents.get(current)
        path.reverse()
        return path if path[0] == start else []

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------

    def node_count(self) -> int:
        return len(self.visited)

    def edge_count(self) -> int:
        return sum(len(v) for v in self.adjacency.values())

    def __repr__(self) -> str:
        return f"WikiGraph(nodes={self.node_count()}, edges={self.edge_count()})"
