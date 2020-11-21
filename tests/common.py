import pandas as pd
import os, json, sys

BASE_URL = os.path.dirname(os.path.dirname(os.path.abspath("__file__")))
sys.path.append(BASE_URL)
from utils.statistics import cleaning



def return_dfs() -> pd.DataFrame:
    dfs = pd.read_csv(os.path.join(BASE_URL, "datas/2020-10/klm1144.csv")), pd.read_csv(os.path.join(BASE_URL, "datas/2020-9/klm1144.csv"))
    t_df, c_df = cleaning(*dfs)

    with open(os.path.join(BASE_URL, "datas/2020-10/adv_info.json"), "r") as f:
        adv_info = pd.Series(json.load(f))
        adv_info.index = adv_info.index.map(int)
    return t_df, c_df, adv_info