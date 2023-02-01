import time
import mydb
import rule_model as rm
import strategy_evaluation as se
import robot


def capture_industry(stock_list_df, industry, basic_entry_rule_dict, industry_entry_rule_dict):
    industry_df = stock_list_df.loc[stock_list_df['industry']==industry]
    
    
    capture_list = []
    for index, row in industry_df.iterrows():
        code = row['code']
        #print('processing {}[{}] with index {}'.format(industry, code, index))
        fetch_days = basic_entry_rule_dict.get('fetch_days')
        
        stock_df = mydb.query_kline_by_entry_window_len(code, fetch_days, date).sort_values(by='date')
        #print(industry, len(stock_df))
        if (se.validate_current_record(stock_df, basic_entry_rule_dict, industry_entry_rule_dict, date)):
            capture_list.append(stock_df.tail(1))
    return capture_list

def gen_content(industry, capture_list):
    content = ['\n###{}, 当日捕获{}个标的。\n'.format(industry, len(capture_list))]
    
    if len(capture_list)==0:
        return ''
    
    print(content)
    
    for stock_df in capture_list:
        code_name = stock_df['code_name'].values[0]
        industry = stock_df['industry'].values[0]
        pctChg = round(stock_df['pctChg'].values[0],2)
        pe = round(stock_df['peTTM'].values[0],2)
        pb = round(stock_df['pbMRQ'].values[0],2)
        volume_multiple = round(stock_df['volume'].values[0]/stock_df['volume_rolling_mean'].values[0],2)
    
        content.append ('{}[{}], 涨幅: {}%, PE: {}, PB: {}, 成交放量倍数: {}'.format(code_name, industry, pctChg, pe, pb, volume_multiple))
    
    return '\n'.join(content)
        
def scan_all(stock_list_df, industry_list_df, basic_entry_rule_dict):  
    content = ''
    total_num = 0
    for index, row in industry_list_df.iterrows():
        industry = row['industry']
        if (industry is None or industry==''):
            continue
        industry_entry_rule_dict = rm.get_industry_entry_rule_dict(industry)
        capture_list = capture_industry(stock_list_df, industry, basic_entry_rule_dict, industry_entry_rule_dict)
        
        industry_content = gen_content(industry, capture_list)
        content += industry_content 
        total_num += len(capture_list)
        
    content += '\n当日总共捕获{}个标的'.format(total_num)
    return content


date = '2023-01-31'
# rule_model会使用20日均线，所以volume_mean_window_len最好大于20
basic_entry_rule_dict = {'volume_mean_window_len':20, 'volume_multiple':1.8, 'close_multiple':1.2,  'amount_min':3000000, 'pctChg_min':0,'pctChg_max':3,'fetch_days':60}

stock_list_df = mydb.query_selected_stock_list(date)
print('len of stock list ', len(stock_list_df))
industry_list_df = mydb.query_industry_list()

content = '# 扫描日期: {}\n\n'.format(date)
content += scan_all(stock_list_df, industry_list_df, basic_entry_rule_dict)
print(content)
#robot.send_markdown(content)



# 需提升效率，分两步来判断，先判断当日数据，再结合历史数据
