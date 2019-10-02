# coding=utf-8

import requests
import json
import contants
import sys
import math

from utils.logger import *
from utils.timeutils import get_timestamp_of_now
from testdata import LAST_13_MONTH_CPI_M2M
from configs import DEBUG

reload(sys)
sys.path.append("..")
sys.setdefaultencoding('utf8')

TAG = "CPI"

last_13_month_cpi_m2m_kw = {
    "m": "QueryData",
    "dbcode": "hgyd",
    "rowcode": "zb",
    "colcode": "sj",
    "wds": "[]",
    "dfwds": '[{"wdcode": "sj", "valuecode": "LAST13"}]'}

HEARDS = {
    "User-Agent": contants.USER_AGEN
}


class CPI():
    def __init__(self, code="", percent="", des="", inc=True):
        self.code = code
        self.percent = percent
        self.des = des
        self.inc = inc


# 最近13个月环比数据(每月增长率)
def get_last_13_month_cpi_m2m():
    global last_13_month_cpi_m2m_kw

    now = get_timestamp_of_now()
    last_13_month_cpi_m2m_kw["k1"] = now
    result = None

    if DEBUG:
        json_str = LAST_13_MONTH_CPI_M2M
        log_d(TAG, "Use the test cpi data")
    else:
        response = requests.get(contants.STATS_GOV_URL, params=last_13_month_cpi_m2m_kw, headers=HEARDS)
        json_str = response.text

    json_obj = json.loads(json_str, strict=False)
    if json_obj["returncode"] == 200:
        log_d(TAG, "Query CPI data success!")
        result = parse_cpi(json_obj)
    else:
        log_e(TAG, "Query CPI data failed! Error code: " + str(json_obj["returncode"]))

    return result


def parse_cpi(json_obj):  # cpi解析
    cpis = list()
    returndata = json_obj["returndata"]
    datanodes = returndata["datanodes"]

    wdnodes = returndata["wdnodes"]

    for nodes in wdnodes:  # 时间和指标中文描述分类
        if nodes["wdcode"] == "zb":  # 指标描述
            zb_nodes = nodes
        if nodes["wdcode"] == "sj":  # 时间描述
            sj_nodes = nodes

    for data in datanodes:
        # log_d(TAG, "cpi info:" + str(data))
        cpi = CPI()
        value = data["data"]["data"]
        if value <= 0:
            continue
        # cpi.value = (int(math.fabs(cpi.value - 100) * 100) / 100.0)
        cpi.inc = value >= 100
        cpi.percent = math.fabs(value - 100)

        for wd in data["wds"]:  # 该项纪录时间与指标编码
            if wd["wdcode"] == "sj":
                sj_wd = wd
            if wd["wdcode"] == "zb":
                zb_wd = wd

        for sj_node in sj_nodes["nodes"]:  # 获取该项纪录时间描述
            if sj_wd["valuecode"] == sj_node["code"]:
                sj_des = sj_node["name"]
                break
        for zb_node in zb_nodes["nodes"]:  # 获取该项纪录指标描述
            if zb_wd["valuecode"] == zb_node["code"]:
                zb_des = zb_node["name"]
                break
        des = sj_des + zb_des
        cpi.des = des.replace("(上月=100)", "")
        cpi.code = zb_wd["valuecode"]
        cpis.append(cpi)
    return cpis


def classify_cpi(cpis):  # cpi分类
    results = dict()

    for cpi in cpis:
        sub_type_cpis = results[cpi.code] if results.has_key(cpi.code) else list()
        sub_type_cpis.append(cpi)
        results[cpi.code] = sub_type_cpis
    return results


# 最近13个月同比数据(与去年同期相比)
def get_last_13_month_cpi_y2y():
    pass


if __name__ == "__main__":
    cpis = get_last_13_month_cpi_m2m()

    # if DEBUG:
    #     for cpi in cpis:
    #         info = "%s:环比上个月 [%s] [%.2f%%] " % (
    #             cpi.des.replace("居民消费价格指数", "CPI"), ("增长" if cpi.inc else "降低"), cpi.percent)
    #         log_d(TAG, info)

    cpis = classify_cpi(cpis)

    sub_type_cpis = dict()
    if DEBUG:
        log_d(TAG,"===========================================")
        for key in cpis:
            log_d(TAG, "类型:" + key)
            for cpi in cpis[key]:
                info = "%s:环比上个月 [%s] [%.2f%%] " % (
                    cpi.des.replace("居民消费价格指数", "CPI"), ("增长" if cpi.inc else "降低"), cpi.percent)
                log_d(TAG, info)
        log_d(TAG, "===========================================")