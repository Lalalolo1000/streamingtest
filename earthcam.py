import sys
import time
import pathlib

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('user-data-dir=/home/pi/.config/chromium/')
#chrome_options.add_argument('--kiosk')
#chrome_options.add_argument('--auto-open-devtools-for-tabs')
prefs = {'exit_type': 'Normal'}
chrome_options.add_experimental_option("prefs", {'profile': prefs})
chrome_options.add_argument('--disable-application-cache')
chrome_options.add_argument('--disable-session-crashed-bubble')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('--disable-web-security')
chrome_options.add_argument('--disable-application-cache')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
# driver = webdriver.Chrome('./chromedriver.exe', chrome_options =chrome_options)
driver = webdriver.Chrome(chrome_options =chrome_options)


youtube_script = """document.body.appendChild(document.querySelector('video'));
                 document.body.style.overflowY = 'hidden';
                 document.querySelector('video').style.width = '100%';
                 document.querySelector('video').style.height = '100%';
                 document.querySelector('video').style.backgroundColor = 'black';
                 document.querySelector('ytd-app').style.display = 'none';"""

earthcam_script = """document.body.appendChild(document.querySelector('video'));
                  document.querySelector('.superWhiteWrapper').style.display = 'none';
                  document.querySelector('video').style.backgroundColor = 'black';
                  setTimeout(function () {ecnPlayerHTML5._playerArea._videoWindow._player._userIdleEventTimer.stop();}, 5000);"""

skylinewebcams_script = """document.body.appendChild(document.querySelector('video'));
                        if (document.querySelector('#trigCookie')) {
                            document.querySelector('#trigCookie').style.display = 'none';
                        }
                        document.querySelector('.header').style.display = 'none';
                        document.querySelector('.content').style.display = 'none';
                        document.querySelector('video').style.backgroundColor = 'black';
                        document.querySelector('.footer').style.display = 'none';"""

i = 0
while i < 3:
    # link = 'https://www.skylinewebcams.com/de/webcam/italia/veneto/venezia/rialto-canal-grande.html'
    # link = 'https://www.earthcam.com/usa/newyork/timessquare/?cam=tsrobo3'
    # link = 'https://www.youtube.com/watch?v=K_fq3l0Mfog'
    #link = 'https://explore.org/livecams/brown-bears/brown-bear-salmon-cam-the-riffles'

    link = '#link#'

    driver.set_window_position(1280, 720)
    
    wait = WebDriverWait(driver, 10)


    try: 

        driver.get(link)

        if 'skylinewebcams.com' in link:
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#webcam')))
            driver.find_element_by_css_selector('#webcam').click()
            time.sleep(3)
            driver.execute_script(skylinewebcams_script)

        if 'earthcam.com' in link:
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'video')))
            driver.execute_script(earthcam_script)

        if 'youtube' in link:
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'video')))
            driver.execute_script(youtube_script)

        time.sleep(5)

        driver.set_window_position(0, 0)
        driver.fullscreen_window()
        
        time.sleep(10)
        
        while True:
            driver.execute_script('if (document.querySelector(".modal")) {document.querySelector(".modal").style.display = "none";}')
            driver.execute_script('if (document.querySelector(".modal-backdrop")) {document.querySelector(".modal-backdrop").style.display = "none";}')
            if driver.execute_script('return [...document.querySelectorAll("video")].pop().readyState < 1 || [...document.querySelectorAll("video")].pop().paused == true'):
                print('Video stopped, waiting for restore.')
                time.sleep(60)
                if driver.execute_script('return [...document.querySelectorAll("video")].pop().readyState < 1 || [...document.querySelectorAll("video")].pop().paused == true'):
                    print('Video could not be restored, reloading.')
                    break
            time.sleep(5)
        
        print('Video not running!')
        
        time.sleep(5)
    
    except WebDriverException as e:
        print('Error loading page.')
        print(e)
        time.sleep(1)
        
    i = i + 1

driver.quit()
