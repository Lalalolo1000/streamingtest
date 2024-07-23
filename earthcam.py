TESTING = False

import sys
import time
import pathlib

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService


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
while i < 3:

    #link = "https://www.earthcam.com/usa/tennessee/nashville/?cam=nashville"
    #link = "https://www.skylinewebcams.com/de/webcam/deutschland/north-rhine-westphalia/cologne/cologne.html"
    #link = "https://www.whatsupcams.com/de/webcams/italien/trentino-sudtirol/muehlbach/gitschberg-jochtal-webcam-skiexpress-tal/#google_vignette"
    if not TESTING:
        link = '#link#'
    else:
        link = "https://www.earthcam.com/usa/tennessee/nashville/?cam=nashville"
    driver.set_window_position(1280, 720)
    
    wait = WebDriverWait(driver, 10)


    try: 

        driver.get(link)

        
        if "earthcam.com" in link:
            # Wait for the button to be present and clickable, then click it
            button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.fc-button.fc-cta-do-not-consent.fc-secondary-button"))
            )
            button.click()

            # Wait for the element to be present
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "video"))
            )

            # Add multiple CSS rules to the element
            driver.execute_script("""
                var element = arguments[0];
                document.body.appendChild(element);
                element.style.cssText += 'position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 9999999999999999999999999;';

                document.body.parentElement.style.cssText += 'min-height: 0 !important;'
                document.body.style.cssText += 'overflow: hidden !important; height: 100vh !important;'
            """, element)


        if "skylinewebcams.com" in link:
            # Wait for the button to be present and clickable, then click it
            button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.fc-button.fc-cta-consent.fc-primary-button"))
            )
            button.click()


            playerbutton = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".player-poster.clickable"))
            )

            # Wait for the element to be present
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "video"))
            )

            playerbutton.click()

            driver.execute_script("""
                var element = arguments[0];
                document.body.appendChild(element);
                element.style.cssText += 'position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 9999999999999999999999999;';

                document.body.style.cssText += 'overflow: hidden !important; height: 100vh !important;'
            """, element)


        # if "whatsupcams.com" in link:
        #     # Wait for the button to be present and clickable, then click it
        #     button = WebDriverWait(driver, 20).until(
        #         EC.element_to_be_clickable((By.CSS_SELECTOR, "button.fc-button.fc-cta-consent.fc-primary-button"))
        #     )
        #     button.click()

        #     # Wait until the iframe with the specified CSS selector is present
        #     iframe_css_selector = "iframe.embed-responsive-item.home-page-webcam-container"
        #     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, iframe_css_selector)))

        #     # Grab the URL from the iframe
        #     iframe_element = driver.find_element(By.CSS_SELECTOR, iframe_css_selector)
        #     driver.switch_to.frame(iframe_element)


        #     driver.execute_script("""
        #         var element = document.querySelector('video');
        #         document.body.appendChild(element);
        #         element.style.cssText += 'position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 9999999999999999999999999;';

        #         document.body.style.cssText += 'overflow: hidden !important; height: 100vh !important;'
        #     """)

        #     # driver.switch_to.default_content()

        #     driver.execute_script("""
        #         var element = arguments[0];
        #         document.body.appendChild(element);
        #         element.style.cssText += 'position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 9999999999999999999999999;';

        #         document.body.style.cssText += 'overflow: hidden !important; height: 100vh !important;'
        #     """, iframe_element)

        time.sleep(5)

        driver.set_window_position(0, 0)
        driver.fullscreen_window()
        
        time.sleep(120)
        
        print('Video not running!')
        
        time.sleep(5)
    
    except WebDriverException as e:
        print('Error loading page.')
        print(e)
        time.sleep(1)
        
    i = i + 1

driver.quit()
