import os
from betfair import Betfair

import urllib
from urllib import request
from urllib.error import HTTPError
import json
import datetime
import requests

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
        print ('Oops not a valid operation from the service ' + str(url))
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
print(EventList)


def getMarketCatalogue():
    market_data = []
    now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    market_catalogue_req = '{"jsonrpc": "2.0", ' \
                               '"method": "SportsAPING/v1.0/listMarketCatalogue", ' \
                               '"params": ' \
                               '{"filter":' \
                                    '{' \
                                        '"eventTypeIds":["2"],' \
                                        '"marketStartTime":{"from":"' + now + '"},' \
                                                                              '},' \
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
        print(market_catalouge_results)
        for market in market_catalouge_results:
            if market['marketName'] == 'Match Odds':
                market_id = market['marketId']
                event = market['event']
                event_id = event['id']
                event_name = event['name']
                market_data.append([market_id, event_id, event_name])
        return market_data
    except:
        print ('Exception from API-NG' + str(market_catalouge_loads['error']))
        exit()

marketCatalogresult = getMarketCatalogue()
#print(marketCatalogresult)

#for market in marketCatalogresult:
#    print(market)


def getMarketId(marketCatalogueResult):
    if( marketCatalogueResult is not None):
        for market in marketCatalogueResult:
            return market['marketId']

def getMarketBetLine():
    bet_line_req = '{"jsonrpc": "2.0",' \
                   ' "method": "SportsAPING/v1.0/listMarketBook", ' \
                   '"params": {' \
                   '"marketIds":["1.144612640"],' \
                   '"priceProjection":{' \
                   '"priceData":["EX_BEST_OFFERS"]}}, "id": 1}'

    bet_line_response = callAping(bet_line_req)
    bet_line_loads = json.loads(bet_line_response)
    try:
            bet_line_results = bet_line_loads['result']
            for result_part in bet_line_results:
                for runners in result_part['runners']:
                    print(runners['ex'])

            return bet_line_results
    except:
        print ('Exception from API-NG' + str(bet_line_loads['error']))
        exit()

#getMarketBetLine()

def test():
    market_catalogue_req = '{"jsonrpc": "2.0", ' \
                               '"method": "SportsAPING/v1.0/listMarketCatalogue", ' \
                               '"params": {"filter": ' \
                                                '{"eventIds" : "28761545"}}, ' \
                                        '"maxResults": "50",' \
                                        '"marketProjection": ["EVENT"], "id": 1}'
    data = requests.post(url, market_catalogue_req, headers)
    return data.json()

print(test())

