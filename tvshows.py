import urllib
import json
import requests
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from datetime import date
import telepot


class TvShows:
    def __init__(self):
        opts = Options()
        opts.add_argument('--headless')
        opts.add_argument('--no-sandbox')
        opts.add_argument('--disable-dev-shm-usage')
        opts.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36")

        self.driver = webdriver.Chrome(options=opts)
        self.username = ''
        self.password = ''
        self.chat_id = ''
        self.token = ''

    def login(self):
        driver = self.driver
        driver.get('https://bancodeseries.com.br/index.php?action=mygrade')
        sleep(3)

        login = driver.find_element_by_xpath(
            '//*[@id="dcenter"]/div[2]/form/table/tbody/tr[1]/td[2]/input')
        login.send_keys(self.username)

        password = driver.find_element_by_xpath(
            '//*[@id="dcenter"]/div[2]/form/table/tbody/tr[2]/td[2]/input')
        password.send_keys(self.password)

        login_btn = driver.find_element_by_xpath(
            '//*[@id="dcenter"]/div[2]/form/table/tbody/tr[3]/td[1]/input')
        login_btn.click()

    def look_for_updates(self):
        driver = self.driver
        driver.get('https://bancodeseries.com.br/index.php?action=calendar')

        request = driver.wait_for_request('/api/calendar', timeout=30)

        query = request.querystring
        parsed = urllib.parse.parse_qs(query)

        uid = parsed['uid'][0]
        user_key = parsed['userkey'][0]
        api_key = parsed['apikey'][0]
        today = date.today()

        base_url = 'https://bancodeseries.com.br'
        response = requests.get(
            base_url + f'/api/calendar.php?uid={uid}&userkey={user_key}&apikey={api_key}&start={today}&end={today}')

        tv_shows = json.loads(response.text)

        for tv_show in tv_shows:
            self.send_message(tv_show)

    def send_message(self, tv_show):
        bot = telepot.Bot(self.token)
        title = tv_show['stitle']
        ep = tv_show['sxe']
        channel = tv_show['canal']
        bot.sendMessage(
            self.chat_id, f'Séries Hoje: {title} {ep} no canal {channel}')


bot = TvShows()
bot.login()
bot.look_for_updates()
