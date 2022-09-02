import os
import pandas as pd
import datetime
from ..crypto.helpers import get_crypto_info
from ..stocks.helpers import get_stocks_info
from ..stocks.constants import *


def gen_csv_file_name(dir_name=None, file_name=None, hldg_type='stock'):
    if not dir_name:
        dir_name = os.path.abspath('.')
        folder_name = f'/records/{datetime.datetime.now().strftime("%B%Y")}/'
        dir_name = dir_name + folder_name
    if not file_name:
        time_now = datetime.datetime.now().strftime('%B%d%Y_%H%M')
        file_name = hldg_type + time_now + '.csv'

    abs_filename = os.path.join(os.path.abspath(dir_name), file_name)
    abs_dirname = os.path.dirname(abs_filename)
    if not os.path.exists(abs_dirname):
        os.makedirs(abs_dirname)
    if not os.path.exists(abs_filename):
        open(abs_filename, 'w').close()
    return abs_filename


def export_stocks(dir_name=None, file_name=None, rh=None):
    df = pd.DataFrame(get_stocks_info(rh))
    filename = gen_csv_file_name(dir_name, file_name, hldg_type='stock')
    df.to_csv(filename, index=False)
    print(f'Success! File can be found at the location {filename}')


def export_crypto(dir_name=None, file_name=None, rh=None):
    df = pd.DataFrame(get_crypto_info(rh))
    filename = gen_csv_file_name(dir_name, file_name, hldg_type='crypto')
    df.to_csv(filename, index=False)
    print(f'Success! File can be found at the location {filename}')


def export_profitability(dir_name=None, file_name=None, rh=None):
    stocks_dict = get_stocks_info(rh)
    stocks_df = pd.DataFrame(stocks_dict)
    crypto_dict = get_crypto_info(rh)
    crypto_df = pd.DataFrame(crypto_dict)

    total_equity_change_stocks = sum(stocks_dict[equity_change])
    total_equity_change_crypto = sum(crypto_dict[equity_change])
    total_equity_change = total_equity_change_crypto + total_equity_change_stocks

    total_purchased_equity_stocks = sum(stocks_dict[purchased_equity])
    total_purchased_equity_crypto = sum(crypto_dict[purchased_equity])
    total_purchased_equity = total_purchased_equity_crypto + \
        total_purchased_equity_stocks

    stocks_pct = 100 * (total_equity_change_stocks /
                        total_purchased_equity_stocks)
    crypto_pct = 100 * (total_equity_change_crypto /
                        total_purchased_equity_crypto)
    total_pct = 100 * (total_equity_change/total_purchased_equity)

    disp_dict = {
        "Investment Type": ["Stocks", "Crypto", "Total"],
        "Purchased Equity": [total_purchased_equity_stocks, total_purchased_equity_crypto, total_purchased_equity],
        "Equity Change": [total_equity_change_stocks, total_equity_change_crypto, total_equity_change],
        "Percent Change": [stocks_pct, crypto_pct, total_pct],
    }
    df = pd.DataFrame(disp_dict)
    report_filename = gen_csv_file_name(
        dir_name, file_name, hldg_type='report')
    stocks_filename = gen_csv_file_name(
        dir_name, file_name, hldg_type='stocks')
    crypto_filename = gen_csv_file_name(
        dir_name, file_name, hldg_type='crypto')

    df.to_csv(report_filename, index=False)
    stocks_df.to_csv(stocks_filename, index=False)
    crypto_df.to_csv(crypto_filename, index=False)

    print(
        f'Success! Report Files can be found at the location {os.path.abspath(os.path.dirname(report_filename))}')
