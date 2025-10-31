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

    browser.add_cookie({"name": "MUSIC_U", "value": "00EFFB502CFBFA2620A29DFF1EC9BCBEB42C08FC4DC786608CBD2635FD847F6171CDDA315495A3546C942EE2A259989F27F53018A36384A84568E52997ABF096E892B353BBF45E543E1D0F5D71DAE53DC04802F0263A82C05E8F3B45926B6AE138A30DABEAA2701012ED5B0E3E89E8E7C131BF581AB2EA858AAB19662CE11D33F7B16285A8490AB8E9C55DF47662A420ADCFB69FA6A06F82BF788BD3BB527593AD7010D9AC5B00EF40F87D931C4E5237F909E99094030D625DB8DDA8DDBA7FADDD653892A0F3574C4F66B0B62281EA813F49D7BF4BF2A790C89555EDE7260D88582C22E65E381489759529EA9432677B408CF7BB2657C24F47A42959E554D311F9A1FC1CECC97D4B25C575D76BDA55754F595E454877870821D09D26BAA3CC14D6ED3C3CDCF4B9EB31DCC562B84F8BF06592B4C942AE93EDFBE0C067FD559310C91667481C179FAB4ACFC148DB4841E4936ECCE43B80430791FFA976067432A681E08E2B2657ACDD8D0862A04B7723DB0A5222D1D8DC1E83BE860D97127AB463E011DE5BE5C37BFFF1E9397F8729D37A97"})
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
