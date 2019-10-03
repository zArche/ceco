# coding=utf-8

import sys

from data_source.stats_gov.cpi import get_last_13_month_cpi_m2m, get_last_13_month_cpi_y2y, \
    get_last_13_month_food_cpi_y2y
from utils.logger import *

reload(sys)
sys.path.append("..")
sys.setdefaultencoding('utf8')

ZB_CPI_M2M = "A01030101"  # cpi环比总指标
ZB_CPI_Y2Y = "A01010101"  # cpi同比总指标
ZB_FOOD_CPI_Y2Y = "A01010301"  # 食品类cpi同比总指标

THRESHOLD = 5  # 波动5%即预警

TAG = "cpi_monitor"


def print_dic(dic):
    for key in dic:
        print key, dic[key][0].percent


def print_couple(couple):
    for k, v in couple:
        print k, v[0].percent


def analyse(cpi, cpis):  # cpi指数大盘分析
    log_d(TAG, "%s处于%s期,单位货币购买物品量%s" % (cpi.sj_des, ("通胀" if cpi.inc else "通缩"),
                                        ("降低" if cpi.inc else "增加")))

    log_d(TAG, "---------------------------------------------")
    sorted_cpis = sorted(cpis.items(), key=lambda x: x[1][0].percent, reverse=True)

    _, largest_cpi = sorted_cpis[0]
    largest_cpi = largest_cpi[0]

    log_d(TAG, "其中：[%s] 行业 [%s] 幅度最大,幅度为[%.2f%%]" % (
        largest_cpi.zb_des.replace("居民消费价格指数", ""), ("上升" if largest_cpi.inc else "下降"),
        largest_cpi.percent))
    log_d(TAG, "---------------------------------------------")


def monitor(cpi, cpis):  # cpi指数异常预警

    if cpi.percent >= THRESHOLD:
        log_e(TAG, "%sCPI波动较大! [%s] 幅度为 [%.2f%%]" % (
            cpi.sj_des, ("上升" if cpi.inc else "下降"), cpi.percent))
    else:
        log_d(TAG, "%sCPI较为平稳" % cpi.sj_des)

    log_d(TAG, "---------------------------------------------")
    sorted_cpis = sorted(cpis.items(), key=lambda x: x[1][0].percent, reverse=True)

    warning_cpis = list()

    for k, v in sorted_cpis:
        if k == ZB_CPI_M2M or k == ZB_CPI_Y2Y or k == ZB_FOOD_CPI_Y2Y:
            continue

        sub_type_cpi = v[0]
        if v[0].percent >= THRESHOLD:
            log_e(TAG, "%s [%s] CPI波动较大! [%s] 幅度为 [%.2f%%]" % (
                sub_type_cpi.sj_des,
                sub_type_cpi.zb_des.replace("居民消费价格指数", ""),
                ("上升" if sub_type_cpi.inc else "下降"), sub_type_cpi.percent))

            warning_cpis.append(v)

    return warning_cpis


def analyse_m2m(last_13_month_cpi_m2m):  # 环比指数分析
    last_month_cpi_m2m = last_13_month_cpi_m2m[ZB_CPI_M2M][0]  # 最近一个月cpi
    analyse(last_month_cpi_m2m, last_13_month_cpi_m2m)


def monitor_m2m(last_13_month_cpi_m2m):  # 环比指数监控

    last_month_cpi_m2m = last_13_month_cpi_m2m[ZB_CPI_M2M][0]  # 最近一个月cpi

    return monitor(last_month_cpi_m2m, last_13_month_cpi_m2m)


def analyse_y2y(last_13_month_cpi_y2y):  # 同比指数分析
    last_month_cpi_y2y = last_13_month_cpi_y2y[ZB_CPI_Y2Y][0]  # 最近一个月cpi
    analyse(last_month_cpi_y2y, last_13_month_cpi_y2y)


def monitor_y2y(last_13_month_cpi_y2y):  # 同比指数监控

    last_month_cpi_y2y = last_13_month_cpi_y2y[ZB_CPI_Y2Y][0]  # 最近一个月cpi

    return monitor(last_month_cpi_y2y, last_13_month_cpi_y2y)


def analyse_food_y2y(last_13_month_food_cpi_y2y):  # 食品类同比指数分析
    last_month_food_cpi_y2y = last_13_month_food_cpi_y2y[ZB_FOOD_CPI_Y2Y][0]  # 最近一个月cpi
    analyse(last_month_food_cpi_y2y, last_13_month_food_cpi_y2y)


def monitor_food_y2y(last_13_month_food_cpi_y2y):  # 食品类同比指数监控

    last_month_food_cpi_y2y = last_13_month_food_cpi_y2y[ZB_FOOD_CPI_Y2Y][0]  # 最近一个月cpi

    return monitor(last_month_food_cpi_y2y, last_13_month_food_cpi_y2y)


if __name__ == "__main__":
    last_13_month_cpi_m2m = get_last_13_month_cpi_m2m()

    log_d(TAG, "=================CPI环比分析==================")
    analyse_m2m(last_13_month_cpi_m2m)
    log_d(TAG, "=============================================")
    log_d(TAG, "\n")

    log_d(TAG, "=================CPI环比监控===================")
    monitor_m2m(last_13_month_cpi_m2m)
    log_d(TAG, "=============================================")
    log_d(TAG, "\n")

    last_13_month_cpi_y2y = get_last_13_month_cpi_y2y()

    log_d(TAG, "=================CPI同比分析==================")
    analyse_y2y(last_13_month_cpi_y2y)
    log_d(TAG, "=============================================")
    log_d(TAG, "\n")

    log_d(TAG, "=================CPI同比监控===================")
    monitor_y2y(last_13_month_cpi_y2y)
    log_d(TAG, "=============================================")
    log_d(TAG, "\n")

    last_13_month_food_cpi_y2y = get_last_13_month_food_cpi_y2y()
    log_d(TAG, "===============食品类CPI同比分析================")
    analyse_food_y2y(last_13_month_food_cpi_y2y)
    log_d(TAG, "=============================================")
    log_d(TAG, "\n")

    log_d(TAG, "===============食品类CPI同比监控================")
    monitor_food_y2y(last_13_month_food_cpi_y2y)
    log_d(TAG, "=============================================")
    log_d(TAG, "\n")
