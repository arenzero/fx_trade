# -*- coding: utf-8 -*-
import pandas_datareader.data as pdr
import yfinance as yfin
import os

def scrape(start = '2021-06-07',end = '2021-09-13'):
    yfin.pdr_override()

    #scrape data
    jpy_usd = pdr.get_data_yahoo('JPY=X',start =start, end=end)
    eur_usd = pdr.get_data_yahoo('EURUSD=X',start =start, end=end)
    jpy_eur = jpy_usd/eur_usd

    #output file
    data_path = 'C:/Users/masay/Documents/Python Scripts/FX_trade/fx_trade/temp_data'
    jpy_usd.to_csv(data_path+'/jpy_usd.csv')
    eur_usd.to_csv(data_path+'/eur_usd.csv')
    jpy_eur.to_csv(data_path+'/jpy_eur.csv')

if __name__ == "__main__":
    scrape()
