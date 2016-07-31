import pymongo
import sys
import datetime
from bottle import route, run, template

# def print_to_html_file(list, name):
#     html1 = """
#     <!DOCTYPE html>
#     <html lang="en">
#         <head>
#             <link rel="stylesheet" href="css/bootstrap.css" type="text/css" />
#             <meta charset="utf-8" />
#         </head>
#         <body>"""
#     html2 = """
#         </body>
#     </html>
#
#      """
#     html_string = html1 + ''.join(list) + html2
#     with open(name + ".html", "w", encoding="utf-8") as f:
#         f.write(html_string)
@route('/show_posts')
def hello():
    client = pymongo.MongoClient()
    db = client.get_database('socialagg')
    posts = db.get_collection('posts')
    posts.create_index('id', unique=True)
    posts.create_index('created_time')

    if len(sys.argv) > 1:
        tmp = sys.argv[1:]
        str_time = ''.join(tmp)
        DAY = datetime.datetime.strptime(str_time, "%Y-%m-%d")
        day1 = DAY+datetime.timedelta(days=1)
        l = []
        for page in posts.find():
            posts_data = page['posts']['data']  # graph.get_object(page['id'], fields="id,posts.limit(50){type,message,id}")
            l.append("<h3>{}</h3>\n".format(page['name']))
            for post in posts_data:
                post_time_str = post['created_time'].replace("T", " ").replace("+0000", "")
                post_time = datetime.datetime.strptime(post_time_str, "%Y-%m-%d %H:%M:%S")
                if DAY < post_time < day1:
                    l.append("<p>{}</p>\n".format(post['message']))
        html_string = ''.join(l)
        return template('templates/show_posts.tpl', post=html_string)
        # print_to_html_file(l, str_time)

    else:
        l = []
        for page in posts.find():
            last_posts = page['posts']['data'][:50]
            l.append("<h3>{}</h3>\n".format(page['name']))
            index = 0
            for post in last_posts:
                index += 1
                if 'message' not in post:
                    continue
                if post['message']:
                    l.append("<p>post #{}: {}</p>\n".format(index, post['message']))
        html_string = ''.join(l)
        return template('templates/show_posts.tpl', post=html_string)

        # print_to_html_file(l, "last_50_posts")
run(host='localhost', port=8002, debug=True)

