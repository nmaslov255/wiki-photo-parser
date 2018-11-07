#!/usr/bin/python3
import sys
import json

from progress.bar import Bar
from logs import Querylog, CLIlog

import parser
import api
import cli


if __name__ == '__main__':
    CLIlog.info('Загружаю чиновников из файла')
    persons = parser.get_persons_from_dump(cli.args.persons)

    photos = []
    Progress = Bar('Чиновники загруженны, обрабатываю каждую персону:', max=10)
    for idx, person in enumerate(persons[:10]):
        person_name = person['main']['person']['name']
        person_id   = person['main']['person']['id']

        try:
            pages = parser.get_pages_from_wiki_search(person_name)
            page  = parser.select_page_like_person(pages, person)

            license = api.wiki_search_licence(page['pageimage'])
            photos.append({
                'id': person_id, 
                'fullname': person_name,
                'photo': {
                    'url': page['original']['source'],
                    'title': page['pageimage'],
                    'license': license['query']['rightsinfo']['text']
                }
            })
        except KeyError as e:
            Querylog.error('Bad api response for person_id: %i' % person_id)

        Progress.next()
    Progress.finish()

    CLIlog.info(('Время работы %i сек' % Progress.elapsed))
    json.dump(photos, open(cli.args.out ,'w'))
    
    import ipdb; ipdb.set_trace()