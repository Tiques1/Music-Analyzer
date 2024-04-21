from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
from source.Exceptions import UnknownLink, GetError
import requests
import re


class YaMusicParser:
    def __init__(self):
        self.save_dir = 'D:\\Music\\'

        self.opt = webdriver.ChromeOptions()
        prefs = {
            "download.default_directory": 'D:\\Music\\',
            "download.prompt_for_download": False,
            "download.directory_upgrade": True
        }

        self.opt.add_experimental_option("prefs", prefs)
        self.opt.add_argument(r'--profile-directory=Default')
        self.opt.add_argument(r"--user-data-dir=C:\Users\Сергей\AppData\Local\Google\Chrome\User Data")
        # self.opt.add_extension('..\\..\\recources\\HFOFHOFFDCFCJGMILKPNHKAMCGEMABAN_2_0_8_0.crx')

        self.browser = webdriver.Chrome(options=self.opt)
        self.browser.set_page_load_timeout(1000)

    def parse(self, url, download_button) -> None:
        try:
            self.browser.get(url)
        except TimeoutException:
            return

        elements = self.browser.find_elements(By.ID, download_button)

        for elem in elements:
            parent = elem.find_element(By.XPATH, "./..")

            # Don't touch scrollbar motherfuckers
            # If you touch scrollbar, you will fuck
            while True:
                try:
                    elem.click()
                except ElementClickInterceptedException:
                    continue
                break

            while True:
                try:
                    button = parent.find_element(By.ID, download_button)
                    if button.text == '100%':
                        break
                except StaleElementReferenceException:
                    pass


class LinkHandler:
    def __init__(self):
        self.types = ('artist', 'album')
        self.patterns = (r'https://music\.yandex\.ru/album/\d+',
                         r'https://music\.yandex\.ru/artist/\d+/tracks')

    def define(self, link: str) -> str:
        if link[0:24] != 'https://music.yandex.ru/':
            raise UnknownLink(link)
        ltype = link.split('/')
        if ltype[3] in self.types:
            return ltype[3]
        else:
            raise UnknownLink(link)

    # Does not tell if artist or album not exists
    def exists(self, link: str) -> bool:
        match = False
        for pattern in self.patterns:
            if re.match(pattern, link):
                match = True
        if not match:
            raise UnknownLink(link)

        try:
            if requests.get(link) is not None:
                return True
            else:
                return False
        except Exception as e:
            raise GetError(e)


if __name__ == '__main__':
    # parser = YaMusicParser()
    # parser.parse('https://music.yandex.ru/artist/8855006/tracks', '_music_save_button')

    album = 'https://music.yandex.ru/album/16698062'
    artist = 'https://music.yandex.ru/artist/8855006/tracks'

    lh = LinkHandler()
    if lh.exists(artist):
        link_type = lh.define(artist)


