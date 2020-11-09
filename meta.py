from calendar import monthrange

def get_dates(year: str, month: str):
    year_int = int(year)
    month_int = int(month.replace('0', ''))
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
            "password": "aa1144aa"
        }
    ]


date_picker_root = "#root > div > div.frame-container > div.frame-wrap > div.frame-body > div.filter-container.py-0.pt-sm-3.pb-sm-0 > div:nth-child(2) > div > "
start_day_root = date_picker_root + 'span:nth-child(1) > div > '
end_day_root = date_picker_root + 'span:nth-child(3) > div >'   
def css():
    return {
        "date_picker_root": date_picker_root,
        "start_day_root": start_day_root,
        "end_day_root": end_day_root,
        "start_calendar_btn" :start_day_root + "input",
        "end_calendar_btn": end_day_root + "input",
        "start_calendar_component": start_day_root + "div",
        "end_calendar_component": end_day_root + "div",
        "search_btn": '//*[@id="root"]/div/div[1]/div[3]/div[1]/div[1]/div[2]/button',
        "table": '//*[@id="root"]/div/div[1]/div[3]/div[1]/div[2]/table',
        "next_page": '//*[@id="root"]/div/div[1]/div[3]/div[1]/nav/ul/li[8]/a/i'
    }