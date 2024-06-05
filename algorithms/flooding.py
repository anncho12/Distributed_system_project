import networkx as nx

def flooding(graph, start_node):
    visited = set()
    to_visit = [start_node]

    while to_visit:
        node = to_visit.pop()
        if node not in visited:
            # print(f"Visited {node}")
            visited.add(node)
            to_visit.extend(neighbor for neighbor in graph.neighbors(node) if neighbor not in visited)
