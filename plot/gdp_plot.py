# coding=utf8

import matplotlib.pyplot as plt
import sys
import random

from data_source.stats_gov.gdp import get_last_12_quarter_gdp_y2y

from monitor.gdp_monitor import monitor
from configs import PROJECT_DIR

reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append("..")

ZB_GDP_Y2Y = "A010301"  # gdp当季同比总指标

COLOR = ['red', 'green', 'blue', 'orange', 'brown', 'purple', 'pink', 'gray', 'olive', 'cyan']

plt.rcParams['savefig.dpi'] = 150  # 图片像素 
plt.rcParams['figure.dpi'] = 150  # 分辨率

OUT_PUT_DIR = PROJECT_DIR + "/output/"


def get_random_color():
    index = random.randint(0, len(COLOR) - 1)
    return COLOR[index]


def draw_normal_gdp(gdp_y2y_data):
    x_y2y = list()
    y_y2y = list()
    gdp_y2y_data = gdp_y2y_data[ZB_GDP_Y2Y] if gdp_y2y_data.has_key(ZB_GDP_Y2Y) else list()
    for gdp in gdp_y2y_data:
        x_y2y.append(gdp.sj_des)
        y_y2y.append(gdp.percent if gdp.inc else -gdp.percent)

    x_y2y.reverse()
    y_y2y.reverse()

    plt.figure(figsize=(10, 5))  # 设置画布大小
    plt.title(u'%s' % gdp_y2y_data[0].zb_des)  # 标题
    plt.xlabel(u'时间')  # x坐标
    plt.ylabel(u'涨幅')  # y坐标

    # 这里设置线宽、线型、线条颜色、点大小等参数
    plt.plot(x_y2y, y_y2y, label=u'同比去年同期', linewidth=1, color='red', marker='o',
             markerfacecolor='orange',
             markersize=3)

    # 每个数据点加标签
    for a, b in zip(x_y2y, y_y2y):
        plt.text(a, b, "%.2f%%" % b, ha='center', va='bottom', fontsize=10)

    # plt.legend(loc='upper left')

    plt.savefig(OUT_PUT_DIR + 'normal_gdp.png', bbox_inches='tight')  # bbox_inches去掉两边留白
    plt.show()


def draw_warning_gdp(warning_gdps):
    if len(warning_gdps) == 0:
        return

    plt.figure(figsize=(10, 5))  # 设置画布大小
    plt.title(u'涨幅>=10%行业增加值指数')  # 标题
    plt.xlabel(u'时间')  # x坐标
    plt.ylabel(u'涨幅')  # y坐标

    for gdps in warning_gdps:
        zb_des = gdps[0].zb_des
        x = list()
        y = list()
        for gdp in gdps:
            x.append(gdp.sj_des)
            y.append(gdp.percent if gdp.inc else -gdp.percent)

        x.reverse()
        y.reverse()

        # 这里设置线宽、线型、线条颜色、点大小等参数
        plt.plot(x, y, label=u'%s' % zb_des, linewidth=1, color=get_random_color(), marker='o',
                 markerfacecolor=get_random_color(),
                 markersize=3)

        for a, b in zip(x, y):
            plt.text(a, b, "%.2f%%" % b, ha='center', va='bottom', fontsize=10)

    plt.legend(loc='upper left')

    plt.savefig(OUT_PUT_DIR + 'warning_gdp.png', bbox_inches='tight')  # bbox_inches去掉两边留白
    plt.show()


if __name__ == "__main__":
    gdp_y2y_data = get_last_12_quarter_gdp_y2y()

    draw_normal_gdp(gdp_y2y_data)
    warning_gdps = monitor(gdp_y2y_data[ZB_GDP_Y2Y][0], gdp_y2y_data)

    draw_warning_gdp(warning_gdps)
