import os
import pandas as pd
import datetime
from ..crypto.helpers import get_crypto_info
from ..stocks.helpers import get_stocks_info


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






