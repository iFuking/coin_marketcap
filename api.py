#/usr/bin/python
# -*- coding=utf-8 -*-

from flask import Flask, url_for, request, json
from flask_restful import Resource, Api

from bs4 import BeautifulSoup
import urllib, urllib2
import json, csv
import logging
import sys
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

def get_token_rank(token_name):
    l = list()
    url = 'https://coinmarketcap.com'
    try:
        soup = get_soup_by_url(url)
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

def get_market_trading(url, token):
    print url
    rank = get_token_rank(token)

    l = list()
    soup = get_soup_by_url(url)
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

def get_btc_or_eth_in_usd(token):
    url = 'https://coinmarketcap.com/currencies/%s/' % token
    soup = get_soup_by_url(url)
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

def get_trading_pairs(url, topk=5):
    print url
    l = list()
    soup = get_soup_by_url(url)
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

token_in_usd = dict()


app = Flask(__name__)
api = Api(app)

@app.route('/market_trading')
def api_market_trading():
    l = list()
    if 'date' in request.args and 'token' in request.args:
        date = request.args['date']
        token = request.args['token']
        if token not in token_names:
            return token_not_exists_err(token)

        try:
            url = 'https://coinmarketcap.com/currencies/%s/historical-data/?start=%s&end=%s' % (token, date, date)
            l = get_market_trading(url, token)
        except Exception, e:
            print e
    elif 'start_date' in request.args and 'end_date' in request.args and 'token' in request.args:
        start_date = request.args['start_date']
        end_date = request.args['end_date']
        token = request.args['token']
        if token not in token_names:
            return token_not_exists_err(token)

        try:
            url = 'https://coinmarketcap.com/currencies/%s/historical-data/?start=%s&end=%s' % (token, start_date, end_date)
            l = get_market_trading(url, token)
        except Exception, e:
            print e

    if 'type' in request.args:
        type = request.args['type']
        token_in_usd['usd'] = 1
        token_in_usd['btc'] = get_btc_or_eth_in_usd('bitcoin')
        token_in_usd['eth'] = get_btc_or_eth_in_usd('ethereum')
        get_market_trading_in_btc_or_eth(l, float(token_in_usd[type]))
    return trading_market_json_to_csv(l)
    # return json.dumps(l)

@app.route('/trading_pair')
def api_trading_pair():
    l = list()
    if 'token' in request.args:
        token = request.args['token']
        if token not in token_names:
            return token_not_exists_err(token)

        try:
            url = 'https://coinmarketcap.com/currencies/%s/#markets' % token
            if 'topk' in request.args:
                topk = request.args['topk']
                l = get_trading_pairs(url, int(topk))
            else:
                l = get_trading_pairs(url)
        except Exception, e:
            print e

    return trading_pair_json_to_csv(l)
    # return json.dumps(l)

@app.route('/tokens')
def api_token_names():
    return json.dumps(token_names) + '\n'

@app.route('/hello')
def api_hello():
    return 'hello\n'

if __name__ == '__main__':
    # create Stream Handler.
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(ch)

    app.run(debug=True)
