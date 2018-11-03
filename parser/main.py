#!/usr/bin/python3
import json
import sys

import api
import cli


def get_pages_from_search_results(results):
    """filter for raw api results
    
    Arguments:
        results {dict} -- json dict with api results
    
    Returns:
        list -- api results list
    """
    pages = []
    for idpage in results['query']['pageids']:
        page = results['query']['pages'][idpage]
        pages.append(page)
    return pages

def get_persons_from_dump(file):
    """read json file"""
    persons = open(file).read()
    return json.loads(persons)

def select_page_like_person(pages, person):
    """select relevant page from the search results
    
    Arguments:
        pages {list} -- information about wiki page
        person {list} -- information about declarator person
    
    Returns:
        dict -- most relevant page
    """
    return pages[0]


if __name__ == '__main__':
    print('Загружаю чиновников из файла')
    persons = get_persons_from_dump(cli.args.persons)

    print('Чиновники загруженны, обрабатываю каждую персону.')
    photos = []
    for idx, person in enumerate(persons[:50]):
        search_results = api.wiki_search(person['main']['person']['name'])
        api.print_wiki_api_error(search_results)

        try:
            pages = get_pages_from_search_results(search_results)
            page  = select_page_like_person(pages, person)

            photos.append({
                'id': person['main']['person']['id'], 
                'fullname': person['main']['person']['name'],
                'photo': {
                    'url': page['original']['source'],
                    'title': page['pageimage'],
                }
            })
        except Exception as e:
            print("%i) %s" % (idx, e))
            

    
    import ipdb; ipdb.set_trace()