from typing import Any, Dict, List, TypedDict

DateRanges = List[Dict[str, str]]

class DatePack(TypedDict):
    year_str: str
    month_str: str
    month_int: int
    year_int: int
    dates: DateRanges

def get_dates(year: str=..., month: str=...) -> DatePack: ...

User: Any

def users() -> List[User]: ...

date_picker_root: str
start_day_root: Any
end_day_root: Any
table: str

def css(): ...
