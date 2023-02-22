from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
from bs4 import BeautifulSoup

# Set the URL for the UFC Spanish athlete directory page
url = "https://www.espn.com.mx/mma/fightcenter"
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=options)
driver.get(url)

# get the updated HTML content
html = driver.page_source

# parse the HTML with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

eventHeader = soup.find('div', {'class': 'MMAEventHeader__Event'})
eventDropDown = eventHeader.find_all('div', {'class': 'dropdown'})
eventSelect = eventDropDown[-1].find('select', {'class': 'dropdown__select'})
events = eventSelect.find_all('option')
events.pop(0)
eventsStr = []
eventsUrl = []
for event in events:
  eventsUrl.append(event['data-url'])

print(eventsUrl)

for event in eventsUrl:
  driver.get(f"https://www.espn.com.mx{event}")
  soup = BeautifulSoup(driver.page_source, 'html.parser')
  header = soup.find('div', {'class': 'MMAEventHeader__Event'})
  title = header.find('h1', {'class': 'headline'})
  date = header.find('div', {'class': 'n6 mb2'})
  place = header.find('div', {'class': 'n8'})
  eventsStr.append({"Event": title.text.strip(),"Date": date.text.strip(), "Place": place.text.strip()})
# Convert the list of fighters to a pandas DataFrame
df = pd.DataFrame(eventsStr)

# Write the DataFrame to an Excel file
df.to_csv("ufc_events.csv", index=False)
