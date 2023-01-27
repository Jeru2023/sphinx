# volume_mean_window_len 为对比滚动移动平均线的时间窗口长度，如10则对比过去10日的平均成交量
# volume_multiple 为当日成交量对比过去mean_window_len范围内平均成交量的倍数
# exit_window_len 为卖出的时间窗口长度，如-15则在15日后卖出

entry_rule_dict = {'volume_mean_window_len':15, 'multiple':1.5, 'amount_min':3000000, 
                   'pctChg_min':0,'pctChg_max':3,'pe_max':30, 'pe_min':0, 'pb_max':1}

exit_rule_dict = {'exit_window_len':-60}

def evaluate_entry(row, entry_rule_dict=entry_rule_dict, exit_rule_dict=exit_rule_dict):
    valid = row['volume']>(row['volume_rolling_mean'] * entry_rule_dict.get('multiple'))
    valid = valid and (row['pctChg'] > entry_rule_dict.get('pctChg_min')) and (row['pctChg'] < entry_rule_dict.get('pctChg_max'))
    valid = valid and (row['peTTM'] < entry_rule_dict.get('pe_max'))and (row['peTTM'] > entry_rule_dict.get('pe_min'))
    valid = valid and (row['pbMRQ'] < entry_rule_dict.get('pb_max'))
    valid = valid and (row['amount'] > entry_rule_dict.get('amount_min'))
    return valid