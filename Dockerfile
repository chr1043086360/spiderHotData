FROM python:3.7

COPY ./test_oodata /app


RUN pip install -U pip
RUN pip config set global.index-url http://mirrors.aliyun.com/pypi/simple
RUN pip config set install.trusted-host mirrors.aliyun.com
RUN cd app\
&& pip install -r requirements.txt


CMD ["python","main.py","&"]