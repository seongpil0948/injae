from typing import Dict, NewType, Type, TypedDict, List

# type alias for instance 
# interface(new type) for Global
User = TypedDict("User", {'id':str, 'password':str, 'shop':str})
AdvertisementInfo = NewType('AdvertisementInfo', Dict[str, str])

DateRanges = List[Dict[str, str]]
class DatePack(TypedDict):
    year_str: str
    month_str: str
    month_int: int
    year_int: int
    dates: DateRanges

CssSelector = NewType('CssSelector', str)
CssXpath = Type[CssSelector]