import redis
from core.settings import HOST_IP, REDIS_PASSWORD


def Redis_producer(data):
    r = redis.StrictRedis(
        host=f'{HOST_IP}', port=6379, password=f'{REDIS_PASSWORD}')

    map = {"微博热搜榜": "weibo",
           "百度搜索风云榜": "baidu",
           "搜狗热搜榜": "sougou",
           "神马搜索": "shenma",
           "抖音": "douyin",
           "360搜索": "360sou",
           "豆瓣话题广场": "douban",
           "网易热点排行": "wangyi",
           "百度贴吧热议榜": "tieba",
           "V2EX最热": "v2ex",
           "知乎热榜": "zhihu",
           "GitHub-Trending": "github",
           "哔哩哔哩全站日榜": "bilibili",
           "Packagist-Popular Packages": "ppp"}

    # print(map[data["head"].strip()])
    string = ";".join(data["hot_href"])
    r.set(map[data["head"].strip()], string)
    # print(data["head"])
    # print(r.get(data["head"]).decode("utf-8").split(";"))
