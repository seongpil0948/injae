import json, os
import pandas as pd

from utils.input import input_info
from crawler import Crawler
from utils.statistics import *


CHROME_DEBUG = True

curr_year, curr_month, compare_year, compare_month, user = input_info()
c = Crawler(user=user, year=curr_year, month=curr_month, req_advertise_info=True, chrome_debug=CHROME_DEBUG)
target_df = c.go()
c2 = Crawler(user=user, year=compare_year, month=compare_month, chrome_debug=CHROME_DEBUG)
compare_df = c2.go()

t_df, c_df = cleaning(t_df=target_df, c_df=compare_df)
order_df = get_stat_by_order(t_df, c_df)

with open(f"datas/{curr_year}-{curr_month}/adv_info.json", "r") as f:
    adv_info = pd.Series(json.load(f))

campaign_df = get_stat_by_campaign_id(t_df=target_df, c_df=compare_df, adv_info=adv_info)

result_dir = f"./results/{curr_year}-{curr_month}-{user['id']}"
if os.path.isdir(result_dir) == False:
    os.makedirs(result_dir)

order_df.to_csv(f"{result_dir}/order.csv")
campaign_df.to_csv(f"{result_dir}/campaign.csv")