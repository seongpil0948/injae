from selenium import webdriver
import os


__all__ = [
  'get_chrome_driver'
]

def get_chrome_driver():
  file_path = os.path.abspath(__file__)
  driver_path = os.path.join(
    file_path[:file_path.rfind('/') + 1],
    "chromedriver"
  )
  driver = webdriver.Chrome(executable_path=driver_path)
  return driver