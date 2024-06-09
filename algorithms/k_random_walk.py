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

# 예제 사용
if __name__ == "__main__":
    G = nx.erdos_renyi_graph(10, 0.5)  # 예제 그래프 생성
    start_node = 0
    k = 2  # 한 번에 방문할 이웃 노드의 수

    print("Flooding (BFS) Order with K Neighbors:")
    for node in k_random_walk(G, start_node, k):
        print(node)

    G = nx.erdos_renyi_graph(10, 0.5)  # 예제 그래프 생성
    nx.draw(G, with_labels=True)
    plt.show()