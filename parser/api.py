#!/usr/bin/python3
import requests

DOMAIN = 'https://ru.wikipedia.org/'
PATH   = '/w/api.php'

# headers by wiki api etiquette
HEADERS = {
    'User-Agent':'source: github.com/nmaslov255/wiki-photo-parser, \
                  feedback: nmaslov255@yandex.ru'
}

def request(URL, params=None):
    response = requests.get(URL, params=params)
    
    if response.status_code != 200:
        response.raise_for_status()
    return response

def wiki_search(s, params=None):
    """function for search in wikipedia

    Arguments:
        s {str} -- search string
    
    Keyword Arguments:
        params {dict} -- api params for search (default: {None})
    
    Returns:
        dict -- json dict with server responce
    """

    # search in category and deepcategory don't work :(
    default_params = {
        "action": "query", "format": "json", "maxlag": "3",
        "errorformat": "plaintext", "generator": "search",
        "prop": "pageimages|revisions|extlinks",
        "piprop": "name|original", "rvprop": "content", 
        "rvslots": "main","ellimit": "500",
        "gsrsearch": "intitle:'%s'" % s,
        "gsrlimit": "3", "gsrinfo": "", "gsrprop": ""
    }

    if params == None:
        params = default_params

    response = request(DOMAIN+PATH, params)
    return response.json()

def print_wiki_api_error(response):
    if 'warnings' in response.keys():
        for warning in response['warnings']:
            print(warning['*'])
    if 'errors' in response.keys():
        for error in response['errors']:
            print(error['*'])

