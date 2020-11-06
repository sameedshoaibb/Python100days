from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(executable_path="./drivers/chromedriver")
driver.get('https://hypeauditor.com/login/?r=app/redirect')
#browser = webdriver.Chrome(executable_path="./drivers/chromedriver")
#browser.get('https://hypeauditor.com/preview/shaunylbenson')


username = driver.find_element_by_id("email")
password = driver.find_element_by_id("password")

username.send_keys("YourUsername")
password.send_keys("Pa55worD")

driver.find_element_by_class("login-form-state--link").click()

sleep(1115)
#browser.quit()
