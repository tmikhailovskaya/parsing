import csv
import time
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox(
    executable_path='/home/tatiana/Рабочий стол/geckodriver/geckodriver-v0.26.0-linux64/geckodriver')

driver.get("https://amtsblatt.be.ch/#!/search/publications?filterId=3cb0327e-2236-11ea-a385-0050569db5fb")

element = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CLASS_NAME, "list-row"))
)
# pagination
###########################
SCROLL_PAUSE_TIME = 20

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
####################################

now = ((datetime.date.today() + datetime.timedelta(days=-14)).strftime("%d.%m.%Y"))
count = 0
times, contents, hrefs = [], [], []

for option in driver.find_elements_by_class_name("publication-info"):

    date_1 = datetime.datetime.strptime(option.text[:10], '%d.%m.%Y')
    date_2 = datetime.datetime.strptime(now, '%d.%m.%Y')
    if (date_1 - date_2).days <= 14 and (date_1 - date_2).days >= 0 :
        times.append(option.text[:10])

        contents.append(driver.find_elements_by_class_name("list-col-highlighted")[count].text)

        hrefs.append(driver.find_element_by_link_text(
            driver.find_elements_by_class_name("list-col-highlighted")[count].text).get_attribute("href"))

        count += 1

driver.quit()

betrifft, rubrik, unterrubrik, veröffentlichungsdatum, publizierende_stelle, meldungsnummer, sprache, kanton = [], [], [], [], [], [], [], []
i = 0
while i < count:
    p = webdriver.Firefox(
        executable_path='/home/tatiana/Рабочий стол/geckodriver/geckodriver-v0.26.0-linux64/geckodriver')
    p.get(hrefs[i])

    elements = WebDriverWait(p, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "field-value"))
    )
    betrifft.append(p.find_element_by_class_name("field-value").text)
    date = (p.find_elements_by_tag_name("dd"))
    rubrik.append(date[0].text)
    unterrubrik.append(date[1].text)
    veröffentlichungsdatum.append(date[2].text)
    publizierende_stelle.append(date[3].text)
    meldungsnummer.append(date[4].text)
    sprache.append(date[5].text)
    kanton.append(date[6].text)

    p.quit()
    i += 1

myData = [["content", "href", "time", "rubrik", "unterrubrik", "veröffentlichungsdatum", "publizierende_stelle",
           "meldungsnummer", "sprache", "kanton"]]

i = 0
while i < len(times):
    data = []
    data.append(contents[i])
    data.append(hrefs[i])
    data.append(times[i])
    data.append(rubrik[i])
    data.append(unterrubrik[i])
    data.append(veröffentlichungsdatum[i])
    data.append(publizierende_stelle[i])
    data.append(meldungsnummer[i])
    data.append(sprache[i])
    data.append(kanton[i])
    myData.append(data)
    i += 1

myFile = open('data.csv', 'w')
with myFile:
    writer = csv.writer(myFile)
    writer.writerows(myData)
