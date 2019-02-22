#!/usr/bin/python3
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from logs import Querylog

DOMAIN = 'https://ru.wikipedia.org/'
PATH   = '/w/api.php'

# headers by wiki api etiquette
HEADERS = {
    'User-Agent':'source: github.com/nmaslov255/wiki-photo-parser, \
                  feedback: nmaslov255@yandex.ru'
}

def request(URL, params=None):
    session = requests.Session()
    retry = Retry(total=5, read=5, connect=5, backoff_factor=5)

    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    response = session.get(URL, params=params, timeout=10.0)
    
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
        "action": "query", "format": "json", "maxlag": "3",
        "errorformat": "plaintext", "prop": "imageinfo",
        "generator": "search", "utf8": 1, "indexpageids": 1,
        "iiprop": "extmetadata", "iiextmetadatafilter": "UsageTerms",
        "gsrsearch": 'File:' + s if file else s,
        "gsrlimit": "3", "gsrinfo": "", "gsrprop": ""

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
