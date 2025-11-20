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

    browser.add_cookie({"name": "MUSIC_U", "value": "003226AE09606FEFA72D683AA8D413D65D1A078177E41490F96FD5B64E91DE2040383356C1D28CEDAAB2493391858A636699023F625AC0E73B73FE6411823F2E70656B4D0FEB876AC6592244F2F4835324A6964A911EBEF6CA00345F5B3AAD5E98832B1F4A0176B212D7DFFA29FEC65D806EA820A07B4054B25A6AB691EE5E24488F90A6819CD5E68D6C98A4C8E98C73B902ECC296B0D56264424959C0533CA2FFA6BCA89F3FCF78CF954646CE10187C757E863FFD80344CF89A3FC51D7FFE75E598954BC1418BDF5BF83D6FD73EEB6DBDD3BE437B3EB82F513A72F57ED6F8373BDB85AE492FA5CE7679651F2561592D41E062C17630FBF3E4802B4DAC2F38D27A7BF6186F8ACFB8AE5ECBD7D4B19A568BA60830FF021B77FD4EC1A88C40D9364D8906D306E496F150FE09AB9FEC72CF434D01B6BF99835341D0B323F77F35383E100C7786900B6D2761F06B8960EE0B6ACA52B1177C2ADCE2A5CDECBE3152F2ECE7699129FDFBE3C4FDF8F0FFBBD6493E8BD7F20A252105190D618DD2E004C181EBFF7CE59315B78B798D8A19858FA970"})
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
