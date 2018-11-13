#!/usr/bin/python3
from string import punctuation as ASCII_punctuation
import json

from logs import Querylog
import exceptions 
import api


def parse_person(person):
    """Parse info about person in wiki

    Arguments:
        person {dict} -- json info about person
    
    Returns:
        dict -- found person info in wiki
    """
    person_name = person['name']
    person_id   = person['id']

    pages = get_pages_from_wiki_search(person_name)
    page  = select_page_like_person(pages, person)

    wiki_person = {
        'id': person_id, 'fullname': person_name,
        'url': page.get('fullurl', None), 
        'declarator_profile': page.get('declarator_profile', None),
        'words_intersection': page.get('words_intersection', None),
    }

    # if page with image
    if 'pageimage' in page:
        try:
            image = page['pageimage']
            url   = page['original']['source']
            license = get_license_from_wiki(image, is_file=True)

            photo = {'title': image, 'url': url, 'license': license}
            wiki_person['photo'] = photo
        except KeyError as e:
            message = "person_id: %i, Not found key: %s" % (person_id, e)
            Querylog.error(message)
    return wiki_person

def get_license_from_wiki(s, *, is_file=False):
    """search licence in wiki

    Arguments:
        s {str} -- document in wiki (photo, page, etc)
    
    Keyword Arguments:
        is_file {bool} -- if you need search file (default: {False})
    
    Returns:
        str|None -- licence name or none
    """
    response = api.wiki_search_licence(s, file=is_file)

    idpage = response['query']['pageids'][0]

    try:    
        imageinfo = response['query']['pages'][idpage].get('imageinfo', None)
        return imageinfo[0]['extmetadata']['UsageTerms']['value']
    except (KeyError, TypeError) as e:
        Querylog.error('License not found for %s' % s)
        return None

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

def get_pages_from_wiki_search(person_name):
    """search wiki pages and aggregate it if
    
    Arguments:
        person_name {str} -- person name for search string
    
    Returns:
        list -- api results list
    """
    results = api.wiki_search(person_name)

    if not 'query' in results:
        raise exceptions.WikiError('Empty search result')

    pages = get_pages_from_search_results(results)
    if 'continue' in results:
        search_offset = int(results['continue']['gsroffset'])

        for offset in range(1, search_offset+1):
            results = api.wiki_search(person_name, gsroffset=offset)
            pages.extend(get_pages_from_search_results(results))
    return pages

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
            page['declarator_profile'] = declapage
            return page

    # TODO: check duplicate in count of words
    max_intersections = max(words_intersections_in_pages)
    relevant_page = words_intersections_in_pages.index(max_intersections)
    page = pages[relevant_page]

    page['words_intersection'] = max_intersections
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
    if 'offices' in json:
        for office in json['offices']:
            words = words.union(get_bag_of_words(office))

    if 'roles' in json:
        for role in json['roles']:
            words = words.union(get_bag_of_words(role))

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

def get_persons_from_dump(file):
    """read json file"""
    with open(file) as fp:
        persons = fp.read()
    return json.loads(persons)
