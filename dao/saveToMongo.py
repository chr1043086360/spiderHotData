from .initMongo import db
from pprint import pprint
# from datetime import datetime, date
# import json

# 自定义序列化
# class JsonToDatetime(json.JSONEncoder):
#     """
#     JSONEncoder不知道怎么去把这个数据转换成json字符串的时候，
#     它就会调用default()函数，default()函数默认会抛出异常。
#     所以，重写default()函数来处理datetime类型的数据。
#     """

#     def default(self, obj):
#         if isinstance(obj, datetime):
#             return obj.strftime('%Y-%m-%d %H: %M: %S')
#         elif isinstance(obj, date):
#             return obj.strftime('%Y-%m-%d')
#         else:
#             return json.JSONEncoder.default(self, obj)


def save_to_mongodb(data):

    # json_data = json.dumps(data, cls=JsonToDatetime)
    # 创建一个collection
    spider_hot_data = db.spider_hot_data
    # 插入数据，必须是字典
    spider_id = spider_hot_data.insert_one(data).inserted_id

    # 获取结果
    # for x in spider_hot_data.find():
        # pprint(x)
