# coding=utf-8

import sys

from utils.logger import *
from stats_gov.cpi import get_last_13_month_cpi_m2m, get_last_13_month_cpi_y2y, get_last_13_month_food_cpi_y2y

reload(sys)
sys.path.append("..")
sys.setdefaultencoding('utf8')

ZB_CPI_M2M = "A01030101"  # cpi环比总指标
ZB_CPI_Y2Y = "A01010101"  # cpi同比总指标
ZB_FOOD_CPI_Y2Y = "A01010301"  # cpi同比总指标

THRESHOLD = 5  # 波动5%即预警

TAG = "cpi_monitor"


def print_dic(dic):
    for key in dic:
        print key, dic[key][0].percent


def print_couple(couple):
    for k, v in couple:
        print k, v[0].percent


def analyse_m2m(last_13_month_cpi_m2m):  # 环比指数分析
    last_month_cpi_m2m = last_13_month_cpi_m2m[ZB_CPI_M2M][0]  # 最近一个月cpi
    log_d(TAG, "%s处于%s期,单位货币购买物品量%s" % (last_month_cpi_m2m.sj_des, ("通胀" if last_month_cpi_m2m.inc else "通缩"),
                                        ("降低" if last_month_cpi_m2m.inc else "增加")))

    log_d(TAG, "---------------------------------------------")
    sorted_last_month_cpi_m2m = sorted(last_13_month_cpi_m2m.items(), key=lambda x: x[1][0].percent, reverse=True)

    _, largest_cpi_m2m = sorted_last_month_cpi_m2m[0]
    largest_cpi_m2m = largest_cpi_m2m[0]
    log_d(TAG, "其中：[%s] 行业 [%s] 幅度最大,幅度为[%.2f%%]" % (
        largest_cpi_m2m.zb_des.replace("居民消费价格指数", ""), ("上升" if largest_cpi_m2m.inc else "下降"),
        largest_cpi_m2m.percent))
    log_d(TAG, "---------------------------------------------")


def monitor_m2m(last_13_month_cpi_m2m):  # 环比指数监控

    last_month_cpi_m2m = last_13_month_cpi_m2m[ZB_CPI_M2M][0]  # 最近一个月cpi

    # 最近一个月cpi环比波动监控
    if last_month_cpi_m2m.percent >= THRESHOLD:
        log_e(TAG, "%sCPI环比上月波动较大! [%s] 幅度为 [%.2f%%]" % (
            last_month_cpi_m2m.sj_des, ("上升" if last_month_cpi_m2m.inc else "下降"), last_month_cpi_m2m.percent))
    else:
        log_d(TAG, "%s整体CPI环比上月较为平稳" % last_month_cpi_m2m.sj_des)

    sorted_last_month_cpi_m2m = sorted(last_13_month_cpi_m2m.items(), key=lambda x: x[1][0].percent, reverse=True)

    warning_cpis = list()

    for k, v in sorted_last_month_cpi_m2m:
        if k == ZB_CPI_M2M:
            continue

        last_month_sub_type_cpi_m2m = v[0]
        if v[0].percent >= THRESHOLD:
            log_e(TAG, "%s%sCPI环比上月波动较大! [%s] 幅度为 [%.2f%%]" % (
                last_month_sub_type_cpi_m2m.sj_des,
                last_month_sub_type_cpi_m2m.zb_des,
                ("上升" if last_month_sub_type_cpi_m2m.inc else "下降"), last_month_sub_type_cpi_m2m.percent))

            warning_cpis.append(v)

    return warning_cpis


def analyse_y2y(last_13_month_cpi_y2y):  # 同比指数分析
    last_month_cpi_y2y = last_13_month_cpi_y2y[ZB_CPI_Y2Y][0]  # 最近一个月cpi
    log_d(TAG, "%s处于%s期,单位货币购买物品量%s" % (last_month_cpi_y2y.sj_des, ("通胀" if last_month_cpi_y2y.inc else "通缩"),
                                        ("降低" if last_month_cpi_y2y.inc else "增加")))

    log_d(TAG, "---------------------------------------------")
    sorted_last_month_cpi_y2y = sorted(last_13_month_cpi_y2y.items(), key=lambda x: x[1][0].percent, reverse=True)

    _, largest_cpi_y2y = sorted_last_month_cpi_y2y[0]
    largest_cpi_y2y = largest_cpi_y2y[0]
    log_d(TAG, "其中：[%s] 行业 [%s] 幅度最大,幅度为[%.2f%%]" % (
        largest_cpi_y2y.zb_des.replace("居民消费价格指数", ""), ("上升" if largest_cpi_y2y.inc else "下降"),
        largest_cpi_y2y.percent))
    log_d(TAG, "---------------------------------------------")


def monitor_y2y(last_13_month_cpi_y2y):  # 同比指数监控

    last_month_cpi_y2y = last_13_month_cpi_y2y[ZB_CPI_Y2Y][0]  # 最近一个月cpi

    # 最近一个月cpi环比波动监控
    if last_month_cpi_y2y.percent >= THRESHOLD:
        log_e(TAG, "%sCPI同比去年同月波动较大! [%s] 幅度为 [%.2f%%]" % (
            last_month_cpi_y2y.sj_des, ("上升" if last_month_cpi_y2y.inc else "下降"), last_month_cpi_y2y.percent))
    else:
        log_d(TAG, "%s整体CPI同比去年同月较为平稳" % last_month_cpi_y2y.sj_des)

    sorted_last_month_cpi_y2y = sorted(last_13_month_cpi_y2y.items(), key=lambda x: x[1][0].percent, reverse=True)

    warning_cpis = list()

    for k, v in sorted_last_month_cpi_y2y:
        if k == ZB_CPI_Y2Y:
            continue

        last_month_sub_type_cpi_y2y = v[0]
        if v[0].percent >= THRESHOLD:
            log_e(TAG, "%s%sCPI同比去年同月波动较大! [%s] 幅度为 [%.2f%%]" % (
                last_month_sub_type_cpi_y2y.sj_des,
                last_month_sub_type_cpi_y2y.zb_des.replace("居民消费价格指数", ""),
                ("上升" if last_month_sub_type_cpi_y2y.inc else "下降"), last_month_sub_type_cpi_y2y.percent))

            warning_cpis.append(v)

    return warning_cpis


def analyse_food_y2y(last_13_month_food_cpi_y2y):  # 食品类同比指数分析
    last_month_food_cpi_y2y = last_13_month_food_cpi_y2y[ZB_FOOD_CPI_Y2Y][0]  # 最近一个月cpi
    log_d(TAG, "%s处于%s期,单位货币购买物品量%s" % (last_month_food_cpi_y2y.sj_des, ("通胀" if last_month_food_cpi_y2y.inc else "通缩"),
                                        ("降低" if last_month_food_cpi_y2y.inc else "增加")))

    log_d(TAG, "---------------------------------------------")
    sorted_last_month_food_cpi_y2y = sorted(last_13_month_food_cpi_y2y.items(), key=lambda x: x[1][0].percent,
                                            reverse=True)

    _, largest_food_cpi_y2y = sorted_last_month_food_cpi_y2y[0]
    largest_food_cpi_y2y = largest_food_cpi_y2y[0]
    log_d(TAG, "其中：[%s] 行业 [%s] 幅度最大,幅度为[%.2f%%]" % (
        largest_food_cpi_y2y.zb_des.replace("居民消费价格指数", ""), ("上升" if largest_food_cpi_y2y.inc else "下降"),
        largest_food_cpi_y2y.percent))
    log_d(TAG, "---------------------------------------------")


def monitor_food_y2y(last_13_month_food_cpi_y2y):  # 食品类同比指数监控

    last_month_food_cpi_y2y = last_13_month_food_cpi_y2y[ZB_FOOD_CPI_Y2Y][0]  # 最近一个月cpi

    # 最近一个月cpi环比波动监控
    if last_month_food_cpi_y2y.percent >= THRESHOLD:
        log_e(TAG, "%sCPI同比去年同月波动较大! [%s] 幅度为 [%.2f%%]" % (
            last_month_food_cpi_y2y.sj_des, ("上升" if last_month_food_cpi_y2y.inc else "下降"),
            last_month_food_cpi_y2y.percent))
    else:
        log_d(TAG, "%s整体CPI同比去年同月较为平稳" % last_month_food_cpi_y2y.sj_des)

    sorted_last_month_food_cpi_y2y = sorted(last_13_month_food_cpi_y2y.items(), key=lambda x: x[1][0].percent,
                                            reverse=True)

    warning_cpis = list()

    for k, v in sorted_last_month_food_cpi_y2y:
        if k == ZB_FOOD_CPI_Y2Y:
            continue

        last_month_sub_food_type_cpi_y2y = v[0]
        if v[0].percent >= THRESHOLD:
            log_e(TAG, "%s%sCPI同比去年同月波动较大! [%s] 幅度为 [%.2f%%]" % (
                last_month_sub_food_type_cpi_y2y.sj_des,
                last_month_sub_food_type_cpi_y2y.zb_des.replace("居民消费价格指数", ""),
                ("上升" if last_month_sub_food_type_cpi_y2y.inc else "下降"), last_month_sub_food_type_cpi_y2y.percent))

            warning_cpis.append(v)

    return warning_cpis


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
