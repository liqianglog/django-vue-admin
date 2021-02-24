import logging
from django.core.cache import cache


class RedisHandler(logging.StreamHandler):

    def emit(self, record):
        msg = self.format(record)
        print(msg)

