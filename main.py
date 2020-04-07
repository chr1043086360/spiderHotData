from task_apscheduler.task import scheduler
from core.spider import HotDataSpider
from core.settings import TARGET_IP
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# 每5分钟爬一次
@scheduler.scheduled_job('interval', seconds=300)
def main():
    obj = HotDataSpider(f"{TARGET_IP}")
    obj.parser()


if __name__ == "__main__":
    main()
    scheduler.start()
