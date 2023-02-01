import baostock as bs
import pandas as pd

def merge_result(rs):
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    return pd.DataFrame(data_list, columns=rs.fields)
	
def get_stock_basic(code):
    lg = bs.login()
    rs = bs.query_stock_basic(code=code)
    return merge_result(rs)
	
def get_stock_industry(code):
    lg = bs.login()
    rs = bs.query_stock_industry(code)
    return merge_result(rs)
	
def query_stock_kline_daily(code, start_date, end_date):
    lg = bs.login()
    query = "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM"
    rs = bs.query_history_k_data_plus(code, query, start_date=start_date, end_date=end_date, frequency="d", adjustflag="3")
    return merge_result(rs)
    
def query_trade_dates(start_date, end_date):
    lg = bs.login()
    rs = bs.query_trade_dates(start_date=start_date, end_date=end_date)
    return merge_result(rs)