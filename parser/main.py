#!/usr/bin/python3
import sys
import json

from progress.bar import Bar
from logs import Querylog

import parser
import api
import cli


if __name__ == '__main__':
    print('Загружаю чиновников из файла')
    persons = parser.get_persons_from_dump(cli.args.persons)

    photos = []
    Progress = Bar('Чиновники загруженны, обрабатываю каждую персону.', max=10)
    for idx, person in enumerate(persons[:10]):
        results = api.wiki_search(person['main']['person']['name'])
        api.print_wiki_api_error(results)

        try:
            pages = parser.get_pages_from_search_results(results)
            page  = parser.select_page_like_person(pages, person)

            photos.append({
                'id': person['main']['person']['id'], 
                'fullname': person['main']['person']['name'],
                'photo': {
                    'url': page['original']['source'],
                    'title': page['pageimage'],
                }
            })
        except KeyError as e:
            Querylog.error(e)

        Progress.next()
    Progress.finish()

    json.dump(photos, open(cli.args.out ,'w'))
    
    import ipdb; ipdb.set_trace()