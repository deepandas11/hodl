#!/usr/bin/env python
import argparse
import os
import pyotp
import robin_stocks.robinhood as rh

from src.export.csv_exporter import export_crypto, export_stocks

parser = argparse.ArgumentParser(description='arguments for hodl app')

parser.add_argument('--type', type=str, help='specify the kind of holdings you want to snapshot', default='')
parser.add_argument('--name', type=str, help='specify the filepath for saving the snapshots')


if __name__ == '__main__':
    args = parser.parse_args()

    RH_UNAME = os.environ.get("robinhood_username")
    RH_PWD = os.environ.get("robinhood_password")
    totp = pyotp.TOTP("authy").now()
    lg = rh.login(username=RH_UNAME, password=RH_PWD, mfa_code=totp)

    file_name = None
    dir_name = None
    if args.name:
        try:
            dir_name = os.path.dirname(args.name)
            file_name = args.name.split(dir_name)[1][1:]
        except:
            pass

    if args.type == 'crypto':
        export_crypto(dir_name=dir_name, file_name=file_name, rh=rh)
    elif args.type == 'stocks':
        export_stocks(dir_name=dir_name, file_name=file_name, rh=rh)
    elif args.type == 'both' or args.type == '':
        export_crypto(dir_name=dir_name, file_name=file_name, rh=rh)
        export_stocks(dir_name=dir_name, file_name=file_name, rh=rh)
    else:
        print("Please specify valid type")

    rh.logout()
    
    print('Done!')
