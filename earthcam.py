TESTING = False

import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains



chrome_options = webdriver.ChromeOptions()


# Running
if not TESTING:
    chrome_options.add_argument('user-data-dir=/home/pi/.config/chromium/')

prefs = {'exit_type': 'Normal'}
chrome_options.add_experimental_option("prefs", {'profile': prefs})
chrome_options.add_argument('--disable-application-cache')
chrome_options.add_argument('--disable-session-crashed-bubble')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('--disable-web-security')
chrome_options.add_argument('--disable-application-cache')
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

if not TESTING:
    # Running
    driver = webdriver.Chrome(chrome_options=chrome_options)
else:
    # Testing
    service = ChromeService(executable_path='/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)


i = 0
while i < 30:

    link = "https://www.earthcam.com/usa/newyork/timessquare/?cam=tsrobo1"
    #link = "https://www.skylinewebcams.com/de/webcam/deutschland/north-rhine-westphalia/cologne/cologne.html"
    #link = "https://www.whatsupcams.com/de/webcams/italien/trentino-sudtirol/muehlbach/gitschberg-jochtal-webcam-skiexpress-tal/#google_vignette"
    if not TESTING:
        link = '#link#'
    
    driver.set_window_position(1280, 720)
    
    # wait = WebDriverWait(driver, 10)

    try: 

        driver.get(link)

        if "earthcam.com" in link:
            # Wait for the button to be present and clickable, then click it
            # button = WebDriverWait(driver, 20).until(
            #     EC.element_to_be_clickable((By.CSS_SELECTOR, "button.fc-button.fc-cta-do-not-consent.fc-secondary-button"))
            # )
            # button.click()

            # Wait for the element to be present
            element = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "video"))
            )

            WebDriverWait(driver, 20).until(
                lambda d: d.execute_script('return document.querySelector("video") && document.querySelector("video").readyState === 4')
            )

            actions = ActionChains(driver)

            actions.double_click(element).perform()

            while True:
                WebDriverWait(driver, 10).until(
                    lambda d: d.execute_script('return document.querySelector("video") && document.querySelector("video").readyState === 4')
                )
                print("still running")
                time.sleep(10)
            
            # driver.execute_script("""
            #     var sheet = window.document.styleSheets[0];
            #     sheet.insertRule('body * { display: none !important; }', sheet.cssRules.length);
            #     sheet.insertRule('video { display: block !important; }', sheet.cssRules.length);
            # """)


            # # Add multiple CSS rules to the element
            # driver.execute_script("""
            #     var sheet = window.document.styleSheets[0];
            #     sheet.insertRule('body * { display: none !important; }', sheet.cssRules.length);
                

            #     var element = arguments[0];
            #     document.body.appendChild(element);
            #     element.style.cssText += 'display: block !important; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 9999999999999999999999999;';

            #     document.body.parentElement.style.cssText += 'min-height: 0 !important;'
            #     document.body.style.cssText += 'overflow: hidden !important; height: 100vh !important;'
            # """, element)



        # time.sleep(5)

        # driver.set_window_position(0, 0)
        # driver.fullscreen_window()
        
        print('Video not running!')
        
        time.sleep(1)
    
    except WebDriverException as e:
        print('Error loading page.')
        print(e)
        time.sleep(1)
        
    i = i + 1

driver.quit()
