import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, \
    ElementClickInterceptedException
import os
from Exceptions import UnknownLink, WrongLink
import re
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

"""
В браузере должно быть установлено расширение https://chromewebstore.google.com/detail/
%D1%81%D0%BA%D0%B0%D1%87%D0%B0%D1%82%D1%8C-%D0%BC%D1%83%D0%B7%D1%8B%D0%BA%D1%83/hfofhoffdcfcjgmilkpnhkamcgemaban
А также выполнен вход в яндекс музыку

Стандартный цикл работы выглядит следующим образом
    parser = YaMusicParser()
    parser.save_dir = 'D:\\Music\\'
    parser.profile = 'Default'
    parser.user_data = r'C:\\Users\\Сергей\\AppData\\Local\\Google\\Chrome\\User Data'
    
    parser.start()
    # Parsing
    parser.close()
    
Парсить можно как отдельные треки, так и альбомы, артистов, лейблы
    browse(url, timeout=None) -> None
        Открывает переданную ссылку в текущей вкладке.
        Если установлен timeout для загрузки страницы, после истечения времени будет выброшено исключение TimeoutError
        
    get_buttons() -> (WebElement, )
        Возвращает кортеж кнопок для скачивания на открытой странице
        
    donwload(button) -> album_id, track_id
        Скачивает трек на открытой странице, кнопку для скачивания которого передали, в папку save_dir
            и возвращает id трека и id альбома, благодаря которым позднее можно будет допарсить всю необходимую 
            информацию
        Во время скачивания лучше не трогать скролбар и поменьше активничать на странице, чтобы не помешать корректной
            работе парсера
        
    get_track() -> artists_id, name, number_in_album
        Используется исключительно вместе со ссылкой вида /album/album_id/track/track_id
    
    get_album() -> cover, name, year, genres, artists_id, label_id
        Используется со ссылками вида /album/album_id и /album/album_id/track/track_id
        
    get_artist() -> name, avatar
        Используется со ссылками вида /artist/artist_id
        
    get_label() -> name
        Используется со ссылками вида /label/label_id
"""


class YaMusicParser:

    def __init__(self):
        # You must use format like this 'D:\\Music\\'
        self.__save_dir = None
        self.profile = 'Default'
        self.user_data = r'C:\Users\Сергей\AppData\Local\Google\Chrome\User Data'

        self.__browser = None

        self.__method = None

    def start(self):
        opt = webdriver.ChromeOptions()
        prefs = {
            "download.default_directory": f'{self.__save_dir}',
            "download.prompt_for_download": False,
            "download.directory_upgrade": True
        }
        opt.add_experimental_option("prefs", prefs)
        opt.add_argument(f'--profile-directory={self.profile}')
        opt.add_argument(f'--user-data-dir={self.user_data}')
        # opt.add_argument("--disable-dev-shm-usage")  # Отключение использования /dev/shm
        # opt.add_argument("--remote-debugging-port=15000")  # Указание порта для удаленной отладки
        # opt.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

        # opt.add_extension('..\\..\\resources\\HFOFHOFFDCFCJGMILKPNHKAMCGEMABAN_2_0_8_0.crx')
        # service=Service(ChromeDriverManager().install())
        self.__browser = webdriver.Chrome(options=opt)

    def close(self):
        self.__browser.quit()

    @property
    def save_dir(self):
        return self.__save_dir

    @save_dir.setter
    def save_dir(self, directory):
        if os.path.exists(directory):
            self.__save_dir = directory
        else:
            raise FileNotFoundError

    # If set timeout, beware TimeoutError
    def browse(self, url, timeout: int = None):
        self._check(url)
        if self.__browser.current_url == url:
            return 1
        if timeout is not None:
            self.__browser.set_page_load_timeout(timeout)
        try:
            self.__browser.get(url)
        except TimeoutException:
            return
        time.sleep(0.5)
        return self.__method

    def get_buttons(self):
        return self.__browser.find_elements(By.ID, '_music_save_button')

    # Click button and download track into self.save_dir. Return track info
    def download(self, button):
        # Because button will updated and I need observe it
        parent = button.find_element(By.XPATH, "./..")

        # Get album id, it needs to further parsing
        album = None
        while True:
            try:
                album = parent.find_element(By.XPATH, "./../a[@class='d-track__title deco-link deco-link_stronger']")
            except Exception:
                continue
            break

        # Don't touch scrollbar motherfuckers
        # If you touch scrollbar, you will fuck

        # Start download
        while True:
            try:
                button.click()
            except ElementClickInterceptedException:
                continue
            break

        # Waiting for download
        while True:
            try:
                button = parent.find_element(By.ID, '_music_save_button')
                if button.text == '100%':
                    break
            except StaleElementReferenceException:
                pass

        self.__browser.execute_script("arguments[0].scrollIntoView();", button)
        # Album id, Track id
        return album.get_attribute('href').split('/')[4], album.get_attribute('href').split('/')[6]

    # Only with link like /album/album_id/track/track_id
    def get_track(self, id_):
        if self.__method != 'track':
            raise WrongLink('Link must look like /album/album_id/track/track_id')

        sidebar = self.__browser \
            .find_element(By.CSS_SELECTOR, "div[class^='sidebar__info']")
        artist_list = sidebar.find_element(By.CSS_SELECTOR, "span[class^='d-artists']")
        artist_list = artist_list.find_elements(By.TAG_NAME, "a")

        artists_id = []
        for artist in artist_list:
            artists_id.append(artist.get_attribute('href').split('/')[4])

        # name = self.__browser.find_elements(By.XPATH, "//div[@class='d-track__name']")

        numbers = self.__browser.find_elements(By.CSS_SELECTOR, "div[class^='d-track typo-track d-track_selectable']")
        number = 0
        for num in numbers:
            if num.get_attribute('data-item-id') == id_:
                number = num.get_attribute('data-id')
                name = num.find_element(By.CSS_SELECTOR, "div[class^='d-track__name']").get_attribute('title')
                break

        return artists_id, name, number

    # Only on album's page
    def get_album(self):
        if self.__method not in ('album', 'track'):
            raise WrongLink('Link must look like /album/album_id/track/track_id or /album/album_id')

        try:
            cover = self.__browser.find_element(By.XPATH, "//img[@class='entity-cover__image deco-pane']") \
                .get_attribute('src')
        except:
            cover = None

        information_div = self.__browser.find_element(By.XPATH, "//div[@class='d-generic-page-head__main-top']")
        name = information_div.find_element(By.XPATH, "//span[@class='deco-typo']").text
        # is_single = information_div.find_element(By.XPATH, "//span[@class='stamp__entity']").text
        year = information_div.find_element(By.XPATH, "//span[@class='typo deco-typo-secondary']").text

        genres = []
        for g in information_div.find_elements(By.XPATH, "//a[@class='d-link deco-link deco-link_mimic typo']"):
            genres.append(g.text)
        genres = ';'.join(genres)

        artists_id = []
        span = information_div.find_element(By.XPATH, "//span[@class='d-artists']")
        for a in span.find_elements(By.TAG_NAME, 'a'):
            artists_id.append(a.get_attribute('href').split('/')[4])

        label_id = []
        label_div = self.__browser.find_element(By.XPATH, "//div[@class='page-album__label']")
        for lbl in label_div.find_elements(By.XPATH,
                                           "//a[@class='d-album-summary__group d-album-summary__item typo-disabled']"):
            label_id.append(lbl.get_attribute('href'))

        return cover, name, year, genres, artists_id, label_id

    # Only on artist page
    def get_artist(self):
        if self.__method != 'artist':
            raise WrongLink('Link must look like /artist/artist_id')

        try:
            name = self.__browser.find_element(By.XPATH, "//h1[@class='page-artist__title typo-h1 typo-h1_big']").text
        except:
            try:
                name = self.__browser.find_element(By.XPATH, "//h1[@class='page-artist__title typo-h1 typo-h1_small']") \
                    .text
            except:
                name = ''

        # try:
        #     avatar = self.__browser.find_element(By.XPATH, "//img[@class='artist-pics__pic']") \
        #         .get_attribute('src')
        # except Exception:
        #     avatar = None

        return name

    # Only on label's page
    def get_label(self):
        if self.__method != 'label':
            raise WrongLink('Link must look like /label/label_id')

        name = self.__browser.find_element(By.XPATH, "//div[@class='page-label__title']") \
            .find_element(By.TAG_NAME, "h1").text

        return name

    # Every function will work only if __method has correspondig value
    def _check(self, url):
        method = None
        for pattern in LINKTYPE.keys():
            if re.match(pattern, url):
                method = LINKTYPE.get(pattern)
        if method is None:
            raise UnknownLink(url)
        self.__method = method

    def __del__(self):
        self.__browser.close()


LINKTYPE = {
    r'https://music\.yandex\.ru/album/(\d+)/track/(\d+)$': 'track',
    r'https://music\.yandex\.ru/artist/(\d+)$': 'artist',
    r'https://music\.yandex\.ru/album/(\d+)$': 'album',
    r'https://music\.yandex\.ru/label/(\d+)$': 'label',
    r'https://music\.yandex\.ru/artist/(\d+)/tracks$': 'track'
}
