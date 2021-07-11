import logging


class RedisHandler(logging.StreamHandler):

    def emit(self, record):
        msg = self.format(record)
        print(msg)
