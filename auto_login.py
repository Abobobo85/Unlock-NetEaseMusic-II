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

    browser.add_cookie({"name": "MUSIC_U", "value": "00D7AC3E04DCA77451BD3ED4BA3C3C937DB6C141BB3DFCB059D0418A48361E3F3311E493C701B638ABBE568D4F9A398B203E33BD9C6DC4485287CDD94AB3DED9A661810479AECAD3223F84BFE961DFEEAA86DA2BDB05BCE174CB6A074D898ED13EC585D7FB2746F46F56FB59DDF1676C01341C03541BFF7329A1610E727182435C0DEF18EAFF39C8F8079CCAA1096B357AB2B8209DA274C859608F8C3D91B4FA27613187ABCEF48B774E1895011FDD04980C06C00CD86A8AC474C41DB40C1F09A83424DD83D98C63EF82A70D1118B46B69A9B68656C96ECC3364E61D4A3BA7B2316AD26D045A74F2F4A4AC4C7778320FA028BB8443B5E550CDEF952EC74407EB1BE3599C069542196ED3EFE2BF090785A1D946FA2925AC0E4A0FEB5A89E8D564AD6F2362F5CD9B95469DC5237ACB650CE6C4EC35A32E02731FC82E481CB741B93CA456F0103AEA282BA27960FA5D4153BF84884E1D617159BEF358D2974E3CF14779D4E00CE17D29DD31E829C06346847A1D3613CC59CF94D26B8B98B6EC13F85D6526F7F833B341BA8A9CD32FB4AFA201"})
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
