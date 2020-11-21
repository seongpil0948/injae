from typing import Any, Dict, List
from .common import User, DatePack



def get_dates(year: str=..., month: str=...) -> DatePack: ...

def users() -> List[User]: ...

date_picker_root: str
start_day_root: Any
end_day_root: Any
table: str

def css() -> Dict[str, str]: ...
