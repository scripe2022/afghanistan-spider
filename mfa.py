import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Table, Column, MetaData
from sqlalchemy.types import INT, JSON
import json

def preprocess(filename):
    f_html = open(filename, encoding = "utf-8")
    html_doc = f_html.read()
    soup = BeautifulSoup(html_doc, 'lxml')
    dom = soup.select('section[class="basic-result_content"] > div[class="item"] > div[class="description"] > a[class="source"]')
    print(dom)

preprocess("mfalinks/page1.html")