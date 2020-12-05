from calendar import monthrange



 
def get_dates(year="2020", month="9"):
    year_int = int(year)
    month_int = int(month.replace('0', '')) if len(month) < 2 else int(month)
    return {
        'year_str': year,
        'month_str': month,
        'month_int': month_int,
        'year_int': year_int,
        'dates': [
            {
                "start_date": "1",
                "end_date": "7"
            }, 
            {
                "start_date": "8",
                "end_date": "14"
            }, 
            {
                "start_date": "15",
                "end_date": "21"
            }, 
            {
                "start_date": "22",
                "end_date": "28"
            }, 
            {
                "start_date": "29",
                "end_date": str(monthrange(year_int, month_int)[1])
            }
        ]
    }



def users(): 
    return [
        {
            "id": "amor",
            "password": "sotkfkd4050",
            "shop": "취성"
        },
        {
            "id": "seogdae",
            "password": "aksd6381",
            "shop": "한국인의 족발보쌈"
        },
        {
            "id": "wpspfpek",
            "password": "le577222",
            "shop": "족보쌈냉온국수"
        },
        {
            "id": "parkcy1472",
            "password": "pcyoung0041!",
            "shop": "신성정육식당&김치찌개전문점"
        },
        {
            "id": "klm1144",
            "password": "aa1144aa",
            "shop": "아리성"
        },
        {
            "id": "park1985",
            "password": "ahffk1818",
            "shop": "전곱"
        },
        {
            "id": "msp0312",
            "password": "kbk1218kbk",
            "shop": "THE만족한족"
        },
        {
            "id": "A01067881155",
            "password": "lykk3307",
            "shop": "게랑회랑"
        },
        {
            "id": "eunjy0415",
            "password": "eunjy!991006",
            "shop": "수제 Gogo함박&돈가스"
        },
        {
            "id": "eunjy0415",
            "password": "eunjy!991006",
            "shop": "연휘포차"
        },        {
            "id": "topsjingu1016",
            "password": "KJG101616",
            "shop": "엄청맛있는탕수육집"
        },    
        {
            "id": "lianji85",
            "password": "lianji.85",
            "shop": "해신마라탕"
        },    
        {
            "id": "whougogo",
            "password": "@00dnddhkd",
            "shop": "8번가"
        }, 
        {
            "id": "a0313839585",
            "password": "ha929564",
            "shop": "쉐프돼지&냉면 안양본점"
        },    
    ]


date_picker_root = "#root > div > div.frame-container > div.frame-wrap > div.frame-body > div.filter-container.py-0.pt-sm-3.pb-sm-0 > div:nth-child(2) > div > "
start_day_root = date_picker_root + 'span:nth-child(1) > div > '
end_day_root = date_picker_root + 'span:nth-child(3) > div >'
table = '//*[@id="root"]/div/div[1]/div[3]/div[1]/div[2]/table' 
def css():
    return {
        # class
        "curr_date_range_class": 'DateRangePicker',
        "dialog_exist_class": "Dialog",
        # xpath
        "drawer_btn": '//*[@id="root"]/div/div[1]/div[1]/button',
        "advertise_management_btn": '#root > div > div.frame-container.lnb-open > div.frame-aside > div > nav > ul > li:nth-child(4) > ul > li:nth-child(1) > a',
        "advertise_management_btn2": '#root > div > div.frame-container > div.frame-aside > div > nav > ul > li:nth-child(4) > ul > li:nth-child(1) > a',
        "dialog_btn": table + '/tbody/tr[{}]/td[5]/a', # row 당 한개.
        "dialog_close_btn": '//*[@id="root"]/div/div[2]/div/form/div[3]/button',
        "dialog_pickup_address": '//*[@id="root"]/div/div[2]/div/form/div[2]/div/div/table[2]/tbody/tr[3]/td',
        "dialog_order_no": '//*[@id="root"]/div/div[2]/div/form/div[2]/div/div/div',
        "next_page": '//*[@id="root"]/div/div[1]/div[3]/div[1]/nav/ul/li[8]/a/i',
        "search_btn": '//*[@id="root"]/div/div[1]/div[3]/div[1]/div[1]/div[2]/button',
        "table": table,
        # css         
        "date_picker_root": date_picker_root,
        "start_day_root": start_day_root,
        "end_day_root": end_day_root,
        "start_calendar_btn": start_day_root + "input",
        "end_calendar_btn": end_day_root + "input",
        "start_calendar_component": start_day_root + "div",
        "end_calendar_component": end_day_root + "div",

        # meta
        "order_empty_text": '//*[@id="root"]/div/div[1]/div[3]/div[1]/div[2]'
    }