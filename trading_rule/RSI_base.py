# -*- coding: utf-8 -*-
import pandas as pd

import matplotlib.pyplot as plt
import numpy as np

import sys
sys.path.append('C:/Users/masay/Documents/Python Scripts/FX_trade/fx_trade')
from utils.RSI import output_rsi_time_series

def trade(current_day = '2021-06-14',posses = {'JPY':10000,'USD':0},df = pd.read_csv('C:/Users/masay/Documents/Python Scripts/FX_trade/fx_trade/temp_data/jpy_usd.csv')):

    df_c = df.copy()

    #データの前処理
    try:
        df_c.index = pd.to_datetime(df_c['Date'])
        del df_c['Date']
    except:
        pass
    
    df_c = df_c[:current_day]

    df_c = df_c.drop(['Adj Close','Volume','High','Low','Open'],axis=1)

    #過去約3年で最も利益率が高いRSI値を使い、直近半年で一応確認して最終的に使う

    about_three_years = 250
    about_half_years = 60

    train = df_c.iloc[-about_three_years-about_half_years:-about_half_years,:]
    test = df_c.iloc[-about_half_years:,:]

    max_sharp = -np.inf

#     for param in [9,11,13,14,16,18]:

#         # print('param:',param)
#         #RSIの計算
#         train['RSI_'+str(param)] = output_rsi_time_series(train['Close'],param=param)
#         train['buy_sell_flag'] = 0
#         train.loc[train['RSI_'+str(param)]>=70,'buy_sell_flag'] = 'sell'
#         train.loc[train['RSI_'+str(param)]<=30,'buy_sell_flag'] = 'buy'
        
#         #バックテスト
#         rec = []
#         posses_ = {'JPY':10000,'USD':0}
#         for i in range(len(train)):
#             if train['buy_sell_flag'][i]=='buy':
#                 posses_['JPY'] += posses_['USD']*train.iloc[i,0]
#                 posses_['USD'] = 0
#                 rec.append(posses_['JPY']+posses_['USD']*train.iloc[i,0])

#             elif train['buy_sell_flag'][i]=='sell':
#                 posses_['USD'] += posses_['JPY']/train.iloc[i,0]
#                 posses_['JPY'] = 0
#                 rec.append(posses_['JPY']+posses_['USD']*train.iloc[i,0])
        
#         #シャープレシオ計算
#         rec = np.array(rec)
#         risk = rec.std()/10000
#         ret = (rec.mean()-10000)/10000
#         sharp = ret/risk
#         # print('シャープレシオ:',sharp)
        
#         # print('最終収支:',rec[-1])
        
#         #最高記録
#         if max_sharp < sharp:
#             max_sharp = sharp
#             max_param = param
    max_param = 9
    # print('最も良いRSIパラメータ:',max_param)

#     #RSIの計算
#     test['RSI_'+str(max_param)] = output_rsi_time_series(test['Close'],param=max_param)
#     test['buy_sell_flag'] = 0
#     test.loc[test['RSI_'+str(max_param)]>=70,'buy_sell_flag'] = 'sell'
#     test.loc[test['RSI_'+str(max_param)]<=30,'buy_sell_flag'] = 'buy'

#     #バックテスト
#     rec = []
#     posses_ = {'JPY':10000,'USD':0}
#     for i in range(len(test)):
#         if test['buy_sell_flag'][i]=='buy':
#             posses_['JPY'] += posses_['USD']*test.iloc[i,0]
#             posses_['USD'] = 0
#             rec.append(posses_['JPY']+posses_['USD']*test.iloc[i,0])

#         elif test['buy_sell_flag'][i]=='sell':
#             posses_['USD'] += posses_['JPY']/test.iloc[i,0]
#             posses_['JPY'] = 0
#             rec.append(posses_['JPY']+posses_['USD']*test.iloc[i,0])

#     #シャープレシオ計算
#     rec = np.array(rec)
#     risk = rec.std()/10000
#     ret = (rec.mean()-10000)/10000
#     sharp = ret/risk
#     # print('シャープレシオ:',sharp)

#     # print('最終収支:',rec[-1])

    #トレード
    df_c['RSI_'+str(max_param)] = output_rsi_time_series(df_c['Close'],param=max_param)

    last_rsi = df_c['RSI_'+str(max_param)][-1]

    #直近半年の収支がきちんと＋になるなら売買をRSIによって行う
    sharp = 1
    flag = 0
    if sharp>0:
        flag = 0
        # if last_rsi<=30:
        #     posses['JPY'] += posses['USD']*df_c.iloc[-1,0]
        #     posses['USD'] = 0

        if last_rsi>=70:
            posses['USD'] += posses['JPY']/df_c.iloc[-1,0]
            posses['JPY'] = 0
            flag = 'buy'

    return posses,flag

if __name__ == "__main__":
    trade()
