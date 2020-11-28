import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame

def cleaning(t_df, c_df):
    c_df = c_df.loc[:, ~c_df.columns.str.contains('^Unnamed')]
    t_df = t_df.loc[:, ~t_df.columns.str.contains('^Unnamed')]
    if not c_df.dtypes.equals(t_df.dtypes):
        raise ValueError('두 데이터의 타입이 다르다')
    elif not all(c_df.columns.__eq__(t_df.columns)):
        raise ValueError('두 데이터의 컬럼이 다르다')
    else:
        return c_df, t_df

def get_stat_by_order(t_df, c_df):
    t_order = t_df.groupby('address').sum('payment').sort_index()
    c_order = c_df.groupby('address').sum('payment').sort_index()

    for df in (t_order, c_order):
        if 'campaign_id' in df.columns:
            df = df.drop('campaign_id', axis=1)

    t_order['profit'] = t_order.payment - c_order.payment
    t_order['profit_p'] = t_order.profit / c_order.payment * 100
    t_order['compare_payment'] = c_order.payment
    t_order['benefit'] = t_order.payment / 88000
    t_order = t_order[['payment', 'benefit', 'compare_payment', 'profit', 'profit_p']]
    return t_order

def get_stat_by_campaign_id(t_df, c_df, adv_info):
    " 울트라콜 기준 증가량 계산 "
    cp_df = t_df.groupby('campaign_id').sum('payment')
    cp_df['benefit_p'] = cp_df.payment / 88000
    adv_info = pd.Series(adv_info, name="address")
    return pd.concat([cp_df, adv_info], axis=1)