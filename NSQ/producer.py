import nsq
import tornado.ioloop
import time
import pickle
from core.settings import NSQ_HOST_IP_PORT


class NSQ:
    
    def __init__(self, data):
        self.data = pickle.dumps(data)
        self.writer = nsq.Writer([f'{NSQ_HOST_IP_PORT}'])

    def send(self):
        tornado.ioloop.PeriodicCallback(
            self._pub_message,500).start()
        nsq.run()

    def _pub_message(self):
        self.writer.pub('spider', self.data, self._finish_pub)

    @staticmethod
    def _finish_pub(onn, res_data):
        print(res_data)
