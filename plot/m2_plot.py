# coding=utf8

import matplotlib.pyplot as plt
import sys

from configs import PROJECT_DIR
from data_source.tushare.m2 import get_last_12_month_m2_changes

reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append("..")

plt.rcParams['savefig.dpi'] = 150  # 图片像素 
plt.rcParams['figure.dpi'] = 150  # 分辨率

OUT_PUT_DIR = PROJECT_DIR + "/output/"


def draw_m2(m2):
    x = m2[0]
    y = m2[1]

    plt.figure(figsize=(10, 5))  # 设置画布大小
    plt.title(u'广义货币增长幅度')  # 标题
    plt.xlabel(u'时间')  # x坐标
    plt.ylabel(u'涨幅')  # y坐标

    # 这里设置线宽、线型、线条颜色、点大小等参数
    plt.plot(x, y, label=u'M2同比增长幅度', linewidth=1, color='green', marker='o',
             markerfacecolor='blue', markersize=3)

    for a, b in zip(x, y):
        plt.text(a, b, "%.2f%%" % b, ha='center', va='bottom', fontsize=10)
    # 只给最后一个点加标签
    # plt.text(x[-1], y1[-1], ("%s%%" % y1[-1]), ha='center', va='bottom', fontsize=10)

    plt.legend(loc='upper left')

    plt.savefig(OUT_PUT_DIR + 'm2.png', bbox_inches='tight')  # bbox_inches去掉两边留白
    plt.show()


if __name__ == "__main__":
    m2 = get_last_12_month_m2_changes()

    draw_m2(m2)
