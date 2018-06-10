from requests.exceptions import HTTPError
import requests


URL = url = "https://api.betfair.com/exchange/betting/json-rpc/v1"
jsonrpc_req = '{"jsonrpc": "2.0", ' \
              '"method": "SportsAPING/v1.0/listEvents", ' \
              '"params": {"filter":{"eventTypeIds": ["2"], "inPlayOnly" : true }}, "id": 1}'
headers = {'X-Application': 'OclZSgXWwsQNpQky', 'X-Authentication': 'GKk0sa/ZVCqOcxeWm34+0FYO6HH9ft6skRaFpKhZz0E=', 'content-type': 'application/json'}
 
def get_tennis_event_ids_list(jsonrpc_req):
    event_ids = []
    try:
        req = requests.post(url, jsonrpc_req, headers=headers)
        for event in req.json()['result']:
            d = event['event']
            event_ids.append(d["id"])
        return event_ids

    except HTTPError:
        print('Not a valid operation from the service ' + str(url))
        exit()

event_ids_list = get_tennis_event_ids_list(jsonrpc_req)

jsonrpc = '{"jsonrpc": "2.0", ' \
              '"method": "SportsAPING/v1.0/listMarketCatalogue", ' \
              '"params": {"filter":{"eventIds": "[{}]"}}, "id": 1}'.format(event_ids_list[0])

def get_market_id(jsonrpc):
    req = requests.post(url, jsonrpc, headers=headers)
    return req.json()

print(get_market_id(jsonrpc))