#!/usr/bin/python3
import sys, os
import json

from requests import exceptions as reqext
from progress.bar import Bar
from logs import Querylog, CLIlog

import exceptions 
import parser
import api
import cli


if __name__ == '__main__':
    CLIlog.info('Загружаю чиновников из файла')
    persons = parser.get_persons_from_dump(cli.args.persons)

    Progress = Bar('Обрабатываю каждую персону:', max=len(persons))

    if cli.args.start_from:
        try:
            with open(cli.args.start_from) as fp:
                wiki_persons = json.loads(fp.read())
            
            persons = persons[len(wiki_persons):]

            for i in range(len(wiki_persons)):
                Progress.next()
        except FileNotFoundError:
            CLIlog.error('Не найден файл: %s' % cli.args.start_from)
            sys.exit(0)    
    else:
        wiki_persons = []
    
    try:
        for idx, person in enumerate(persons):
            try:
                wiki_persons.append(parser.parse_person(person))
            except exceptions.WikiError as e:
                # TODO: idx must be equal person_id
                Querylog.error("person_number: %i, %s" % (idx, e.msg))
            except reqext.Timeout:
                message = "person_number: %i, Query timeout is expired" % idx
                Querylog.error(message)
            Progress.next()
    except BaseException as e:
        Querylog.critical(e)
    finally:    
        Progress.finish()

        CLIlog.info(('Время работы %i сек' % Progress.elapsed))

        with open(cli.args.out ,'w') as fp:
            json.dump(wiki_persons, fp)

        CLIlog.info('Данные сохранены в папке: ')
        CLIlog.info(os.path.abspath(cli.args.out))
