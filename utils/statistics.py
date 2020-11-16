import numpy as np
import pandas as pd

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
    t_order = t_df.groupby('address').sum('payment')
    c_order = c_df.groupby('address').sum('payment')
    t_order['profit'] = t_order.payment - c_order.payment
    for address in t_order[t_order.profit.isna()].index.to_list():
        if address in t_order.index:
            t_order.loc[address] = t_order.loc[address].payment
        elif address in c_order.index:
            t_order.loc[address] = -c_order.loc[address].payment
        else:
            raise ValueError('뭔가 잘못 되었다.')
    return t_order

def apply_adv_info(df_by_campaign_id, adv_info):
    adv_info = pd.Series(adv_info, name="address")

    for k in adv_info.index:
        if k not in df_by_campaign_id.index:
            df_by_campaign_id.loc[k] = [np.nan, np.nan]
    df_by_campaign_id = pd.concat([df_by_campaign_id, adv_info], axis=1)
    return df_by_campaign_id

def get_stat_by_campaign_id(t_df, c_df, adv_info):
    curr_order = t_df.groupby('campaign_id').sum('payment')
    compare_order = c_df.groupby('campaign_id').sum('payment')

    try:
        curr_order = curr_order.drop('기타')
    except KeyError:
        pass
    try:
        compare_order = compare_order.drop('기타')
    except KeyError:
        pass

    " 증가율 계산 "
    # 이전달에 울트라콜이 있고 이번달에 없을 수 없음. 왜나하면 이번달 기준으로 adv_info를 구했기 때문 무조건 현재달 기준.
    curr_order['profit'] = curr_order.payment.subtract(compare_order.payment + 88000, fill_value=0)
    curr_order['profit'] = curr_order.profit / curr_order.payment
    curr_order['profit'] = curr_order['profit'].map(lambda x: x % -1 if x < 0 else x % 1)
    curr_order['profit'] = curr_order['profit'] * 100
    curr_order = apply_adv_info(curr_order, adv_info)
    return curr_order