
from bs4 import BeautifulSoup
import utils
import json, csv

def get_trading_pairs(url, topk=5):
    print url
    l = list()
    soup = utils.get_soup_by_url(url)
    records = soup.find('table', id='markets-table').find('tbody').find_all('tr')
    cnt = 1
    for record in records:
        fields = record.find_all('td')
        rank = fields[0].text.replace('\n','')
        source = fields[1].text.replace('\n','')
        pair = fields[2].text.replace('\n','')
        volume = fields[3].text.replace('\n','').replace(',','').replace('$','')
        price = fields[4].text.replace('\n','').replace(',','').replace('$','')
        percent = fields[5].text.replace('\n','')

        d = {
            'rank': rank,
            'source': source,
            'pair': pair,
            'volume': volume,
            'price': price,
            'percent': percent
        }
        print json.dumps(d)
        l.append(d)

        if cnt >= topk:
            break
        cnt = cnt + 1
    return l

def trading_pair_json_to_csv(rows):
    csv_str = 'rank,source,pair,price,volume,volume_percentage\n'
    for r in rows:
        csv_str += (r['rank'] + ',')
        csv_str += (str(r['source']) + ',')
        csv_str += (str(r['pair']) + ',')
        csv_str += (str(r['price']) + ',')
        csv_str += (str(r['volume']) + ',')
        csv_str += (str(r['percent']) + '\n')
    return csv_str


