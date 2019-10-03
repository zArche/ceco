# coding=utf8

import matplotlib.pyplot as plt
import sys
import random

from data_source.stats_gov.cpi import get_last_13_month_cpi_m2m, get_last_13_month_cpi_y2y, \
    get_last_13_month_food_cpi_y2y

from monitor.cpi_monitor import monitor

reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append("..")

ZB_CPI_M2M = "A01030101"  # cpi环比总指标
ZB_CPI_Y2Y = "A01010101"  # cpi同比总指标
ZB_FOOD_CPI_Y2Y = "A01010301"  # 食品类cpi同比总指标

COLOR = ['red', 'green', 'blue', 'orange', 'brown', 'purple', 'pink', 'gray', 'olive', 'cyan']

plt.rcParams['savefig.dpi'] = 150  # 图片像素 
plt.rcParams['figure.dpi'] = 150  # 分辨率


def get_random_color():
    index = random.randint(0, len(COLOR) - 1)
    return COLOR[index]


def draw_normal_cpi(cpi_m2m_data, cpi_y2y_data):
    x_m2m = list()
    y_m2m = list()
    cpi_m2m_data = cpi_m2m_data[ZB_CPI_M2M] if cpi_m2m_data.has_key(ZB_CPI_M2M) else list()

    for cpi in cpi_m2m_data:
        x_m2m.append(cpi.sj)
        y_m2m.append(cpi.percent if cpi.inc else -cpi.percent)

    x_y2y = list()
    y_y2y = list()
    cpi_y2y_data = cpi_y2y_data[ZB_CPI_Y2Y] if cpi_y2y_data.has_key(ZB_CPI_Y2Y) else list()
    for cpi in cpi_y2y_data:
        x_y2y.append(cpi.sj)
        y_y2y.append(cpi.percent if cpi.inc else -cpi.percent)

    x_m2m.reverse()
    y_m2m.reverse()

    x_y2y.reverse()
    y_y2y.reverse()

    plt.figure(figsize=(10, 5))  # 设置画布大小
    plt.title(u'%s' % cpi_y2y_data[0].zb_des)  # 标题
    plt.xlabel(u'时间')  # x坐标
    plt.ylabel(u'涨幅')  # y坐标

    # 这里设置线宽、线型、线条颜色、点大小等参数
    plt.plot(x_m2m, y_m2m, label=u'环比上月', linewidth=1, color='green', marker='o',
             markerfacecolor='blue', markersize=3)
    plt.plot(x_y2y, y_y2y, label=u'同比去年同月', linewidth=1, color='red', marker='o',
             markerfacecolor='orange',
             markersize=3)

    # 每个数据点加标签
    for a, b in zip(x_m2m, y_m2m):
        plt.text(a, b, "%.2f%%" % b, ha='center', va='bottom', fontsize=10)

    for a, b in zip(x_y2y, y_y2y):
        plt.text(a, b, "%.2f%%" % b, ha='center', va='bottom', fontsize=10)
    # 只给最后一个点加标签
    # plt.text(x[-1], y1[-1], ("%s%%" % y1[-1]), ha='center', va='bottom', fontsize=10)

    plt.legend(loc='upper left')

    plt.savefig('/Users/arche/Workspace/Python/ceco/plot/normal_cpi.png', bbox_inches='tight')  # bbox_inches去掉两边留白
    plt.show()


def draw_food_cpi(cpi_food_y2y_data):
    x_y2y = list()
    y_y2y = list()
    cpi_y2y_data = cpi_food_y2y_data[ZB_FOOD_CPI_Y2Y]
    for cpi in cpi_y2y_data:
        x_y2y.append(cpi.sj)
        y_y2y.append(cpi.percent if cpi.inc else -cpi.percent)

    x_y2y.reverse()
    y_y2y.reverse()

    plt.figure(figsize=(10, 5))  # 设置画布大小
    plt.title(u'%s' % cpi_y2y_data[0].zb_des)  # 标题
    plt.xlabel(u'时间')  # x坐标
    plt.ylabel(u'涨幅')  # y坐标

    # 这里设置线宽、线型、线条颜色、点大小等参数
    plt.plot(x_y2y, y_y2y, label=u'同比去年同月', linewidth=1, color=get_random_color(), marker='o',
             markerfacecolor=get_random_color(),
             markersize=3)

    for a, b in zip(x_y2y, y_y2y):
        plt.text(a, b, "%.2f%%" % b, ha='center', va='bottom', fontsize=10)

    plt.legend(loc='upper left')

    plt.savefig('/Users/arche/Workspace/Python/ceco/plot/food_cpi.png', bbox_inches='tight')  # bbox_inches去掉两边留白
    plt.show()


def draw_warning_cpi(warning_cpis):
    if len(warning_cpis) == 0:
        return

    plt.figure(figsize=(10, 5))  # 设置画布大小
    plt.title(u'涨幅>=5%行业居民消费价格指数')  # 标题
    plt.xlabel(u'时间')  # x坐标
    plt.ylabel(u'涨幅')  # y坐标

    for cpis in warning_cpis:
        zb_des = cpis[0].zb_des.replace("居民消费价格指数", "")
        x = list()
        y = list()
        for cpi in cpis:
            x.append(cpi.sj)
            y.append(cpi.percent if cpi.inc else -cpi.percent)

        x.reverse()
        y.reverse()

        # 这里设置线宽、线型、线条颜色、点大小等参数
        plt.plot(x, y, label=u'%s(同比去年同月)' % zb_des, linewidth=1, color=get_random_color(), marker='o',
                 markerfacecolor=get_random_color(),
                 markersize=3)

        for a, b in zip(x, y):
            plt.text(a, b, "%.2f%%" % b, ha='center', va='bottom', fontsize=10)

    plt.legend(loc='upper left')

    plt.savefig('/Users/arche/Workspace/Python/ceco/plot/warning_cpi.png', bbox_inches='tight')  # bbox_inches去掉两边留白
    plt.show()


if __name__ == "__main__":
    cpi_m2m_data = get_last_13_month_cpi_m2m()
    cpi_y2y_data = get_last_13_month_cpi_y2y()
    cpi_food_y2y_data = get_last_13_month_food_cpi_y2y()

    draw_normal_cpi(cpi_m2m_data, cpi_y2y_data)
    draw_food_cpi(cpi_food_y2y_data)
    warning_cpis = monitor(cpi_food_y2y_data[ZB_FOOD_CPI_Y2Y][0], cpi_food_y2y_data)
    draw_warning_cpi(warning_cpis)
