import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('')
handler = RotatingFileHandler('spider.log', maxBytes=100 * 1024 * 1024, backupCount=10)
formatter = logging.Formatter('%(asctime)-12s [%(name)s] [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


