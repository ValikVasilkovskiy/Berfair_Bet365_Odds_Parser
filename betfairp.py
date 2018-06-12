import os
from betfair import Betfair
from openpyxl import Workbook

import urllib
from urllib import request
from urllib.error import HTTPError
import json

from bet356 import getCardCompetitionData, getListCompetition, driver

ITERATION = 40

# connect to API and keep alive session key
dir = os.path.abspath(os.path.dirname(__file__))
key = 'betfair.pem'
base_dir = dir + '\cert\\{}'.format(key)
out_file_dir = dir + '\data\\'

client = Betfair('OclZSgXWwsQNpQky', '{}'.format(base_dir))
client.login(username='ValliRich', password='k6Nawras')
client.keep_alive()

url = client.api_url
headers = client.headers

def callAping(jsonrpc_req):
    try:
        req = request.Request(url, jsonrpc_req.encode('utf-8'), headers)
        response = urllib.request.urlopen(req)
        jsonResponse = response.read()
        return jsonResponse.decode('utf-8')
    except HTTPError:
        print ('Not a valid operation from the service ' + str(url))
        exit()

def getMarketBetLine(marketId):
    match_odds = []
    bet_line_req = '{"jsonrpc": "2.0",' \
                   ' "method": "SportsAPING/v1.0/listMarketBook", ' \
                   '"params": {' \
                   '"marketIds":["'+  marketId  +'"],' \
                   '"priceProjection":{' \
                   '"priceData":["EX_BEST_OFFERS"]}}, "id": 1}'

    bet_line_response = callAping(bet_line_req)
    bet_line_loads = json.loads(bet_line_response)
    try:
            bet_line_results = bet_line_loads['result']
            for result_part in bet_line_results:
                if result_part['runners']:
                    for runners in result_part['runners']:
                        if runners['ex']['availableToBack'] and runners['ex']['availableToLay']:
                            match_odds.extend([runners['ex']['availableToBack'][-1]['price'],
                                              runners['ex']['availableToLay'][0]['price']])
                            match_odds.extend([runners['ex']['availableToBack'][-1]['size'],
                                              runners['ex']['availableToLay'][0]['size']])
                        else:
                            match_odds.extend(["0", "0", "0", "0"])
    except:
        print ('Exception from API-NG' + str(bet_line_loads['error']))
        exit()
    return match_odds


def getMarketCatalogueId():
    listCompetitionResult = getListCompetition()
    cardCompetitionResult = getCardCompetitionData(listCompetitionResult)
    cardList = []
    market_catalogue_req = '{"jsonrpc": "2.0", ' \
                               '"method": "SportsAPING/v1.0/listMarketCatalogue", ' \
                               '"params": ' \
                               '{"filter":' \
                                    '{' \
                                        '"eventTypeIds":["2"],' \
                                        '"inPlayOnly" : true},' \
                                        '"sort":"MAXIMUM_TRADED",' \
                                        '"maxResults":"100",' \
                                        '"marketBettingTypes": "LINE",' \
                                        '"marketProjection":["EVENT"]' \
                                    '},' \
                                        ' "id": 1}'


    market_catalogue_response = callAping(market_catalogue_req)
    market_catalouge_loads = json.loads(market_catalogue_response)

    try:
        market_catalouge_results = market_catalouge_loads['result']
        for market in market_catalouge_results:
            if market['marketName'] == 'Match Odds':
                market_id = market['marketId']
                event = market['event']
                event_name = event['name']
                runner = str(event_name).split(' ')[0]
                if len(runner) <= 1:
                    runner = str(event_name).split(' ')[1]

                for card in cardCompetitionResult:
                    for data_card in card[4:6]:
                        if runner in data_card:
                            card.extend(getMarketBetLine(market_id))
                            cardList.append(card)
    except:
        print ('Exception from API-NG' + str(market_catalouge_loads['error']))
        exit()
    return cardList

# out data to file
wb = Workbook()
ws = wb.create_sheet("ODDS")
ws.append([
               "TimeStamp",
               "Match Score",
               "Set Score",
               "Game Score",
               "Player1 Name",
               "Player2 Name",
               "Player1 Odds Bet365",
               "Player2 Odds Bet365",
               "Player1 Back Odds Betfair",
               "Player1 Lay Odds Betfair",
               "Player2 Back Odds Betfair",
               "Player2 Lay Odds Betfair",
               "Player1 Back Stake Betfair",
               "Player1 lay Stake Betfair",
               "Player2 Back Stake Betfair",
               "Player2 Lay Stake Betfair"
              ])
n = 0
print("Start...")
print("Open WebDriver...")
while n <= ITERATION:
    print('Iteration --> {}'.format(n))
    for event in getMarketCatalogueId():
        ws.append(event)
        wb.save('{}betfair.xlsx'.format(out_file_dir))
    n += 1
print("Close WebDriver...")
driver.close()










