import requests
from bs4 import BeautifulSoup
# import pymysql
from sqlalchemy import create_engine, Table, Column, MetaData
from sqlalchemy.types import INT, JSON, VARCHAR
import json

link_list = [
    'https://www.whitehouse.gov/briefing-room/statements-releases/2021/09/10/statement-by-nsc-spokesperson-emily-horne-on-further-u-s-citizen-departures-from-afghanistan/',
    'https://www.whitehouse.gov/briefing-room/speeches-remarks/2021/08/31/remarks-by-president-biden-on-the-end-of-the-war-in-afghanistan/',
    'https://www.whitehouse.gov/briefing-room/statements-releases/2021/08/27/statement-by-press-secretary-jen-psaki-on-the-president-and-vice-presidents-meeting-with-their-national-security-team-on-afghanistan/',
    'https://www.whitehouse.gov/briefing-room/presidential-actions/2021/08/26/a-proclamation-honoring-the-victims-of-the-attack-in-kabul-afghanistan/',
    'https://www.whitehouse.gov/briefing-room/speeches-remarks/2021/08/24/remarks-by-president-biden-on-the-ongoing-evacuation-efforts-in-afghanistan-and-the-house-vote-on-the-build-back-better-agenda/',
    'https://www.whitehouse.gov/briefing-room/speeches-remarks/2021/08/22/remarks-by-president-biden-on-tropical-storm-henri-and-the-evacuation-operation-in-afghanistan/',
    'https://www.whitehouse.gov/briefing-room/statements-releases/2021/08/21/readout-of-president-bidens-call-with-speaker-pelosi-on-afghanistan-evacuations-and-the-build-back-better-agenda/',
    'https://www.whitehouse.gov/briefing-room/speeches-remarks/2021/08/20/remarks-by-president-biden-on-evacuations-in-afghanistan/',
    'https://www.whitehouse.gov/briefing-room/speeches-remarks/2021/08/16/remarks-by-president-biden-on-afghanistan/'
]

def init_db():
    f_json = open('config.json')
    config = json.load(f_json)
    connect_address = 'mysql+pymysql://{}:{}@{}/{}'.format(config['user'], config['password'], config['host'], config['dbname'])
    engine = create_engine(connect_address)
    return engine


def main(url):
    data = {}
    x = requests.get(url)
    html_doc = x.text
    soup = BeautifulSoup(html_doc, 'lxml')
    data['title'] = soup.title.string
    data['datetime'] = soup.time.string
    data['type'] = "whitehouse.gov"
    data['url'] = url
    data['source'] = ''
    dom = soup.select('section[class="body-content"] > div[class="container"] > div[class="row"]')
    content_list = dom[0].find_all("p", attrs={'class': None})
    for i in range(len(content_list)):
        content_list[i] = content_list[i].getText()
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
    data = main(link_list[i])
    write_db(engine, data)


# engine = init_db()
# write_db(engine, data)
