from time import sleep
import pandas as pd
import re, json, os, logging
from typing import NoReturn
from selenium.common.exceptions import (
    TimeoutException, 
    ElementNotInteractableException, 
    NoSuchElementException,
    StaleElementReferenceException
)

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import get_logger
from assets import get_chrome_driver
from meta import get_dates, css
from utils.login import login


class Crawler:
    # FIXME: year, month 는 서로 관계가 있지만 Struct 형태로 묶어져 있지 않다.
    def __init__(self, user, year="2020", month="10", req_advertise_info=False, chrome_debug=False):
        self.login_url = "https://ceo.baemin.com/web/login"
        self.redirect_url = "https%3A%2F%2Fceo.baemin.com%2Fself-service/orders/history"
        self.driver = get_chrome_driver(chrome_debug=chrome_debug)        
        self.dates = get_dates(year, month)
        self.dir_path = f"./datas/{self.dates['year_str']}-{self.dates['month_str']}"
        self.user = user
        self.css = css()
        self.req_advertise_info = req_advertise_info
        self.logger = get_logger()
        if os.path.isdir(self.dir_path) == False:
            os.makedirs(self.dir_path)

    def __getstate__(self):
        d = self.__dict__.copy()
        if 'logger' in d:
            d['logger'] = d['logger'].name

        return d

    def __setstate__(self, d):
        if 'logger' in d:
            d['logger'] = logging.getLogger(d['logger'])
        self.__dict__.update(d)

    @staticmethod
    def fix_calendar(start_calendar_component, year_int, month_int) -> NoReturn:
        "시작캘린더만 선택하면 된다는 전제하에, 캘린더에서 찾는 년, 월로 이동 해줍니다. start_calendar_component: element"
        text = start_calendar_component.text
        year_idx = text.find('년')
        cal_year = text[:year_idx]
        month_idx = text.find('월')
        cal_month = text[year_idx + 1: month_idx].strip()
        cal_month_int = int(cal_month)
        diff = (int(cal_year) * 12 +  cal_month_int) -  (year_int * 12 + month_int)
        if diff > 0:
            for month in range(1, diff + 1):
                # 월 만큼 이전버튼 클릭.
                start_calendar_component.find_element_by_class_name('DayPicker-NavButton--prev').click()    

    def paring_dialog(self, row_num):
        dialog_btn = WebDriverWait(self.driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, self.css['dialog_btn'].format(row_num))))                    
        dialog_btn.click()
        address = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.XPATH, self.css['dialog_pickup_address']))).text
        dialog_close_btn = self.driver.find_element_by_xpath(self.css['dialog_close_btn'])
        dial_no = self.driver.find_element_by_xpath(self.css['dialog_order_no']).text\
            .replace('배달완료', '').strip()
        dialog_close_btn.click()
        return (dial_no, address)

    def parsing_table(self, max_page:int=100):
        datas = []
        for page in list(range(1, max_page)):
            try:
                table = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, self.css['table'])))
            except TimeoutException as e:
                if page == 1 and '없습니다' in \
                    self.driver.find_element_by_xpath(self.css["order_empty_text"]).text:
                    self.logger.debug(f"{self.dates['year_str']}년 {self.dates['month_str']}월 일부 기간내에 데이터가 존재하지 안습니다")
                    return []
                else:
                    raise e
            rows = table.find_elements_by_tag_name('tr')
            # 0은 헤더이기 때문에 1부터
            for row_num in list(range(1, len(rows))):
                address = None; dial_no = None
                try:
                    (dial_no, address) = self.paring_dialog(row_num)
                except (NoSuchElementException, StaleElementReferenceException, TimeoutException) as e:
                    self.logger.error(f"page: {page} \n {row_num} row \n {e}")
                    raise e

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
                if dial_no != data[0]:
                    self.logger.error(f"difference between \n dial_no: {dial_no} and data[0]: {data[0]} \n row_num: {row_num}, page: {page + 1} \n {row.text}")
                    breakpoint()
                datas.append(data)
            try:
                e = WebDriverWait(self.driver, 1).until(
                    EC.element_to_be_clickable((By.XPATH, self.css['next_page']))
                )
                self.driver.find_element_by_xpath(self.css['next_page'])    
                e.click()
            except (ElementNotInteractableException, TimeoutException) as e:
                break # Last Page
            sleep(1)
        return datas

    def filtering(self):
        # Calendar
        start_calendar_btn = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.css["start_calendar_btn"])))
        # Open Calendar
        start_calendar_btn.click()
        start_calendar_component = self.driver.find_element_by_css_selector(self.css['start_calendar_component'])
        self.fix_calendar(start_calendar_component, year_int=self.dates['year_int'], month_int=self.dates['month_int'])
        # ETC
        filter_area = self.driver.find_element_by_class_name('filter-row')
        filters = filter_area.find_elements_by_tag_name('select')
        # 상세가계
        shops = filters[0].find_elements_by_tag_name('option')
        try:
            list(filter(lambda x: x.text ==self.user['shop'], shops))[0].click()
        except IndexError:
            self.logger.error(f"{self.user['shop']} 가 실제 존재하는게 맞습니까?")
            self.driver.close()
            exit()
        # 배달 완료
        status = filters[1].find_elements_by_tag_name('option')
        list(filter(lambda x: x.get_attribute('value') == 'CLOSED', status))[0].click()
        # 광고 그룹
        try:
            groups = filters[2].find_elements_by_tag_name('option')
        except StaleElementReferenceException:
            filters = filter_area.find_elements_by_tag_name('select')
            groups = filters[2].find_elements_by_tag_name('option')
        list(filter(lambda x: x.get_attribute('value') == 'ULTRA_CALL', groups))[0].click()
    
    def click_day_in_calendar(self, calendar_btn, day_root, click_date):
        calendar_btn.click()
        calendar_component = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, day_root + "div"))
        )

        cal_month = int(calendar_component.text[
            calendar_component.text.find('년') + 1: calendar_component.text.find('월')
        ].strip())
        if cal_month > self.dates['month_int']:
            calendar_component.find_element_by_class_name('DayPicker-NavButton--prev').click() 
        days = calendar_component.find_elements_by_class_name('DayPicker-Day')
        " 이전달 일자 클릭을 방지하기 위함"
        days = days[10: ] if int(click_date) > 20 else days[: -5]
        list(filter(lambda day: day.text == click_date, days))[0].click()
        
    

    def collect_data(self):
        start_calendar_btn = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.css["start_calendar_btn"])))
        end_calendar_btn = self.driver.find_element_by_css_selector(self.css["end_calendar_btn"])        
        datas = []
        for date in self.dates['dates']:
            # 날짜 1~7, 8 ~14 ... 순으로 데이터 수집
            self.click_day_in_calendar(
                calendar_btn=start_calendar_btn,
                day_root=self.css['start_day_root'],
                click_date=date['start_date']
            )
            self.click_day_in_calendar(
                calendar_btn=end_calendar_btn,
                day_root=self.css['end_day_root'],
                click_date=date['end_date']           
            )
            # check curr selected data is valid
            end_date = end_calendar_btn.get_attribute('value')
            curr_end_date = end_date.split('-')[-1] if '-' in end_date else end_date[end_date.rfind(' ') + 1:]

            if date['end_date'] != curr_end_date:
                self.logger.debug(f"{curr_end_date} 일이 선택 되었습니다. \n 하지만 {date['end_date']}'이 이번달의 마지막 날짜입니다.")
                self.click_day_in_calendar(
                    calendar_btn=start_calendar_btn,
                    day_root=self.css['start_day_root'],
                    click_date=date['end_date']
                )
                self.click_day_in_calendar(
                    calendar_btn=start_calendar_btn,
                    day_root=self.css['start_day_root'],
                    click_date=date['start_date']
                )                

            self.driver.find_element_by_xpath(self.css["search_btn"]).click()
            datas += self.parsing_table()
        df = pd.DataFrame(data=datas, columns=['no', 'date', 'group', 'campaign_id', 'order_info', 'address', 'payment'])
        return df

    def advertise_traverse(self):
        """
            Prerequisite Required Login
        """
        try:
            self.driver.find_element_by_xpath(self.css['drawer_btn']).click()
            WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.css['advertise_management_btn']))).click()
        except ElementNotInteractableException:
            # 이미 메뉴가 열려있음.
            self.driver.find_element_by_css_selector(self.css['advertise_management_btn2']).click()
            pass
        self.driver.implicitly_wait(1)

        shops = self.driver.find_elements_by_css_selector('div.ShopSelect > select > option')
        list(filter(lambda x: x.text == self.user['shop'], shops))[0].click()

        cards = self.driver.find_elements_by_class_name('Card')
        card = list(filter(lambda card: '울트라콜' in card.find_element_by_class_name('card-header').text, cards))[0]
        table = card.find_element_by_tag_name('tbody')
        rows = table.find_elements_by_tag_name('tr')
        datas = {}
        for row in rows:
            cols = row.find_elements_by_tag_name('td')
            campaign_id = re.search('\d+', cols[0].text).group()
            address = cols[2].text.replace('노출위치', '')
            datas[campaign_id] = address
        
        with open(f"{self.dir_path}/adv_info.json", 'w') as f:
            json.dump(datas, f)


    def go(self):
        login(self.driver, self.login_url, self.redirect_url, self.user)
        self.filtering()
        df = self.collect_data()
        try:
            df["date"] = pd.to_datetime(df["date"], format='%y. %m. %d %H:%M:%S')
        except ValueError:
            df["date"] = pd.to_datetime(df["date"], format='%y-%m-%d %H:%M:%S')
        df = df.sort_values(by=['date'], axis=0)
        if self.req_advertise_info == True:
            self.advertise_traverse()
        # df = df.set_index('date', drop=True)
        df.to_csv(f"{self.dir_path}/{self.user['id']}.csv")
        self.driver.close()
        return df

