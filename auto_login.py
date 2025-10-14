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

    browser.add_cookie({"name": "MUSIC_U", "value": "001933834CAA0D40ED485F011986FC7E406F776467E3DD6FAD8C382DA3B9D1A2366C234FC61003A9D9C1E80C1F1E32E2A788A8087B292E1BA06CEC6BAFFDCDF804AEA066533590DD553CB4BDC27560023A1348AB56F9BA87EAB8E32BDE1A5DF4192EF6E52D185EF72E1F19860C6F592AFD1836050B17C2BB1D12E75989054AE44BBBE92FDB879847355F5584D5951EF700B16A138018FF91CB348199EC7FEE41CB5C1235C06F342D92E5CF1EBAEC922DD3F767D15050B17C02A2406C61373366DEEDAA67A0FEE0875D8154A5BC85B0CB59BCEA33D6D0801BFB0045A66E7380CF448E82E4AF113CE7CEBEF907CB55FD85CEC05090D323FDBA96BB10CC51F2F80062D9A9938562D9B61B6456A71262EFB761249A000604F2206021C1F67EB0C3FFD2616C8394FB6EB7F2C134DC920F6856A305A72CE14D66807971F24292362964BF614990D837DCF6F25DDFB8120F11F73720AC5768F434FEF70B6B7B02AB9CC919DF6487D2A1D7052D538F41D593C4ED58E067CB60389B8AC799140464AF22A08058308692B57EC3F76AAC6421B71781C0"})
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
