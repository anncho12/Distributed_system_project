import time
from matplotlib import pyplot as plt
import networkx as nx
from algorithms.flooding import flooding
from algorithms.random_walk import random_walk
from algorithms.k_random_walk import k_random_walk
from algorithms.gossip import gossip

from graph import create_distributed_graph

def measure_time_and_propagation(algorithm, *args, iterations=1):
    total_time = 0
    total_propagation_ratio = 0
    for _ in range(iterations):
        start_time = time.time()
        visited_nodes = list(algorithm(*args))
        end_time = time.time()
        total_time += end_time - start_time
        total_propagation_ratio += len(visited_nodes) / len(args[0].nodes())  # 전파된 노드의 수 비율 계산
    avg_time = total_time / iterations
    avg_propagation_ratio = total_propagation_ratio / iterations
    return avg_time, avg_propagation_ratio

def recommend_algorithm(G):
    start_node = 1
    # 전파 알고리즘에 사용되는 파라미터
    steps = 10000
    prob = 0.5


    min_propagation_ratio = float(input("Enter the minimum propagation ratio (between 0 and 1): "))
    if not 0 <= min_propagation_ratio <= 1:
        print("Invalid input. Minimum propagation ratio should be between 0 and 1.")
        return
    
    flooding_time, flooding_ratio = measure_time_and_propagation(flooding, G, start_node)
    random_walk_time, random_walk_ratio = measure_time_and_propagation(random_walk, G, start_node, steps)
    gossip_time, gossip_ratio = measure_time_and_propagation(gossip, G, start_node, prob)
    k_random_walk_time, k_random_walk_ratio = measure_time_and_propagation(k_random_walk, G, start_node, 3)
    #여기서는 k=3

    times = {
        "Flooding": flooding_time,
        "Random Walk": random_walk_time,
        "Gossip": gossip_time,
        "K Random Walk": k_random_walk_time
    }

    propagation_ratios = {
        "Flooding": flooding_ratio,
        "Random Walk": random_walk_ratio,
        "Gossip": gossip_ratio,
        "K Random Walk": k_random_walk_ratio
    }
    
    print("Algorithm Execution Times:")

    sorted_times = sorted(times.items(), key=lambda x: x[1])  # 시간을 기준으로 정렬
    best_algorithm = None
    best_time = float('inf')

    for algorithm, time_taken in sorted_times:
        propagation_ratio = propagation_ratios[algorithm]
        print(f"{algorithm}: {time_taken:.6f} seconds, Propagation Ratio: {propagation_ratio:.2%}")
        # print(f"{algorithm}: {time_taken:.6f} seconds, Propagation Ratio: {propagation_ratio}")

        if propagation_ratio >= min_propagation_ratio and time_taken < best_time:
            best_algorithm = algorithm
            best_time = time_taken


    print(f" ---- The recommended algorithm is {best_algorithm}.\n\n")

    return best_algorithm

def visualize_graph(G, title):
    plt.figure(figsize=(10, 10))
    pos = nx.kamada_kawai_layout(G)  # 노드 배치를 위해 spring layout 사용
    nx.draw(G, pos, node_size=10, node_color='blue', with_labels=False)
    plt.title(title)
    plt.show()


if __name__ == "__main__":
    G_decentralized = create_distributed_graph(num_servers=100, clients_per_server=1000)  # 서버-클라이언트 그래프 생성
    G_dense = nx.complete_graph(n=10000)  # 중앙 집중식 그래프 생성
    G_p2p1 = nx.erdos_renyi_graph(n=10000, p=0.3)  # 분산식 그래프 생성
    G_p2p2 = nx.barabasi_albert_graph(n=10000, m=3)  # P2P 그래프 생성

    # G_server_client = create_distributed_graph(num_servers=5, clients_per_server=10)  # 서버-클라이언트 그래프 생성
    # G_centralized = nx.complete_graph(n=50)  # 중앙 집중식 그래프 생성
    # G_decentralized = nx.erdos_renyi_graph(n=50, p=0.3)  # 분산식 그래프 생성
    # G_p2p = nx.barabasi_albert_graph(n=50, m=3)  # P2P 그래프 생성

    # visualize_graph(G_decentralized, "Server-Client Distributed Graph")
    # visualize_graph(G_dense, "Centralized Graph")
    # visualize_graph(G_p2p1, "Decentralized Graph")
    # visualize_graph(G_p2p2, "Peer-to-Peer (P2P) Graph")

    recommend_algorithm(G_decentralized)
    recommend_algorithm(G_dense)
    recommend_algorithm(G_p2p1)
    recommend_algorithm(G_p2p2)
