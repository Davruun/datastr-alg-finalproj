# datastr-alg-finalproj
**Polymorphic Wikipedia Graph Explorer** — Georgetown DSAN 5500, Spring 2025  
*Troy Cheng & Stacy Che*

---

## Background and motivation

This project builds directly on concepts from Homework 3, where implementing Breadth-First Search (BFS) and Depth-First Search (DFS) on binary search trees helped us understand that traversal is fundamentally about the strategy used to visit nodes. In particular, the idea that simply swapping a stack for a queue can change the entire traversal behavior led us to think about how this concept could be applied beyond trees. This inspired us to build a web scraper on Wikipedia and to think of it as a large, real-world data structure—a network of knowledge.

Wikipedia can be understood as a graph, where each article is a node and each hyperlink between articles is a connection. Unlike a binary search tree, this structure is not hierarchical. Instead, it contains many cycles, dense cross-connections, and no single root. However, the underlying traversal logic remains structurally similar: we take a node from a frontier, process it, and add its unvisited neighbors back into the system.

The key difference lies in how we define a node’s “children.” In a binary search tree, these are fixed as the left and right nodes. In Wikipedia, they are dynamically determined by the hyperlinks on each page. This shift allows us to take a concept learned in a structured, controlled setting and apply it to a much more complex and open-ended system.

## Core OOP design

The `Frontier` abstract base class defines a simple interface: `add()`, `pop()`, `is_empty()`. Two concrete subclasses implement this interface in different ways:

- `BFSFrontier` — wraps the course `Queue` (FIFO), exploring pages layer by layer and staying close to the starting topic. 
- `DFSFrontier` — wraps the course `Stack` (LIFO), diving deep into one chain of pages and often reaching unrelated topics quickly. 

The key idea is that `WikiExplorer` depends only on the `Frontier` interface and never needs to know which specific strategy is being used. By simply passing in another subclass, the entire wiki exploration behavior changes without modifying any other part of the system. This demonstrates 'polymorphism' in a real-world setting: the same code produces different behaviors depending on the object it takes in.

## Features

**1. Exploration** — Starting from a chosen starting Wikipedia page, the system explores up to a fixed number of pages or a maximum depth. Running BFS and DFS from the same starting point often produces very different sets of visited pages. We think that BFS tends to stay close to the original topic, while DFS quickly moves into less related areas. 

**2. Shortest Path** — The system can find the minimum number of clicks (min steps) between any 2 Wikipedia articles, like a step-counter game. This feature highlights how traversal strategies are not just different in behavior, but also in the types of problems they can solve.

**3. Knowledge Mindmap** — Given a central topic and a list of target topics, the system computes how many steps away each target is and visualizes these distances as a mindmap. This adds a fun knowledge discovery dimension to the project: it allows us to see how closely related different concepts are. For example, “Machine Learning” may be only one step away from “Data Science,” while something like “Dinosaur” might be several steps away, revealing less obvious connections within the network of knowledge while also exploring endless possiblities behind a knowledge realm. 

---

## Project structure

```
datastr-alg-finalproj/
│
├── src/
│   ├── bst.py          Course foundations: ThingContainer / Stack / Queue /
│   │                   BinarySearchTree / BSTNode / NodeProcessor / WikiPage
│   ├── frontier.py     Frontier interface + BFSFrontier using Queue + DFSFrontier using Stack
│   ├── scraper.py      WikiScraper — fetches article links from Wikipedia
│   ├── graph.py        WikiNode + WikiGraph — stores page connections and visited pages
│   ├── explorer.py     WikiExplorer — traversal engine with max_pages and max_depth limits
│   └── mindmap.py      WikiMindmap — multi-target distance map and radial visualization
│
├── notebooks/
│   ├── 00_bst_foundations.ipynb   Start here: BST homework → Wikipedia graph bridge
│   ├── 01_exploration.ipynb       BFS vs DFS comparison with page and depth limits
│   ├── 02_shortest_path.ipynb     Shortest path / Wikipedia game
│   └── 03_mindmap.ipynb           Knowledge mindmap builder
│
├── run_example.py      Quick terminal demo: BFS vs DFS from "Data science"
├── requirements.txt
└── index.qmd           Project proposal / report
```

> The `wiki-bfs-workspace/` virtual environment is excluded from the repo (see `.gitignore`).  
> Recreate it locally with the instructions below.

---

## Setup

```bash
# Create and activate a virtual environment
python3 -m venv wiki-bfs-workspace
source wiki-bfs-workspace/bin/activate

# Install dependencies
pip install -r requirements.txt

# Graphviz system binary (required for BST visualisation in notebook 00)
brew install graphviz        # macOS
# sudo apt install graphviz  # Linux
```

---

## Quick usage

### Feature 1 — BFS vs DFS exploration Differences

```python
from src import BFSFrontier, DFSFrontier, WikiScraper, WikiExplorer

scraper = WikiScraper(delay=0.3)

# BFS: explore up to 50 pages, no more than 2 hops from start
bfs = WikiExplorer(BFSFrontier(), scraper=scraper, max_pages=50, max_depth=2)
bfs_graph = bfs.explore("Data science")


# DFS: same limits, often produces a very different set of visited pages
dfs = WikiExplorer(DFSFrontier(), scraper=scraper, max_pages=50, max_depth=2)
dfs_graph = dfs.explore("Data science")
```

### Feature 2 — Shortest path Calculation

```python
# Finds the minimum amount of clicks between two topics using BFS
from src import BFSFrontier, WikiScraper, WikiExplorer

explorer = WikiExplorer(BFSFrontier(), scraper=WikiScraper(delay=0.3))
path = explorer.shortest_path("Data science", "Ancient Rome", max_pages=300)

print(f"{len(path) - 1} hops: {' → '.join(path)}")
```

### Feature 3 — Knowledge mindmap

```python
# Shows how closely different concepts are connected, reveals both expected and surprising relationships.
from src import WikiMindmap, WikiScraper

mm = WikiMindmap(center="Data science", scraper=WikiScraper(delay=0.3))
mm.build(["Machine learning", "Ancient Rome", "Dinosaur", "Philosophy"])
mm.summary()     # displays topics sorted by distance from the center
mm.visualize()   # radial graph: distance from centre = # hops
```

---

## Notebook guide

| Notebook | Usage |
|---|---|
| `00_bst_foundations` | Shows how foundational BST code maps to the Wikipedia explorer. |
| `01_exploration` | BFS vs DFS from the same start page, comparing differences. |
| `02_shortest_path` | Wikipedia step counter calculates minimum clicks between two articles. |
| `03_mindmap` | User pick a center topic, measure distances to several targets, draws mindmap. |
