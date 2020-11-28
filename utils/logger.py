import logging
from os.path import dirname, abspath, join


LOGPATH = join(dirname(dirname(abspath(__file__))), "log.log")

def get_logger():
    # package name
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s: %(message)s')
    logger.setLevel(logging.ERROR)

    # for stdout
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.ERROR)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # for file write
    file_handler = logging.FileHandler(LOGPATH)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger    