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
    return create_engine('mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, database))
	
# query full stock list from DB
def query_stock_list():
    engine = get_connection()
    sql = "select * from stock_code;"
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
    sql = "select * from stock_kline_daily where code='{}' and date>='{}' and date<='{}';".format(code, start_date, end_date)
    df = pd.read_sql_query(sql, engine)
    return df

# query stock daily K line data by industry
def query_stock_kline_by_industry(industry, end_date, start_date='2000-01-01'):
    engine = get_connection()
    sql = "select skd.date, skd.code, sc.code_name, skd.open, skd.close, skd.volume, skd.amount, skd.pctChg, skd.pbMRQ, skd.peTTM from stock_kline_daily skd, stock_code sc where skd.code=sc.code and sc.industry='{}' and date>='{}' and date<='{}';".format(industry, start_date, end_date)
    df = pd.read_sql_query(sql, engine)
    return df