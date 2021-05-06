
from .constants import *
# import robin_stocks.robinhood as rh
import copy
import datetime

def get_stocks_info(rh):
    overall_data = copy.deepcopy(DATA_JSON)
    stocks_meta = rh.build_holdings()
    for i, tkr_name in enumerate(stocks_meta.keys()):
        val = stocks_meta[tkr_name]
        overall_data[sl_no].append(i)
        overall_data[ticker].append(tkr_name)
        overall_data[quantity].append(float(val['quantity']))
        overall_data[item_type].append(val['type'])
        overall_data[avg_purchase_price].append(float(val['average_buy_price']))
        overall_data[curr_price].append(float(val['price']))
        purchased_equity_val = str(float(val['average_buy_price']) * float(val['quantity']))
        overall_data[purchased_equity].append(purchased_equity_val)
        overall_data[curr_equity].append(float(val['equity']))
        overall_data[equity_change].append(float(val['equity_change']))
        overall_data[pe_ratio].append(float(val['pe_ratio']))
        overall_data[logging_time].append(
            datetime.datetime.now().strftime('%H:%M:%S'))
        overall_data[logging_date].append(
            datetime.datetime.now().date().strftime('%y-%m-%d'))
    return overall_data
