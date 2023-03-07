from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import re
from bs4 import BeautifulSoup

# Set the URL for the UFC Spanish athlete directory page
url = "https://www.ufcespanol.com/athletes/all?filters[0]=status:23"
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=options)
driver.get(url)

while True:
  try:
    # wait for the button to become clickable
    wait = WebDriverWait(driver, 3)
    button  = wait.until(EC.presence_of_element_located((By.XPATH, '//ul[@class="js-pager__items pager"]//a[@class="button"]')))
    # click the button
    button.click()
    # wait for the page to load
    time.sleep(2)
  except:
    print("Last Touch find it")
    break



# get the updated HTML content
html = driver.page_source

# parse the HTML with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Find the table that contains the fighter data
athletes = soup.find_all('div', {'class': 'c-listing-athlete-flipcard__front'})
athletes_back = soup.find_all('div', {'class': 'c-listing-athlete-flipcard__back'})
# Find all the rows in the table that contain fighter data
fighters = []
for index, row in enumerate(athletes):
    # Extract the fighter's name
    name = row.find("span", {"class": "c-listing-athlete__name"}).text.strip()

    # Extract the fighter's weight class
    weight_class = row.find("div", {"class": "field field--name-stats-weight-class field--type-entity-reference field--label-hidden field__items"}).find("div", {"field__item"}).text.strip()

    # Extract the figther's record
    record = row.find("span", {"class": "c-listing-athlete__record"}).text.strip()

    # Extract the figther's nickname
    nickname = row.find("span", {"class": "c-listing-athlete__nickname"}).text.strip()

    # Extract the figther's uri
    uri = athletes_back[index].find("a", {"class": "e-button--black"}).get('href')

    # Add the fighter data to the list of fighters
    words = name.split()
    first_name = words[0]
    pattern = r'^[a-zA-Z]+$'
    last_name = ""
    if len(words) > 1:
      if re.match(pattern, words[1]):
        last_name = words[1]
    fighter = {"first_name": first_name,
               "last_name": last_name,
               "nickname": nickname ,
               "weight_class": weight_class,
               "record": record,
               "uri":uri}
    print("\n", fighter, "\n")
    fighters.append(fighter)


# Convert the list of fighters to a pandas DataFrame
df = pd.DataFrame(fighters)

# Write the DataFrame to an Excel file
df.to_csv("ufc_spanish_fighters_update.csv", index=False)