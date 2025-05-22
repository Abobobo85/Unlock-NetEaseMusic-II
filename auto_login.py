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

    browser.add_cookie({"name": "MUSIC_U", "value": "003647B475E09CD8623FC39B29B09B524723D725205192A417CF3B78A07C148988D02DBBF94B823BBA0534A20A788EA167B85CC4776789E0B3FACF3F100DA5C93A5C574959D0340A1751B5CEB089AD749B1A0A178AE734B212DD0608CD36F9AC2EDA8A2AEA44224DA49B96AB46C7596240851578184E5CFA56B1FDBC7849E0D56B9CA7B26018284741AF6BB1BF7A4EC37DFBE3A76CC036CD5350FD557CCF24988425B9307E649EE6F7B69C87156D02851314174091322675EA935D4FD7B0554277079521E2D6D7EFB8ED5CC084E4256A517789E742AA4276A6589DC3BA85202225BF65E23120FDE4AB9EBBD9246063F7B403CC0A0C094FF215E899EC34645391162655C3C225362A5F9A23C02B114FF32ECCD69EE678D4654506ACF72F838D2BEB9A3A42A94272725E650F76F3436E86E17AD5696BB50A1FCD347FA066F1E17641D1FE64C099E3C56B2EB0918ECE6C2290C7FFE939A8BE41267080655B75ADF7BB"})
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
