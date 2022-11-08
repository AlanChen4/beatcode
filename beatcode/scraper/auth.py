from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import time


class Authentication:
    """
    Helper to sign-in for Leetcode using selenium
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password

        # initialize Chrome browser as headless
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        self.driver = webdriver.Chrome(options=chrome_options)

    def get_auth_info(self):
        """
        return the csrftoken and leetcode_session cookies in a dictionary
        """
        self.driver.get('https://leetcode.com/accounts/login/')

        # time.sleep is needed to give time for js to load + cookies to be injected
        time.sleep(1)
        self.driver.find_element(By.ID, 'id_login').send_keys(self.username)
        self.driver.find_element(By.ID, 'id_password').send_keys(self.password)
        self.driver.find_element(By.ID, 'signin_btn').click()
        time.sleep(3)

        return {
            'csrftoken': self.driver.get_cookie('csrftoken')['value'],
            'leetcode_session': self.driver.get_cookie('LEETCODE_SESSION')['value']
        }
