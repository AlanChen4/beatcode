from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time


class Authentication:
    """
    Helper to sign-in for Leetcode using selenium
    """

    def __init__(self, username, password, headless=True):
        self.username = username
        self.password = password

        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")

        self.driver = webdriver.Chrome(options=chrome_options)

    def get_auth_cookies(self):
        """
        return the csrftoken and leetcode_session cookies in a dictionary
        """
        self.driver.get('https://leetcode.com/accounts/login/')

        time.sleep(1)
        self.driver.find_element(By.ID, 'id_login').send_keys(self.username)
        self.driver.find_element(By.ID, 'id_password').send_keys(self.password)
        self.driver.find_element(By.ID, 'signin_btn').click()
        time.sleep(3)

        try:
            return {
                'csrftoken': self.driver.get_cookie('csrftoken')['value'],
                'LEETCODE_SESSION': self.driver.get_cookie('LEETCODE_SESSION')['value'],
                'messages': self.driver.get_cookie('messages')['value'],
                '_ga': self.driver.get_cookie('_ga')['value'],
                '_gid': self.driver.get_cookie('_gid')['value'],
                '_gat': self.driver.get_cookie('_gat')['value'],
            }
        except TypeError as e:
            raise Exception('Could not fetch authentication cookies properly', e)

    def get_cookie_as_header_string(self, cookie_dict):
        cookie_string = []
        for key, value in cookie_dict.items():
            cookie_string.append(f"{key}={value}")
        return '; '.join(cookie_string)

    def quit_driver(self):
        self.driver.quit()