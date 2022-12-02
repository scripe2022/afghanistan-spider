import requests
from bs4 import BeautifulSoup
pages = []
links = []

def add_link(base, n):
    pages.append(base)
    for i in range(2, n+1):
        pages.append(base + "page/" + str(i) + '/')

add_link("https://www.alemarahenglish.af/category/news/", 5)
add_link("https://www.alemarahenglish.af/category/top-news/", 5)
add_link("https://www.alemarahenglish.af/category/photoreport/", 6)
add_link("https://www.alemarahenglish.af/category/weekily-comment/", 5)
add_link("https://www.alemarahenglish.af/category/statements/", 5)
add_link("https://www.alemarahenglish.af/category/remarks-reactions/", 5)
add_link("https://www.alemarahenglish.af/category/articles-and-opinions/", 5)
add_link("https://www.alemarahenglish.af/category/interviewes-and-reports/", 5)
total = len(pages)

def get_article_link(url):
    # f_html = open("demo.html", encoding = "utf-8")
    # html_doc = f_html.read()
    x = requests.get(url)
    x = str(x.content, 'utf-8')
    html_doc = x
    soup = BeautifulSoup(html_doc, 'lxml')
    a = soup.select('div[class="cat-body no-head"] > ul[class="nb1 cat-list clearfix"] > li > h2[class="cat-list-title"] > a')
    for i in a:
        links.append(i['href'])

for i in pages:
    print(i)
    get_article_link(i)

result = list(set(links))

with open('links.txt', 'w') as fp:
    for item in result:
        fp.write("%s\n" % item)
