from bs4 import BeautifulSoup
from selenium import webdriver

from time import sleep
from datetime import datetime

URL_BATFAIR = "https://www.betfair.com/exchange/plus/tennis/inplay"
SLEEP = 5
ITERATIONS = 10
driver = webdriver.Chrome()

def scraping_betfair():

    driver.get(URL_BATFAIR)
    driver.minimize_window()

    sleep(SLEEP)
    data = driver.page_source
    bsObj = BeautifulSoup(data, "html.parser")

    competitions = bsObj.find_all("table", class_="coupon-table")

    for card in competitions:
        players_card = card.find_all("li")
        player1 = players_card[0].get_text()
        player2 = players_card[1].get_text()
        print(player1, player2)

scraping_betfair()
driver.close()