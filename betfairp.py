import os
from betfair import Betfair

import urllib
from urllib import request
from urllib.error import HTTPError
import json
import datetime


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

def getTennisEventIdsList():
    event_ids = []
    event_list_req = '{"jsonrpc": "2.0", ' \
              '"method": "SportsAPING/v1.0/listEvents", ' \
              '"params": {"filter":{' \
                     '"eventTypeIds": ["2"], ' \
                     '"inPlayOnly" : true }' \
                     '}, "id": 1}'

    eventListResponse = callAping(event_list_req)
    eventListLoads = json.loads(eventListResponse)
    try:
        for event in eventListLoads['result']:
            d = event['event']
            if not str(d["name"]).startswith('Set'):
                event_ids.append([d['id'], d['name']])
        return event_ids
    except:
        print ('Exception from API-NG' + str(eventListLoads['error']))
        exit()

EventList = getTennisEventIdsList()

def getMarketBetLine(marketId):
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
                for runners in result_part['runners']:
                    print(runners['ex'])

    except:
        print ('Exception from API-NG' + str(bet_line_loads['error']))
        exit()

def getMarketCatalogueId():
    market_id_name = []
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
                market_id_name.append([market_id, event_name])
                market_id_only.append(market_id)
                print(market_id)
                getMarketBetLine(market_id)
        return market_id_only
    except:
        print ('Exception from API-NG' + str(market_catalouge_loads['error']))
        exit()

getMarketCatalogueId()










