import lxml
import requests
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch, client


def create_index():
    es = Elasticsearch()
    ic = client.IndicesClient(es)

    # 判断索引是否存在
    if not ic.exists(index="poetry"):
        # 创建索引
        doc = {
            "mappings": {
                "properties": {
                    "title": {
                        "type":  "keyword"
                    },
                    "epigraph": {
                        "type":  "keyword"
                    },
                    "dynasty": {
                        "type":  "keyword"
                    },
                    "author": {
                        "type":  "keyword"
                    },
                    "content": {
                        "type":  "text"
                    }
                }
            }
        }

        ic.create(index='poetry', body=doc)


def get_poetry(list_url):
    es = Elasticsearch()

    # 取得列表页面
    html = requests.get(list_url).text
    soup = BeautifulSoup(html, "lxml")
    typecont = soup.find_all(attrs={"class": "typecont"})

    # 遍历列表
    for div in typecont:
        for ch in div.children:
            if ch.name == 'span':
                # 取得诗词内容
                print('get:', ch.a.text, ch.a.attrs['href'])
                html = requests.get(
                    'https://so.gushiwen.org' + ch.a.attrs['href']).text
                soup = BeautifulSoup(html, "lxml")
                cont = soup.select('.main3 .left .sons .cont')[0]

                # 标题
                title = cont.h1.text

                # 词牌
                epigraph = ""
                if '·' in title:
                    epigraph = title[:title.index('·')]

                al = cont.p.select('a')

                # 朝代
                dynasty = al[0].text

                # 作者
                author = al[1].text

                # 内容
                content = cont.select('.contson')[0].text.strip()

                # 索引数据
                doc = {
                    "title": title,
                    "epigraph": epigraph,
                    "dynasty": dynasty,
                    "author": author,
                    "content": content
                }
                # ret = es.index(index='poetry', doc_type='poetry', body=doc)
                ret = es.index(index='poetry', body=doc)
                print(ret)


def main():
    create_index()
    get_poetry('https://so.gushiwen.org/gushi/tangshi.aspx')
    get_poetry('https://so.gushiwen.org/gushi/songsan.aspx')


if __name__ == '__main__':
    main()
