#!/usr/bin/python3
import json

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

def get_declapage_from_extlinks(extlinks):
    pass

def get_bag_of_words_from_persons_dump(json):
    pass

def get_bar_of_words_from_wiki_page(page):
    pass
