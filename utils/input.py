from meta import users

def input_info():
    users_by_shop = { i['shop']: i for i in users()}
    shops = list(users_by_shop.keys())
    options = { str(j): shops[j - 1] for j in range(1, len(shops) + 1) }

    option_str = "인재씨 원하시는 매장의 번호를 입력 해주세요. \n"
    for num, shop in options.items():
        option_str += f"    {num})  {shop}\n" 
    pick = input(option_str)

    user = None
    try:
        user = users_by_shop[options[pick]]
    except KeyError:
        print('잘못 입력했다. :', pick)
        exit()
    print('당신의 선택은: ', user)

    curr_year = input("기준 년도를 입력해라. ex) 2020 : ").strip()
    curr_month = input("기준 월을 입력해라. ex) 9 : ").strip()
    compare_year = input("비교 년도을 입력해라. ex) 2020 : ").strip()
    compare_month = input("비교 월을 입력해라. ex) 7 : ").strip()
    
    return (curr_year, curr_month, compare_year, compare_month, user)