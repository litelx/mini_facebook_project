from bottle import route, run, template
import pymongo

@route('/show_pages')
def hello():

    client = pymongo.MongoClient()
    db = client.get_database('socialagg')
    pages = db.get_collection('pages')
    l = []
    for page in pages.find():
        l.append(page)
    id_Str = list()
    for e in l:
        if 'picture':
            id_Str.append("<img class=\"img-responsive\" src=" + e['picture']['data']['url'] + " alt=\"\">")
        if 'name':
            id_Str.append("<h1>name: " + e['name'] + "</h1>\n")
        if 'about' in e:
            id_Str.append("<h3>about: " + e['about'] + "</h3>\n")
        if 'fan_count':
            id_Str.append("<h3>fans: {}</h3>".format(e['fan_count']))

    txt = "\n".join(id_Str)

    return template('templates/show_pages.tpl', page=txt)
run(host='localhost', port=8002, debug=True)



    # htmlA = """
    # <!DOCTYPE html>
    # <html lang="en">
    #     <head>
    #         <link rel="stylesheet" href="css/bootstrap.css" type="text/css" />
    #         <meta charset="utf-8" />
    #     </head>
    #     <body>"""
    # htmlB = """
    #     </body>
    # </html>
    # """
    # o = htmlA + "{}".format(txt) + htmlB

    # hello(o)
# with open("show_pages.html", "w") as f:
#     f.writelines(o)