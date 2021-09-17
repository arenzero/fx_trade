# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

def ema(s, term=5):
    '''
    指数平滑移動平均の計算
    s:pd.Series,fx data
    term:term
    return ema
    '''
    sma = s.rolling(term).mean()[:term]
    return pd.concat([sma, s[term:]]).ewm(span=term, adjust=False).mean()

def calc_macd(s,short_term=12,long_term=26, signal_term=9):
    """
    s: pd.Series、為替データ
    return: macd,macd_signal
    """
    short_term_ema = ema(s,short_term)
    long_term_ema = ema(s,long_term)
    macd = short_term_ema - long_term_ema
    macd_signal = ema(macd,signal_term)
    return macd,macd_signal

def out_cross_flag(macd,macd_signal):
    """
    macdからgolden flagやdead flagを立てる
    return:pd.Series, contents = ['gold','dead',np.nan,0]
    
    """

    cross_list = []
    be_flag = 0
    af_flag = 0
    for i in range(len(macd)):

        #欠損値でないなら
        if ~np.isnan(macd[i]):
            #どちらが上かによるフラグ
            if macd[i] <= macd_signal[i]:
                af_flag = 0
            else:
                af_flag = 1

            #一つ前のフラグより大きい小さいがあればクロス
            if be_flag < af_flag:
                cross_list.append('gold')
            elif be_flag > af_flag:
                cross_list.append('dead')
            else:
                cross_list.append(0)
        else:
            cross_list.append(np.nan)

        #フラグ更新
        be_flag = af_flag
    return pd.Series(cross_list,index=macd.index)

def trade(current_day = '2021-06-07',posses = {'JPY':10000,'USD':0},jpy_usd = pd.read_csv('../temp_data/jpy_usd.csv')):
    

    #データの前処理
    jpy_usd.index = pd.to_datetime(jpy_usd['Date'])
    del jpy_usd['Date']
    jpy_usd = jpy_usd[:current_day]

    #MACDの計算
    macd,macd_signal = calc_macd(jpy_usd['Close'],short_term=6,long_term=14,signal_term=6)
    jpy_usd['macd_flag'] = out_cross_flag(macd,macd_signal)

    today = jpy_usd.iloc[-1,:]

    #trading rule
    if today['macd_flag'] == 'gold':
        posses['USD'] += posses['JPY']*0.1/today['Close']
    elif today['macd_flag'] == 'dead':
        posses['JPY'] += posses['USD']*today['Close']
    
    print(posses)

if __name__ == "__main__":
    trade()
