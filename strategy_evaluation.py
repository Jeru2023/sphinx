import rule_model as rm
import math

# 捕获单只股票满足策略模型的记录
def get_capture_record(stock_df, entry_rule_dict, exit_rule_dict):
    volume_mean_window_len = rm.entry_rule_dict.get('volume_mean_window_len')
    exit_window_len = rm.exit_rule_dict.get('exit_window_len')
    
    stock_df['volume_rolling_mean'] = stock_df['volume'].rolling(volume_mean_window_len).mean()
    stock_df['profit'] = stock_df['close'].shift(exit_window_len)-stock_df['close']
    
    row_list = []
    for index, row in stock_df.iterrows():
        if (index < volume_mean_window_len):
            continue

        if (rm.valid_entry(row, entry_rule_dict)):
            row_list.append(row)
    return row_list
    
# 检测当前日期记录是否满足入场条件
def validate_current_record(stock_df, entry_rule_dict, date):
    volume_mean_window_len = rm.entry_rule_dict.get('volume_mean_window_len')
    exit_window_len = rm.exit_rule_dict.get('exit_window_len')
    
    stock_df['volume_rolling_mean'] = stock_df['volume'].rolling(volume_mean_window_len).mean()
    format_code = '%Y-%m-%d'
    
    is_valid = False
    for index, row in stock_df.iterrows():
        if (row['date'].strftime(format_code)==date and rm.valid_entry(row, entry_rule_dict)):
            is_valid = True
    return is_valid

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
def evaluate_industry_profit(stock_list_df, entry_rule_dict, exit_rule_dict):
    code_list = stock_list_df['code'].unique()
    
    total_profit_ratio = 0.0
    total_size = 0
    
    for code in code_list:
        stock_df = stock_list_df[stock_list_df['code']==code]
        print(stock_df['code_name'].unique(), code)
    
        row_list = get_capture_record(stock_df, entry_rule_dict, exit_rule_dict)
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