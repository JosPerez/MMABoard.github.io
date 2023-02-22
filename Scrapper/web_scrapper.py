from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
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

# Find all the rows in the table that contain fighter data
fighters = []
for row in athletes:
    # Extract the fighter's name
    name = row.find("span", {"class": "c-listing-athlete__name"}).text.strip()

    # Extract the fighter's weight class
    weight_class = row.find("div", {"class": "field field--name-stats-weight-class field--type-entity-reference field--label-hidden field__items"}).find("div", {"field__item"}).text.strip()

    # Extract the figther's record
    record = row.find("span", {"class": "c-listing-athlete__record"}).text.strip()

    # Add the fighter data to the list of fighters
    fighters.append({"Name": name, "Weight Class": weight_class, "Record": record})

print(fighters)
# Convert the list of fighters to a pandas DataFrame
df = pd.DataFrame(fighters)

# Write the DataFrame to an Excel file
df.to_csv("ufc_spanish_fighters_update.csv", index=False)

# read the two excel files into pandas dataframes
df1 = pd.read_csv('ufc_spanish_fighters_update.csv')
df2 = pd.read_csv('fighters.csv')

# get the data that is in file1 but not in file2
added = pd.concat([df1, df2]).drop_duplicates(keep=False)

# get the data that is in file2 but not in file1
removed = pd.concat([df2, df1]).drop_duplicates(keep=False)

# Write the DataFrame to an Excel file
added.to_csv("fighters_added.csv", index=False)
removed.to_csv("fighters_removed.csv", index=False)
df.to_csv("fighters.csv", index=False)