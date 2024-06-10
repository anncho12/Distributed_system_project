import networkx as nx
from collections import deque

def flooding(graph, start_node):
    visited = set()
    to_visit = deque([start_node])  # 큐 초기화

    while to_visit:
        node = to_visit.popleft()  # FIFO 방식으로 큐의 맨 앞에서 노드를 꺼냄
        if node not in visited:
            yield node  # 노드 방문을 반환
            visited.add(node)
            to_visit.extend(neighbor for neighbor in graph.neighbors(node) if neighbor not in visited)