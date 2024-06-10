import networkx as nx
from collections import deque
import matplotlib.pyplot as plt
import random

def k_random_walk(graph, start_node, k):
    visited = set()
    to_visit = deque([start_node])  # 큐 초기화

    while to_visit:
        node = to_visit.popleft()  # FIFO 방식으로 큐의 맨 앞에서 노드를 꺼냄
        if node not in visited:
            yield node  # 노드 방문을 반환
            visited.add(node)
            neighbors = list(graph.neighbors(node))
            if len(neighbors) <= k:
                selected_neighbors = neighbors
            else:
                selected_neighbors = random.sample(neighbors, k)
            to_visit.extend(neighbor for neighbor in selected_neighbors if neighbor not in visited)