from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def return_driver():
    global driver
    options = Options()
    options.add_experimental_option('prefs', {'intl.accept_languages': 'English-US'})
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--lang=en-us')
    driver = webdriver.Chrome(
        r"C:\selenium demo\selenium_demo\selenium_driver\setup\chromedriver.exe")  # , options=self.options)
    return driver

def browser():
    global driver
    return driver