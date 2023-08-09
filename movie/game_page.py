import datetime

import pymongo
from datetime import datetime

mongo_client = pymongo.MongoClient('mongodb://username:password@localhost:27017/')

headers = {
    "'user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/113.0.0.0 Safari/537.36'"}


def games_336k():
    import requests
    from lxml import etree

    mongo_conn = mongo_client.get_database('games').get_collection('游戏平台336k')
    for page in range(1, 141):
        print('games_336k:', page)
        response = requests.get(f"https://336k.cn/q/page/{page}/", headers=headers)
        xpath_dom = etree.HTML(response.text)
        for item in xpath_dom.xpath("//div[@class='col-lg-5ths col-lg-3 col-md-4 col-6']"):
            one_game = dict()
            one_game['img'] = item.xpath(".//img/@data-src")[0]
            one_game['title'] = item.xpath(".//h2[@class='entry-title']/a/@title")[0]
            one_game['detail_url'] = item.xpath(".//h2[@class='entry-title']/a/@href")[0]
            one_game['category'] = item.xpath(".//span[@class='meta-category-dot']/a/text()")
            mongo_conn.insert_one(one_game)


def games_leyouduo():
    import requests
    from lxml import etree

    mongo_conn = mongo_client.get_database('games').get_collection('乐游多')
    for page in range(1, 206):
        print('leyoudao:', page)
        response = requests.get(f"https://www.leyouduo.vip/game/page/{page}/", headers=headers)
        xpath_dom = etree.HTML(response.text)
        for item in xpath_dom.xpath("//posts[@class='posts-item list ajax-item flex']"):
            one_game = dict()
            one_game['img'] = item.xpath(".//div[@class='item-thumbnail']/a/img/@data-src")[0]
            one_game['title'] = item.xpath(".//div[@class='item-thumbnail']/a/img/@alt")[0]
            one_game['detail_url'] = item.xpath(".//div[@class='item-thumbnail']/a/@href")[0]
            # print(one_game)
            mongo_conn.insert_one(one_game)


def yinghua_anime():
    import requests
    from lxml import etree

    mongo_conn = mongo_client.get_database('games').get_collection('樱花动漫')
    for page in range(1, 138):
        print('yinghua_anime:', page)
        response = requests.get(f"https://www.dm815.com/show/riben/page/{page}.html", headers=headers)
        xpath_dom = etree.HTML(response.text)
        xpath_doms = xpath_dom.xpath("//div[@class='stui-vodlist__box']")

        for xpath_dom in xpath_doms:
            pic = xpath_dom.xpath("./a/@data-original")[0]
            detail_url = xpath_dom.xpath("./a/@href")[0]
            title = xpath_dom.xpath("./a/@title")[0]
            mongo_conn.insert_one({
                'img': pic,
                "detail_url": detail_url,
                "title": title,
            })


def 美剧天堂_美剧():
    import requests
    from lxml import etree

    mongo_conn = mongo_client.get_database('games').get_collection('美剧天堂-美剧')
    for page in range(22, 191):
        print('美剧:', page)
        response = requests.get(f"https://www.mjttz.com/show/meiju/page/{page}.html", headers=headers)
        xpath_dom = etree.HTML(response.text)
        xpath_doms = xpath_dom.xpath("//article[@class='u-movie']")

        for xpath_dom in xpath_doms:
            pic = xpath_dom.xpath(".//img/@data-original")[0]
            detail_url = xpath_dom.xpath("./a/@href")[0]
            title = xpath_dom.xpath("./a/h2/text()")[0]
            tags = xpath_dom.xpath(".//span[@class='tags']/a/text()")
            scores = xpath_dom.xpath(".//div[@class='pingfen']/span/text()")[0]

            info = {
                'img': pic,
                "detail_url": detail_url,
                "title": title,
                "tags": tags,
                'scores': scores,
            }
            # print(info)
            mongo_conn.insert_one(info)


def 美剧天堂_电影板块():
    import requests
    from lxml import etree
    mongo_conn = mongo_client.get_database('games').get_collection('美剧天堂-电影')
    for page in range(1, 662):
        print("电影:", page)
        response = requests.get(f"https://www.mjttz.com/show/dianying/page/{page}.html", headers=headers)
        xpath_dom = etree.HTML(response.text)
        xpath_doms = xpath_dom.xpath("//article[@class='u-movie']")

        for xpath_dom in xpath_doms:
            pic = xpath_dom.xpath(".//img/@data-original")
            detail_url = xpath_dom.xpath("./a/@href")
            title = xpath_dom.xpath("./a/h2/text()")
            tags = xpath_dom.xpath(".//span[@class='tags']/a/text()")
            scores = xpath_dom.xpath(".//div[@class='pingfen']/span/text()")[0]
            info = {
                'img': pic[0],
                "detail_url": detail_url[0],
                "title": title[0],
                "tags": tags,
                'scores': scores,
            }
            # print(info)
            mongo_conn.insert_one(info)


def 美剧天堂_电视剧():
    import requests
    from lxml import etree

    mongo_conn = mongo_client.get_database('games').get_collection('美剧天堂-电视剧')
    for page in range(310, 343):
        print("电视剧:", page)
        response = requests.get(f"https://www.mjttz.com/show/dianshiju/page/{page}/", headers=headers)
        xpath_dom = etree.HTML(response.text)
        xpath_doms = xpath_dom.xpath("//article[@class='u-movie']")

        for xpath_dom in xpath_doms:
            pic = xpath_dom.xpath(".//img/@data-original")[0]
            detail_url = xpath_dom.xpath("./a/@href")[0]
            title = xpath_dom.xpath("./a/h2/text()")[0]
            tags = xpath_dom.xpath(".//span[@class='tags']/a/text()")
            status = xpath_dom.xpath(".//div[@class='zhuangtai']/span/text()")
            scores = xpath_dom.xpath(".//div[@class='pingfen']/span/text()")[0]

            info = {
                'img': pic,
                "detail_url": detail_url,
                "title": title,
                "tags": tags,
                'status': status,
                'scores': scores,
            }

            mongo_conn.insert_one(info)


import requests
import os


def download_consumer():
    collection = mongo_client['games']['美剧天堂-电影']
    index = 0
    for one in collection.find({}):
        index += 1
        print(index)
        if not os.path.exists(f"/www/upload/{datetime.now().strftime('%Y-%m-%d')}"):
            os.mkdir(f"/www/upload/{datetime.now().strftime('%Y-%m-%d')}")
        save_fp = f"/www/upload/{datetime.now().strftime('%Y-%m-%d')}/{str(one['_id'])}." + one['img'].split('.')[-1]
        local_path = f"/upload/{datetime.now().strftime('%Y-%m-%d')}/{str(one['_id'])}." + one['img'].split('.')[-1]

        if os.path.exists(save_fp):
            continue

        if one['img'].startswith('http'):
            request_url = one['img']
        else:
            request_url = "https://www.mjttz.com" + one['img']

        response = requests.get(request_url, headers=headers)
        print(save_fp)
        with open(save_fp, 'wb+') as f:
            f.write(response.content)
            collection.update_one({'_id': one['_id']},
                                  {'$set': {'local_path': local_path}})

# games_336k()
# games_leyouduo()
# yinghua_anime()
# 美剧天堂_美剧()
# 美剧天堂_电影板块()
# 美剧天堂_电视剧()
