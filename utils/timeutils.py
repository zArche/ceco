# coding=utf-8

import time, datetime

CURRENT_MONTH_WITH_YEAR_FORMAT = "%Y%m"
CURRENT_FORMAT_TIME = "%m-%d %H:%M:%S.%f"

# 获取当前时间戳
def get_timestamp_of_now():
    return int(round(time.time() * 1000))


# 获取带年份的当前月
def get_current_month_with_year():
    return time.strftime(CURRENT_MONTH_WITH_YEAR_FORMAT, time.localtime())


# 获取当前年份
def get_current_year():
    return datetime.datetime.now().year


# 获取当前月份
def get_current_month():
    return datetime.datetime.now().month


# 获取当前日
def get_current_day():
    return datetime.datetime.now().day


# 获取当前格式化时间
def get_current_format_time():
    return datetime.datetime.now().strftime(CURRENT_FORMAT_TIME)


if __name__ == "__main__":
    print get_current_format_time()