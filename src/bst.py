"""
bst.py
------
Foundation layer: the original data structures from homework 3,
inspired by the idea of working with Wikipedia page titles instead of regular InventoryItem objects.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum

try:
    from graphviz import Digraph, nohtml
    from IPython.display import display as _display
    _GRAPHVIZ_AVAILABLE = True
except ImportError:
    _GRAPHVIZ_AVAILABLE = False


class WikiPage:
    """
    Replaces InventoryItem from the homework 3 
    Same comparison logic (<, >, ==) as BinarySearchTree.
    Just looping over page titles instead of inventory records.
    Alphabetical ordering: "Aardvark" < "Zebra".
    """

    def __init__(self, title: str) -> None:
        self.title = title
        self.item_name = title  

    def __lt__(self, other: WikiPage) -> bool:
        return self.title < other.title

    def __gt__(self, other: WikiPage) -> bool:
        return self.title > other.title

    def __eq__(self, other: object) -> bool:
        if isinstance(other, WikiPage):
            return self.title == other.title
        return NotImplemented

    def __le__(self, other: WikiPage) -> bool:
        return self.title <= other.title

    def __ge__(self, other: WikiPage) -> bool:
        return self.title >= other.title

    def __hash__(self) -> int:
        return hash(self.title)

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return f"WikiPage({self.title!r})"


class ThingContainer(ABC):
    """
    Abstract class for a generic container of things.
    - subclasses: Stack, Queue
    - difference: LIFO vs FIFO behavior
    """

    def __init__(self) -> None:
        self.internal_list: list = []

    @abstractmethod
    def put_new_thing_in(self, item) -> None:
        pass

    def is_empty(self) -> bool:
        return len(self) == 0

    def __len__(self) -> int:
        return len(self.internal_list)

    @abstractmethod
    def take_existing_thing_out(self):
        pass


class Stack(ThingContainer):
    """
    LIFO container that drives Depth-First Search. The most recently discovered node is
    always explored next, so traversal dives deep before backtracking.
        - add (put_new_thing_in): machine learning, statistics
        - stack: ["Machine learning", "Statistics"]
        - remove (take_existing_thing_out): statistics
        - stack: ["Machine learning"]
        - We explore "Statistics" first because it was added last.
    """

    def __init__(self) -> None:
        super().__init__()

    def __push(self, item) -> None:
        self.internal_list.append(item)

    def __pop(self):
        return self.internal_list.pop()

    def put_new_thing_in(self, item) -> None:
        return self.__push(item)

    def take_existing_thing_out(self):
        return self.__pop()


class Queue(ThingContainer):
    """
    FIFO container that drives Breadth-First Search. The first item added is
    the first item removed.
    - add (put_new_thing_in): machine learning, statistics
    - queue: ["Machine learning", "Statistics"]
    - remove (take_existing_thing_out): machine learning
    - queue: ["Statistics"]
    - We explore "Machine learning" first because it was added first.
    """

    def __init__(self) -> None:
        super().__init__()

    def __enqueue(self, item) -> None:
        self.internal_list.insert(0, item)  # O(n) — fine for small BSTs

    def __dequeue(self):
        return self.internal_list.pop()

    def put_new_thing_in(self, item) -> None:
        return self.__enqueue(item)

    def take_existing_thing_out(self):
        return self.__dequeue()


# ============================================================
# IterAlgorithm + NodeProcessor 
# ============================================================

class IterAlgorithm(Enum):
    """Selects which traversal strategy NodeProcessor will use."""
    DEPTH_FIRST = 1
    BREADTH_FIRST = 2


class NodeProcessor:
    """
    Iterates over a BinarySearchTree using either DFS or BFS.
    The algorithm choice is made entirely by picking which ThingContainer
    subclass (Stack vs Queue) is used while the loop itself never changes.
    """

    def __init__(self, iter_method_arg: IterAlgorithm) -> None:
        self.iter_method = iter_method_arg
        self.initialize_empty_node_container()

    def initialize_empty_node_container(self) -> None:
        if self.iter_method == IterAlgorithm.DEPTH_FIRST:
            self.node_container: ThingContainer = Stack()
        else:
            self.node_container = Queue()

    def iterate_over(self, tree: BinarySearchTree) -> None:
        """Traverse every node in `tree`, printing each node's content."""
        self.initialize_empty_node_container()

        cur_node = tree.root
        self.node_container.put_new_thing_in(cur_node)

        while not self.node_container.is_empty():
            cur_node = self.node_container.take_existing_thing_out()

            if cur_node.has_left_child():
                self.node_container.put_new_thing_in(cur_node.left)

            if cur_node.has_right_child():
                self.node_container.put_new_thing_in(cur_node.right)

            print(cur_node.content)


# ============================================================
# BinarySearchTree + BSTNode  
# ============================================================

class BinarySearchTree:
    """
    A binary search tree whose nodes store comparable objects.

    Works with WikiPage objects (or any type that supports <, >, ==).
    Items are stored in sorted order so that:
        left subtree  < parent node < right subtree
    """

    def __init__(self) -> None:
        self.root: BSTNode | None = None

    def add(self, new_item) -> bool:
        if self.root is None:
            self.root = BSTNode(new_item)
            return True
        return self.root.add(new_item)

    def find_item_steps(self, item) -> int:
        """Return the number of nodes examined to find `item`."""
        if self.root is None:
            return 0
        return self.root.find_item_steps(item)

    def __len__(self) -> int:
        return 0 if self.root is None else len(self.root)

    def to_string(self, recurse: bool) -> str:
        if self.root is None:
            return "BinarySearchTree[]"
        return f"BinarySearchTree[{self.root.to_string(recurse)}]"

    def __repr__(self) -> str:
        return self.to_string(recurse=False)

    def __str__(self) -> str:
        return self.to_string(recurse=True)


class BSTNode:
    """
    A single node in a BinarySearchTree.

    Stores one item and pointers to optional left and right child nodes.
    The recursive add() and find_item_steps() methods embody the BST
    invariant: smaller items go left, larger items go right.
    """

    def __init__(self, item) -> None:
        self.content = item
        self.left: BSTNode | None = None
        self.right: BSTNode | None = None

    def add(self, new_item) -> bool:
        if new_item < self.content:
            if self.left is None:
                self.left = BSTNode(new_item)
                return True
            return self.left.add(new_item)
        elif new_item > self.content:
            if self.right is None:
                self.right = BSTNode(new_item)
                return True
            return self.right.add(new_item)
        else:
            # Duplicate key → update in place
            self.content = new_item
            return True

    def find_item_steps(self, item) -> int:
        if self.content == item:
            return 1
        if item < self.content:
            return 1 + (self.left.find_item_steps(item) if self.left else 0)
        return 1 + (self.right.find_item_steps(item) if self.right else 0)

    def has_left_child(self) -> bool:
        return self.left is not None

    def get_left_child(self) -> BSTNode | None:
        return self.left

    def has_right_child(self) -> bool:
        return self.right is not None

    def get_right_child(self) -> BSTNode | None:
        return self.right

    def __len__(self) -> int:
        left_len = 0 if self.left is None else len(self.left)
        right_len = 0 if self.right is None else len(self.right)
        return 1 + left_len + right_len

    def to_string(self, recurse: bool) -> str:
        if recurse:
            left_str = "" if self.left is None else self.left.__repr__() + ","
            right_str = "" if self.right is None else "," + self.right.__repr__()
            return f"{left_str}{str(self.content)}{right_str}"
        return str(self.content)

    def __repr__(self) -> str:
        return self.to_string(recurse=False)

    def __str__(self) -> str:
        return self.to_string(recurse=True)


# ============================================================
# BST visualizer  
# ============================================================

def visualize_bst(tree: "BinarySearchTree") -> None:
    if not _GRAPHVIZ_AVAILABLE:
        raise ImportError(
            "graphviz is required for visualize_bst(). "
        )

    dot = Digraph(node_attr={"shape": "record", "height": ".1"})

    node_info_list = []
    if tree.root is not None:
        node_info_list.append({"node": tree.root, "parent_name": None, "dir": None})

    while len(node_info_list) > 0:
        cur_node_info = node_info_list.pop()
        cur_node      = cur_node_info["node"]
        cur_name      = cur_node.content.item_name   # WikiPage.item_name == title
        cur_parent    = cur_node_info["parent_name"]
        cur_dir       = cur_node_info["dir"]

        dot.node(name=cur_name, label=nohtml(f"<f0>|<f1> {cur_name}|<f2>"))

        if cur_parent is not None:
            which_port = "f2" if cur_dir == "R" else "f0"
            dot.edge(f"{cur_parent}:{which_port}", f"{cur_name}:f1", label=cur_dir)

        if cur_node.right is not None:
            node_info_list.append({"node": cur_node.right, "parent_name": cur_name, "dir": "R"})
        if cur_node.left is not None:
            node_info_list.append({"node": cur_node.left, "parent_name": cur_name, "dir": "L"})

    _display(dot)
