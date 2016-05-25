import pymongo
import facebook
from pprint import pprint

client = pymongo.MongoClient()
db = client.get_database('socialagg')
pages = db.get_collection('pages')
l = []
for page in pages.find():
    l.append(page)
idStr = list()
for e in l:
    idStr.append("<h1>name: " + e['name'] + "</h1>\n<h3>about: " + e['about'] + "</h3>\n<h3>fans: {}</h3>".format(e['fan_count']))

txt = "\n".join(idStr)

htmlA = """
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
    </head>
    <body>"""
htmlB = """
    </body>
</html>

 """
o = htmlA + "{}".format(txt) + htmlB
with open("shoe_pages.html", "wb") as f:
    f.writelines(o)

