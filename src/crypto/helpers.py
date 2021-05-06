import datetime
import copy
from .constants import *

def get_crypto_info(rh):
    overall_data = copy.deepcopy(DATA_JSON)
    current_orders = fetch_active_crypto_transactions(rh)

    for i, coin in enumerate(current_orders.keys()):
        coin_dict = process_each_crypto(current_orders[coin], rh)
        for key in coin_dict.keys():
            overall_data[key].append(coin_dict[key])
        overall_data[sl_no].append(i)
    
    return overall_data


def fetch_active_crypto_transactions(rh):
    crypto_positions = rh.get_crypto_positions()
    active_positions = [item['currency']['code']+'USD' for item in crypto_positions if float(item['quantity']) ]
    transactions = {key : [] for key in active_positions}
    all_orders = rh.get_all_crypto_orders()
    for order in all_orders:
        order_key = rh.get_crypto_quote_from_id(order['currency_pair_id'], 'symbol')
        if order_key in transactions:
            transactions[order_key].append({
                'date' : order['last_transaction_at'],
                'tx_type': order['side'],
                'quantity': float(order['quantity']),
                'average_price': float(order['average_price']),
                'crypto_symbol': order_key.split('USD')[0]
            })
            
    for key in transactions:
        transactions[key] = sorted(transactions[key], key=lambda i: i['date'])
    
    return transactions


def process_each_crypto(meta, rh):
    avg_price_list = [0]
    total_coins_list = [0]
    for i, order in enumerate(meta):
        tkr = order['crypto_symbol']
        if order['tx_type'] == 'sell' and i == 0:
            raise Exception('First order cannot be sold')
        avg_price_list, total_coins_list = process_each_order(
            avg_price_list, total_coins_list, order)

    avg_price, total_coins = avg_price_list[-1], total_coins_list[-1]

    current_price = float(rh.get_crypto_quote(tkr, info='mark_price'))
    crypto_dict = {
        ticker: tkr,
        quantity: total_coins,
        item_type: 'crypto',
        avg_purchase_price: avg_price,
        curr_price: current_price,
        purchased_equity: avg_price * total_coins,
        curr_equity: current_price * total_coins,
        equity_change: (current_price - avg_price) * total_coins,
        pe_ratio: 0,
        logging_time: datetime.datetime.now().strftime('%H:%M:%S'),
        logging_date: datetime.datetime.now().date().strftime('%y-%m-%d'),
    }

    return crypto_dict


def process_each_order(avg_price_list={}, total_coins_list=[], order={}):

    buy = True if order['tx_type'] == 'buy' else False

    if len(avg_price_list) == 0 and not buy:
        raise Exception('Cannot sell when liquidity list is empty')

    order_coins, order_price = order['quantity'], order['average_price']
    total_coins, avg_price = total_coins_list[-1], avg_price_list[-1]

    if not buy:
        total_coins_list.append(total_coins-order_coins)
        avg_price_list.append(avg_price)
    else:
        prev_liquidity = total_coins * avg_price
        order_liquidity = order_coins * order_price
        new_avg_price = (prev_liquidity + order_liquidity) / \
            (total_coins + order_coins)
        total_coins_list.append(total_coins+order_coins)
        avg_price_list.append(new_avg_price)

    return avg_price_list, total_coins_list



