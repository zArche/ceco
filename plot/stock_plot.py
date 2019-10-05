# coding=utf8

import matplotlib.pyplot as plt
import sys

from configs import PROJECT_DIR
from data_source.tushare.stock import get_sh_last_12_month_stock_exponential_changes, \
    get_sz_last_12_month_stock_exponential_changes

reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append("..")

plt.rcParams['savefig.dpi'] = 150  # 图片像素 
plt.rcParams['figure.dpi'] = 150  # 分辨率

OUT_PUT_DIR = PROJECT_DIR + "/output/"


def draw_stock(sh_stock, sz_stock):
    x_sh = sh_stock[0]
    y_sh = sh_stock[1]

    x_sz = sz_stock[0]
    y_sz = sz_stock[1]

    plt.figure(figsize=(10, 5))  # 设置画布大小
    plt.title(u'股市指数涨幅')  # 标题
    plt.xlabel(u'时间')  # x坐标
    plt.ylabel(u'涨幅')  # y坐标

    # 这里设置线宽、线型、线条颜色、点大小等参数
    plt.plot(x_sh, y_sh, label=u'上证指数', linewidth=1, color='green', marker='o',
             markerfacecolor='blue', markersize=3)
    plt.plot(x_sz, y_sz, label=u'深证成指', linewidth=1, color='red', marker='o',
             markerfacecolor='orange',
             markersize=3)

    # 每个数据点加标签
    for a, b in zip(x_sh, y_sh):
        plt.text(a, b, "%.2f%%" % b, ha='center', va='bottom', fontsize=10)

    for a, b in zip(x_sz, y_sz):
        plt.text(a, b, "%.2f%%" % b, ha='center', va='bottom', fontsize=10)
    # 只给最后一个点加标签
    # plt.text(x[-1], y1[-1], ("%s%%" % y1[-1]), ha='center', va='bottom', fontsize=10)

    plt.legend(loc='upper left')

    plt.savefig(OUT_PUT_DIR + 'stock.png', bbox_inches='tight')  # bbox_inches去掉两边留白
    plt.show()


if __name__ == "__main__":
    sh = get_sh_last_12_month_stock_exponential_changes()

    sz = get_sz_last_12_month_stock_exponential_changes()

    draw_stock(sh, sz)
