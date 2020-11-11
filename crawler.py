from time import sleep
from assets import get_chrome_driver
from meta import get_dates, users, css
from utils import login

import pandas as pd
import re
from selenium.common.exceptions import (
    TimeoutException, 
    ElementNotInteractableException, 
    NoSuchElementException,
    StaleElementReferenceException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Crawler:
    def __init__(self, user, year="2020", month="10"):
        self.login_url = "https://ceo.baemin.com/web/login"
        self.redirect_url = "https%3A%2F%2Fceo.baemin.com%2Fself-service/orders/history"
        self.driver = get_chrome_driver()        
        self.dates = get_dates(year, month)
        self.user = user
        self.css = css()

    @staticmethod
    def click_day_in_calendar(driver, calendar_btn, day_root, click_date):
        calendar_btn.click()
        calendar_component = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, day_root + "div"))
        )  
        days = calendar_component.find_elements_by_class_name('DayPicker-Day')
        for day in days:
            if day.text == click_date:
                day.click()
                break     
    
    @staticmethod
    def fix_calendar(start_calendar_component, year_int, month_int):
        "시작캘린더만 선택하면 된다는 전제하에, 캘린더에서 찾는 년, 월로 이동 해줍니다. start_calendar_component: element"
        text = start_calendar_component.text
        year_idx = text.find('년')
        cal_year = text[:year_idx]
        month_idx = text.find('월')
        cal_month = text[year_idx + 1: month_idx].strip()
        cal_month_int = int(cal_month.replace('0', ''))
        diff = (int(cal_year) * 12 +  cal_month_int) -  (year_int * 12 + month_int)
        if diff > 0:
            for month in range(1, diff + 1):
                # 월 만큼 이전버튼 클릭.
                start_calendar_component.find_element_by_class_name('DayPicker-NavButton--prev').click()    

    def parsing_table(self, max_page:int=100):
        datas = []
        for _ in list(range(max_page)):
            table = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, self.css['table']))
            )
            sleep(1)
            rows = table.find_elements_by_tag_name('tr')
            
            for row_num in list(range(1, len(rows))):
                """ 
                    0은 헤더이기 때문에 1부터. 다이얼로그 클릭 이벤트로 인해 DOM 이 변경된후에 다시 이전에 사용하던 
                    Element 변수를 사용하게 되면 StaleElementReferenceException 에러 발생.. 고로 다시 찾아야함.
                """
                address = None; dial_no = None
                try:
                    dialog_btn = self.driver.find_element_by_xpath(self.css['dialog_btn'].format(row_num))
                    dialog_btn.click()
                    address = self.driver.find_element_by_xpath(self.css['dialog_pickup_address']).text
                    dialog_close_btn = self.driver.find_element_by_xpath(self.css['dialog_close_btn'])
                    dial_no = self.driver.find_element_by_xpath(self.css['dialog_order_no']).text\
                        .replace('배달완료', '').strip()
                    dialog_close_btn.click()
                except (NoSuchElementException, StaleElementReferenceException) as e:
                    print('========================\n', e)
                    pass
                # WebDriverWait(self.driver, 3).until(
                #     EC.invisibility_of_element((By.CLASS_NAME, self.css['dialog_exist_class']))
                # )

                row = self.driver.find_element_by_xpath(f"{self.css['table']}/tbody/tr[{row_num}]")
                cols = row.find_elements_by_tag_name('td')
                data = [
                    cols[0].text.replace('배달완료\n', '').strip(), # 주문번호
                    cols[1].text, # 주문시각
                    cols[2].text, # 광고상품그룹
                    cols[3].text, # 캠페인 ID
                    cols[4].text,  # 주문내역
                    address,
                    int(re.search("\d+", cols[5].text.replace(',', '')).group()), # 결제금액
                ]
                assert dial_no == data[0], f"difference between \n dial_no: {dial_no} and data[0]: {data[0]} \n row_num: {row_num}, page: {_ + 1} \n {row.text}"
                datas.append(data)
            try:
                e = WebDriverWait(self.driver, 1).until(
                    EC.element_to_be_clickable((By.XPATH, self.css['next_page']))
                )
                self.driver.find_element_by_xpath(self.css['next_page'])    
                e.click()
            except (ElementNotInteractableException, TimeoutException) as e:
                """
                    -- indicate --
                    ElementNotInteractableException: page = 1
                    TimeoutException: last page
                """
                break
        return datas

    def go(self):
        login(self.driver, self.login_url, self.redirect_url, self.user)

        # Filtering 나중에 함수로 변경.
        # Calendar
        start_calendar_btn = WebDriverWait(self.driver, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.css["start_calendar_btn"]))
        )
        end_calendar_btn = self.driver.find_element_by_css_selector(self.css["end_calendar_btn"])
        # Open Calendar
        start_calendar_btn.click()
        start_calendar_component = self.driver.find_element_by_css_selector(self.css['start_calendar_component'])
        self.fix_calendar(
            start_calendar_component,
            year_int=self.dates['year_int'], 
            month_int=self.dates['month_int']
        )
        # ETC
        filter_area = self.driver.find_element_by_class_name('filter-row')
        filters = filter_area.find_elements_by_tag_name('select')
        # 상세가계
        businesses = filters[0].find_elements_by_tag_name('option')
        list(filter(lambda x: x.text ==self.user['business'], businesses))[0].click()
        # 배달 완료
        status = filters[1].find_elements_by_tag_name('option')
        list(filter(lambda x: x.get_attribute('value') == 'CLOSED', status))[0].click()
        # 광고 그룹
        groups = filters[2].find_elements_by_tag_name('option')
        list(filter(lambda x: x.get_attribute('value') == 'ULTRA_CALL', groups))[0].click()        
        # ===== Filtering END ========

        datas = []
        for date in self.dates['dates']:
            # 날짜 1~7, 8 ~14 ... 순으로 데이터 수집
            self.click_day_in_calendar(
                driver=self.driver,
                calendar_btn=start_calendar_btn,
                day_root=self.css['start_day_root'],
                click_date=date['start_date']           
            )
            self.click_day_in_calendar(
                driver=self.driver,
                calendar_btn=end_calendar_btn,
                day_root=self.css['end_day_root'],
                click_date=date['end_date']           
            )
            self.driver.find_element_by_xpath(self.css["search_btn"]).click()
            self.driver.implicitly_wait(1)
            datas += self.parsing_table()

        df = pd.DataFrame(data=datas, columns=['no', 'date', 'group', 'campaign_id', 'order_info', 'address', 'payment'])
        try:
            df["date"] = pd.to_datetime(df["date"], format='%y. %m. %d %H:%M:%S')
        except ValueError:
            df["date"] = pd.to_datetime(df["date"], format='%y-%m-%d %H:%M:%S')
        df = df.sort_values(by=['date'], axis=0)
        df = df.set_index('date', drop=True)
        df.to_csv(f"./datas/{self.dates['year_str']}-{self.dates['month_str']}__{self.user['id']}__dataframe.csv")
        self.driver.close()
        
        return df

if __name__ == "__main__":
    users = users()
    user = users[0]
    curr_year = "2020"
    curr_month = "11"
    compare_year = "2020"
    compare_month = "10"
    c = Crawler(user=user, year=curr_year, month=curr_month)
    df = c.go()
    c2 = Crawler(user=user, year=compare_year, month=compare_month)
    df2 = c2.go()
    # TODO: 증가량 검사
