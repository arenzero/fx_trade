# -*- coding: utf-8 -*-

def calc_rsi(x):
    """
    paramで指定された区間の系列内で前日比を元にRSIを計算
    input
        x:指定された区間の前日比系列
    output
        指定された区間のRSI系列
    """
    x_plus = x[x>0]
    x_minus = x[x<0]
    xpm = x_plus.mean()
    xmm = x_minus.mean()
    
    return xpm/(xpm-xmm)*100

def output_rsi_time_series(s,param):
    """
    paramで指定された区間の系列内で前日比を元にRSIを計算
    input
        s:pd.series どこか一列
        param:パラメータ
    output
        RSI系列
    """
    return s.diff().rolling(param).apply(calc_rsi)