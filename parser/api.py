#!/usr/bin/python3
import requests
from logs import Querylog

DOMAIN = 'https://ru.wikipedia.org/'
PATH   = '/w/api.php'

# headers by wiki api etiquette
HEADERS = {
    'User-Agent':'source: github.com/nmaslov255/wiki-photo-parser, \
                  feedback: nmaslov255@yandex.ru'
}

def request(URL, params=None):
    response = requests.get(URL, params=params, timeout=3.0)
    
    if response.status_code != 200:
        response.raise_for_status()
    return response

def wiki_search(s, params=None, *, gsroffset=0):
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
        "prop": "pageimages|extracts|extlinks|info", "indexpageids": 1,
        "piprop": "name|original", "inprop": "url",
        "elprotocol": "", "elquery": "declarator.org", "ellimit": "1",
        "gsrsearch": "intitle:'%s'" % s, 
        "gsrlimit": "1", "gsroffset": "%i" % gsroffset,
        "gsrinfo": "", "gsrprop": "", 'utf8': 1,
        "exlimit": "1", "explaintext": 1, "exsectionformat": "plain",
    }

    if params == None:
        params = default_params

    response = request(DOMAIN+PATH, params).json()
    log_wiki_api_error(response)
    return response

def wiki_search_licence(s, params=None, *, file=False):
    """Will return image property from wiki

    Arguments:
        filename {str} -- filename in wiki
    
    Keyword Arguments:
        params {dict} -- overload default api params (default: {None})
    
    Returns:
        dict -- json dict with wiki responce
    """
    default_params = {
        "action": "query", "format": "json",
        "meta": "siteinfo", "siprop": "rightsinfo",
        "titles": 'File:' + s if file else s
    }

    if params != None:
        params = {**default_params, **params}
    else:
        params = default_params

    return wiki_search('', params)

def log_wiki_api_error(response):
    if 'warnings' in response.keys():
        for warning in response['warnings']:
            Querylog.warning(warning['*'])
    if 'errors' in response.keys():
        for error in response['errors']:
            Querylog.warning(error['*'])
