import networkx as nx
import random

def random_walk(graph, start_node, steps):
    current_node = start_node
    visited = {current_node}

    for _ in range(steps):
        # print(f"Visited {current_node}")
        neighbors = list(graph.neighbors(current_node))
        if not neighbors:
            break
        next_node = random.choice(neighbors)
        current_node = next_node
        visited.add(current_node)
