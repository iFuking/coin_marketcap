
from bs4 import BeautifulSoup
import utils
import json, csv

def get_btc_or_eth_in_usd(token):
    url = 'https://coinmarketcap.com/currencies/%s/' % token
    soup = utils.get_soup_by_url(url)
    price = soup.find('span', class_='h2 text-semi-bold details-panel-item--price__value').text.replace(',','')
    return price

def get_market_trading_in_btc_or_eth(trading_list, token):
    for info in trading_list:
        info['open'] = float(info['open']) / token
        info['high'] = float(info['high']) / token
        info['low'] = float(info['low']) / token
        info['close'] = float(info['close']) / token
        info['volume']= float(info['volume']) / token
        info['market_cap'] = float(info['market_cap']) / token

def trading_market_json_to_csv(rows):
    csv_str = 'date,market_cap,rank,price_last,hight,low,volume\n'
    for r in rows:
        csv_str += (r['date'] + ',')
        csv_str += (str(r['market_cap']) + ',')
        csv_str += (str(r['rank']) + ',')
        csv_str += (str(r['open']) + ',')
        csv_str += (str(r['high']) + ',')
        csv_str += (str(r['low']) + ',')
        csv_str += (str(r['volume']) + '\n')
    return csv_str

def get_token_rank(token_name):
    l = list()
    url = 'https://coinmarketcap.com'
    try:
        soup = utils.get_soup_by_url(url)
        token_list = soup.find('tbody').find_all('tr')
        for token in token_list:
            rank = token.find('td').text.replace('\n','').replace(' ','')
            id = token.get('id')[3:]
            if id == token_name:
                return int(rank)

            d = dict()
            d[id] = rank
            l.append(d)

    except Exception, e:
        print e
    return 0

def month_convert(month):
    month_str = [
        '', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
        'Oct', 'Nov', 'Dec'
    ]
    for index in range(len(month_str)):
        if month_str[index] == month:
            return str(index).zfill(2)
    return str(0)

def date_format(date):
    fields = date.split(' ')

    year = fields[2]
    month = month_convert(fields[0])
    day = fields[1]
    return year + '/' + month + '/' + day

def get_market_trading(url, token):
    print url
    rank = get_token_rank(token)

    l = list()
    soup = utils.get_soup_by_url(url)
    records = soup.find_all('tr', class_='text-right')
    for record in records:

        fields = record.find_all('td')

        date = fields[0].text.replace(',','')
        open_price = fields[1].text.replace(',','')
        high_price = fields[2].text.replace(',','')
        low_price = fields[3].text.replace(',','')
        close_price = fields[4].text.replace(',','')
        volume = fields[5].text.replace(',','')
        market_cap = fields[6].text.replace(',','')

        d = {
            'date': date_format(date),
            'open': open_price,
            'high': high_price,
            'low': low_price,
            'close': close_price,
            'volume': volume,
            'market_cap': market_cap,
            'rank': rank
        }
        print json.dumps(d)
        l.append(d)
    return l

