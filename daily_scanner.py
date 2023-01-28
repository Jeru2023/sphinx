import time
import mydb
import rule_model as rm
import strategy_evaluation as se

date = '2023-01-20'
entry_rule_dict = {'volume_mean_window_len':15, 'multiple':1.5, 'amount_min':3000000, 
                   'pctChg_min':0,'pctChg_max':7,'pe_max':30, 'pe_min':0, 'pb_max':1}
				   
stock_list_df = mydb.query_selected_stock_list(date)

start_time = time.time()

capture_list = []
# 需提升效率，分两步来判断，先判断当日数据，再结合历史数据
for index, row in stock_list_df.iterrows():
    code = row['code']
    print('processing ', index)
    volume_mean_window_len = entry_rule_dict.get('volume_mean_window_len')
    stock_df = mydb.query_kline_by_entry_window_len(code, volume_mean_window_len, date).sort_values(by='date')
    if (se.validate_current_record(stock_df, entry_rule_dict, date)):
        capture_list.append(stock_df.tail(1))

end_time = time.time()
print('execute time: ', end_time-start_time)

print(capture_list)