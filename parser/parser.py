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

    words_intersections_in_pages = []
    for page in pages:
        declapage = get_declapage_from_extlinks(page.get('extlinks', None))

        if declapage is None:
            person_words = get_bag_of_words_from_persons_dump(person)
            wiki_words = get_bag_of_words_from_wiki_page(page)

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
        words = words.union(separate(json['main']['party'].get('name', '')))

    if 'office' in json['main']:
        words = words.union(separate(json['main']['office'].get('name', '')))
        words = words.union(separate(json['main']['office'].get('region', '')))

    return words

def get_bag_of_words_from_wiki_page(pagetext):
    """
    Arguments:
        pagetext {str} -- text from wiki page
    
    Returns:
        set -- set with bag of words
    """
    return set().union(separate(pagetext))
    
def separate(string):
    if isinstance(string, str):
        return string.lower().replace('\n', '').split(' ')
    return ''
