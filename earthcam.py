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
else:
    chrome_options.add_argument('user-data-dir=/home/ki-lab/user-data')

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
    #link = "https://www.whatsupcams.com/en/webcams/slovenia/upper-carniola/kranjska-gora/ski-resort-kranjska-gora-vitranc-1-upper-station/"
    #link = "https://www.webcamtaxi.com/en/spain/lanzarote/lanzarote-airport.html"
    #link = "https://www.whatsupcams.com/en/webcams/st-barths/st-barths/gustavia/live-webcam-st-barth-island-fond-de-rade-french-antilles-caribbean/"
    #link = "https://www.skylinewebcams.com/de/webcam/deutschland/north-rhine-westphalia/cologne/cologne.html"
    #link = "https://www.whatsupcams.com/de/webcams/italien/trentino-sudtirol/muehlbach/gitschberg-jochtal-webcam-skiexpress-tal/#google_vignette"
    if not TESTING:
        link = '#link#'
    
    driver.set_window_position(1280, 720)
    
    # wait = WebDriverWait(driver, 10)

    try: 

        driver.get(link)

        if "earthcam.com" in link:
            element = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "video"))
            )

            WebDriverWait(driver, 20).until(
                lambda d: d.execute_script('return document.querySelector("video") && document.querySelector("video").readyState !== 0')
            )

            time.sleep(20)
            actions = ActionChains(driver)

            actions.double_click(element).perform()


            while True:
                print("still running:")
                print(driver.execute_script('return document.querySelector("video").readyState'))
                WebDriverWait(driver, 15).until(
                    lambda d: d.execute_script('return document.querySelector("video") && document.querySelector("video").readyState !== 0')
                )
                time.sleep(15)
            
        if "whatsupcams.com" in link:
            # Wait until the iframe is clickable
            iframe = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".embed-responsive iframe"))
            )

            # Click the iframe
            iframe.click()

            # Wait a short period (e.g., 0.5 seconds)
            time.sleep(20)

            # Initialize ActionChains
            actions = ActionChains(driver)

            # Perform a double-click on the iframe
            actions.double_click(iframe).perform()

            # Switch to the iframe
            driver.switch_to.frame(iframe)

            # Wait until the video element is ready within the iframe
            while True:
                WebDriverWait(driver, 15).until(
                    lambda d: d.execute_script('return document.querySelector("video") && document.querySelector("video").readyState !== 0')
                )
                print("still running")
                time.sleep(15)


        # driver.set_window_position(0, 0)
        # driver.fullscreen_window()
        
        print('Video not running!')
        
        time.sleep(5)
    
    except WebDriverException as e:
        print('Error loading page.')
        print(e)
        time.sleep(1)
        
    i = i + 1

driver.quit()
