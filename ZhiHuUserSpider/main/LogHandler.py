import logging
import sys


class LogHandler:

    logger = None

    @classmethod
    def create_logger(cls):
        log_format = logging.Formatter('%(levelname)s | %(asctime)s | %(message)s')
        file = logging.FileHandler('../file/log.txt', encoding='utf-8')
        file.setFormatter(log_format)
        file.setLevel(logging.DEBUG)
        console = logging.StreamHandler(sys.stdout)
        console.setFormatter(log_format)
        console.setLevel(logging.INFO)
        cls.logger = logging.getLogger('log')
        cls.logger.addHandler(console)
        cls.logger.addHandler(file)
        # 有一个默认的level,是warning不设置只能打印warning信息
        cls.logger.setLevel(logging.DEBUG)

    @classmethod
    def get_logger(cls):
        if not cls.logger:
            cls.create_logger()
        return cls.logger

if __name__ == '__main__':
    logger = LogHandler.get_logger()
    logger.debug('debug')
    logger.info('info')
    logger.warning('warning')
