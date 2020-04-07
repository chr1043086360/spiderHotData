from pytz import utc
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from core.settings import MYSQL_NAME, MYSQL_PASSWORD, HOST_IP
# 配置作业存储器
jobstores = {
    'mongo': MongoDBJobStore(),
    # 'default': SQLAlchemyJobStore(url=f'mysql+pymysql://root:{MYSQL_PASSWORD}@{HOST_IP}:3306/{MYSQL_NAME}')
}
# 配置执行器，并设置线程数
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': False,     # 默认情况下关闭新的作业
    'max_instances': 3     # 设置调度程序将同时运行的特定作业的最大实例数3
}

# BlockingScheduler：前台阻塞任务可以用 &到后台执行  /  BackgroundScheduler：后台任务
scheduler = BlockingScheduler(
    jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)
