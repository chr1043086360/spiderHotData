from pymongo import MongoClient
from core.settings import MONGODB_PASSWORD, HOST_IP

client = MongoClient(f'mongodb://root:{MONGODB_PASSWORD}@{HOST_IP}:27017/')

# 创建数据库
db = client.spider
