# -*- coding: utf-8 -*-
from trading_rule.only_macd_signal import trade

def main():

    try:
        trade()
        print('done')
    except BaseException as e:
        print(e)
        print('error')

if __name__ == "__main__":
    main()
    
