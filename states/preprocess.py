import requests
from bs4 import BeautifulSoup
# import pymysql
from sqlalchemy import create_engine, Table, Column, MetaData
from sqlalchemy.types import INT, JSON, VARCHAR
import json

filename = "department_press_briefings"

f_html = open(filename + ".html", encoding = "utf-8")
html_doc = f_html.read()

soup = BeautifulSoup(html_doc, "lxml")
dom = soup.select('ul[class="collection-results"] > li[class="collection-result"] > a[class="collection-result__link"]')
link_list = []
for i in dom:
    link_list.append(i['href'])

with open(filename + '.txt', 'w') as fp:
    for item in link_list:
        fp.write("%s\n" % item)
