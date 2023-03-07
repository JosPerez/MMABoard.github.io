from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import re
from bs4 import BeautifulSoup

# Set the URL for the UFC Spanish athlete directory page
url = "https://www.ufcespanol.com"

df = pd.read_csv('ufc_spanish_fighters_update.csv') 

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=options)

fighters_info = []
for index, row in df.iterrows():
  uri = row['uri']
  print("Se buscan peleador en", url + uri)
  driver.get(url + uri)
  time.sleep(2)
  # get the updated HTML content
  html = driver.page_source

  # parse the HTML with BeautifulSoup
  soup = BeautifulSoup(html, 'html.parser')

  #Obtain the container for the athlete l-container stats-record-wrap
  container_record = soup.find("div", {"class": "l-container stats-record-wrap"})

  #Obtain the wins by KO and First_round_ko
  first_banner = container_record.find_all("p", {"class": "athlete-stats__stat-numb"})
  wins_by_ko = "0"
  wins_by_first_round_ko = "0"
  if first_banner:
    wins_by_ko = first_banner[0].text.strip()
    wins_by_first_round_ko = first_banner[1].text.strip()

  #Obtain significant striking data overlap-athlete-content overlap-athlete-content--horizontal
  second_banner = container_record.find("div", {"class": "overlap-athlete-content overlap-athlete-content--horizontal"})
  sig_striking_landed = "0"
  sig_striking_throw = "0"
  if second_banner:
    sig_striking = second_banner.find_all("dd", {"class": "c-overlap__stats-value"})
    if sig_striking:
      sig_striking_landed = sig_striking[0].text.strip()
      sig_striking_throw = sig_striking[1].text.strip()

  #Obtain takedown information
  third_banner_array = container_record.find_all("div", {"class":"overlap-athlete-content overlap-athlete-content--horizontal"})
  takedowns_avg = "0"
  takedowns_landed = "0"
  takedowns_attempted = "0"

  if len(third_banner_array) >= 2:
    third_banner = third_banner_array[1]
    takedowns_avg = third_banner.find("text", {"class": "e-chart-circle__percent"}).text.strip()
    takedowns_data = third_banner.find_all("dd", {"class": "c-overlap__stats-value"})
    if takedowns_data:
      takedowns_landed = takedowns_data[0].text.strip()
      takedowns_attempted = takedowns_data[1].text.strip()

  #Obtain two banner with the class stats-records--compare stats-records-inner
  fourth_banner_array = container_record.find_all("div", {"class": "c-stat-compare c-stat-compare--no-bar"})
  sig_striking_landed_min = ""
  avg_knockdown_fight = ""
  striking_defence = ""
  knockdown_avg = ""
  sig_striking_recieved_min = ""
  sub_avg_per_fight = ""
  takedown_defence = ""
  avg_fight_time = ""

  
  if fourth_banner_array:
    for group in fourth_banner_array:
      group1 = group.find_all("div", {"class": "c-stat-compare__group c-stat-compare__group-1 "})
      group2 = group.find_all("div", {"class": "c-stat-compare__group c-stat-compare__group-2 "})
      class_group = group1 + group2
      for value in class_group:
        title = value.find("div", {"c-stat-compare__label"}).text.strip()
        number_html = value.find("div", {"c-stat-compare__number"})
        number = ""
        if number_html:
          number = number_html.text.strip()
        if title == "Golpes Sig. Conectados":
          sig_striking_landed_min = number
        elif title == "Promedio de Knockdown":
          avg_knockdown_fight = number
        elif title == "Defensa de Golpes Sig.":
          number_array = number.split()
          striking_defence = number_array[0] if len(number_array) >= 1 else ""
        elif title == "Knockdown Avg":
          knockdown_avg = number
        elif title == "Golpes Sig. Recibidos":
          sig_striking_recieved_min = number
        elif title == "Promedio de Sumisión":
          sub_avg_per_fight = number
        elif title == "Defensa De Derribo":
          number_array = number.split()
          takedown_defence = number_array[0] if len(number_array) >= 1 else ""
        elif title == "Promedio de Tiempo de Pelea":
          avg_fight_time = number
  
  #Obtain striking by body part and Wins type class="c-stat-3bar c-stat-3bar--no-chart"
  fifthy_banner_array = container_record.find_all("div", {"class": "c-stat-3bar c-stat-3bar--no-chart"})
  sig_striking_landed_by_pos = {}
  wins_by_method = {}
  if fifthy_banner_array:
    for value in fifthy_banner_array:
      title = value.find("h2", {"class": "c-stat-3bar__title"}).text.strip()
      group_no_chart = value.find_all("div", {"class": "c-stat-3bar__group"})
      col_array = []
      for group in group_no_chart:
        label = group.find("div", {"class": "c-stat-3bar__label"}).text.strip()
        total = group.find("div", {"class": "c-stat-3bar__value"}).text.strip().split()
        number = total[0]
        percentage = total[1]
        col_value = {"name": label,
                      "value": {
                          "percentage": percentage,
                          "number": number
                          }
                      }
        col_array.append(col_value)
      if title == "Golpes Sig. por Posición":
        sig_striking_landed_by_pos = {"title": title, "content": col_array}
      elif title == "Win by Method":
        wins_by_method = {"title": title, "content": col_array}

  #Obtain significant striking by target e-stat-body_x5F__x5F_head-txt. / e-stat-body_x5F__x5F_body-txt / e-stat-body_x5F__x5F_leg-txt
  sixth_banner = container_record.find("div", {"class", "c-stat-body__diagram"})
  sig_striking_by_target = {}
  if sixth_banner:
    g_values = sixth_banner.find_all("text", {"fill": "#D20A0A"})
    head_entity = {}
    if len(g_values) >= 2:
      head_per = g_values[0].text.strip()
      head_value = g_values[1].text.strip()
      head_entity = {"percentage": head_per, "value": head_value}
    body_entity = {}
    if len(g_values) >= 4:
      body_per = g_values[2].text.strip()
      body_value = g_values[3].text.strip()
      body_entity = {"percentage": body_per, "value": body_value}
    legs_entity = {}
    if len(g_values) >= 6:
      legs_per = g_values[4].text.strip()
      legs_value = g_values[5].text.strip()
      legs_entity = {"percentage": legs_per, "value": legs_value}

    sig_striking_by_target = {"head": head_entity, "body": body_entity, "legs": legs_entity}
  
  # Obtain list of detailed information
  seventh_banner = soup.find("div", {"class": "l-container--ufc-black faq-athlete"})
  born_town = ""
  academy = ""
  fighter_style = ""
  if seventh_banner:
    details_columns = seventh_banner.find_all("div", {"class", "c-bio__field c-bio__field--border-bottom-small-screens"})

    if details_columns:
      for details in details_columns:
        details_label = details.find("div", {"class": "c-bio__label"}).text.strip()
        details_value = details.find("div", {"class": "c-bio__text"}).text.strip()
        if details_label == "Ciudad natal":
          born_town = details_value
        elif details_label == "Trenes en":
          academy = details_value
        elif details_label == "Estilo de lucha":
          fighter_style = details_value
    
    #Obtain the personal information like Age - Height - Weight - Debut - Reach - Leg_Reach
    personal_info_banner = seventh_banner.find_all("div", {"class", "c-bio__row--3col"})
    age = ""
    height = ""
    weight = ""
    rebut = ""
    arm_reach = ""
    leg_reach = ""
    if personal_info_banner:
      for info_row in personal_info_banner:
        info_columns = info_row.find_all("div", {"class": "c-bio__field"})
        if info_columns:
          for info_element in info_columns:
            info_label = info_element.find("div", {"class": "c-bio__label"}).text.strip()
            info_value = info_element.find("div", {"class": "c-bio__text"}).text.strip()
            if info_label == "Años":
              age = info_value
            elif info_label == "Alto":
              height = info_value
            elif info_label == "Peso":
              weight = info_value
            elif info_label == "Debut del octágono":
              debut = info_value
            elif info_label == "Alcance":
              arm_reach = info_value
            elif info_label == "Alcance de la pierna":
              leg_reach = info_value




  figtherStat = {"first_name": row['first_name'],
                 "last_name": "" if pd.isnull(row['last_name']) else row['last_name'],
                 "nickname": "" if pd.isnull(row['nickname']) else row['nickname'],
                 "age": age,
                 "height": height,
                 "weight": weight,
                 "weight_class": row['weight_class'],
                 "debut": debut,
                 "arm_reach": arm_reach,
                 "leg_reach": leg_reach,
                 "born_town": born_town,
                 "academy": academy,
                 "fighter_style": fighter_style,
                 "wins_by_ko":wins_by_ko,
                 "wins_by_first_round_ko":wins_by_first_round_ko,
                 "sig_striking_landed": sig_striking_landed,
                 "sig_striking_throw": sig_striking_throw,
                 "takedowns_attempted": takedowns_attempted,
                 "takedowns_landed": takedowns_landed,
                 "takedowns_avg": takedowns_avg,
                 "sig_striking_landed_min": sig_striking_landed_min,
                 "avg_knockdown_fight": avg_knockdown_fight,
                 "striking_defence": striking_defence,
                 "knockdown_avg": knockdown_avg,
                 "sig_striking_recieved_min": sig_striking_recieved_min,
                 "sub_avg_per_fight": sub_avg_per_fight,
                 "takedown_defence": takedown_defence,
                 "avg_fight_time": avg_fight_time,
                 "sig_striking_landed_by_pos": sig_striking_landed_by_pos,
                 "wins_by_method": wins_by_method,
                 "sig_striking_by_target": sig_striking_by_target
                 }

  print(figtherStat)
  fighters_info.append(figtherStat)
  # Convert the list of fighters to a pandas DataFrame
  df = pd.DataFrame(fighters_info)

  # Write the DataFrame to an Excel file
  df.to_csv("fighters_extended_info.csv", index=False)


