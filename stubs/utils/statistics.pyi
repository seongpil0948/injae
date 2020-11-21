from pandas.core.frame import DataFrame as DataFrame
from typing import Any, List
from stubs.common import AdvertisementInfo

def cleaning(t_df: DataFrame, c_df: DataFrame) -> List[DataFrame] : ...
def get_stat_by_order(t_df: DataFrame, c_df: DataFrame) -> DataFrame: ...
# def apply_adv_info(df_by_campaign_id: DataFrame, adv_info: AdvertisementInfo) -> DataFrame: ...
def get_stat_by_campaign_id(t_df: DataFrame, c_df: DataFrame, adv_info: AdvertisementInfo) -> DataFrame: ...
