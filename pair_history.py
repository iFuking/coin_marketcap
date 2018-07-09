
from bs4 import BeautifulSoup
import json, time
import utils

def get_token_trading_pairs(url, token):
    print url
    l = list()
    soup = utils.get_soup_by_url(url)
    records = soup.find('table', id='markets-table').find('tbody').find_all('tr')
    for record in records:
        fields = record.find_all('td')
        rank = fields[0].text.replace('\n','')
        source = fields[1].text.replace('\n','')
        pair = fields[2].text.replace('\n','')
        volume = fields[3].text.replace('\n','').replace(',','').replace('$','').replace(' ','').replace('*','')
        price = fields[4].text.replace('\n','').replace(',','').replace('$','').replace(' ','').replace('*','')
        percent = fields[5].text.replace('\n','').replace(' ','')
        date = time.strftime("%Y/%m/%d", time.gmtime())

        if float(percent.replace('%','')) == 0:
            continue

        d = {
            'token': token,
            'date': date,
            'rank': rank,
            'source': source,
            'pair': pair,
            'volume': volume,
            'price': price,
            'percent': percent
        }
        print json.dumps(d)
        l.append(d)

        if len(l) == 5:
            break

    print len(l)
    return l

def get_all_tokens_trading_pairs():
    token_names = utils.get_token_names()
    url = 'https://coinmarketcap.com'
    all_tokens_trading_pairs = list()
    for token in token_names:
        pair_url = url + '/currencies/' + token + '/#markets'
        l = get_token_trading_pairs(pair_url, token)
        all_tokens_trading_pairs.append(l)
    return all_tokens_trading_pairs

def write_trading_pairs_to_db():
    all_tokens_trading_pairs = get_all_tokens_trading_pairs()
    for token in all_tokens_trading_pairs:
        for record in trading_pairs:
            break
    return

