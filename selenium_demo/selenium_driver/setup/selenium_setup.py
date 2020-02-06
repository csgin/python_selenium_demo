from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging
import datetime



def return_driver():
    global driver
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("--window-size=1920,1080")
    d = DesiredCapabilities.CHROME
    d['loggingPrefs'] = {'browser': 'ALL'}
    driver = webdriver.Chrome(
        r"C:\Users\x2x\Desktop\selenium demo\selenium_demo\selenium_driver\setup\chromedriver.exe",
        desired_capabilities=d, options=options)
    return driver


def chrome_handler(test):
    global driver
    driver = return_driver()
    driver.get("https://www.booking.com/")

    levels = ['browser', 'driver']

    gather_logs(str(test.__name__))

    try:
        test()
        for i in levels:
            for entry in driver.get_log(i):
                print(entry)
        driver.quit()
    except Exception as e:
        print(e)
        now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        driver.save_screenshot(
            fr'C:\\Users\\x2x\Desktop\\selenium demo\\selenium_demo\\logs\\{str(test.__name__)}-%s.png' % now)
        for i in levels:
            for entry in driver.get_log(i):
                print(entry)
        driver.quit()

def browser():
    global driver
    return driver

def gather_logs(filename):
    logging.basicConfig(filename=fr'C:\\Users\\x2x\\Desktop\\selenium demo\\selenium_demo\\logs\{filename}.log',
                        format = '%(asctime)s: %(levelname)s: %(message)s',
                        datefmt = '%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
