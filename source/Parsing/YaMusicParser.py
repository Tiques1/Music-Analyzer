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
        # self.opt.add_extension('..\\..\\resources\\HFOFHOFFDCFCJGMILKPNHKAMCGEMABAN_2_0_8_0.crx')

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

    # Click button and download track into self.save_dir. Return album id, track id
    def download(self, button) -> (str, str):
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
        return album.get_attribute('href').split('/')[4], album.get_attribute('href').split('/')[6]

    # Only with link like /album/album_id/track/track_id
    def get_track(self):
        side_bar = self.browser.find_element(By.XPATH, "//div[@class='sidebar__placeholder sidebar__sticky']")
        span = side_bar.find_element(By.XPATH, "//span[@class='d-artists']")
        artist_list = span.find_elements(By.XPATH, "//a[@class='d-link deco-link']")
        artists = []
        for artist in artist_list:
            artists.append(artist.get_attribute('href').split('/')[4])

        name = self.browser.find_element(By.XPATH, "//div[@class='d-track__name']").get_attribute('title')

        album_num = self.browser.find_element(By.XPATH, "//div[@class='d-track typo-track d-track_selectable"
                                                        " d-track_inline-meta _music_ready']").get_attribute('data-id')
        return artists, name, album_num

    # Only on album's page
    def get_album(self):
        cover = self.browser.find_element(By.XPATH, "//img[@class='entity-cover__image deco-pane']")\
            .get_attribute('src')

        information_div = self.browser.find_element(By.XPATH, "//div[@class='d-generic-page-head__main-top']")
        name = information_div.find_element(By.XPATH, "//span[@class='deco-typo']").text
        is_single = information_div.find_element(By.XPATH, "//span[@class='stamp__entity']").text
        year = information_div.find_element(By.XPATH, "//span[@class='typo deco-typo-secondary']").text

        genre = []
        for g in information_div.find_elements(By.XPATH, "//a[@class='d-link deco-link deco-link_mimic typo']"):
            genre.append(g.text)

        artists = []
        for a in information_div.find_elements(By.XPATH, "//a[@class='page-album__artists-short']"):
            artists.append(a.get_attribute('href').split('/')[4])

        label = []
        label_div = self.browser.find_element(By.XPATH, "//div[@class='page-album__label']")
        for lbl in label_div.find_elements(By.XPATH, "//a[@class='d-link deco-link']"):
            label.append(lbl.get_attribute('href'))

        return cover, name, is_single, year, genre, artists, label

    # Only on artist page
    def get_artist(self):
        name = self.browser.find_element(By.XPATH, "//h1[@class='page-artist__title typo-h1 typo-h1_big']").text
        try:
            avatar = self.browser.find_element(By.XPATH, "//img[@class='artist-pics__pic']") \
                .get_attribute('src')
        except:
            avatar = self.browser.find_element(By.XPATH, "//img[@class='artist-pics__pic artist-pics__pic_empty']") \
                .get_attribute('src')

        return name, avatar

    # Only on label's page
    def get_label(self):
        name = self.browser.find_element(By.XPATH, "//div[@class='page-label__title']")\
            .find_element(By.TAG_NAME, "h1").text

        return name

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
    links = ('https://music.yandex.ru/album/20448306/track/98462689', )
    for link in links:
        parser.url = link
        try:
            parser.browse()
            tracks = parser.get_track()
            for track in tracks:
                # writing in db track information
                pass
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
