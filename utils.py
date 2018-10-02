from bs4 import BeautifulSoup
import urllib, urllib2
import logging
from difflib import SequenceMatcher
import json

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


def get_cryptocurrencies_info():
    l = list()
    url = 'https://coinmarketcap.com'
    try:
        soup = get_soup_by_url(url)
        record_list = soup.find('tbody').find_all('tr')
        for record in record_list:
            fields = record.find_all('td')
            rank = fields[0].text.replace('\n', '')
            token = fields[1].find_all('a')[0].text
            full_name = fields[1].find_all('a')[1].text
            market_cap = fields[2].text.replace('$', '').replace(',', '').replace('\n', '')
            price = fields[3].text.replace('$', '').replace(',', '').replace('\n', '')
            volume = fields[4].text.replace('$', '').replace(',', '').replace('\n', '')
            circulating_supply = fields[5].text.replace(',', '').split('\n')[2]
            change = fields[6].text.replace('%', '').replace('\n', '')

            d = {
                'rank': rank,
                'token': token,
                'full_name': full_name,
                'market_cap': market_cap,
                'price': price,
                'volume': volume,
                'circulating_supply': circulating_supply,
                'change': change
            }
            l.append(d)
    except Exception, e:
        print e
    return json.dumps(l)


token_names = get_token_names()
token_in_usd = dict()
