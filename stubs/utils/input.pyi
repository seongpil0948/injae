from typing import Dict, Tuple
from stubs.common import User

def input_info() -> Tuple[str, str, str, str, User]:
    users_by_shop: Dict[str, User]
    ...