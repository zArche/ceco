import tushare as ts


def get_last_12_month_m2_changes():
    df = ts.get_money_supply()
    df = df[0:12]

    k = [i for i in df['month']]
    v = [float(i) for i in df['m2_yoy']]
    k.reverse()
    v.reverse()

    return [k, v]


if __name__ == "__main__":
    r = get_last_12_month_m2_changes()

    print r[0]
    print r[1]
