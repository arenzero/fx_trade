# -*- coding: utf-8 -*-
import configparser

# ファイルの存在チェック用モジュール
import os
import errno

def read_config(config_ini_path='C:/Users/masay/Documents/Python Scripts/FX_trade/fx_trade/config.ini'):
    """
    iniファイルの読み込み
    """

    config_ini = configparser.ConfigParser()

    # 指定したiniファイルが存在しない場合、エラー発生
    if not os.path.exists(config_ini_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_ini_path)

    config_ini.read(config_ini_path, encoding='utf-8')

    return config_ini

if __name__ == "__main__":
    read_config()
