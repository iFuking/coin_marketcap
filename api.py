#/usr/bin/python
# -*- coding=utf-8 -*-

from flask import Flask, url_for, request, json
from flask_restful import Resource, Api
import sys, logging
import threading

from mysql_tables import app
import utils, market_trading, trading_pair, pair_history
from utils import logger, token_in_usd, token_names

api = Api(app)


@app.route('/market_trading')
def api_market_trading():
    l = list()
    if 'date' in request.args and 'token' in request.args:
        date = request.args['date']
        token = request.args['token']
        if token not in token_names:
            return utils.token_not_exists_err(token)

        try:
            url = 'https://coinmarketcap.com/currencies/%s/historical-data/?start=%s&end=%s' % (
                token, date, date)
            l = market_trading.get_market_trading(url, token)
        except Exception, e:
            print e
    elif 'start_date' in request.args and 'end_date' in request.args and 'token' in request.args:
        start_date = request.args['start_date']
        end_date = request.args['end_date']
        token = request.args['token']
        if token not in token_names:
            return utils.token_not_exists_err(token)

        try:
            url = 'https://coinmarketcap.com/currencies/%s/historical-data/?start=%s&end=%s' % (
                token, start_date, end_date)
            l = market_trading.get_market_trading(url, token)
        except Exception, e:
            print e

    if 'type' in request.args:
        type = request.args['type']
        token_in_usd['usd'] = 1
        token_in_usd['btc'] = market_trading.get_btc_or_eth_in_usd('bitcoin')
        token_in_usd['eth'] = market_trading.get_btc_or_eth_in_usd('ethereum')
        market_trading.get_market_trading_in_btc_or_eth(
            l, float(token_in_usd[type]))
    return market_trading.trading_market_json_to_csv(l)
# return json.dumps(l)


@app.route('/trading_pair')
def api_trading_pair():
    l = list()
    if 'token' in request.args:
        token = request.args['token']
        if token not in token_names:
            return utils.token_not_exists_err(token)

        try:
            url = 'https://coinmarketcap.com/currencies/%s/#markets' % token
            if 'topk' in request.args:
                topk = request.args['topk']
                l = trading_pair.get_trading_pairs(url, int(topk))
            else:
                l = trading_pair.get_trading_pairs(url)
        except Exception, e:
            print e

    return trading_pair.trading_pair_json_to_csv(l)
# return json.dumps(l)


@app.route('/pair_history_sum')
def api_pair_history_sum():
    token = 'all'
    topk = 5
    l = list()

    if 'date' in request.args:
        date = request.args['date']
        token = 'all'
        topk = 5

        if 'token' in request.args:
            token = request.args['token']
            if token not in token_names:
                return utils.token_not_exists_err(token)
        if 'topk' in request.args:
            topk = request.args['topk']
        l = pair_history.read_trading_pairs_sum_from_db(date, date, token, int(topk))

    elif 'start_date' in request.args and 'end_date' in request.args:
        # start_date = request.args['start_date']
        end_date = request.args['end_date']

        if 'token' in request.args:
            token = request.args['token']
            if token not in token_names:
                return utils.token_not_exists_err(token)
        if 'topk' in request.args:
            topk = request.args['topk']
        l = pair_history.read_trading_pairs_sum_from_db(start_date, end_date, token, int(topk))

    return pair_history.pair_history_sum_json_to_csv(l)


@app.route('/pair_history')
def api_pair_history():
    token = 'all'
    k = 1
    topk = 5
    l = list()

    if 'date' in request.args:
        date = request.args['date']

        if 'token' in request.args:
            token = request.args['token']
            if token not in token_names:
                return utils.token_not_exists_err(token)
        if 'topk' in request.args:
            topk = request.args['topk']
            l = pair_history.read_trading_pair_from_db_with_topk(date, date, token, int(topk))
        elif 'k' in request.args:
            k = request.args['k']
            l = pair_history.read_trading_pair_from_db_with_k(date, date, token, int(k))

    elif 'start_date' in request.args and 'end_date' in request.args:
        start_date = request.args['start_date']
        end_date = request.args['end_date']

        if 'token' in request.args:
            token = request.args['token']
            if token not in token_names:
                return utils.token_not_exists_err(token)
        if 'topk' in request.args:
            topk = request.args['topk']
            l = pair_history.read_trading_pair_from_db_with_topk(start_date, end_date, token, int(topk))
        elif 'k' in request.args:
            k = request.args['k']
            l = pair_history.read_trading_pair_from_db_with_k(start_date, end_date, token, int(k))

    return pair_history.pair_history_json_to_csv(l)


@app.route('/start_timer')
def api_start_timer():
    pair_history.write_trading_pairs_to_db()
    return ''


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
