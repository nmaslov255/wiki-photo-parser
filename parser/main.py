#!/usr/bin/python3

import api

if __name__ == '__main__':
    req = api.wiki_search('вольфович жириновский')
    # req = api.wiki_search('Путин')
    import ipdb; ipdb.set_trace()