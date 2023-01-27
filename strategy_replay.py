import baostock as bs
import pandas as pd
import mydb
import rule_model as rm
import strategy_evaluation as se

entry_rule_dict = {'volume_mean_window_len':15, 'multiple':1.5, 'amount_min':3000000, 
                   'pctChg_min':0,'pctChg_max':3,'pe_max':30, 'pe_min':0, 'pb_max':1}
exit_rule_dict = {'exit_window_len':-60}

###################################################

# Usage 1: 个股分析

# 兴业银行
code = 'sh.601166'
stock_df = mydb.query_stock_kline_by_code(code)

# 返回策略模型匹配到的所有数据
row_list = se.get_capture_record(stock_df, entry_rule_dict, exit_rule_dict)
total_profit, size = se.evaluate_stock_profit(row_list)

print('总共找到匹配次数: {}\n'.format(size))
print('整体收益率:  {}\n'.format(total_profit/size))
# 打印策略模型匹配到的日期
print('所有匹配日期: ', se.get_capture_record_date(row_list))

###################################################

# Usage 2: 行业分析
industry = '银行'
stock_list_df = mydb.query_stock_kline_by_industry(industry)

total_profit_ratio, total_size = se.evaluate_industry_profit(stock_list_df, entry_rule_dict, exit_rule_dict)
print('profit ratio mean', float(total_profit_ratio/total_size))
