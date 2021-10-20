# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.metrics import accuracy_score

import sys
sys.path.append('C:/Users/masay/Documents/Python Scripts/FX_trade/fx_trade')
from utils.macd import calc_macd,out_cross_flag

"""
半年検証後、良ければ再学習して予測
"""


def trade(current_day = '2021-06-14',posses = {'JPY':10000,'USD':0},df = pd.read_csv('C:/Users/masay/Documents/Python Scripts/FX_trade/fx_trade/temp_data/jpy_usd.csv')):

    df_c = df.copy()

    #データの前処理
    try:
        df_c.index = pd.to_datetime(df_c['Date'])
        del df_c['Date']
    except:
        pass
    
    next_day = df_c[current_day:].index[0]
    df_c = df_c[:current_day]

    #次の1日の分行を足しておく
    df_c.loc[next_day] = 0

    #MACDの計算
    macd,macd_signal = calc_macd(df_c['Close'],short_term=12,long_term=26,signal_term=9)
    df_c['macd_flag'] = out_cross_flag(macd,macd_signal)

    macd = pd.concat([macd,macd_signal],axis=1)
    macd.columns = ['macd','macd_signal']

    df_c = pd.concat([df_c,macd],axis=1)
    df_c = df_c.drop(['Adj Close','Volume'],axis=1)

    col = df_c.columns

    for i in range(1,20):
        x = df_c[col].shift(i)
        x.columns = [col+'_shift'+str(i) for col in x.columns]
        df_c = pd.concat([df_c,x],axis=1)

    df_c = df_c.drop(col[col!='Close'],axis=1)
    close = df_c['Close'].copy()

    df_c[df_c.columns[~df_c.columns.isin([col for col in df_c.columns if 'macd' in col])]] = (df_c[df_c.columns[~df_c.columns.isin([col for col in df_c.columns if 'macd' in col])]].div(df_c['Close_shift1'],axis=0)-1)*100

    df_c['Close'] = close

    for i in range(1,20):
        x = df_c['Close'].shift(i)
        df_c['Close_raw_shift'+str(i)] = x

    df_c = df_c.replace({np.inf:0})
    df_c = df_c.iloc[40:,:]
    df_c = df_c.replace({'gold':1,'dead':-1})

    
    reg = lgb.LGBMRegressor()

    about_three_years = 750
    about_half_years = 110

    train = df_c.iloc[-about_three_years-about_half_years:-about_half_years,:]

    reg.fit(train.drop('Close',axis=1),train['Close'])

    test = df_c.iloc[-about_half_years:,:]
    pred = reg.predict(test.drop('Close',axis=1))

    t = test[:-1]['Close'].diff()
    t = t.mask(t>0,1)
    t = t.mask(t<0,0)

    y = pd.Series(pred,index=test.index).diff()
    y = y.mask(y>0,1)
    y = y.mask(y<0,0)

    acc = accuracy_score(t.dropna(),y[:-1].dropna())

    flag = 0
    print('accuracy:',acc)
    #直近半年の精度が80％以上なら再学習して予測に応じて取引
    if acc>0.7:
        train = df_c.iloc[-about_three_years:-1,:]
        pred_data = df_c.iloc[-1,:]
        reg.fit(train.drop('Close',axis=1),train['Close'])
        pred = reg.predict(pd.DataFrame(pred_data).T.drop('Close',axis=1))
        #今日の引値より明日の予想引値が高いなら買い、逆なら売り（翌日のOpenからCloseで取引）
        if df_c['Close'][-2] < pred[0]:
            posses['USD'] += (posses['JPY']*0.5/df_c['Close'][-2]*0.9999)
            posses['JPY'] = posses['JPY']*0.5
            flag = 'after_sell'

        elif df_c['Close'][-2] > pred[0]:
            posses['JPY'] += (posses['USD']*0.5*df_c['Close'][-2]*0.9999)
            posses['USD'] = posses['USD']*0.5
            flag = 'after_buy'

    del df_c
    return posses,flag

if __name__ == "__main__":
    trade()
