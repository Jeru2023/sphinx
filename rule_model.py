import configparser as cp

# volume_mean_window_len 为对比滚动移动平均线的时间窗口长度，如10则对比过去10日的平均成交量
# volume_multiple 为当日成交量对比过去mean_window_len范围内平均成交量的倍数
# exit_window_len 为卖出的时间窗口长度，如-15则在15日后卖出

# generic entry rule
basic_entry_rule_dict = {'volume_mean_window_len':15, 'volume_multiple':2, 'close_multiple':1.2, 'market_cap_min':5000000000, 'turn_min':1.5, 
                   'pctChg_min':0, 'pctChg_max':3, 'fetch_days':60}

# industry specified entry rule
industry_entry_rule_dict = {'pe_max':50, 'pe_min':0, 'pb_max':3}

exit_rule_dict = {'exit_window_len':-60}

# pe和pb的设定来源于行业标杆配置
def valid_entry(row, basic_entry_rule_dict=basic_entry_rule_dict, industry_entry_rule_dict=industry_entry_rule_dict):
    # 通用设定
    turn_min = basic_entry_rule_dict.get('turn_min') # 最小换手率, 建议至少大于1
    pctChg_min = basic_entry_rule_dict.get('pctChg_min') # 最低涨幅，建议大于0
    pctChg_max = basic_entry_rule_dict.get('pctChg_max') # 最高涨幅，建议小于3
    market_cap_min = float(basic_entry_rule_dict.get('market_cap_min')) # 最小市值, 建议大于50亿
    
    # 行业设定
    pe_max = float(industry_entry_rule_dict.get('pe_max')) # 最高市盈率
    pe_min = float(industry_entry_rule_dict.get('pe_min')) # 最低市盈率, 大于0
    pb_max = float(industry_entry_rule_dict.get('pb_max')) # 最高市净率
    
    market_cap = row['amount']/row['turn']
    
    valid = row['volume']>(row['volume_ma_20'] * float(basic_entry_rule_dict.get('volume_multiple')))
    valid = valid and (row['pctChg'] > pctChg_min) and (row['pctChg'] < pctChg_max)
    valid = valid and (row['close'] > row['open'])
    valid = valid and (market_cap > market_cap_min)
    valid = valid and (row['peTTM'] < pe_max*0.8) and (row['peTTM'] > pe_min)
    valid = valid and (row['pbMRQ'] < pb_max)
    # 收盘价5日均线上穿10日均线
    valid = valid and (row['close_ma_5'] > row['close_ma_10'])
    # 成交量5日均线上穿10日均线
    valid = valid and (row['volume_ma_5'] > row['volume_ma_10'])
    # 当前股价不高于过去60天均值的close_multiple倍
    valid = valid and (row['close'] < row['close_ma_60'] * basic_entry_rule_dict.get('close_multiple'))
    #valid = valid and (row['close'] < row['close_ma_10'] * basic_entry_rule_dict.get('close_multiple'))
    # 最低换手率
    valid = valid and (row['turn'] > turn_min)
    return valid

# 获取每个行业的PE/PB基准
def get_industry_entry_rule_dict(industry):
    config = cp.ConfigParser()
    config.read('sphinx.config', encoding='utf-8-sig')
    industry_entry_rule_dict = {}
    industry_entry_rule_dict['pe_min'] = 0
    industry_entry_rule_dict['pe_max'] = config.get(industry, 'pe_max')
    industry_entry_rule_dict['pb_max'] = config.get(industry, 'pb_max')
    return industry_entry_rule_dict