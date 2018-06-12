from bs4 import BeautifulSoup
from selenium import webdriver
from openpyxl import Workbook

from time import sleep
from datetime import datetime


#wb = Workbook()
#ws = wb.create_sheet("Bet356")
#ws.append(["TimeStamp",
#               "Match Score",
#               "Set Score",
#               "Game Score",
#               "Player1 Name",
#               "Player2 Name",
#               "Player1 Odds Bet365",
#               "Player2 Odds Bet365"
#               ]
#              )
URL = "https://mobile.bet365.com/#type=InPlay;key=13;ip=1;lng=1"
SLEEP = 5
ITERATIONS = 10
driver = webdriver.Chrome()

def getListCompetition():

    driver.get(URL)
    driver.minimize_window()

    sleep(SLEEP)
    data = driver.page_source
    bsObj = BeautifulSoup(data, "html.parser")

    competitions = bsObj.find_all("div", class_="ipo-CompetitionBase ")
    driver.close()
    return competitions


def getCardCompetitionData(competition_list):
    tennisInPlayResult = []
    if competition_list:
        for card_list in competition_list:
            for card in card_list.find_all("div", class_="ipo-Fixture ipo-Fixture_NoTimings ipo-Fixture_ShortScores "):
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
                if odds[0].get_text()[0].isdigit() and odds[1].get_text()[0].isdigit():
                    odds_player1 = str(int(str(odds[0].get_text()).split('/')[0]) / int(str(odds[0].get_text()).split('/')[1]))[:4]
                    odds_player2 = str(int(str(odds[1].get_text()).split('/')[0]) / int(str(odds[1].get_text()).split('/')[1]))[:4]
                else:
                    odds_player1 = odds[0].get_text()
                    odds_player2 = odds[1].get_text()

                tennisInPlayResult.append([str(datetime.now()),
                                            "{}-{}".format(point1_player1, point1_player2),
                                            "{}-{}".format(point2_player1, point2_player2),
                                            "{}-{}".format(point3_player1, point3_player2),
                                            player1, player2,
                                            odds_player1, odds_player2
                                            ]
                                           )
    return tennisInPlayResult

#wb.save('Odds_Bet365.xlsx')







