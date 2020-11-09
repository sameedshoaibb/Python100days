from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
browser = webdriver.Chrome(executable_path="./drivers/chromedriver")
browser.get('https://hypeauditor.com/login/?r=app/redirect')


username = browser.find_element_by_id("email")
password = browser.find_element_by_id("password")

username.send_keys("boxetiv149@appnox.com")
password.send_keys("boxetiv149@appnox.com")

browser.find_element_by_class_name('button-block').click()
list_of_influencers = ['linaderman','piperoninsta','natia_natsi','yaseminxkaradag','tesdress','hijab_by_turkey','muslimawear']
for i in list_of_influencers:
    browser.get('https://app.hypeauditor.com/preview/{}'.format(i))
# browser.get('https://app.hypeauditor.com/preview/natia_natsi')

    html_source = browser.page_source
    print (i)
    with open('dog_breeds_reversed.txt', 'w') as writer:
        writer.write(html_source)
        
    with open('dog_breeds_reversed.txt', 'r') as reader:
        line = reader.readline()
        while line != '':  # The EOF char is an empty string
            line = reader.readline()
            if "kyb-user-info-v2__sub-title" in line:
                a = line.split(">")[1]
                b = a.split("<")[0]
                print(b)
