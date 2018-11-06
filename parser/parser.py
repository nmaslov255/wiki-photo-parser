#!/usr/bin/python3
from string import punctuation as ASCII_punctuation
import json

import api

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

def get_pages_by_wiki_search(person_name):
    """search wiki pages and aggregate it if
    
    Arguments:
        person_name {str} -- person name for search string
    
    Returns:
        list -- api results list
    """
    results = api.wiki_search(person_name)
    pages = get_pages_from_search_results(results)

    if 'continue' in results:
        search_offset = int(results['continue']['gsroffset'])

        for offset in range(1, search_offset+1):
            results = api.wiki_search(person_name, gsroffset=offset)
            pages.extend(get_pages_from_search_results(results))
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

    words_intersections_in_pages = []
    for page in pages:
        declapage = get_declapage_from_extlinks(page.get('extlinks', None))

        if declapage is None:
            person_words = get_bag_of_words_from_persons_dump(person)
            wiki_words = get_bag_of_words_from_wiki_page(page['extract'])

            intersection = len(person_words & wiki_words)
            words_intersections_in_pages.append(intersection)
        else:
            return page

    # TODO: check duplicate in count of words
    max_intersections = max(words_intersections_in_pages)
    relevant_page = words_intersections_in_pages.index(max_intersections)

    return pages[relevant_page]

def get_declapage_from_extlinks(extlinks):
    """will return url to declarator if it exist
    
    Arguments:
        extlinks {list} -- list with extlinks in wiki page

    Returns:
        str|None -- link to declarator page or none
    """
    if isinstance(extlinks, list):
        for link in extlinks:
            if 'declarator' in link['*']:
                return link['*']
    return None

def get_bag_of_words_from_persons_dump(json):
    """parse person declaration and make bag of words
    
    Arguments:
        json {dict} -- dict with json declaration of person

    Returns:
        sets -- set with words from declaration
    """
    words = set()
    if 'party' in json['main']:
        bag = get_bag_of_words(json['main']['party'].get('name', ''))
        words = words.union(bag)

    if 'office' in json['main']:
        bag = get_bag_of_words(json['main']['office'].get('name', ''))
        words = words.union(bag)

        bag = get_bag_of_words(json['main']['office'].get('region', ''))
        words = words.union(bag)

    return words

def get_bag_of_words_from_wiki_page(pagetext):
    """
    Arguments:
        pagetext {str} -- text from wiki page
    
    Returns:
        set -- set with bag of words
    """
    return set().union(get_bag_of_words(pagetext))
    
def get_bag_of_words(string):
    """Will return list with words in string
    
    Arguments:
        string {str} -- text
    
    Returns:
        list -- list with words
    """
    if isinstance(string, str):
        string = string.lower()

        punctuation = ASCII_punctuation
        for char in punctuation:
            string = string.replace(char, '')

        string = string.replace('\n', ' ')
        words = string.split()

        for idw, word in enumerate(words):
            if len(word) <= 3:
                del words[idw]
        return words
    return []
