import configparser as cp

# volume_mean_window_len 为对比滚动移动平均线的时间窗口长度，如10则对比过去10日的平均成交量
# volume_multiple 为当日成交量对比过去mean_window_len范围内平均成交量的倍数
# exit_window_len 为卖出的时间窗口长度，如-15则在15日后卖出

# generic entry rule
basic_entry_rule_dict = {'volume_mean_window_len':15, 'volume_multiple':2, 'close_multiple':1.2, 'amount_min':3000000, 
                   'pctChg_min':0, 'pctChg_max':3, 'fetch_days':60}

# industry specified entry rule
industry_entry_rule_dict = {'pe_max':50, 'pe_min':0, 'pb_max':3}

exit_rule_dict = {'exit_window_len':-60}

def valid_entry(row, basic_entry_rule_dict=basic_entry_rule_dict, industry_entry_rule_dict=industry_entry_rule_dict):
    valid = row['volume']>(row['volume_ma_20'] * float(basic_entry_rule_dict.get('volume_multiple')))
    valid = valid and (row['pctChg'] > basic_entry_rule_dict.get('pctChg_min')) and (row['pctChg'] < basic_entry_rule_dict.get('pctChg_max'))
    valid = valid and (row['close'] > row['open'])
    valid = valid and (row['amount'] > basic_entry_rule_dict.get('amount_min'))
    valid = valid and (row['peTTM'] < (float(industry_entry_rule_dict.get('pe_max'))*0.8)) and (row['peTTM'] > float(industry_entry_rule_dict.get('pe_min')))
    valid = valid and (row['pbMRQ'] < float(industry_entry_rule_dict.get('pb_max')))
    valid = valid and (row['close_ma_5'] > row['close_ma_10'])
    valid = valid and (row['volume_ma_5'] > row['volume_ma_10'])
    #print(row['close'],row['close_ma_60'])
    valid = valid and (row['close'] < row['close_ma_60'] * basic_entry_rule_dict.get('close_multiple'))
    #valid = valid and (row['close'] < row['close_ma_10'] * basic_entry_rule_dict.get('close_multiple'))
    # 换手率超过2%
    #valid = valid and (row['turn']>2)
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