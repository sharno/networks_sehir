import facebook
import json

version = '2.5'
limit = 100
page_id = "120064698011379"
data = {}

access_token = open("access_token", "r").read()

graph = facebook.GraphAPI(access_token=access_token, version=version)

# file = open("data.json", 'r')
posts = json.load(file)
# posts = set(post['id'] for post in posts)
# print len(posts)

for post in posts:
    if "message" in post:
        print post['message']
    elif "story" in post:
        print post['story']
    post_id = post['id']
    likes = graph.get_connections(post['id'], connection_name="likes", limit=100)
    data[post_id] = likes['data']
    while "paging" in likes and "next" in likes["paging"]:
        next_page = likes['paging']['next'][27:]
        likes = graph.request(next_page)
        data[post_id] += likes['data']
    print "    " + str(len(data[post_id])) + " likes"

with open('likes.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)

# file = open("likes.json", "r")
# likes = json.load(file)
# posts = set(post['id'] for post in posts)
# likes = set(likes.keys())
# diff = posts.difference(likes)
# print diff
# print len(posts)
# print len(likes)
