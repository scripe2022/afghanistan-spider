import requests
from bs4 import BeautifulSoup
# import pymysql
from sqlalchemy import create_engine, Table, Column, MetaData
from sqlalchemy.types import INT, JSON, VARCHAR
import json

fp = open('links.txt', 'r')
link_list = fp.read().split('\n')
fp.close()

def init_db():
    f_json = open('../config.json')
    config = json.load(f_json)
    connect_address = 'mysql+pymysql://{}:{}@{}/{}'.format(config['user'], config['password'], config['host'], config['dbname'])
    engine = create_engine(connect_address)
    return engine

def write_db(engine, data):
    metadata = MetaData()
    data_table = Table('posts', metadata,
        Column('id', INT, primary_key=True),
        Column('url', VARCHAR),
        Column('datetime', VARCHAR),
        Column('title', VARCHAR),
        Column('type', VARCHAR),
        Column('titletrans', VARCHAR),
        Column('content', JSON)
    )
    json_object = {
        "url": data['url'],
        "datetime": data['datetime'],
        "title": data['title'],
        "titletrans": data["titletrans"],
        "type": data['type'],
        "source": data['source'],
        "content": data['content'],
    }
    with engine.connect() as conn:
        conn.execute(
            data_table.insert(),
            json_object
        )


def main(url):
    data = {}
    x = requests.get(url)
    x = str(x.content, 'utf-8')
    html_doc = x
    # html_doc = url
    soup = BeautifulSoup(html_doc, 'lxml')
    found = 0
    data['title'] = soup.select('header > h1[class="entry-title"]')[0].getText()
    if ("Afghanistan".casefold() in data['title'].casefold()):
        found = 1
    data['datetime'] = soup.select('div[class="entry-post-meta"] > div > time')[0].getText()
    data['titletrans'] = ''
    data['url'] = url
    data['source'] = ''
    data['type'] = 'alemarahenglish.af'
    dom = soup.select('article > div[class="entry-content clearfix"] > p')
    content_list = []
    for i in dom:
        p_str = i.getText()
        if ("Afghanistan".casefold() in p_str.casefold()):
            found = 1
        content_list.append(p_str)
    data['content'] = content_list
    return found, data

engine = init_db()

# f_html = open("demo.html", encoding = "utf-8")
# html_doc = f_html.read()

for i in range(len(link_list)):
    print((i+1), '/', len(link_list))
    rtn, data = main(link_list[i])
    if (rtn == 1):
        write_db(engine, data)