import time
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from algorithms.flooding import flooding
from algorithms.random_walk import random_walk
from algorithms.krandom_walk import k_random_walk
from algorithms.gossip import gossip

from graph import create_distributed_graph

def visualize_algorithms(graph, visited_nodes_dict, layout, description):
    pos = layout(graph)
    node_size = [50 if graph.nodes[node].get('type') == 'client' else 300 for node in graph.nodes()]  # 서버와 클라이언트의 노드 크기 설정

    fig, axs = plt.subplots(1, 4, figsize=(20, 5))

    def create_update(ax, visited_nodes, title):
        node_colors = ['lightblue'] * len(graph.nodes())
        nx.draw(graph, pos, with_labels=True, node_color=node_colors, edge_color='gray', node_size=node_size, font_size=8, ax=ax)
        nodes = nx.draw_networkx_nodes(graph, pos, node_color=node_colors, node_size=node_size, ax=ax)
        ax.set_title(title)

        def update(frame):
            if frame < len(visited_nodes):
                for node in visited_nodes[:frame + 1]:
                    node_colors[node] = 'red'
                nodes.set_color(node_colors)

        return update

    titles = ["Flooding", "Random Walk", "Gossip", "K Random Walk"]
    updates = []
    for i, (algorithm, visited_nodes) in enumerate(visited_nodes_dict.items()):
        updates.append(create_update(axs[i], visited_nodes, titles[i]))

    max_frames = max(len(nodes) for nodes in visited_nodes_dict.values())
    anims = [FuncAnimation(fig, update, frames=max_frames, interval=10, repeat=False) for update in updates]  # 간격을 200ms로 설정

    fig.suptitle(description, fontsize=16)  # 그래프 설명 추가
    plt.tight_layout()
    plt.show()

def measure_time(algorithm, *args, iterations=1):
    total_time = 0
    for _ in range(iterations):
        start_time = time.time()
        for _ in algorithm(*args):
            pass
        end_time = time.time()
        total_time += end_time - start_time
    return total_time / iterations

def recommend_algorithm(G):
    start_node = 0
    steps = 100
    prob = 0.5

    flooding_time = measure_time(flooding, G, start_node)
    random_walk_time = measure_time(random_walk, G, start_node, steps)
    gossip_time = measure_time(gossip, G, start_node, prob)
    k_random_walk_time = measure_time(k_random_walk, G, start_node, 3)

    times = {
        "Flooding": flooding_time,
        "Random Walk": random_walk_time,
        "Gossip": gossip_time,
        "K Random Walk": k_random_walk_time
    }
    sorted_times = sorted(times.items(), key=lambda x: x[1])  # 시간을 기준으로 정렬
    best_algorithm = sorted_times[0][0]
    
    print("Algorithm Execution Times:")
    for algorithm, time_taken in sorted_times:
        print(f"{algorithm}: {time_taken:.6f} seconds")

    print(f"\nThe recommended algorithm is {best_algorithm}.")

    return best_algorithm

if __name__ == "__main__":
    graphs = []

    # #n은 노드 수, m은 엣지 수, 노드간의 연결이 매우 밀집됨
    # G_dense = nx.dense_gnm_random_graph(n=100, m=200)
    # graphs.append((G_dense, nx.spring_layout, "Dense Network"))

    # #n의 노드 수, p는 노드 사이에 엣지가 존재할 확률, 노드 간의 연결이 무작위로 생성됨. 
    # G_sparse = nx.erdos_renyi_graph(n=100, p=0.1)
    # graphs.append((G_sparse, nx.circular_layout, "Sparse Network"))

    # #n은 노드 수, m은 새로 추가되는 노드가 기존 노드와 연결할 엣지의 수, m이 작을수록 그래프는 희소해짐
    # G_scale_free = nx.barabasi_albert_graph(n=100, m=3)
    # graphs.append((G_scale_free, nx.spring_layout, "Scale-Free Network"))

    

    # G_centralized = nx.complete_graph(n=100)  # 중앙 집중식 그래프 생성
    # G_decentralized = nx.erdos_renyi_graph(n=100, p=0.3)  # 분산식 그래프 생성
    # G_p2p = nx.barabasi_albert_graph(n=100, m=3)  # P2P 그래프 생성
    G_server_client = create_distributed_graph(num_servers=5, clients_per_server=50)  # 서버-클라이언트 그래프 생성

    # graphs.append((G_centralized, nx.spring_layout, "Centralized Network"))
    # graphs.append((G_decentralized, nx.spring_layout, "Decentralized Network"))
    # graphs.append((G_p2p, nx.circular_layout, "P2P Network"))
    graphs.append((G_server_client, nx.spring_layout, "Server-Client Network"))

    for G, layout, description in graphs:
        print(f"Visualizing {description}")
        start_node = 0

        # 방문된 노드들을 각 알고리즘별로 저장
        visited_nodes_flooding = list(flooding(G, start_node))
        visited_nodes_random_walk = list(random_walk(G, start_node, steps=100))
        visited_nodes_gossip = list(gossip(G, start_node, prob=0.5))
        visited_nodes_k_random_walk = list(k_random_walk(G, start_node, k=3))

        visited_nodes_dict = {
            "Flooding": visited_nodes_flooding,
            "Random Walk": visited_nodes_random_walk,
            "Gossip": visited_nodes_gossip,
            "K Random Walk": visited_nodes_k_random_walk
        }

        visualize_algorithms(G, visited_nodes_dict, layout, description)
        recommend_algorithm(G)
