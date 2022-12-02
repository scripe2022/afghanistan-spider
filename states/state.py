import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Table, Column, MetaData
from sqlalchemy.types import INT, JSON, VARCHAR
import json


def init_db():
    f_json = open('../config.json')
    config = json.load(f_json)
    connect_address = 'mysql+pymysql://{}:{}@{}/{}'.format(config['user'], config['password'], config['host'], config['dbname'])
    engine = create_engine(connect_address)
    return engine

def process(url, filename):
    x = requests.get(url)
    x = str(x.content, 'utf-8')
    html_doc = x
    data = {}
    soup = BeautifulSoup(html_doc, 'lxml')
    data['title'] = soup.select('div[class="row"] > div[class="featured-content__copy"] > h1')[0].getText().strip()
    data['titletrans'] = ''
    data['datetime'] = soup.select('div[class="article-meta"] > p[class="article-meta__publish-date"]')[0].getText().strip()
    data['url'] = url
    data['source'] = ''
    data['type'] = 'state.gov@' + filename
    dom = soup.select('div[class="row"] > div[class="entry-content"] > p')
    content_list = []
    for i in dom:
        content_list.append(i.getText())
    data['content'] = content_list
    return data

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

engine = init_db()

def main(filename):
    fp = open(filename + '.txt', 'r')
    link_list = fp.read().split('\n')
    fp.close()
    for i in range(0, len(link_list)):
        if (link_list[i] == ''):
            continue
        print(filename + ": " + str(i))
        data = process(link_list[i], filename)
        write_db(engine, data)

# f_html = open("demo.html", encoding = "utf-8")
# html_doc = f_html.read()
# main('press_release')
main('from_the_secretary')
main('department_press_briefings')