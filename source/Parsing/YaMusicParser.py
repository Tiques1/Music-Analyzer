from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
from source.Exceptions import UnknownLink
import re


class YaMusicParser:
    """mode: simple - required any yandex music page where is list of tracks
             predefined - required /tracks url
    """
    def __init__(self, url, mode='simple'):
        self.mode = mode
        self.__url = url

        self.__save_dir = 'D:\\Music\\'
        self.__download_button = '_music_save_button'

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

    # Beware of TimeoutException
    def browse(self):
        try:
            self.browser.get(self.__url)
        except TimeoutException:
            raise TimeoutError('Current page load timeout: ', 1000)

    def get_buttons(self):
        return self.browser.find_elements(By.ID, self.__download_button)

    # Click button and download track into self.save_dir. Return album id, track id, track name
    def download(self, button) -> (str, str, str):
        # Because button will updated and I need observe it
        parent = button.find_element(By.XPATH, "./..")

        # Get album id
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
                button = parent.find_element(By.ID, self.__download_button)
                if button.text == '100%':
                    break
            except StaleElementReferenceException:
                pass

        # Album id, Track id, Track name
        return album.get_attribute('href').split('/')[4], album.get_attribute('href').split('/')[6], album.text

    # Only on album's page
    def get_artist(self):
        artname = self.browser.find_elements(By.XPATH, "//h1[@class='page-artist__title typo-h1 typo-h1_big']")[0].text
        artid = self.url.split('/')[4]
        return artid, artname

    # Only on album's page
    def get_album(self):
        pass

    # Only on label's page
    def get_label(self):
        pass

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url):
        if self._match(url):
            self.__url = url

    # check links
    def _match(self, link: str):
        modes = {'predefined': r'https://music\.yandex\.ru/artist/\d+/tracks$',
                 'simple': r'https://music\.yandex\.ru/'}

        if not re.match(modes.get(self.mode), link):
            raise UnknownLink(link, 'Please, read about modes')


def main():
    parser = YaMusicParser('https://music.yandex.ru/artist/8855006/tracks', 'predefined')
    try:
        parser.browse()
    except TimeoutError:
        return

    for elem in parser.get_buttons():
        alb, track_id, track_name = parser.download(elem)
        # writing into db
        print('id трека', track_id)
        print('название', track_name)
        print('id альбома', alb, end='\n\n')

    # Get list of links from db
    links = ('https://music.yandex.ru/album/20307442/track/98072491', )
    for link in links:
        parser.url = link
        try:
            parser.browse()
        except TimeoutException:
            return


if __name__ == '__main__':
    """ Есть два способа парсинга:
            Первый - просто скачать треки. Тогда подойдет любая ссылка на яндекс музыку, где есть
                список треков.
            Второй - парсинг по предопределенному сценарию:
            
        Предопределенный сценарий состоит из двух этапов:
            1. Загрузка треков по ссылке вида https://music.yandex.ru/artist/artist_id/tracks
            2. Догрузка информации по ссылке вида https://music.yandex.ru/album/album_id/track/track_id
            
            Пример:
                parser = YaMusicParser('https://music.yandex.ru/artist/8855006/tracks', 'predefined')
                try:
                    parser.browse()
                except TimeoutException:
                    return
            
                for elem in parser.get_buttons():
                    alb, track_id, track_name = parser.download(elem)
                    # writing into db
                    
                    
                   
        
        
    """

    main()
