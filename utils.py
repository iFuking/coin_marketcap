from bs4 import BeautifulSoup
import urllib, urllib2
import logging
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

user_agent = 'Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'


def get_soup_by_url(url):
    success = True
    try:
        req = urllib2.Request(url, headers={'User-Agent': user_agent})
        webpage = urllib2.urlopen(req)
        return BeautifulSoup(webpage.read(), 'lxml')
    except Exception, e:
        success = False
        raise e


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def token_not_exists_err(token):
    most_sim = 0
    token_name = str()

    for name in token_names:
        sim = similar(name, token)
        if sim > most_sim:
            most_sim = sim
            token_name = name
    return 'token \'' + token + '\' not in token name set, do you mean: \'%s\'?\n' % token_name


def get_token_names():
    l = list()
    url = 'https://coinmarketcap.com'
    try:
        soup = get_soup_by_url(url)
        token_list = soup.find('tbody').find_all('tr')
        for token in token_list:
            l.append(token.get('id')[3:])
    except Exception, e:
        print e
    return l


token_names = get_token_names()
token_in_usd = dict()
