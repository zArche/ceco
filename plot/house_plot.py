# coding=utf8

import matplotlib.pyplot as plt
import sys
import random

from configs import PROJECT_DIR
from data_source.anjuke.house import get_bj_last_12_month_house_price, \
    get_sh_last_12_month_house_price, get_sz_last_12_month_house_price

reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append("..")

plt.rcParams['savefig.dpi'] = 150  # 图片像素 
plt.rcParams['figure.dpi'] = 150  # 分辨率

OUT_PUT_DIR = PROJECT_DIR + "/output/"
COLOR = ['red', 'green', 'blue', 'orange', 'brown', 'purple', 'pink', 'gray', 'olive', 'cyan']


def get_random_color():
    index = random.randint(0, len(COLOR) - 1)
    return COLOR[index]


def draw_house_prices(prices):
    if len(prices) == 0:
        return

    plt.figure(figsize=(10, 5))  # 设置画布大小
    plt.title(u'北上深房价(单位:元)')  # 标题
    plt.xlabel(u'时间')  # x坐标
    plt.ylabel(u'价格')  # y坐标

    for city in prices:
        x = prices[city][0]
        y = prices[city][1]

        # 这里设置线宽、线型、线条颜色、点大小等参数
        plt.plot(x, y, label=u'%s' % city, linewidth=1, color=get_random_color(), marker='o',
                 markerfacecolor=get_random_color(),
                 markersize=3)

        for a, b in zip(x, y):
            plt.text(a, b, b, ha='center', va='bottom', fontsize=10)

    plt.legend(loc='upper left')

    plt.savefig(OUT_PUT_DIR + 'house_prices.png', bbox_inches='tight')  # bbox_inches去掉两边留白
    plt.show()


if __name__ == "__main__":
    bj = get_bj_last_12_month_house_price()
    sh = get_sh_last_12_month_house_price()
    sz = get_sz_last_12_month_house_price()

    prices = dict()
    prices["北京"] = bj
    prices["上海"] = sh
    prices["深圳"] = sz

    draw_house_prices(prices)
