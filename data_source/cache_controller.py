# coding=utf-8

from utils.time_utils import get_timestamp_of_now
from configs import PROJECT_DIR

CACHE_EFFECTIVE_TIME = 60 * 60 * 1000  # 缓存数据有效时长

CACHE_FLAG_FILE_NAME = "cache_flag"
CACHE_FILE_NAME = "cache"

CACHE_DIR = PROJECT_DIR + "/cache/"


def save_cache(tag, cache):
    with open(CACHE_DIR + tag + CACHE_FILE_NAME, "wb") as fout, open(CACHE_DIR + tag + CACHE_FLAG_FILE_NAME,
                                                                     "wb") as fout2:
        fout.write(cache)
        fout2.write(str(get_timestamp_of_now()))


def get_cache(tag):
    with open(CACHE_DIR + tag + CACHE_FILE_NAME, "rb") as fin:
        cache = fin.read()
    return cache


def is_cache_invalid(tag):
    try:
        with open(CACHE_DIR + tag + CACHE_FLAG_FILE_NAME, "rb") as fin:
            last_cache_time = fin.read()

        last_cache_time = 0 if len(last_cache_time) == 0 else long(last_cache_time)
        now = get_timestamp_of_now()
        return now - last_cache_time >= CACHE_EFFECTIVE_TIME
    except:
        return True
