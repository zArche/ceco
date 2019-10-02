# coding=utf-8

import requests
import json
import contants
import sys
import math

from utils.logger import *
from utils.timeutils import get_timestamp_of_now
from testdata import LAST_13_MONTH_CPI_M2M, LAST_13_MONTH_CPI_Y2Y, LAST_13_MONTH_FOOD_CPI_Y2Y
from configs import DEBUG

reload(sys)
sys.path.append("..")
sys.setdefaultencoding('utf8')

TAG = "CPI"

LAST_13_MONTH_CPI_KW = {
    "m": "QueryData",
    "dbcode": "hgyd",
    "rowcode": "zb",
    "colcode": "sj",
    "wds": "[]"
}

# 近13个月环比数据请求参数
LAST_13_MONTH_CPI_M2M_DFWDS = {
    "dfwds": '[{"wdcode": "sj", "valuecode": "LAST13"}]'
}

# 近13个月同比数据请求参数
LAST_13_MONTH_CPI_Y2Y_DFWDS = {
    "dfwds": '[{"wdcode":"zb","valuecode":"A010101"}]'
}

# 近13个月食品类同比数据请求参数
LAST_13_MONTH_CPI_FOOD_Y2Y_DFWDS = {
    "dfwds": '[{"wdcode":"zb","valuecode":"A010103"}]'
}

HEARDS = {
    "User-Agent": contants.USER_AGEN
}

last_13_month_cpi_m2m_kw = dict(LAST_13_MONTH_CPI_KW, **LAST_13_MONTH_CPI_M2M_DFWDS)

last_13_month_cpi_y2y_kw = dict(LAST_13_MONTH_CPI_KW, **LAST_13_MONTH_CPI_Y2Y_DFWDS)

last_13_month_food_cpi_y2y_kw = dict(LAST_13_MONTH_CPI_KW, **LAST_13_MONTH_CPI_FOOD_Y2Y_DFWDS)

test_data = LAST_13_MONTH_CPI_M2M


class CPI():
    def __init__(self, zb, sj, value, zb_des, sj_des):
        self.zb = zb  # 指标类型
        self.sj = sj  # 时间
        self.value = value  # cpi值
        self.zb_des = zb_des  # 指标详细描述
        self.sj_des = sj_des  # 时间描述
        self.inc = value >= 100  # 是增长还是下降
        self.percent = math.fabs(value - 100)  # 变化比例


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
        value = data["data"]["data"]
        if value <= 0:
            continue

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
                zb_des = zb_node["name"].replace("(上月=100)", "")  # 清洗数据
                break

        zb = zb_wd["valuecode"]
        sj = sj_wd["valuecode"]

        cpi = CPI(zb, sj, value, zb_des, sj_des)

        cpis.append(cpi)
    return cpis


def classify_cpi(cpis):  # 按cpi指标分类
    results = dict()
    for cpi in cpis:
        key = cpi.zb
        sub_type_cpis = results[key] if results.has_key(key) else list()
        sub_type_cpis.append(cpi)
        results[key] = sub_type_cpis
    return results


# 最近13个月数据
def get_last_13_month_cpi(last_13_month_cp_kw):
    result = None
    if DEBUG:
        json_str = test_data
        log_d(TAG, "Use the test cpi data")
    else:
        response = requests.get(contants.STATS_GOV_URL, params=last_13_month_cp_kw, headers=HEARDS)
        json_str = response.text

    json_obj = json.loads(json_str, strict=False)
    if json_obj["returncode"] == 200:
        log_d(TAG, "Query CPI data success!")
        result = parse_cpi(json_obj)
    else:
        log_e(TAG, "Query CPI data failed! Error code: " + str(json_obj["returncode"]))

    return result


# 最近13个月环比数据(每月增长率)
def get_last_13_month_cpi_m2m():
    global last_13_month_cpi_m2m_kw
    now = get_timestamp_of_now()
    last_13_month_cpi_m2m_kw["k1"] = now

    results = get_last_13_month_cpi(last_13_month_cpi_m2m_kw)
    return classify_cpi(results)


# 最近13个月同比数据(与去年同期相比)
def get_last_13_month_cpi_y2y():
    global last_13_month_cpi_y2y_kw
    now = get_timestamp_of_now()
    last_13_month_cpi_y2y_kw["k1"] = now
    results = get_last_13_month_cpi(last_13_month_cpi_y2y_kw)
    return classify_cpi(results)


# 最近13个月食品类同比数据(与去年同期相比)
def get_last_13_month_food_cpi_y2y():
    global last_13_month_food_cpi_y2y_kw
    now = get_timestamp_of_now()
    last_13_month_food_cpi_y2y_kw["k1"] = now
    results = get_last_13_month_cpi(last_13_month_food_cpi_y2y_kw)
    return classify_cpi(results)


def test_last_13_month_cpi_m2m():
    global test_data
    test_data = LAST_13_MONTH_CPI_M2M
    cpis = get_last_13_month_cpi_m2m()

    if DEBUG:
        for key in cpis:
            log_d(TAG, "-----------------------------------------")
            log_d(TAG, "类型:" + key)
            for cpi in cpis[key]:
                info = "%s%s:环比上个月 [%s] [%.2f%%] " % (cpi.sj_des,
                                                      cpi.zb_des.replace("居民消费价格指数", "CPI"),
                                                      ("增长" if cpi.inc else "降低"), cpi.percent)
                log_d(TAG, info)
            log_d(TAG, "-----------------------------------------")


def test_last_13_month_cpi_y2y():
    global test_data
    test_data = LAST_13_MONTH_CPI_Y2Y

    cpis = get_last_13_month_cpi_y2y()

    if DEBUG:
        for key in cpis:
            log_d(TAG, "-----------------------------------------")
            log_d(TAG, "类型:" + key)
            for cpi in cpis[key]:
                info = "%s%s:同比去年同月 [%s] [%.2f%%] " % (cpi.sj_des,
                                                       cpi.zb_des.replace("居民消费价格指数", "CPI"),
                                                       ("增长" if cpi.inc else "降低"), cpi.percent)
                log_d(TAG, info)
            log_d(TAG, "-----------------------------------------")


def test_last_13_month_food_cpi_y2y():
    global test_data
    test_data = LAST_13_MONTH_FOOD_CPI_Y2Y

    cpis = get_last_13_month_food_cpi_y2y()

    if DEBUG:
        for key in cpis:
            log_d(TAG, "-----------------------------------------")
            log_d(TAG, "类型:" + key)
            for cpi in cpis[key]:
                info = "%s%s:同比去年同月 [%s] [%.2f%%] " % (cpi.sj_des,
                                                       cpi.zb_des.replace("居民消费价格指数", "CPI"),
                                                       ("增长" if cpi.inc else "降低"), cpi.percent)
                log_d(TAG, info)
            log_d(TAG, "-----------------------------------------")


if __name__ == "__main__":
    test_last_13_month_cpi_m2m()
    # test_last_13_month_cpi_y2y()
    # test_last_13_month_food_cpi_y2y()
