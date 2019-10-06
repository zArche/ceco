# coding=utf8

import matplotlib.pyplot as plt
import sys
import random

from data_source.stats_gov.house_invest import get_last_12_month_house_invest_y2y

from monitor.gdp_monitor import monitor
from configs import PROJECT_DIR

reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append("..")

ZB_TOTAL_HOUSE_INVEST = "A060102"  # 房地产投资累积增长

COLOR = ['red', 'green', 'blue', 'orange', 'brown', 'purple', 'pink', 'gray', 'olive', 'cyan']

plt.rcParams['savefig.dpi'] = 150  # 图片像素 
plt.rcParams['figure.dpi'] = 150  # 分辨率

OUT_PUT_DIR = PROJECT_DIR + "/output/"


def get_random_color():
    index = random.randint(0, len(COLOR) - 1)
    return COLOR[index]


def draw_house_invest(house_invests):
    x = list()
    y = list()
    house_invests = house_invests[ZB_TOTAL_HOUSE_INVEST] if house_invests.has_key(ZB_TOTAL_HOUSE_INVEST) else list()
    for house_invest in house_invests:
        x.append(house_invest.sj_des)
        y.append(house_invest.value)

    x.reverse()
    y.reverse()

    plt.figure(figsize=(10, 5))  # 设置画布大小
    plt.title(u'房地产投资累计增长')  # 标题
    plt.xlabel(u'时间')  # x坐标
    plt.ylabel(u'涨幅')  # y坐标

    # 这里设置线宽、线型、线条颜色、点大小等参数
    plt.plot(x, y, label=u'%s' % house_invests[0].zb_des,
             linewidth=1, color='red', marker='o',
             markerfacecolor='orange',
             markersize=3)

    # 每个数据点加标签
    for a, b in zip(x, y):
        plt.text(a, b, "%.2f%%" % b, ha='center', va='bottom', fontsize=10)

    plt.legend(loc='upper left')

    plt.savefig(OUT_PUT_DIR + 'house_invest.png', bbox_inches='tight')  # bbox_inches去掉两边留白
    plt.show()


if __name__ == "__main__":
    house_invest = get_last_12_month_house_invest_y2y()

    draw_house_invest(house_invest)
