from meta import get_users
from dateutil.parser import parse
from typing import Dict, TypedDict, List

from utils.logger import get_logger

User = TypedDict("User", {'id':str, 'password':str, 'shop':str})
logger = get_logger()
def validate(year, month):
    if len(year) != 4:
        logger.error("년도는 4자리 여야만 합니다")
        return False
    elif len(month) > 2:
        logger.error("월은 2자리 이하여야 합니다") 
        return False
    try:
        parse(f"01-{month}-{year}")
    except Exception as e:
        logger.error(e)
        return False
    return True

def input_info():
    users = get_users()
    options = { str(j): users[j - 1] for j in range(1, len(users) + 1) }

    option_str = "인재씨 원하시는 매장의 번호를 입력 해주세요. \n"
    for num, user in options.items():
        if 'order' in user:
            option_str += f"    {num})  {user['shop']} {user['order']} {user['cate']}\n"     
        else:
            option_str += f"    {num})  {user['shop']}\n" 
    pick = input(option_str)

    user = None
    try:
        user = options[pick]
    except KeyError:
        logger.error('잘못 입력했다. :', pick)
        exit()
    logger.info('당신의 선택은: ', user)

    curr_year = input("기준 년도를 입력해라. ex) 2020 : ").strip()
    curr_month = input("기준 월을 입력해라. ex) 9 : ").strip()
    compare_year = input("비교 년도을 입력해라. ex) 2020 : ").strip()
    compare_month = input("비교 월을 입력해라. ex) 7 : ").strip()
    
    valid_curr = validate(curr_year, curr_month)
    valid_comp = validate(compare_year, compare_month)
    if valid_curr == True and valid_comp == True:
        return (curr_year, curr_month, compare_year, compare_month, user)
    else:
        logger.error("날짜 입력이 잘 못 되었습니다.")
        exit()