from my_utils import SHlogger


logger = SHlogger('aaaaa').logger


def run():
    logger.debug('1111111')
    logger.info('1111111')
    logger.warning('1111111')


run()
