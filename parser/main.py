#!/usr/bin/python3
import sys
import json

from requests import exceptions as requext
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

    wiki_person = []
    for idx, person in enumerate(persons[:10]):
        try:
            wiki_person.append(parser.parse_person(person))
        except exceptions.WikiError as e:
            # TODO: idx must be equal person_id
            Querylog.error("person_number: %i, %s" % (idx, e.msg))
        except requext.Timeout:
            Querylog.error("person_number: %i, Query timeout is expired" % idx)
        Progress.next()
    Progress.finish()

    CLIlog.info(('Время работы %i сек' % Progress.elapsed))

    with open(cli.args.out ,'w') as fp:
        json.dump(wiki_person, fp)
    
    import ipdb; ipdb.set_trace()