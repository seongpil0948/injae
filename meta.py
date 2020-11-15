from calendar import monthrange

def get_dates(year: str, month: str):
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
                "end_date": monthrange(year_int, month_int)[1]
            }
        ]
    }

def users(): 
    return [
        {
            "id": "klm1144",
            "password": "aa1144aa",
            "shop": "아리성"
        }
    ]


date_picker_root = "#root > div > div.frame-container > div.frame-wrap > div.frame-body > div.filter-container.py-0.pt-sm-3.pb-sm-0 > div:nth-child(2) > div > "
start_day_root = date_picker_root + 'span:nth-child(1) > div > '
end_day_root = date_picker_root + 'span:nth-child(3) > div >'
table = '//*[@id="root"]/div/div[1]/div[3]/div[1]/div[2]/table' 
def css():
    return {
        "drawer_btn": '//*[@id="root"]/div/div[1]/div[1]/button',
        "advertise_management_btn": '#root > div > div.frame-container.lnb-open > div.frame-aside > div > nav > ul > li:nth-child(4) > ul > li:nth-child(1) > a',
        "advertise_management_btn2": '#root > div > div.frame-container > div.frame-aside > div > nav > ul > li:nth-child(4) > ul > li:nth-child(1) > a',
        "date_picker_root": date_picker_root,
        "start_day_root": start_day_root,
        "end_day_root": end_day_root,
        "start_calendar_btn" :start_day_root + "input",
        "end_calendar_btn": end_day_root + "input",
        "start_calendar_component": start_day_root + "div",
        "end_calendar_component": end_day_root + "div",
        "search_btn": '//*[@id="root"]/div/div[1]/div[3]/div[1]/div[1]/div[2]/button',
        "table": table,
        "dialog_exist_class": "Dialog",
        "dialog_btn": table + '/tbody/tr[{}]/td[5]/a', # row 당 한개.
        "dialog_close_btn": '//*[@id="root"]/div/div[2]/div/form/div[3]/button',
        "dialog_pickup_address": '//*[@id="root"]/div/div[2]/div/form/div[2]/div/div/table[2]/tbody/tr[3]/td',
        "dialog_order_no": '//*[@id="root"]/div/div[2]/div/form/div[2]/div/div/div',
        "next_page": '//*[@id="root"]/div/div[1]/div[3]/div[1]/nav/ul/li[8]/a/i',
    }