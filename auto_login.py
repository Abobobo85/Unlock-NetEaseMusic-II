# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")

    browser.add_cookie({"name": "MUSIC_U", "value": "00625064AFF62FB790459F63BEF7FF4897A908516A35CBB688E34B73CEF6370879E9D996D7E919F0BED35B474495B756EDDCA773E36FBF6BB1765C5A94B1D3605E968BF4B4F9B58CE9DD1B672CAAE19D360FF148D42677826DDC1B17F684A4DD13FAC4620AFA2C02F958BBDBDA6F39C2E96F6C985BC4B1C416CD0E818728193919C1AFFAEF90F761C1F697C2E17F108D78253AA563A5AE380DD433C31944381CA3694815CB4B6FE945E8B0ED56883D69813BC6EF6F3695180F141CF1044864D93187DC585AC657E8EB88CF11420191059AFA4E50CCDA01FF2FC8A4E3E1547A4D6179319B0B2BB93E3F037DE8C0EAA16AE7770BE4B8B4C403389FEB44FFC08733DF3A632F6EBED1BCCC366ECE5D3423B2CD7E253075CE6CC2DAFC1BA25993AEAD79DBDD5815F254CF387C4DB8F0960B07961F4DD306AF72A1B20219CD98CF9314644049FA49FCDC0104A8205159A0CA6CD572D713708B18C867DB7777B0CDD860D0"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
