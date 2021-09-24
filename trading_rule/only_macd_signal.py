# -*- coding: utf-8 -*-
import pandas as pd
from utils.macd import calc_macd,out_cross_flag
import sys

sys.path.append('C:/Users/masay/Documents/Python Scripts/FX_trade/fx_trade')

def trade(current_day = '2021-06-07',posses = {'JPY':10000,'USD':0},df = pd.read_csv('C:/Users/masay/Documents/Python Scripts/FX_trade/fx_trade/temp_data/jpy_usd.csv')):
    
    #データの前処理
    try:
        df.index = pd.to_datetime(df['Date'])
        del df['Date']
    except:
        pass
    df = df[:current_day]

    #MACDの計算
    macd,macd_signal = calc_macd(df['Close'],short_term=12,long_term=26,signal_term=9)
    df['macd_flag'] = out_cross_flag(macd,macd_signal)

    today = df.iloc[-1,:]

    #trading rule
    if today['macd_flag'] == 'gold':
        posses['USD'] += posses['JPY']/today['Close']
        posses['JPY'] = 0
    elif today['macd_flag'] == 'dead':
        posses['JPY'] += posses['USD']*today['Close']
        posses['USD'] = 0
    
    del df
    return posses

if __name__ == "__main__":
    trade()
