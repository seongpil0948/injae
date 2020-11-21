from typing import Any
from selenium.webdriver.remote.webdriver import WebDriver
from stubs.common import User

def login(driver: WebDriver, login_url: str, redirect_url: str, user: User) -> WebDriver:
    """
        Follow Redirect Url to Load the Logged in Page
    """
    ...