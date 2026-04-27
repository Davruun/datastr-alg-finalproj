"""
frontier.py
-----------
Polymorphic frontier data structures for Wikipedia graph traversal.

Built directly on top of the Stack and Queue from bst.py 

    ThingContainer.put_new_thing_in()    ←→  Frontier.add()
    ThingContainer.take_existing_thing_out() ←→  Frontier.pop()

    DFSFrontier  wraps  Stack  (LIFO)  →  Depth-First Search
    BFSFrontier  wraps  Queue  (FIFO)  →  Breadth-First Search

The abstract Frontier class plays the same role as ThingContainer —
it defines the interface that WikiExplorer depends on, without caring
which concrete subclass is actually running.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

from .bst import Stack, Queue


class Frontier(ABC):
    """
    Abstract base class for the exploration frontier.
    """

    @abstractmethod
    def add(self, item: Any) -> None:
        """Add an item to the frontier (≡ put_new_thing_in)."""

    @abstractmethod
    def pop(self) -> Any:
        """Remove and return the next item to explore (≡ take_existing_thing_out)."""

    @abstractmethod
    def is_empty(self) -> bool:
        """Return True if no items remain."""

    @abstractmethod
    def __len__(self) -> int:
        """Return the number of items currently in the frontier."""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(size={len(self)})"


class BFSFrontier(Frontier):
    """
    Queue-based frontier that produces Breadth-First Search order.

    Wraps the course Queue (ThingContainer) and adapts its interface
    to the Frontier contract used by WikiExplorer.

    Pages are explored layer by layer (FIFO), so the explorer stays
    close to the starting topic before venturing further.

    Performance note: the course Queue uses list.insert(0, …) which is
    O(n).  This is preserved here for pedagogical fidelity.  For large
    graphs the internal container could be swapped for collections.deque
    without changing a single line of WikiExplorer.
    """

    def __init__(self) -> None:
        self._container = Queue()

    def add(self, item: Any) -> None:
        self._container.put_new_thing_in(item)

    def pop(self) -> Any:
        return self._container.take_existing_thing_out()

    def is_empty(self) -> bool:
        return self._container.is_empty()

    def __len__(self) -> int:
        return len(self._container)


class DFSFrontier(Frontier):
    """
    Stack-based frontier that produces Depth-First Search order.

    Wraps the course Stack (ThingContainer) and adapts its interface
    to the Frontier contract used by WikiExplorer.

    The most recently discovered page is explored next (LIFO), so the
    explorer dives deeply into one chain of topics before backtracking.
    """

    def __init__(self) -> None:
        self._container = Stack()

    def add(self, item: Any) -> None:
        self._container.put_new_thing_in(item)

    def pop(self) -> Any:
        return self._container.take_existing_thing_out()

    def is_empty(self) -> bool:
        return self._container.is_empty()

    def __len__(self) -> int:
        return len(self._container)
