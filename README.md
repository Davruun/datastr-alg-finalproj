# datastr-alg-finalproj



At the beginning of this course, we found object-oriented programming (OOP) and data structures like Binary Search Trees (BSTs) quite difficult to understand. Coming from a data science background, we were used to working with tools like pandas, where most structures are already built for you. Writing our own classes, dealing with concepts like self, and linking nodes together felt unfamiliar and abstract. In particular, BSTs required thinking in terms of relationships between nodes instead of just rows and columns of data. However, as we practiced implementing BSTs and learned how to traverse them using Depth-First Search (DFS) and Breadth-First Search (BFS), we started to understand a key idea. These traversal methods are not limited to trees. They are general strategies for exploring structured systems.



This realization led us to think about how these concepts could be applied outside of textbook examples. In this project, we extend the idea of traversal from trees to a real-world system, which is Wikipedia. We model Wikipedia as a network of knowledge, where each page is treated as a node and each hyperlink between pages represents a connection. Unlike a tree, this structure is more complex because pages can link back to one another and form loops and dense connections. As a result, it is closer to a graph than a tree, and it requires careful tracking of which pages have already been visited in order to avoid repetition.



The main goal of this project is to build a flexible Wikipedia exploration tool that can navigate this network using different strategies. When a page is visited, the system processes it by extracting the relevant links on that page and adding them to a list of pages to visit next. The key idea is that this list can be managed in different ways. If we treat it like a line, where pages are explored in the order they are discovered, the system behaves like Breadth-First Search and stays close to the original topic while expanding outward layer by layer. If we treat it like a stack, where the most recently discovered page is explored next, the system behaves like Depth-First Search and dives deeply into one chain of topics before backtracking. By designing the system so that these behaviors can be swapped without changing the overall structure, we apply the concept of polymorphism from OOP. This allows the same system to adapt to different exploration strategies.



One key functionality of this system is the ability to find the shortest path between two Wikipedia pages, similar to the well-known Wikipedia game. For example, starting from a page like “Data Science,” the system can determine the minimum number of clicks needed to reach a target page such as “Deep Learning.” By using a breadth-first exploration strategy, the system ensures that the first time it reaches the target, it has found the most efficient path. It also keeps track of how each page was reached, which allows it to reconstruct the full sequence of links at the end. This demonstrates how traversal algorithms can be used not only for visiting nodes but also for solving meaningful problems.



Beyond calculating shortest paths, we also see this project as a way of building a kind of “mind map” of knowledge. When we start from a familiar topic such as “Data Science,” we might expect to encounter closely related concepts such as “Machine Learning” or “Artificial Intelligence.” However, what makes this exploration interesting is not just confirming what we already know. It is also about discovering unexpected connections. A page about data science might link to a historical figure, a mathematical theory, or even something that initially seems unrelated. As the system explores more pages, it gradually builds a network of connections that reflects how knowledge is actually structured. The structure is interconnected, non-linear, and sometimes surprising. In this way, the project becomes not just a navigation tool but also a way to uncover new ideas and relationships that we might not have thought to search for directly. It mirrors how curiosity works in real life. We start from one idea and follow links that lead to entirely new domains, which can connect topics as distant as technology, history, or even something like dinosaurs.



From a technical perspective, this project also reinforces the importance of data structures in building efficient systems. A set is used to track visited pages, which ensures that each page is only processed once and prevents infinite loops. The list of pages to visit next functions as either a queue or a stack depending on the chosen strategy. Together, these components form a system that behaves like a graph traversal algorithm. Its performance scales based on the number of pages and links explored. This connects directly back to the time complexity concepts learned in class and shows how theoretical ideas translate into practical design decisions.



Overall, this project represents a progression from learning abstract concepts to applying them in a meaningful and intuitive way. What began as an exercise in implementing BST traversal became a tool for exploring large-scale networks of knowledge. It also highlights how OOP can be used to build flexible systems that can adapt to different tasks without needing to be rewritten. For non-technical audiences, this project can be understood simply as creating a smarter way to explore Wikipedia. The system allows users to stay close to a topic, dive deeply into related ideas, or discover unexpected connections along the way.



In conclusion, this project bridges the gap between foundational computer science concepts and real-world applications. By modeling Wikipedia as a network and applying traversal strategies learned from BSTs, we aim to build a system that is both technically meaningful and intuitively understandable. It reflects our learning journey throughout the course and demonstrates how concepts like BFS, DFS, and polymorphism can be used not only to solve problems but also to explore and better understand the structure of knowledge itself.
