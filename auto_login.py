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

    browser.add_cookie({"name": "MUSIC_U", "value": "00BD3D5DA171CDF88976BFA158363D20F5E47FA8205E4B0002A22D3FBE4E0B04A495B63EA20A27641658EC17EE758E1F665C6F5F5EB197DD424369FFE55935B1AA0CA560EAA545ACDFDFF95402A563CD0A2525EAE328F30485864EFD08307331ACCF0B8FEFC4B9BE3C4D1D2740915425194AEE46FC7213AD587A8FBFE4DB4CBE5671320EAC619C80644113F5A8CDD8774938E7CB84627AB7649BE9FC130241EDC02B33CA2AC3D0BE623D026323095ED1B40902C16D32DB9353436AA1E3E8E540AF6CFAE4B8C6F853E3A8A23DD6ADC82B2E402390CB588D9946CFDFF3870EE9817CB58E556324463D49E2467295813623D49D93A6E5BAF9375DA6BA0C5C3AF70F3E1852E0EAE50398353FB192B620BF2EB126F31FFBE8ADBEBDA951D48A8FC060861B5F10232896A629A3E084473B77312E419C4171928D0B408325A0887DFD66F49A4924D86DC9BF4135AFA53F487721EDDEDF765BDAB6B8D45C1177F757B39539"})
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
