import facebook
import json

version = '2.5'
page_id = "120064698011379"
data = []

access_token = open("access_token", "r").read()

graph = facebook.GraphAPI(access_token=access_token, version=version)

page = graph.get_object(id=page_id)


posts = graph.get_connections(id=page_id, connection_name="posts", limit=100)
data += posts["data"]
try:
    while True:
        print len(data)
        next_page = posts['paging']['next'][27:]
        posts = graph.request(next_page)
        data += posts["data"]
        if len(data) == 10000:
            break
        if "paging" not in posts:
            break
        if "next" not in posts["paging"]:
            break
except:
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)

with open('data.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)

print len(data)
