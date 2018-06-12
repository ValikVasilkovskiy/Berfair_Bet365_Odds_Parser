import os
from betfair import Betfair

import urllib
from urllib import request
from urllib.error import HTTPError
import json

from bet356 import getCardCompetitionData, getListCompetition

dir = os.path.abspath(os.path.dirname(__file__))
key = 'betfair.pem'
base_dir = dir + '\cert\\{}'.format(key)

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
                            match_odds.extend([[runners['ex']['availableToBack'][-1]],
                                              [runners['ex']['availableToLay'][0]]])
                        else:
                            match_odds.append([[runners['ex']['availableToBack']],
                                               [runners['ex']['availableToLay']]])
    except:
        print ('Exception from API-NG' + str(bet_line_loads['error']))
        exit()
    return match_odds

listCompetitionResult = getListCompetition()
cardCompetitionResult = getCardCompetitionData(listCompetitionResult)

def getMarketCatalogueId():
    market_id_only = []
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
                            print(card)
                            #print(getMarketBetLine(market_id))
                            break
        return market_id_only
    except:
        print ('Exception from API-NG' + str(market_catalouge_loads['error']))
        exit()

getMarketCatalogueId()










