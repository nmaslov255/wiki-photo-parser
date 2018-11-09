#!/usr/bin/python3
import sys
import json

from progress.bar import Bar
from logs import Querylog, CLIlog

import exceptions 
import parser
import api
import cli


if __name__ == '__main__':
    CLIlog.info('Загружаю чиновников из файла')
    persons = parser.get_persons_from_dump(cli.args.persons)

    Progress = Bar('Обрабатываю каждую персону:', max=10)

    photos = []
    for idx, person in enumerate(persons[:10]):
        person_name = person['main']['person']['name']
        person_id   = person['main']['person']['id']

        try:
            pages = parser.get_pages_from_wiki_search(person_name)
            page  = parser.select_page_like_person(pages, person)
        except exceptions.WikiError as e:
            Querylog.error("person_id: %i, %s" % (person_id, e.msg))

        wiki_person = {'id': person_id, 'fullname': person_name,
                       'url': page['fullurl']}

        if 'pageimage' in page:
            try:
                image = page['pageimage']
                url   = page['original']['source']
                license = parser.get_license_from_wiki(image, file=True)

                photo = {'title': image, 'url': url, 'license': license}
                wiki_person['photo'] = photo
            except KeyError as e:
                message = "person_id: %i, Not found key: %s" % (person_id, e)
                Querylog.error(message)
        photos.append(wiki_person)

        Progress.next()
    Progress.finish()

    CLIlog.info(('Время работы %i сек' % Progress.elapsed))

    with open(cli.args.out ,'w') as fp:
        json.dump(photos, fp)
    
    import ipdb; ipdb.set_trace()