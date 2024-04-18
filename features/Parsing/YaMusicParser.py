import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException


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


if __name__ == '__main__':
    parser = YaMusicParser()
    parser.parse('https://music.yandex.ru/artist/8855006/tracks', '_music_save_button')


