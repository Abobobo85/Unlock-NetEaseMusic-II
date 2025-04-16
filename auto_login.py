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
    
    browser.add_cookie({"name": "MUSIC_U", "value": "00100BF6D2400B0C4ECA80443964F2886CF57167900BD8A2490235A9863A0F46795CAA267EE053AFB31861C792098025738089C2461C4DE05390845574CC94BCC631281010D991BB43774AF59828AAEA837DEB087E0EE69FD7732AD6207665B916650B74AAF6B952C5F333F26F3DC855DE13022C5FF47AD770DC94985E330A6429C286AD6C4455AF17474F6B324021C3C29154757215BC968A8305622797BCDCFD2A64250CC0A1C0F3987EC22B1895DE2EBF6FD79184A82E77BDE65022A9EB65776AB7C6D73241674634589FA04288E13B90C0FFF3DFFA900D394AEAEAC667674EBE1B8F57A8D033C4431AE03DA089480390472CB0D345CCA6668A4DC2AED57C032149C3B58393251F5963D73FE7CE59D048F2198FE3036E18281BF85514460F6CB1F205BE7936B3C0CC19428FEC1A8F4F9452AF382840FB64DA40EC0FC6B5845BCD547AF332971C64FE01A2E82AD64A72F37C7E205D39E6FB4CFCEFAE4F08B594"})
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
