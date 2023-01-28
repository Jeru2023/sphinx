import pandas as pd
from sqlalchemy import create_engine
import configparser as cp

#####################################
# Database access module for stock code table and stock daily K line table
# usage:
# import mydb
# mydb.function_name(params)
#####################################

config = cp.ConfigParser()
config.read('sphinx.config', encoding='utf-8-sig')

# database connection
def get_connection():
    user = config.get('DB', 'user')
    password = config.get('DB', 'password')
    host = config.get('DB', 'host')    
    port = config.get('DB', 'port')
    database = config.get('DB', 'database')
    return create_engine('mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, database), pool_size=20, max_overflow=50, pool_recycle=30)

engine = get_connection()

# query full stock list from DB
def query_stock_list():
    sql = "select * from stock_code;"
    df = pd.read_sql_query(sql, engine)
    return df

# 获取需扫描的股票清单, 去除ST, 仅获取正常交易股票类型
def query_selected_stock_list(date):
    engine = get_connection()
    sql = "select distinct sc.code from stock_code sc, stock_kline_daily skd where sc.isST=0 and sc.type=1 and sc.tradeStatus=1 and sc.status=1 and sc.code=skd.code and skd.pctChg>0 and skd.amount>1000000 and skd.peTTM>0 and skd.date='{}'".format(date)
    df = pd.read_sql_query(sql, engine)
    return df
	
# query stock list by industry
# industry: 申万一级行业名称
def query_stock_list_by_industry(industry):
    engine = get_connection()
    sql = "select * from stock_code where industry='{}';".format(industry)
    df = pd.read_sql_query(sql, engine)
    return df

# query stock daily K line data by code
def query_stock_kline_by_code(code, end_date, start_date='2000-01-01'):
    engine = get_connection()
    sql = "select * from stock_kline_daily where code='{}' and date>'{}' and date<='{}';".format(code, start_date, end_date)
    df = pd.read_sql_query(sql, engine)
    return df

# query stock daily K line data by industry
def query_stock_kline_by_industry(industry, end_date, start_date='2000-01-01'):
    engine = get_connection()
    sql = "select skd.date, skd.code, sc.code_name, skd.open, skd.close, skd.volume, skd.amount, skd.pctChg, skd.pbMRQ, skd.peTTM from stock_kline_daily skd, stock_code sc where skd.code=sc.code and sc.industry='{}' and date>'{}' and date<='{}';".format(industry, start_date, end_date)
    df = pd.read_sql_query(sql, engine)
    return df

# return the latest record per code
def query_kline_latest_line(code):
    engine = get_connection()
    sql = "select * from stock_kline_daily where code='{}' order by date desc limit 0,1;".format(code)
    df = pd.read_sql_query(sql, engine)
    return df

# query latest volume_mean_window_len+1 records per code
def query_kline_by_entry_window_len(code, volume_mean_window_len, end_date):
    sql = "select * from stock_kline_daily where code='{}' and date<='{}' order by date desc limit 0,{};".format(code, end_date, volume_mean_window_len+1)
    df = pd.read_sql_query(sql, engine)
    return df
    

    