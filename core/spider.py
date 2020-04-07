#######################################################################################
# Author ： CHR_崔贺然
# Time ： 2020.04.06
# TODO ： 爬虫主逻辑
# *
# !
# ?
#######################################################################################
import requests
import asyncio
import aiohttp
from lxml import etree
from core import settings
import abc
from dao.saveToMongo import save_to_mongodb
from datetime import datetime
from NSQ.producer import NSQ
from Kafka.producer import Kafka_producer
from utils.log import logger
from dao.initMysql import create_connection, disconnect
from dao.saveToMysql import save_to_mysql

# 抽象类(或接口)，没有必要用abc来做，这样更加灵活


class BaseSpider:
    def __init__(self):
        pass

    def start(self):
        pass

    def parser(self):
        pass


class HotDataSpider(BaseSpider):

    def __init__(self, url: str):
        self.url = url  # 入参url
        self.session = requests.session()  # 带cookie的请求

    # 开始爬虫
    def start(self):
        '''
        rtype :爬取的html网页
        '''
        res = self.session.get(self.url, headers=settings.header)
        return res.text

    # 循环解析，可以看做是DFS模型
    def parser(self):
        # 热搜榜分类(到Bilibili热搜榜),后面的格式就不一样了
        print("***************正在爬取，详见spider.log***************")
        for num in range(1, 8):
            self.dict = {}  # 内存中的缓存容器
            res_data = self._get_info(num)

            # 写入到MongoDB中(默认MongoDB，数据结构最合适)
            try:
                save_to_mongodb(res_data)
                logger.info("写入MongoDB成功")
            except Exception:
                raise "写入MongoDB失败"

            # 写入到MySQL中，可以同步到ES、TiDB、Hive、HBase等
            # create_connection()  # 开启连接
            # logger.info("数据库开启连接")
            # try:
            #     save_to_mysql(res_data)  # 写入数据库
            # except Exception:
            #     raise "写入MySQL失败
            # disconnect()  # 关闭连接
            # logger.info("数据库关闭连接")

            # 写到Kafka中，可以对接Spark、Flink对爬取的数据做大数据分析
            # try:
            #     Kafka_producer(res_data)
            # except Exception:
            #     raise "写入Kafka失败"

            # 写到NSQ消息队列中，golang可以做消费端
            # try:
            #     NSQ(res_data).send()
            # except Exception:
            #     raise "写入NSQ失败"

            # 写到RabbiMQ消息队列中
            # try:
            #     RabbitMQ_producer(res_data)
            # except Exception:
            #     raise "写入RabbitMQ失败"

    # 获取各大平台的热搜

    def _get_info(self, num: int):
        '''
        param num: 爬取的分类
        '''
        html = etree.HTML(self.start())

        # 头部
        head = html.xpath(
            f"/html/body/div/div[1]/div[3]/div/div[2]/div[1]/div[{num}]/div[1]/h4/text()")

        logger.info("**************%s**************" % num)
        self.dict["time"] = datetime.now()
        self.dict["head"] = head[0]

        # 定义dict容器中的数据结构
        self.dict["hot"] = []
        self.dict["search_num"] = []

        # 循环1～10榜单
        for i in range(1, 11):

            # 热点内容
            hot_info = html.xpath(
                f"/html/body/div/div[1]/div[3]/div/div[2]/div[1]/div[{num}]/table/tbody/tr[{i}]/td[2]/a/text()")
            self.dict["hot"].append(hot_info[0])

            # 搜索指数
            search_num = html.xpath(
                f"/html/body/div/div[1]/div[3]/div/div[2]/div[1]/div[{num}]/table/tbody/tr[{i}]/td[3]/span/text()")
            self.dict["search_num"].append(search_num[0])

        print(self.dict)  # 上线注释掉
        return self.dict
        #####################################################################################################################
        #  dict的数据结构:
        #  {
        #    'head': xxx,
        #    'hot': [xxx, xxx, xxx, xxx, xxx, xxx, xxx, xxx, xxx, xxx],
        #    'search_num': [xxx, xxx, xxx, xxx, xxx, xxx, xxx, xxx, xxx, xxx]
        #    'time': xxxx-xx-xx-xx:xx:xx
        #  }
        #
        #
        #  for example:
        #  {
        #    'head': ' 微博热搜榜',
        #    'hot': ['谭维维 谭某某', '湖北高校返校后要求学生不外出不聚餐', '朱广权李佳琦直播', '黎语冰棠雪分手', '演员李菲耶罗感染新冠去世',
        #            '韩真真发文力挺尚雯婕', '极限挑战路透', '郭杰瑞', '安倍称将向收入大减人群发放现金', '中国发布新冠肺炎疫情纪事'],
        #    'search_num': ['3,437,502', '1,731,093', '1,581,078', '1,321,506', '1,237,722',
        #                   '1,143,355', '1,087,639', '1,042,756', '964,518', '924,827']
        #    'time': 2020-04-07-11:28:11
        #  }
        #####################################################################################################################
