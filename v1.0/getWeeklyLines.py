from selenium import webdriver
from bs4 import BeautifulSoup
import time
import datetime
import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName

week = 4

dict = {"Week":[],"Home Team":[],"Road Team":[],"Neutral Field":[],"Favorite":[],"Spread":[],"Home Spread Odds":[],"Road Spread Odds":[],"O/U":[],"Over Odds":[],"Under Odds":[]}

browser = webdriver.Chrome(executable_path='chromedriver.exe')
browser.get("https://www.pinnacle.com/en/football/ncaa/matchups/#period:0")
browser.maximize_window()
time.sleep(5)
for i in range(25):
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    main = soup.find(class_="contentBlock square")
    games = main.find_all(class_="style_row__3q4g_ style_row__3hCMX")
    for game in games:
        dict["Week"].append(week)
        dict["Neutral Field"].append(0)
        dict["Home Team"].append(standardizeTeamName(game.find_all(class_="ellipsis event-row-participant style_participant__H8-ku")[0].text, True))
        dict["Road Team"].append(standardizeTeamName(game.find_all(class_="ellipsis event-row-participant style_participant__H8-ku")[1].text, True))
        spread = game.find(class_="style_buttons__XEQem")
        if (float(spread.find(class_="style_label__2KJur").text) < 0):
            dict["Favorite"].append(standardizeTeamName(game.find_all(class_="ellipsis event-row-participant style_participant__H8-ku")[0].text, False))
        elif (float(spread.find(class_="style_label__2KJur").text) > 0):
            dict["Favorite"].append(standardizeTeamName(game.find_all(class_="ellipsis event-row-participant style_participant__H8-ku")[1].text, False))
        else:
            dict["Favorite"].append("EVEN")
        dict["Spread"].append(abs(float(spread.find(class_="style_label__2KJur").text)))
        dict["Home Spread Odds"].append(spread.find_all(class_="style_price__15SlF")[0].text)
        dict["Road Spread Odds"].append(spread.find_all(class_="style_price__15SlF")[1].text)
        total = game.find_all(class_="style_buttons__XEQem")[2]
        try:
            dict["O/U"].append(abs(float(total.find(class_="style_label__2KJur").text)))
            dict["Over Odds"].append(total.find_all(class_="style_price__15SlF")[0].text)
            dict["Under Odds"].append(total.find_all(class_="style_price__15SlF")[1].text)
        except:
            dict["O/U"].append(np.nan)
            dict["Over Odds"].append(np.nan)
            dict["Under Odds"].append(np.nan)
    try:
        element = browser.find_element_by_xpath("//*[@id='events-chunkmode']/div/div/div[7]/div/div[1]/a/div/div/div[1]/span")
    except:
        element = browser.find_element_by_xpath("//*[@id='events-chunkmode']/div/div/div[8]/div/div[1]/a/div/div/div[2]/span")
    browser.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(5)


dfFinal = pd.DataFrame.from_dict(dict)
dfFinal = dfFinal.drop_duplicates()
dfFinal.to_csv('./new_csv_Data/2021/BettingLinesWeek' + str(week) + '.csv')
