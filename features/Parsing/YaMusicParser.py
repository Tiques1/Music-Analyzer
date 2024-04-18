import time
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import selenium
from selenium.webdriver.support.wait import WebDriverWait
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

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

        self.opt.add_argument(r'--profile-directory=Default')  # e.g. Profile 3
        # self.opt.add_argument('--no-sandbox')
        # self.opt.add_argument('--disable-dev-shm-usage')
        self.opt.add_argument(r"--user-data-dir=C:\Users\Сергей\AppData\Local\Google\Chrome\User Data")
        # self.opt.add_extension('..\\..\\recources\\HFOFHOFFDCFCJGMILKPNHKAMCGEMABAN_2_0_8_0.crx')

        self.browser = webdriver.Chrome(options=self.opt)

    def parse(self, url, elements) -> None:
        self.browser.get(url)
        elements = self.browser.find_elements(By.ID, elements)
        self.browser.execute_script("window.open('chrome://downloads/', 'new_tab')")

        for element in elements:
            element.click()
            # WebDriverWait(self.browser, 120, 1).until(self._wait_for_download)
            self.browser.switch_to.window(self.browser.window_handles[0])

    @staticmethod
    def _wait_for_download(driver):
        driver.switch_to.window(driver.window_handles[1])
        if not driver.current_url.startswith("chrome://downloads"):
            driver.switch_to.window(driver.window_handles[-1])
        return driver.execute_script("""
            var items = document.querySelector('downloads-manager')
                .shadowRoot.getElementById('downloadsList').items;
            if (items.every(e => e.state === "COMPLETE"))
                return items.map(e => e.fileUrl || e.file_url);
            """)


if __name__ == '__main__':
    parser = YaMusicParser()
    parser.parse('https://music.yandex.ru/artist/8855006/tracks', '_music_save_button')
