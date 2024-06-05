import time
import networkx as nx
import matplotlib.pyplot as plt
from algorithms.flooding import flooding
from algorithms.random_walk import random_walk
from algorithms.gossip import gossip

def visualize_graph(graph, layout):
    pos = layout(graph)  # 선택한 레이아웃에 따라 노드 위치 결정
    node_size = [len(list(graph.neighbors(n))) * 100 for n in graph.nodes()]  # 노드 크기를 이웃 수에 비례하여 설정
    node_color = range(len(graph.nodes()))  # 노드 색상을 노드 인덱스에 따라 설정
    nx.draw(graph, pos, with_labels=True, node_color=node_color, edge_color='gray', node_size=node_size, font_size=10, cmap=plt.cm.Blues)
    plt.show()

def measure_time(algorithm, iterations=10, *args):
    total_time = 0
    for _ in range(iterations):
        start_time = time.time()
        algorithm(*args)
        end_time = time.time()
        total_time += end_time - start_time
    return total_time / iterations

def recommend_algorithm(G):
    start_node = 0  # 시작 노드를 선택합니다. 이 부분은 필요에 따라 수정할 수 있습니다.
    steps = 1000    # Random Walk를 위한 기본 steps 설정. 필요에 따라 변경 가능.
    prob = 0.5      # Gossip을 위한 기본 확률 설정. 필요에 따라 변경 가능.

    # 각 알고리즘에 대해 시간 측정
    flooding_time = measure_time(flooding, 10, G, start_node)
    random_walk_time = measure_time(random_walk, 10, G, start_node, steps)
    gossip_time = measure_time(gossip, 10, G, start_node, prob)

    # 시간 출력
    print(f"Flooding algorithm took {flooding_time:.6f} seconds")
    print(f"Random Walk algorithm took {random_walk_time:.6f} seconds")
    print(f"Gossip algorithm took {gossip_time:.6f} seconds")

    # 가장 빠른 알고리즘 선택
    times = {
        "Flooding": flooding_time,
        "Random Walk": random_walk_time,
        "Gossip": gossip_time
    }
    best_algorithm = min(times, key=times.get)
    print(f"The recommended algorithm is {best_algorithm}.")

    return best_algorithm

if __name__ == "__main__":
    # 그래프를 담는 배열 선언
    graphs = []

    # 밀집 네트워크 생성 및 그래프 배열에 추가
    G_dense = nx.dense_gnm_random_graph(n=100, m=200)
    graphs.append((G_dense, nx.spring_layout, "Dense Network"))

    # 희소 네트워크 생성 및 그래프 배열에 추가
    G_sparse = nx.erdos_renyi_graph(n=100, p=0.1)
    graphs.append((G_sparse, nx.spring_layout, "Sparse Network"))

    # 스케일-프리 네트워크 생성 및 그래프 배열에 추가
    G_scale_free = nx.barabasi_albert_graph(n=100, m=3)
    graphs.append((G_scale_free, nx.shell_layout, "Scale-Free Network"))

    # 그래프 시각화 및 알고리즘 추천 적용
    for G, layout, description in graphs:
        print(f"Visualizing {description}")
        visualize_graph(G, layout)
        recommend_algorithm(G)
