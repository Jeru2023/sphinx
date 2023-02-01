# -*- coding: utf-8 -*-

import datetime
import pandas as pd
import time

import stock_api as sa
import mydb

def is_trading_day(date):
    start_date = date
    end_date = date
    
    df = sa.query_trade_dates(start_date, end_date)
    is_trading_day = df.iloc[0]['is_trading_day']
    
    if (is_trading_day=='1'):
        return True
    else: 
        return False

def get_latest_stock(code, end_date):
    latest_df = mydb.query_kline_latest_line(code)
    
    if len(latest_df['date'])==0:
        return

    #向后推移一天
    start_date = (latest_df['date'].values[0]+datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    stock_df = sa.query_stock_kline_daily(code, start_date, str(end_date))
    return stock_df
    
    #mydb.write_df_to_table(stock_df, 'stock_kline_daily')
    
def update_stock(code, end_date):
    latest_df = mydb.query_kline_latest_line(code)
    
    #print('latest date:{},end_date:{}'.format())
    
    if len(latest_df['date'])==0:
        return
    
    latest_date = str(latest_df['date'].values[0])

    if latest_date==str(end_date):
        print('same')
        return
    
    
    #向后推移一天
    start_date = (latest_df['date'].values[0]+datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    
    

    stock_df = sa.query_stock_kline_daily(code, start_date, str(end_date))
    mydb.write_df_to_table(stock_df, 'stock_kline_daily')
    
def update_all(date):
    code_list_df = mydb.query_stock_list()
    print("len ", len(code_list_df))
    
    i = 0
    for index, row in code_list_df.iterrows():
        i += 1
        if (i<5395):
            continue
        code = row['code']
        print('{} updating code: {}'.format(i, code))
        update_stock(code, today)
        
def update_all_backup(stock_list_df):
    df_all = pd.concat(stock_list_df)
    mydb.write_df_to_table(df_all, 'stock_kline_daily')

    
start_time = time.time()

today = datetime.date.today()
if is_trading_day(today):
    #stock_list_df = get_latest_stock_list(today)
    #update_all(stock_list_df)
    update_all(today)
    
end_time = time.time()
print('execute time: ', end_time-start_time)
