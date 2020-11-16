import numpy as np
import pandas as pd

def get_stat_by_order(t_df, c_df):
    t_order = t_df.groupby('address').sum('payment')
    c_order = c_df.groupby('address').sum('payment')
    t_order['profit'] = t_order.payment - c_order.payment
    t_order = t_order.loc[:, ~t_order.columns.str.contains('^Unnamed')]
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
    curr_order.index = curr_order.index.map(str)
    curr_order = curr_order.loc[:, ~curr_order.columns.str.contains('^Unnamed')]
    curr_order.profit= np.nan

    compare_order = c_df.groupby('campaign_id').sum('payment')
    compare_order = compare_order.loc[:, ~compare_order.columns.str.contains('^Unnamed')]
    compare_order.index = compare_order.index.map(lambda x: str(x))
    compare_order.profit = np.nan

    try:
        curr_order = curr_order.drop('기타')
    except KeyError:
        pass
    try:
        compare_order = compare_order.drop('기타')
    except KeyError:
        pass

    curr_order['profit'] = (curr_order.payment - compare_order.payment - 88000)
    curr_order['profit'] = curr_order['profit'].fillna(curr_order['payment'] - 88000) # 이전달에 울트라콜이 있고 이번달에 없을 수 없음. 무조건 현재달 기준.
    curr_order['profit'] = curr_order['profit'] / compare_order.payment * 100
    
    for k in list(adv_info.keys()):
        if k not in curr_order.index:
            curr_order.loc[k] = [np.nan, np.nan]
    curr_order = apply_adv_info(curr_order, adv_info)
    return curr_order