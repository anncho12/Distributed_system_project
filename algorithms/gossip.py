import networkx as nx
import random

def gossip(graph, start_node, prob):
    visited = set()
    to_visit = [start_node]

    while to_visit:
        node = to_visit.pop()
        if node not in visited:
            yield node  # 노드 방문을 반환
            visited.add(node)
            for neighbor in graph.neighbors(node):
                if neighbor not in visited and random.random() < prob:
                    to_visit.append(neighbor)
