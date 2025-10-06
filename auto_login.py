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

    browser.add_cookie({"name": "MUSIC_U", "value": "005EABC31DA0B576860F3A973DED3EADE5F4B80F7AE5D44806E06234A9725B165E277F2D0DC527D7811D95EBE7C6036E59687072C9287357DA5FE1F74E923CD5C0C7F0FE37BB80E12446BA50290004D328C240ABBDEF9D3EB2D21AA7F33C838ACA98C1571943425154E085653F9F9B42C9B13D5DD46AFB53C9E7EA331859AF0A3FEFC9D1348042630EE0C9247095DC363633575CE043653AFFA96B4EDE7A6B4F0350E06DEBDB2A404BE6730E2C048920C8E6522DF2862B2865643CFC04B3584D4BB419232725BE75560EB70ACABC731203FA8F1071B0E8E9BC416A23DB23499BDA2D00B5312077FA803B78F88385822945825F247A0C96D7B47A34770E4598D4FBAB720B89E43BB6229DBA2C5FDE3BAD0211A71323546206B1D45C9E913D4455A2AA6E4DB84052FA593EDB3305C8F432470FCFAB260CF7DA6B4C624D07919FF3FA5333A089EB8C6E8BBEFCF9632AEC6906CBABA92A8729DC48953D6FF8DF3F12C80E6A230FEEFEAB3230C6C5BB2928AB3842B1A874F3C4B3B30E8BD6EA73D369CFE1A91AC3C969BCFEFE297286E2C70CC2"})
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
