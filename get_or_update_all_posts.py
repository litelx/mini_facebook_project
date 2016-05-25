import pymongo
import facebook

client = pymongo.MongoClient()
db = client.get_database('socialagg')
posts = db.get_collection('posts')

with open("TOKEN.txt") as f:
    TOKEN = f.read().strip()

graph = facebook.GraphAPI(access_token=TOKEN, version='2.5')
sOld, sNew = set(), set()
for post in posts.find():
    c = 0
    [sOld.add(i['id']) for i in post['posts']['data']]
    new_posts = graph.get_object(post['id'], fields="id,name,posts.limit(100){type,message,created_time,id}")
    for i in new_posts['posts']['data']:
        sNew.add(i['id'])  # 1, 2, 3 , 4, 5
        if i['id'] in sOld:
            c += 1
    if c < 100:
        posts.delete_many(post)
        posts.create_index('id', unique=True)
        posts.create_index('created_time')  # posts.create_index('published_at')
        posts.update_one({'id': post['id']}, {'$set': new_posts}, upsert=True)  #
    print("Updating page \"" + post['name'] + "\"")
    print("Inserted {} posts, update {} posts.".format(100-c, c))
print("Done.")
