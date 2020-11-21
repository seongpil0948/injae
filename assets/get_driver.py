from selenium import webdriver
import os


__all__ = [
    'get_chrome_driver'
]

def get_chrome_driver(chrome_debug=False):
    file_path = os.path.abspath(__file__)
    driver_path = os.path.join(
        file_path[:file_path.rfind('/') + 1],
        "chromedriver"
    )
    options = webdriver.ChromeOptions()    
    if chrome_debug == False:
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
    return driver