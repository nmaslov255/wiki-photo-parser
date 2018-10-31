#!/usr/bin/python3
import api

if __name__ == '__main__':
    req = api.wiki_search('вольфович жириновский')
    api.print_wiki_api_error(req)
    
    import ipdb; ipdb.set_trace()