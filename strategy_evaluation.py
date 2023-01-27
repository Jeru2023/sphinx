import baostock as bs
import pandas as pd
import mydb
import math
import time

# 捕获单只股票满足策略模型的记录
# volume_mean_window_len 为对比滚动移动平均线的时间窗口长度，如10则对比过去10日的平均成交量
# volume_multiple 为当日成交量对比过去mean_window_len范围内平均成交量的倍数
# exit_window_len 为卖出的时间窗口长度，如-15则在15日后卖出
def get_capture_record(stock_df, volume_mean_window_len, volume_multiple, exit_window_len, pb_cap=100, pe_cap=100):
    stock_df['volume_rolling_mean'] = stock_df['volume'].rolling(volume_mean_window_len).mean()
    stock_df['profit'] = stock_df['close'].shift(exit_window_len)-stock_df['close']
    
    row_list = []
    for index, row in stock_df.iterrows():
        if (index<volume_mean_window_len):
            continue
        
        # 放量收阳线
        if (pb_cap<100):
            indicator_condition = row['pbMRQ']<pb_cap
        elif (pe_cap<100):
            indicator_condition = row['peTTM']<pe_cap

        if (row['volume']>row['volume_rolling_mean']*volume_multiple) and (row['pctChg']>0) and indicator_condition:
            row_list.append(row)
    return row_list

# 根据捕获记录评估单只股票的策略收益
def evaluate_stock_profit(row_list):
    stock_profit_ratio = 0.0
    stock_size = 0
    for row in row_list:
        profit = float(row['profit'])
        profit_ratio = float(profit/row['close'])
        if math.isnan(profit_ratio):
            continue
        stock_size += 1
        stock_profit_ratio += profit_ratio
        
    print('stock size: ', stock_size)
    if stock_size==0:
        return float('nan'), 0
    return stock_profit_ratio, stock_size

# 按行业评估策略模型整体收益
def evaluate_industry_profit(stock_list_df, volume_mean_window_len, volume_multiple, exit_window_len, pb_cap):
    code_list = stock_list_df['code'].unique()
    
    total_profit_ratio = 0.0
    total_size = 0
    
    for code in code_list:
        stock_df = stock_list_df[stock_list_df['code']==code]
        print(stock_df['code_name'].unique(), code)
    
        row_list = get_capture_record(stock_df, volume_mean_window_len, volume_multiple, exit_window_len, pb_cap)
        stock_profit_ratio, stock_size = evaluate_stock_profit(row_list)
        
        if (math.isnan(stock_profit_ratio) or stock_size<1):
            continue
        total_size += stock_size
        total_profit_ratio += float(stock_profit_ratio)
    
        print('average stock profit ratio: ', stock_profit_ratio/stock_size)    
        print('-------------------')
        
    return float(total_profit_ratio), total_size

# 根据捕获记录返回匹配的交易日期
def get_capture_record_date(row_list):
    date_list = []
    for row in row_list:
        date_list.append(row['date'])
    return date_list