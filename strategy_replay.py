import mydb
import rule_model as rm
import strategy_evaluation as se

# rule_model会使用20日均线作为基准
basic_entry_rule_dict = {'volume_multiple':1.8, 'close_multiple':1.1, 'market_cap_min':5000000000, 'turn_min':1, 'pctChg_min':0, 'pctChg_max':3, 'fetch_days':60}
exit_rule_dict = {'one_day_loss':2.5, 'exit_window_len':-240}

###################################################

def evaluate_stock(code, industry):

    # 查询时间范围中开始时间默认为2000-01-01, 可以加入参数重写: start_date='yyyy-mm-dd'
    stock_df = mydb.query_stock_kline_by_code(code, end_date='2023-01-31')

    industry_entry_rule_dict = rm.get_industry_entry_rule_dict(industry)
    print('总记录数: ', len(stock_df))
    
    # 返回策略模型匹配到的所有数据
    row_list = se.get_capture_record(stock_df, basic_entry_rule_dict, industry_entry_rule_dict, exit_rule_dict)
    print('捕获记录数: ', len(row_list))
    total_profit, size = se.evaluate_stock_profit(row_list)

    print('总共找到匹配次数: {}\n'.format(size))
    print('整体收益率:  {}\n'.format(total_profit/size))
    # 打印策略模型匹配到的日期
    print('所有匹配日期: ', se.get_capture_record_date(row_list))


def evaluate_industry(industry):
    print('start...')
    # 查询时间范围中开始时间默认为2000-01-01, 可以加入参数重写: start_date='yyyy-mm-dd'
    stock_list_df = mydb.query_stock_kline_by_industry(industry, end_date='2023-02-03')
    industry_entry_rule_dict = rm.get_industry_entry_rule_dict(industry)
    total_profit_ratio, total_size = se.evaluate_industry_profit(stock_list_df, basic_entry_rule_dict, industry_entry_rule_dict, exit_rule_dict)
    print('profit ratio mean', float(total_profit_ratio/total_size))

###################################################
# Usage 1: 个股分析
# 兴业银行
code = 'sz.002382'
industry = '医药生物'
#evaluate_stock(code, industry)

# Usage 2: 行业分析
industry = '医药生物'
evaluate_industry(industry)