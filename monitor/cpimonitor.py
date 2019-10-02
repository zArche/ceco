# coding=utf-8

import sys

from utils.logger import *
from stats_gov.cpi import get_last_13_month_cpi_m2m, get_last_13_month_cpi_y2y, get_last_13_month_food_cpi_y2y

reload(sys)
sys.path.append("..")
sys.setdefaultencoding('utf8')

ZB_CPI_M2M = "A01030101"  # cpi环比总指标

THRESHOLD = 5  # 波动5%即预警

TAG = "cpi_monitor"


def print_dic(dic):
    for key in dic:
        print key, dic[key][0].percent


def monitor_m2m():  # 环比指数监控
    last_13_month_cpi_m2m = get_last_13_month_cpi_m2m()

    last_month_cpi_m2m_percent = last_13_month_cpi_m2m[ZB_CPI_M2M][0].percent  # 最近整体环比大盘波动幅度

    # 整体环比大盘指数
    # log_d(TAG, "整体环比大盘波动: " + str(last_month_cpi_m2m_percent))
    if last_month_cpi_m2m_percent >= THRESHOLD:
        log_e(TAG, "整体环比大盘波动较大，建议多加关注")
    else:
        log_d(TAG, "整体环比大盘较为平稳")

    print "before"
    print_dic(last_13_month_cpi_m2m)
    sorted(last_13_month_cpi_m2m.items(), key=lambda x: x[1][0].percent)
    print "after"
    print_dic(last_13_month_cpi_m2m)

    warning_cpis = list()

    for key in last_13_month_cpi_m2m:
        print key


if __name__ == "__main__":
    monitor_m2m()
