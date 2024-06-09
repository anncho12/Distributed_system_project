import networkx as nx
import random

def create_distributed_graph(num_servers, clients_per_server):
        G = nx.Graph()
        
        # 서버 노드 추가 및 연결
        server_nodes = range(num_servers)
        G.add_nodes_from(server_nodes, type='server')
        for i in server_nodes:
            for j in server_nodes:
                if i < j:
                    G.add_edge(i, j)
        
        # 클라이언트 노드 추가 및 서버와 연결
        client_node_id = num_servers
        for server in server_nodes:
            client_nodes = range(client_node_id, client_node_id + clients_per_server)
            G.add_nodes_from(client_nodes, type='client')
            for client in client_nodes:
                G.add_edge(server, client)
            client_node_id += clients_per_server
        
        return G