# coding=utf-8

import sys

from data_source.stats_gov.gdp import get_last_12_quarter_gdp_y2y
from utils.logger import *

reload(sys)
sys.path.append("..")
sys.setdefaultencoding('utf8')

ZB_GDP_Y2Y = "A010301"  # gdp当季同比总指标

THRESHOLD = 10  # 波动5%即预警

TAG = "gdp_monitor"


def print_dic(dic):
    for key in dic:
        print key, dic[key][0].percent


def print_couple(couple):
    for k, v in couple:
        print k, v[0].percent


def analyse(gdps):  # gdp指数大盘分析

    log_d(TAG, "---------------------------------------------")
    sorted_gdps = sorted(gdps.items(), key=lambda x: x[1][0].percent, reverse=True)

    _, largest_gdp = sorted_gdps[0]
    largest_gdp = largest_gdp[0]

    log_d(TAG, "其中：[%s] 行业 [%s] 幅度最大,幅度为[%.2f%%]" % (
        largest_gdp.zb_des.replace("居民消费价格指数", ""), ("上升" if largest_gdp.inc else "下降"),
        largest_gdp.percent))
    log_d(TAG, "---------------------------------------------")


def monitor(gdp, gdps):  # cpi指数异常预警

    if gdp.percent >= THRESHOLD:
        log_e(TAG, "%s增加值指数波动较大! [%s] 幅度为 [%.2f%%]" % (
            gdp.sj_des, ("上升" if gdp.inc else "下降"), gdp.percent))
    else:
        log_d(TAG, "%s增加值指数较为平稳" % gdp.sj_des)

    log_d(TAG, "---------------------------------------------")
    sorted_gdps = sorted(gdps.items(), key=lambda x: x[1][0].percent, reverse=True)

    warning_gdps = list()

    for k, v in sorted_gdps:
        if k == ZB_GDP_Y2Y:
            continue

        sub_type_gdp = v[0]
        if sub_type_gdp.zb_des.find("_累计值") > 0:
            continue

        if v[0].percent >= THRESHOLD:
            log_e(TAG, "%s [%s] 波动较大! [%s] 幅度为 [%.2f%%]" % (
                sub_type_gdp.sj_des,
                sub_type_gdp.zb_des.replace("(上年同期=100)_当季值", ""),
                ("上升" if sub_type_gdp.inc else "下降"), sub_type_gdp.percent))

            warning_gdps.append(v)

    return warning_gdps


def monitor_y2y(last_12_quarter_gdp_y2y):  # 同比指数监控

    last_quarter_gdp_y2y = last_12_quarter_gdp_y2y[ZB_GDP_Y2Y][0]  # 最近一个月cpi

    return monitor(last_quarter_gdp_y2y, last_12_quarter_gdp_y2y)


if __name__ == "__main__":
    last_12_quarter_gdp_y2y = get_last_12_quarter_gdp_y2y()

    log_d(TAG, "=================GDP同比监控===================")
    monitor_y2y(last_12_quarter_gdp_y2y)
    log_d(TAG, "=============================================")
    log_d(TAG, "\n")
