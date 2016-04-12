import snap
import json

def create_json_graph(filename):
    """Generates a graph suitable for visualization by D3"""
    myfile = open(filename, "r")
    all_data = json.load(myfile)

    # loading part of the graph
    count = 0
    data = {}
    for post, likes in all_data.items():
        if count == 100: break
        count += 1
        data[post] = likes

    graph = {'nodes': [], 'links': []}
    nodes = {}
    nid = 0

    for post, likes in data.items():
        graph['nodes'].append({'id': post, 'name': post, 'group': 1})
        nodes[post] = nid
        nid += 1
        for like in likes:
            if like['id'] not in nodes:
                nodes[like['id']] = nid
                nid += 1
                graph['nodes'].append({'id': like['id'], 'name': like['name'].encode("utf8"), 'group': 2})
            graph['links'].append({'source': nodes[post], 'target': nodes[like['id']], 'value': 1})
    return graph

def create_graph_from_likes(filename):
    myfile = open(filename, "r")
    all_data = json.load(myfile)

    # loading part of the graph
    count = 0
    data = {}
    for post, likes in all_data.items():
        if count == 100: break
        count += 1
        data[post] = likes

    graph = snap.TUNGraph.New()
    names = snap.TIntStrH()

    posts_ints = {}
    users_ints = {}
    p = 0
    k = 3000
    for post, likes in data.items():
        posts_ints[post] = p
        graph.AddNode(p)
        for like in likes:
            # user_int_id = -1
            if like['id'] in users_ints.keys():
                user_int_id = users_ints[like['id']]
                names[user_int_id] = like['name'].encode("utf8")
            else:
                users_ints[like['id']] = k
                user_int_id = k
                graph.AddNode(user_int_id)
                k += 1
            graph.AddEdge(p, user_int_id)
        p += 1
    print "G1: Nodes %d, Edges %d" % (graph.GetNodes(), graph.GetEdges())

    return graph


def create_graph_from_users(filename):
    myfile = open(filename, "r")
    all_data = json.load(myfile)

    # loading part of the graph
    count = 0
    data = {}
    for post, likes in all_data.items():
        if count == 10: break
        count += 1
        data[post] = likes

    graph = snap.TUNGraph.New()

    posts_ints = {}
    users_ints = {}
    p = 0
    k = 3000
    for post, likes in data.items():
        posts_ints[post] = p
        graph.AddNode(p)
        for like in likes:
            # user_int_id = -1
            if like['id'] in users_ints.keys():
                user_int_id = users_ints[like['id']]
            else:
                users_ints[like['id']] = k
                user_int_id = k
                graph.AddNode(user_int_id)
                k += 1
            graph.AddEdge(p, user_int_id)
        p += 1
    print "G1: Nodes %d, Edges %d" % (graph.GetNodes(), graph.GetEdges())

    return graph

filename = "likes.json"
graph = create_json_graph(filename)

with open("sehir.json", 'w') as f:
    json.dump(graph, f)

# graph = create_graph_from_likes(filename)
#
# colors = snap.TIntStrH()
# for i in range(6000):
#     if i < 3000:
#         colors[i] = "grey"
#     else:
#         colors[i] = "yellow"
# snap.DrawGViz(graph, snap.gvlSfdp, "graph.png", "Likes of users on the facebook page of Istanbul Sehir University", False, colors)
#
#
# snap.SaveEdgeList(graph, 'mygraph.txt')

# gvlDot = _snap.gvlDot
# gvlNeato = _snap.gvlNeato
# gvlTwopi = _snap.gvlTwopi
# gvlCirco = _snap.gvlCirco
# gvlSfdp = _snap.gvlSfdp