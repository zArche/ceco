import tushare as ts


def get_sh_last_12_month_stock_exponential_changes():
    df = ts.get_hist_data('sh', ktype='M')
    df = df[1:13]

    k = [i[0:7] for i in df['p_change'].index]
    v = [i for i in df['p_change'].values]

    k.reverse()
    v.reverse()
    return [k, v]


def get_sz_last_12_month_stock_exponential_changes():
    df = ts.get_hist_data('sz', ktype='M')
    df = df[1:13]

    k = [i[0:7] for i in df['p_change'].index]
    v = [i for i in df['p_change'].values]
    k.reverse()
    v.reverse()

    return [k, v]


if __name__ == "__main__":
    r = get_sz_last_12_month_stock_exponential_changes()

    print r[0]
    print r[1]
