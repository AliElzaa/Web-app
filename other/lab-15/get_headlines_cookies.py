from flask import Flask, render_template
from flask import request, make_response
import feedparser
import datetime

app = Flask(__name__)

RSS_FEEDS = { 'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
              'aljazeera' : 'https://www.aljazeera.com/xml/rss/all.xml',
              'ap':\
              'http://hosted2.ap.org/atom/APDEFAULT/cae69a7523db45408eeb2b3a98c0c9c5'}


@app.route("/")
def headlines():
    publication =''
    if request.cookies.get('publication'):
        publication = request.cookies.get('publication')
    if request.args.get('publication'):
        publication = request.args.get('publication')
        print publication
    if not publication or publication.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:
        publication = publication.lower()
    print(publication)
    feed = feedparser.parse(RSS_FEEDS[publication])
    articles = feed['entries']

    response =\
    make_response(render_template('get_headlines.html',articles=articles))

    expires = datetime.datetime.now() + datetime.timedelta(days=1)
    response.set_cookie("publication", publication, expires=expires)
    return response


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8000)
