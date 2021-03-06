import networkx as nx
import json


class SocialGraph:
    def __init__(self):
        self.data = {}
        self.posts_graph = None
        self.posts_graph_data = {}
        self.users_graph = None
        self.users_graph_data = {}
        self.posts = {}
        self.users = {}

    def load_data(self, filename, num_posts=None):
        myfile = open(filename, "r")
        temp = json.load(myfile)
        if num_posts == None:
            self.data = temp
            return self.data
        for e in temp:
            self.data[e] = temp[e]
            num_posts -= 1
            if num_posts < 0:
                return self.data

    def create_posts_graph(self):
        graph = nx.Graph()
        users_posts = {}
        for post, likes in self.data.items():
            graph.add_node(post)
            for like in likes:
                if like['id'] not in users_posts:
                    users_posts[like['id']] = []
                for p in users_posts[like['id']]:
                    graph.add_edge(post, p)
                users_posts[like['id']].append(post)
        self.posts_graph = graph
        return graph

    def create_users_graph(self, threshold=1):
        user_user_counts = {}
        users_int_id = {}
        int_id_user = {}
        intid = 0
        for post, likes in self.data.items():
            for i in range(len(likes)):
                for j in range(i+1, len(likes)):
                    if likes[i]['id'] not in users_int_id:
                        users_int_id[likes[i]['id']] = intid
                        int_id_user[intid] = likes[i]['id']
                        intid += 1
                    fst = users_int_id[likes[i]['id']]

                    if likes[j]['id'] not in users_int_id:
                        users_int_id[likes[j]['id']] = intid
                        int_id_user[intid] = likes[j]['id']
                        intid += 1
                    snd = users_int_id[likes[j]['id']]

                    first = min(fst, snd)
                    second = max(fst, snd)
                    if (first, second) not in user_user_counts:
                        user_user_counts[(first, second)] = 0
                    user_user_counts[(first, second)] += 1

        graph = nx.Graph()
        for pair, count in user_user_counts.items():
            if count >= threshold:
                graph.add_node(int_id_user[pair[0]])
                graph.add_node(int_id_user[pair[1]])
                graph.add_edge(int_id_user[pair[0]], int_id_user[pair[1]])
        self.users_graph = graph
        return graph
        
    def create_users_weighted_graph(self, likes_threshold=0):
        user_user_counts = {}
        users_intid = {}
        intid_user = {}
        intid = 0
        posts_count = 0
        for post, likes in self.data.items():
            if likes_threshold != 0 and len(likes) > likes_threshold: continue
            print "reached post: ", posts_count, " with likes: ", len(likes)
            posts_count += 1
            for i in xrange(len(likes)):
                for j in xrange(i+1, len(likes)):
                    # add first user to the dictionary of ints
                    if likes[i]['id'] not in users_intid:
                        users_intid[likes[i]['id']] = intid
                        intid_user[intid] = likes[i]['id']
                        intid += 1
                    fst = users_intid[likes[i]['id']]

                    # add second user to the dictionary of ints
                    if likes[j]['id'] not in users_intid:
                        users_intid[likes[j]['id']] = intid
                        intid_user[intid] = likes[j]['id']
                        intid += 1
                    snd = users_intid[likes[j]['id']]

                    first = min(fst, snd)
                    second = max(fst, snd)
                    if (first, second) not in user_user_counts:
                        user_user_counts[(first, second)] = 0
                    user_user_counts[(first, second)] += 1

        graph = nx.Graph()
        for pair, count in user_user_counts.items():
            graph.add_node(intid_user[pair[0]])
            graph.add_node(intid_user[pair[1]])
            graph.add_edge(intid_user[pair[0]], intid_user[pair[1]], weight=count)
        self.users_graph = graph
        return graph

    def create_complete_graph(self):
        graph = nx.Graph()

    def calculate_posts_centralities(self):
        print "Calculating degree centralities ..."
        self.posts_graph_data['degree_centrality'] = nx.degree_centrality(self.posts_graph)
        print "Calculating closeness centralities ..."
        self.posts_graph_data['closeness_centrality'] = nx.closeness_centrality(self.posts_graph)
        print "Calculating betweenness centralities ..."
        self.posts_graph_data['betweenness_centrality'] = nx.betweenness_centrality(self.posts_graph)
        print "Calculating eigenvector centralities ..."
        self.posts_graph_data['eigenvector_centrality'] = nx.eigenvector_centrality(self.posts_graph)
        print "Calculating pagerank centralities ..."
        self.posts_graph_data['pagerank'] = nx.pagerank(self.posts_graph)

        with open('posts_graph_centralities.json', 'w') as outfile:
            json.dump(self.posts_graph_data, outfile, indent=4)
        return self.posts_graph_data

    def calculate_users_centralities(self):
        print "Calculating degree centralities ..."
        self.users_graph_data['degree_centrality'] = nx.degree_centrality(self.users_graph)
        print "Calculating closeness centralities ..."
        self.users_graph_data['closeness_centrality'] = nx.closeness_centrality(self.users_graph)
        print "Calculating betweenness centralities ..."
        self.users_graph_data['betweenness_centrality'] = nx.betweenness_centrality(self.users_graph)
        print "Calculating eigenvector centralities ..."
        self.users_graph_data['eigenvector_centrality'] = nx.eigenvector_centrality(self.users_graph)
        print "Calculating pagerank ..."
        self.users_graph_data['pagerank'] = nx.pagerank(self.users_graph)

        with open('users_graph_centralities.json', 'w') as outfile:
            json.dump(self.users_graph_data, outfile, indent=4)
        return self.users_graph_data
