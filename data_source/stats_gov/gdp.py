# coding=utf-8

import json
import math
import sys

import requests

import contants
from testdata import LAST_12_QUARTER_GDP_Y2Y
from utils.logger import *
from data_source.cache_controller import *
from configs import DEBUG

reload(sys)
sys.path.append("..")
sys.setdefaultencoding('utf8')

TAG = "GDP"

last_12_quarter_gdp_y2y_kw = {
    "m": "QueryData",
    "dbcode": "hgjd",
    "rowcode": "zb",
    "colcode": "sj",
    "wds": "[]",
    "dfwds": '[{"wdcode":"zb","valuecode":"A0103"}]',
    "h": 1
}

HEARDS = {
    "User-Agent": contants.USER_AGEN
}


class GDP():
    def __init__(self, zb, sj, value, zb_des, sj_des):
        self.zb = zb  # 指标类型
        self.sj = sj  # 时间
        self.value = value  # gdp值
        self.zb_des = zb_des  # 指标详细描述
        self.sj_des = sj_des  # 时间描述
        self.inc = value >= 100  # 是增长还是下降
        self.percent = math.fabs(value - 100)  # 变化比例


# 最近12个季度同比数据(与去年同期相比)
def get_last_12_quarter_gdp(tag, last_12_quarter_gdp_y2y_kw):
    result = None
    if DEBUG:
        json_str = LAST_12_QUARTER_GDP_Y2Y
        log_d(TAG, "Use the test gdp data")
    elif not is_cache_invalid(tag):
        json_str = get_cache(tag)
        log_d(TAG, "Use the cache gdp data")
    else:
        response = requests.get(contants.STATS_GOV_URL, params=last_12_quarter_gdp_y2y_kw, headers=HEARDS)
        json_str = response.text
        log_d(TAG, "URL:" + response.url)
        log_d(TAG, "Response code:" + str(response.status_code))

    try:
        json_obj = json.loads(json_str, strict=False)
        if json_obj["returncode"] == 200:
            log_d(TAG, "Query GDP data success!")
            save_cache(tag, json_str)
            result = parse_gdp(json_obj)
        else:
            log_e(TAG, "Query GDP data failed! Error code: " + str(json_obj["returncode"]))
    except Exception, e:
        log_e(TAG, str(e))

    return result


def parse_gdp(json_obj):  # cpi解析
    gdps = list()
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
                zb_des = zb_des.replace("(上年同月=100)", "")
                break

        zb = zb_wd["valuecode"]
        sj = sj_wd["valuecode"]

        gdp = GDP(zb, sj, value, zb_des, sj_des)

        gdps.append(gdp)
    return gdps


def classify_gdp(gdps):  # 按cpi指标分类
    results = dict()
    if gdps is not None and len(gdps) > 0:
        for gdp in gdps:
            key = gdp.zb
            sub_type_gdps = results[key] if results.has_key(key) else list()
            sub_type_gdps.append(gdp)
            results[key] = sub_type_gdps
    return results


def get_last_12_quarter_gdp_y2y():
    global last_12_quarter_gdp_y2y_kw
    now = get_timestamp_of_now()
    last_12_quarter_gdp_y2y_kw["k1"] = now

    results = get_last_12_quarter_gdp("gdp", last_12_quarter_gdp_y2y_kw)
    return classify_gdp(results)


def test_last_12_quarter_gdp_y2y():
    gdps = get_last_12_quarter_gdp_y2y()

    for key in gdps:
        log_d(TAG, "-----------------------------------------")
        log_d(TAG, "类型:" + key)
        for gdp in gdps[key]:
            info = "%s%s:同比去年同月 [%s] [%.2f%%] " % (gdp.sj_des,
                                                   gdp.zb_des,
                                                   ("增长" if gdp.inc else "降低"), gdp.percent)
            log_d(TAG, info)
        log_d(TAG, "-----------------------------------------")


if __name__ == "__main__":
    test_last_12_quarter_gdp_y2y()
