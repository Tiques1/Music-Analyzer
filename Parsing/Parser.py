import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

opt = Options()
opt.add_experimental_option('prefs', {
    'download.default_directory': 'D:\\Music'
})

browser = webdriver.Chrome(options=opt)
browser.get('https://zaycev.net/popular/index.html?sort=month')

elements = browser.find_elements(By.XPATH, '//div[@title="Скачать трек"]')

for element in elements:
    element.click()
    time.sleep(10)

browser.quit()
