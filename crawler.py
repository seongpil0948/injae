from assets import get_chrome_driver
from meta import get_dates, users, css
from utils import login

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
from os.path import join

# TODO: 타입명시 필요 Element 와 Css 구별이 안됌.

class Crawler:
    def __init__(self, user, year="2020", month="06"):
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
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, self.css['table']))
            )
            html = self.driver.page_source
            soup = bs(html, 'html.parser')  
            table = soup.find('table')
            rows = table.find_all('tr')
            for row in rows[1:]:
                cols = row.find_all('td')
                data = [
                    cols[1].text.replace('주문시각', '').replace('. ', '-'), 
                    cols[2].text.replace('광고상품그룹', ''),
                    cols[3].text.replace('캠페인ID', ''), # 캠페인 ID
                    cols[4].text.replace('주문내역', ''),  # 주문내역
                    int(re.search("\d+", cols[5].text.replace(',', '')).group()), # 결제금액
                ]
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

        df = pd.DataFrame(data=datas, columns=['주문시각', '광고그룹', '캠페인', '주문내역', '결제금액'])
        df["주문시각"] = pd.to_datetime(df["주문시각"], format='%y-%m-%d %H:%M:%S')
        df = df.sort_values(by=['주문시각'], axis=0)
        df = df.set_index('주문시각', drop=True)

        # FIXME: 어떻게 할건지 결정.
        dir_name = "./datas"
        file_name = f"{self.user['id']}__dataframe.csv"
        df.to_csv(join(dir_name, file_name))
        self.driver.close()

if __name__ == "__main__":
    users = users()
    c = Crawler(user=users[0])
    c.go()
