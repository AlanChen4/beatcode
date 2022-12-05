import logging
import requests
import time
from .auth import Authentication


class Scraper():

    def __init__(self, username, password, headless=True):
        self.auth = Authentication(username, password, headless=headless)

        auth_cookies = self.auth.get_auth_cookies()
        self.auth_cookies = auth_cookies
        self.auth_cookies_as_header_string = self.auth.get_cookie_as_header_string(self.auth_cookies)
        self.auth.quit_driver()

        self.session = requests.Session()
        self.session.headers.update({
            'cookie': self.auth_cookies_as_header_string,
            'referer': 'https://leetcode.com/submissions/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 OPR/92.0.0.0',
        })

    def _get_submissions_data(self, offset, limit, last_key=''):
        submissions_url = f"https://leetcode.com/api/submissions/?offset={offset}&limit={limit}&lastkey={last_key}"
        submissions_response = self.session.get(submissions_url, cookies=self.auth_cookies)
        if 200 <= submissions_response.status_code < 300:
            return submissions_response.json()
        else:
            raise RuntimeError('Could not fetch submissions', submissions_response.status_code, submissions_response.text, submissions_url)

    
    def get_all_submissions(self):
        all_submissions = []

        offset, limit = 0, 20
        while offset == 0 or submissions_data['has_next']:
            try:
                last_key = submissions_data.get('last_key', '')
                submissions_data = self._get_submissions_data(offset=offset, limit=limit, last_key=last_key)
                offset += 20
                limit += 20
                print(f'Successfully fetched {offset}-{limit}')
            except RuntimeError:
                # this runtime error is raised if we get a 403 (usually from LC rate limit)
                time.sleep(1)
                print(f'Trying again for {offset}-{limit}')
            all_submissions.extend(submissions_data['submissions_dump'])

        return all_submissions