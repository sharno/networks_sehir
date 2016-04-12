import networkx as nx
import network2
import matplotlib.pyplot as plt

G = network2.SocialGraph()
G.load_data("likes.json", num_posts=None)

users_graph = G.create_users_weighted_graph(likes_threshold=1000)
nx.write_edgelist(users_graph, "weighted.edgelist")

