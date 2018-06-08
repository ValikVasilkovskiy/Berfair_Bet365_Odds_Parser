from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime
from selenium import webdriver
from openpyxl import Workbook



wb = Workbook()
ws = wb.create_sheet("Bet356")
ws.append(["TimeStamp",
               "Match Score",
               "Set Score",
               "Game Score",
               "Player1 Name",
               "Player2 Name",
               "Player1 Odds",
               "Player2 Odds"
               ]
              )
URL = "https://mobile.bet365.com/#type=InPlay;key=13;ip=1;lng=1"


def scraping_bet365():
    driver = webdriver.Chrome()
    driver.get(URL)
    driver.minimize_window()

    sleep(5)
    data = driver.page_source
    bsObj = BeautifulSoup(data, "html.parser")



    competitions = bsObj.find_all("div", class_="ipo-CompetitionBase ")

    for card in competitions:
        players_card = card.find_all("div", class_="ipo-Fixture_Truncator ")
        player1 = players_card[0].get_text()
        player2 = players_card[1].get_text()

        points = card.find_all("span", class_="ipo-Fixture_PointField ")
        point1_player1 = points[0].get_text()
        point2_player1 = points[1].get_text()
        point3_player1 = points[2].get_text()

        point1_player2 = points[3].get_text()
        point2_player2 = points[4].get_text()
        point3_player2 = points[5].get_text()

        odds = card.find_all("span", class_="ipo-Participant_OppOdds ")
        odds_player1 = odds[0].get_text()
        odds_player2 = odds[1].get_text()

        ws.append([str(datetime.now()),
                   "{}-{}".format(point1_player1, point1_player2),
                   "{}-{}".format(point2_player1, point2_player2),
                   "{}-{}".format(point3_player1, point3_player2),
                   player1, player2,
                   odds_player1, odds_player2
                   ]
                  )
        #driver.close()

step = 0
print('Get URL --> {}'.format(URL))
while step < 3:
    print('Step --> {}'.format(step))
    scraping_bet365()
    step += 1

wb.save('Odds_Bet365.xlsx')






