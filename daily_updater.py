# -*- coding: utf-8 -*-

import datetime
import time

import stock_api as sa
import mydb

# TODO: 执行时间太久，估计两三个小时才跑完，如何优化? 5000多次请求，一次一秒, 完整执行时间统计为6623秒
# 思路1: 先把所有记录添加到dataframe, 一次性写入，但好像提高并不多，主要瓶颈是baostock接口仅支持单个股票数据查询
# 思路2: 多进程?

# 检查是否交易日
def is_trading_day(date):
    start_date = date
    end_date = date
    
    df = sa.query_trade_dates(start_date, end_date)
    is_trading_day = df.iloc[0]['is_trading_day']
    
    if (is_trading_day=='1'):
        return True
    else: 
        return False


# 增量更新单只股票记录至end_date    
def update_stock(code, end_date):
    
    # 按日期降序后获取最新一条记录
    latest_df = mydb.query_kline_latest_line(code)  
    
    # 如果股票记录为空，跳过
    if len(latest_df['date'])==0:
        return
    
    latest_date = str(latest_df['date'].values[0])

    # 如果数据库最新日期等于传入日期，跳过
    if latest_date==str(end_date):
        return
    
    # 向后推移一天
    start_date = (latest_df['date'].values[0]+datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    

    stock_df = sa.query_stock_kline_daily(code, start_date, str(end_date))
    mydb.write_df_to_table(stock_df, 'stock_kline_daily')


# TODO: 偶尔会中断，需要人工resume
# 更新全部股票数据
def update_all(date):
    code_list_df = mydb.query_stock_list()
    print("len ", len(code_list_df))
    
    i = 0
    for index, row in code_list_df.iterrows():
        i += 1
        #if (i<5395):
        #    continue
        code = row['code']
        print('{} updating code: {}'.format(i, code))
        update_stock(code, today)
        
  
start_time = time.time()

# TODO: 如果不是当天运行，而是非交易日补之前的记录，这里逻辑需更新
#today = datetime.date.today()
today = datetime.date(2023, 2, 3)
if is_trading_day(today):
    update_all(today)
    
end_time = time.time()
print('execute time: ', end_time-start_time)