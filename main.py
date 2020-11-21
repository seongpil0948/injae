import json, os

from utils.input import input_info
from crawler import Crawler
from utils.statistics import *

# target_df = pd.read_csv('datas/2020-9/klm1144.csv')
# compare_df = pd.read_csv('datas/2020-11/klm1144.csv')
# with open(f"datas/2020-11/adv_info.json", "r") as f:
#     adv_info = json.load(f)

curr_year, curr_month, compare_year, compare_month, user = input_info()
c = Crawler(user=user, year=curr_year, month=curr_month, req_advertise_info=True)
target_df = c.go()
c2 = Crawler(user=user, year=compare_year, month=compare_month)
compare_df = c2.go()

t_df, c_df = cleaning(t_df=target_df, c_df=compare_df)
order_df = get_stat_by_order(t_df, c_df)

with open(f"datas/{curr_year}-{curr_month}/adv_info.json", "r") as f:
    adv_info = pd.Series(json.load(f))
    adv_info.index = adv_info.index.map(int)

campaign_df = get_stat_by_campaign_id(t_df=target_df, c_df=compare_df, adv_info=adv_info)


result_dir = f"./results/{curr_year}-{curr_month}-{user['id']}"
if os.path.isdir(result_dir) == False:
    os.makedirs(result_dir)

order_df.to_csv(f"{result_dir}/order.csv")
campaign_df.to_csv(f"{result_dir}/campaign.csv")