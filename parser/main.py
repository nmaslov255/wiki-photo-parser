#!/usr/bin/python3

import api

if __name__ == '__main__':
    url = api.DOMAIN + api.ROUTE
    req = api.request(url, {})
    json = req.json()
    res = json['query']['search']
    import ipdb; ipdb.set_trace()