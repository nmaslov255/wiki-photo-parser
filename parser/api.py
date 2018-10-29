#!/usr/bin/python3
import requests

DOMAIN = 'https://ru.wikipedia.org/'
ROUTE  = '/w/api.php'

DEFAULT_PARAMS = {
    "action": "query",
    "format": "json",
    "maxlag": "10",
    "list": "search",
    "srsearch": "Путин",
    "prop": "categories",
    # "assert": "bot",
    # "namespace": "6|486",
}

def request(URL, params=None):
    if params != None:
        params = {**DEFAULT_PARAMS, **params}

    response = requests.get(URL, params=params)
    
    if response.status_code != 200:
        response.raise_for_status()
    return response