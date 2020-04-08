# 说明文档

---

#### 目录结构

- alembic(数据库迁移工具，详见官网)
- core(核心业务逻辑)
-  ------ settings.py: 项目配置信息(从.env 文件中获取)
- ------ spider.py: 爬虫核心逻辑
- dao(持久层，用于落盘)
- ------ initMysql.py: 初始化 MySQL 连接
- ------ initMongo.py: 初始化 MongoDB 连接
- ------ saveToMysql.py: 保存到 MySQL
- ------ saveToMongo.py: 保存到 MongoDB
- Elasticsearch(将数据写入 ES 用于全文索引)
- Kafka(将数据写到 Kafka 中，可以对接 Spark、Flink 对爬取的数据做大数据分析)
- ------ producer.py: 生产者
- model(ORM 层)
- ------ hotDataModel.py: 表结构
- NSQ(将数据写到 NSQ 消息队列中，golang 可以做消费端)
- ------ producer.py: 生产者
- RabbitMQ(将数据写入到 RabbitMQ 中)
- ------ producer.py: 生产者
- Redis
- task_apscheduler(定时任务框架)
- ------ task.py: 定时任务配置
- utils(工具包)
- ------ log.py: 日志配置

---

#### 快速开始

- 安装虚拟环境(仅限 Python3.5 之后)

```bash
python3 -m venv .spider
```

- 激活虚拟环境

```bash
source .spider/bin/activate
```

- 安装依赖

```bash
pip install -r requirements.txt
```

- 导出依赖

```bash
pip freeze > requirements.txt
```

---

#### 更改配置文件

- 根目录下创建.env 文件

```bash
TARGET_IP = "https://www.hotspotschina.com/"  # 待爬取的IP


######################################### MongoDB ###########################################
HOST_IP = ""  # 远端或本地IP
MONGODB_PASSWORD = ""  # 数据库密码MongoDB
MONGODB_NAME = ""  # 数据库名称


######################################### MySQL ###########################################
HOST_IP = ""  # 远端或本地IP
MYSQL_PASSWORD = ""  # 数据库密码MySQL
MYSQL_NAME = ""  # 数据库名称


######################################### Redis #############################################
REDIS_PASSWORD = ""  # Redis密码


######################################### kafka #############################################
KAFKA_HOST_IP_PORT = ""  # 远端或本地IP


###################################### Elasticsearch ########################################
ES_HOST_IP_PORT = ""  # 远端或本地IP


########################################## NSQ ##############################################
NSQ_HOST_IP_PORT = ""  # 远端或本地IP


######################################## RabbitMQ ###########################################
RABBITMQ_HOST_IP = ""  # 远端或本地IP
RABBITMQ_PASSWORD = ""  # RabbitMQ密码
```

---

#### Docker 部署 MongoDB

- 下载镜像

```bash
docker pull daocloud.io/library/mongo:latest
```

- 运行容器

```bash
docker run --name mongodb -d -p 27017:27017 -v /opt/mongoDB/:/data/db daocloud.io/library/mongo:latest
```

- 进入容器

```bash
docker exec -it “containerid” /bin/bash
```

- 添加用户名密码

```bash
进入mongo命令
mongo

进入admin库
use admin

创建用户
db.createUser({ user: 'root', pwd: 'password', roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]

出现下面信息表示添加成功
Successfully added user: {
     "user" : "root",
     "roles" : [
         {
             "role" : "userAdminAnyDatabase",
             "db" : "admin"
         }
     ]
 }
```

---

#### Docker 部署 MySQL

- https://github.com/chr1043086360/docker_mysql
- 下载官方 mysql5.7 镜像

```bash
docker pull mysql:5.7
```

- 创建数据挂载持久化目录

```bash
mkdir -p /data/mysql/data
```

- dockerfile

```bash
FROM mysql:5.7
ADD mysqld.cnf /etc/mysql/mysql.conf.d/mysqld.cnf
```

- mysqld.cnf

```bash
[client]
port=3306
socket = /var/run/mysqld/mysqld.sock
[mysql]
no-auto-rehash
auto-rehash
default-character-set=utf8mb4
[mysqld]
###basic settings
server-id = 2
pid-file    = /var/run/mysqld/mysqld.pid
socket        = /var/run/mysqld/mysqld.sock
datadir        = /var/lib/mysql
#log-error    = /var/lib/mysql/error.log
# By default we only accept connections from localhost
#bind-address    = 127.0.0.1
# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0
character-set-server = utf8mb4
sql_mode="NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION"
default-storage-engine=INNODB
transaction_isolation = READ-COMMITTED
auto_increment_offset = 1
connect_timeout = 20
max_connections = 3500
wait_timeout=86400
interactive_timeout=86400
interactive_timeout = 7200
log_bin_trust_function_creators = 1
wait_timeout = 7200
sort_buffer_size = 32M
join_buffer_size = 128M
max_allowed_packet = 1024M
tmp_table_size = 2097152
explicit_defaults_for_timestamp = 1
read_buffer_size = 16M
read_rnd_buffer_size = 32M
query_cache_type = 1
query_cache_size = 2M
table_open_cache = 1500
table_definition_cache = 1000
thread_cache_size = 768
back_log = 3000
open_files_limit = 65536
skip-name-resolve
########log settings########
log-output=FILE
general_log = ON
general_log_file=/var/lib/mysql/general.log
slow_query_log = ON
slow_query_log_file=/var/lib/mysql/slowquery.log
long_query_time=10
#log-error=/var/lib/mysql/error.log
log_queries_not_using_indexes = OFF
log_throttle_queries_not_using_indexes = 0
#expire_logs_days = 120
min_examined_row_limit = 100
########innodb settings########
innodb_io_capacity = 4000
innodb_io_capacity_max = 8000
innodb_buffer_pool_size = 6144M
innodb_file_per_table = on
innodb_buffer_pool_instances = 20
innodb_buffer_pool_load_at_startup = 1
innodb_buffer_pool_dump_at_shutdown = 1
innodb_log_file_size = 300M
innodb_log_files_in_group = 2
innodb_log_buffer_size = 16M
innodb_undo_logs = 128
#innodb_undo_tablespaces = 3
#innodb_undo_log_truncate = 1
#innodb_max_undo_log_size = 2G
innodb_flush_method = O_DIRECT
innodb_flush_neighbors = 1
innodb_purge_threads = 4
innodb_large_prefix = 1
innodb_thread_concurrency = 64
innodb_print_all_deadlocks = 1
innodb_strict_mode = 1
innodb_sort_buffer_size = 64M
innodb_flush_log_at_trx_commit=1
innodb_autoextend_increment=64
innodb_concurrency_tickets=5000
innodb_old_blocks_time=1000
innodb_open_files=65536
innodb_stats_on_metadata=0
innodb_file_per_table=1
innodb_checksum_algorithm=0
#innodb_data_file_path=ibdata1:60M;ibdata2:60M;autoextend:max:1G
innodb_data_file_path = ibdata1:12M:autoextend
#innodb_temp_data_file_path = ibtmp1:500M:autoextend:max:20G
#innodb_buffer_pool_dump_pct = 40
#innodb_page_cleaners = 4
#innodb_purge_rseg_truncate_frequency = 128
binlog_gtid_simple_recovery=1
#log_timestamps=system
##############
delayed_insert_limit = 100
delayed_insert_timeout = 300
delayed_queue_size = 1000
delay_key_write = ON
disconnect_on_expired_password = ON
div_precision_increment = 4
end_markers_in_json = OFF
eq_range_index_dive_limit = 10
innodb_adaptive_flushing = ON
innodb_adaptive_hash_index = ON
innodb_adaptive_max_sleep_delay = 150000
#innodb_additional_mem_pool_size = 2097152
innodb_autoextend_increment = 64
innodb_autoinc_lock_mode = 1
```

- run.sh 启动脚本

```bash
docker run -d --name zhulin_mysql --restart=always -e MYSQL_ROOT_PASSWORD=你的密码  -p 3306:3306 -v /data/mysql/data:/var/lib/mysql zhulin_mysql:5.7 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
```

- 生成镜像

```bash
docker build -t mysql:5.7 .
```

- 启动镜像

```bash
bash run.sh
```

---

#### Docker 部署 NSQ

- 创建文件 docker-compose.yml

```yaml
version: "3"
services:
  nsqlookupd:
    image: nsqio/nsq
    command: /nsqlookupd
    ports:
      - "4160"
      - "4161"
  nsqd:
    image: nsqio/nsq
    command: /nsqd --lookupd-tcp-address=172.20.0.2:4160
    depends_on:
      - nsqlookupd
    ports:
      - "4150"
      - "4151"
  nsqadmin:
    image: nsqio/nsq
    command: /nsqadmin --lookupd-http-address=172.20.0.2:4161
    depends_on:
      - nsqlookupd
    ports:
      - "4171"
```

- 启动 NSQ(会生成三个容器 nsqd、lookupd、nsqadmin)

```bash
docker-compose up -d
```

---

#### Docker 部署 Kafka

- 下载 zookeeper 镜像

```
docker pull wurstmeister/zookeeper
```

- 启动镜像生成容器

```
docker run -d --name zookeeper -p 2181:2181 -v /etc/localtime:/etc/localtime wurstmeister/zookeeper
```

- 下载 kafka 镜像

```
docker pull wurstmeister/kafka
```

- 启动 kafka 镜像生成容器

```
docker run -d --name kafka -p 9092:9092 -e KAFKA_BROKER_ID=0 -e KAFKA_ZOOKEEPER_CONNECT=192.168.155.56:2181/kafka -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://192.168.155.56:9092 -e KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092 -v /etc/localtime:/etc/localtime wurstmeister/kafka

-e KAFKA_BROKER_ID=0  在kafka集群中，每个kafka都有一个BROKER_ID来区分自己

-e KAFKA_ZOOKEEPER_CONNECT=192.168.155.56:2181/kafka 配置zookeeper管理kafka的路径192.168.155.56:2181/kafka

-e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://192.168.155.56:9092  把kafka的地址端口注册给zookeeper

-e KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092 配置kafka的监听端口

-v /etc/localtime:/etc/localtime 容器时间同步虚拟机的时间
```

---

#### 数据库迁移

- 配合 sqlalchemy 的数据库迁移工具

```
pip install alembic
```

- 项目初始化文件夹, 用来配置迁移文件和存放迁移历史记录

```
alembic init alembic
```

- 配置你的数据库连接

```
sqlalchemy.url = driver://user:pass@localhost/dbname
```

- 修改 env.py 文件

```
target_metadata = None
```

```
import sys
from os.path import abspath, dirname

sys.path.append(dirname(dirname(abspath(__file__))))
# 注意这个地方是要引入模型里面的Base,不是connect里面的
from model import metadata
target_metadata = metadata
```

- 创建迁移文件

```
alembic revision --autogenerate -m "描述信息类似于git"
```

- 更新到最新的版本

```
alembic upgrade head
```

- 更多功能请查看官网
---
#### Docker部署ES
- 添加GPG: ```curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -```
- sudo apt upgrade
- sudo apt  install docker.io
- systemctl start docker
- systemctl status docker
- sudo apt autoremove
- sudo docker ps
- sudo docker pull elasticsearch:7.4.1
- sudo docker network create chr
- sudo docker run --name elasticsearch --net chr -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -d elasticsearch:7.4.1
- netstat -anpt