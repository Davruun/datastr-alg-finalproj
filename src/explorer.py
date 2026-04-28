"""
explorer.py
-----------
WikiExplorer: the  engine that wires together the Frontier, Scraper, and Graph.
The same class drives both BFS and DF]= by receiving a different subclass.

explore(start, max_pages, max_depth)
    Traverse the Wikipedia graph from `start`, stopping at whichever
    limit (page count OR depth) is hit first.

shortest_path(start, target, max_pages)
    BFS-based shortest-path search from `start` to `target`.
    Always uses BFS regardless of the configured frontier
    Returns the path as an ordered list of page titles, or None.
"""

from __future__ import annotations
from collections import deque

from .frontier import Frontier, BFSFrontier
from .scraper import WikiScraper
from .graph import WikiGraph, WikiNode


class WikiExplorer:
    """
    Polymorphic Wikipedia graph explorer.

    Parameters
    ----------
    frontier : Frontier
        A BFSFrontier for breadth-first or DFSFrontier for depth-first
        exploration.  Any custom Frontier subclass also works.
    scraper : WikiScraper, optional
        Provide your own scraper (e.g. a mock for testing).
    max_pages : int
        Default cap on pages visited per run (can be overridden per call).
    max_depth : int or None
        Default depth cap. None means no depth limit.
    verbose : bool
        Print progress while exploring.
    """

    def __init__(
        self,
        frontier: Frontier,
        scraper: WikiScraper | None = None,
        max_pages: int = 50,
        max_depth: int | None = None,
        verbose: bool = True,
    ) -> None:
        self.frontier = frontier
        self.scraper = scraper or WikiScraper()
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.verbose = verbose
        self.graph = WikiGraph()

    # ------------------------------------------------------------------
    # Primary traversal
    # ------------------------------------------------------------------

    def explore(
        self,
        start: str,
        max_pages: int | None = None,
        max_depth: int | None = None,
    ) -> WikiGraph:
        """
        Explore Wikipedia starting from `start`.

        Stops when the first of these limits is hit:
          • max_pages  — total number of articles visited
          • max_depth  — hop distance from the start page
            (depth 0 = start, depth 1 = direct links, depth 2 = their links…)

        The traversal strategy (BFS / DFS) is entirely determined by
        which Frontier implementation was passed to the constructor.

        Parameters
        ----------
        start : str
            Wikipedia article title to begin from.
        max_pages : int, optional
            Override the instance-level max_pages for this run.
        max_depth : int, optional
            Override the instance-level max_depth for this run.
            None means no depth limit.

        Returns
        -------
        WikiGraph
            The subgraph built during exploration.
        """
        page_limit  = max_pages if max_pages is not None else self.max_pages
        depth_limit = max_depth if max_depth is not None else self.max_depth

        # Reset graph and frontier for a fresh run
        self.graph    = WikiGraph()
        self.frontier = self.frontier.__class__()

        self.frontier.add(WikiNode(title=start, depth=0))

        while not self.frontier.is_empty() and self.graph.node_count() < page_limit:
            node: WikiNode = self.frontier.pop()

            if self.graph.is_visited(node.title):
                continue

            # Depth-limit check — skip nodes that are too deep
            if depth_limit is not None and node.depth > depth_limit:
                continue

            self.graph.mark_visited(node.title, parent=node.parent)

            if self.verbose:
                strategy = self.frontier.__class__.__name__.replace("Frontier", "")
                depth_str = f" depth={node.depth}" if depth_limit is not None else ""
                print(
                    f"[{strategy} | {self.graph.node_count():>3}/{page_limit}{depth_str}] "
                    f"{node.title}"
                )

            # Only fetch and enqueue children if we haven't hit the depth limit
            if depth_limit is None or node.depth < depth_limit:
                links = self.scraper.get_links(node.title)
                for link in links:
                    self.graph.add_edge(node.title, link)
                    if not self.graph.is_visited(link):
                        self.frontier.add(
                            WikiNode(title=link, parent=node.title, depth=node.depth + 1)
                        )

        return self.graph

    # ------------------------------------------------------------------
    # Shortest path (always BFS)
    # ------------------------------------------------------------------

    def shortest_path(
        self,
        start: str,
        target: str,
        max_pages: int = 500,
    ) -> list[str] | None:
        """
        Find the shortest click-path between two Wikipedia articles.

        Uses a dedicated BFS regardless of the explorer's configured
        frontier, because BFS guarantees the minimum-hop path.

        Parameters
        ----------
        start : str
            Source Wikipedia article title.
        target : str
            Destination Wikipedia article title.
        max_pages : int
            Safety cap to prevent unbounded search.

        Returns
        -------
        list[str] or None
            Ordered list of page titles from start to target (inclusive),
            or None if no path was found within the page limit.
        """
        # Normalise to Wikipedia title casing (first letter capitalised)
        start  = start[0].upper()  + start[1:]  if start  else start
        target = target[0].upper() + target[1:] if target else target

        if start == target:
            return [start]

        visited: set[str] = set()
        parent_map: dict[str, str | None] = {start: None}
        queue: deque[str] = deque([start])
        pages_checked = 0

        while queue and pages_checked < max_pages:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            pages_checked += 1

            if self.verbose:
                print(f"[BFS shortest | {pages_checked:>4}/{max_pages}] {current}")

            links = self.scraper.get_links(current)
            for link in links:
                if link not in parent_map:
                    parent_map[link] = current
                    if link == target:
                        if self.verbose:
                            print(f"[BFS shortest |  FOUND] {target}  ← target reached via '{current}'")
                        return self._build_path(parent_map, start, target)
                    queue.append(link)

        return None  # target not reached within page limit

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _build_path(
        parent_map: dict[str, str | None], start: str, target: str
    ) -> list[str]:
        """Reconstruct the path from start → target via parent_map."""
        path: list[str] = []
        current: str | None = target
        while current is not None:
            path.append(current)
            current = parent_map.get(current)
        path.reverse()
        return path
