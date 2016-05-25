import sys
import pymongo
import facebook
import requests
import secrets


def save_to_db(page_id_name, t, pages_coll, posts_coll):
    graph = facebook.GraphAPI(access_token=t, version='2.5')
    page = graph.get_object(page_id_name, fields="id,about,name,fan_count")    # posts.limit(100){type,message, id}
    pages_coll.create_index('id', unique=True)
    pages_coll.update_one({'id': page['id']}, {'$set': page}, upsert=True)

    post_rec = graph.get_object(page_id_name, fields="id,name,posts.limit(100){type,message,created_time,id}")
    posts_coll.create_index('id', unique=True)
    posts_coll.create_index('created_time') # posts.create_index('published_at')
    posts_coll.update_one({'id': post_rec['id']}, {'$set': post_rec}, upsert=True)  #

    return "{}".format(page['id']), "{}".format(page['fan_count'])

client = pymongo.MongoClient()
db = client.get_database('socialagg')
pages = db.get_collection('pages')
posts = db.get_collection('posts')
# posts = posts.drop()
# posts = db.get_collection('posts')
with open("TOKEN.txt") as f:
    TOKEN = f.read().strip()

for URL in sys.argv[1:]:
    r = requests.get(URL, {
        'client_id': secrets.APP_ID,
        'client_secret': secrets.APP_SECRET,
        'grant_type': 'client_credentials',
    })

    page_id = URL.replace("https://www.facebook.com/", "")

    u = r.status_code
    if u == 200:
        result = save_to_db(page_id, TOKEN, pages, posts)
        print("OK, added id #{} with {} fans.".format(result[0], result[1]))
    else:
        print("Not a page")

# l = [
#     "beyonce",
#      "barbie",
#      "oscapitalmarket",
#      "SaritHadadMusic",
#      "kimkardashian",
#      "RocketKingGnR",
#      "Beckham",
#      "victoriabeckham",
#      "ShimonPeresInt",
#      "Ilanit.Levi",
#      "Denmark.dk",
#      "japanika.net",
#      "TelAvivGlobalCity",
#     "MarilynMonroe"
#      ]
