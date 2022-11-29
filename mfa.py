import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Table, Column, MetaData
from sqlalchemy.types import INT, JSON, VARCHAR
import json

link_list = []

def preprocess(filename):
    f_json = open(filename, encoding = "utf-8")
    json_content = json.loads(f_json.read())['data']['middle']['list']
    for i in json_content:
        link_list.append(i['url'])

for i in range(1, 10):
    preprocess("mfalinks/page{}.json".format(i))

def init_db():
    f_json = open('config.json')
    config = json.load(f_json)
    connect_address = 'mysql+pymysql://{}:{}@{}/{}'.format(config['user'], config['password'], config['host'], config['dbname'])
    engine = create_engine(connect_address)
    return engine


def main_mfa(url):
    x = requests.get(url)
    x = str(x.content, 'utf-8')
    html_doc = x
    data = {}
    soup = BeautifulSoup(html_doc, 'lxml')
    data['type'] = 'mfa.gov.cn'
    data['title'] = soup.select('div[class="news-details"] > div[class="news-title"] > h1')[0].getText()
    data['datetime'] = soup.select('p[class="time"] > span')[0].getText()
    data['url'] = url
    data['source'] = ''
    dom = soup.select('div[class="news-details"] > div[class="news-main"] > p')
    content_list = []
    for i in dom:
        if (i.getText() == ''):
            continue
        content_list.append(i.getText())
    data['content'] = content_list
    return data

def main_fmprc(url):
    x = requests.get(url)
    x = str(x.content, 'utf-8')
    html_doc = x
    data = {}
    soup = BeautifulSoup(html_doc, 'lxml')
    data['type'] = 'fmprc.gov.cn'
    data['title'] = soup.select('div[class="vibox"] > div[class="title"]')[0].getText()
    data['source'] = soup.select('div[class="time"] > span[id="News_Body_source"] > span[id="myDocsource2"]')[0].getText()
    data['datetime'] = soup.select('div[class="time"] > span[id="News_Body_Time"]')[0].getText()
    data['url'] = url
    dom = soup.select('div[class="vibox"] > div[id="News_Body_Txt_A"] > p')
    content_list = []
    for i in dom:
        if (i.getText() == ''):
            continue
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
        Column('content', JSON)
    )
    json_object = {
        "url": data['url'],
        "datetime": data['datetime'],
        "title": data['title'],
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
for i in range(len(link_list)):
    print((i+1), '/', len(link_list))
    if ("fmprc.gov" in link_list[i]):
        data = main_fmprc(link_list[i])
    else:
        data = main_mfa(link_list[i])
    write_db(engine, data)