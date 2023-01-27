# Sphinx
A Data Driven Trading Strategy application

## File description

sphinx.config - DB configuration 

rule_model.py - entry and exit rule validation for the strategy

mydb.py - database query function on single stock and industry

strategy_evaluation.py - replay evaluation functions

-------------------------------------------------------

strategy_replay.py - this is your only concern, make finetune here to find the best parameters combination

## Strategy Validation
只需要用到strategy_replay.py一个文件即可, 首先设定策略参数，不同行业/个股的主要差异是经营指标，比如银行看PB, 医药看PE
### 策略参数
#对比过去15日成交量均值判断是否放量1.5倍, 当日成交金额大于300万, 涨幅为正且低于3个点，pe在0-30之间，pb<1

entry_rule_dict = {'volume_mean_window_len':15, 'multiple':1.5, 'amount_min':3000000, 
                   'pctChg_min':0,'pctChg_max':3,'pe_max':30, 'pe_min':0, 'pb_max':1}
#持仓60日后卖出
exit_rule_dict = {'exit_window_len':-60}

然后有两种验证方式

### 行业验证
指定一个申万一级行业的名字, 获取全部日线数据, 按照设定规则过滤, 计算收益率

#Usage 2: 行业分析 - 计算整个行业的策略平均收益率
industry = '银行'
stock_list_df = mydb.query_stock_kline_by_industry(industry)

total_profit_ratio, total_size = se.evaluate_industry_profit(stock_list_df, entry_rule_dict, exit_rule_dict)
print('profit ratio mean', float(total_profit_ratio/total_size))

### 个股验证
#兴业银行
code = 'sh.601166'
stock_df = mydb.query_stock_kline_by_code(code)

# 返回策略模型匹配到的所有数据
row_list = se.get_capture_record(stock_df, entry_rule_dict, exit_rule_dict)
total_profit, size = se.evaluate_stock_profit(row_list)

print('总共找到匹配次数: {}\n'.format(size))
print('整体收益率:  {}\n'.format(total_profit/size))
# 打印策略模型匹配到的日期
print('所有匹配日期: ', se.get_capture_record_date(row_list))

## Tables
### Stock Code
| Column        | Description |
| ------------- | ------------- |
| code          | Stock code  |
| code_name     | Stock name  |
| industry      | Stock industry |
| industryClassification | A股对应申万一级行业 |
| ipoDate       | IPO listing date |
| outDate       | Delisting date |
| type          | 1:stock; 2:index; 3:others; 4:convertable debt; 5:ETF |
| isST          | 1:ST; 0:normmal |
| tradeStatus   | 1:trade; 0:halt |
| status        | 1:listing; 0:delisting |


### Stock Kline Daily
| Column        | Description | Formular|
| ------------- | ------------- | ------------- |
| code          | Stock code  | |
| date          | Trading date | |
| open          | Open price | |
| high          | Highest price | |
| low           | Lowest price | |
| close         | Close price | |
| preclose      | 前收盘价 | 证券在指定交易日行情数据的前收盘价，当日发生除权除息时，“前收盘价”不是前一天的实际收盘价，而是根据股权登记日收盘价与分红现金的数量、配送股的数里和配股价的高低等结合起来算出来的价格。|
| volume         | Trading volume | |
| amount         | Trading amount | |
| adjustFlag     | 复权状态(1:后复权; 2:前复权; 3:不复权） | 复权是对股价和成交量进行权息修复，按照股票的实际涨跌绘制股价走势图，并把成交量调整为相同的股本口径。 |
| turn            | 换手率 | [指定交易日的成交量(股)/指定交易日的股票的流通股总股数(股)] * 100% |
| pctChg        | 涨跌幅 | 日涨跌幅=[(指定交易日的收盘价-指定交易日前收盘价)/指定交易日前收盘价] * 100%|
| peTTM         | 滚动市盈率 | (指定交易日的股票收盘价/指定交易日的每股盈余TTM)=(指定交易日的股票收盘价 * 截至当日公司总股本)/归属母公司股东净利润TTM |
| pbMRQ | 市净率 | (指定交易日的股票收盘价/指定交易日的每股净资产)=总市值/(最近披露的归属母公司股东的权益-其他权益工具) |
| psTTM | 滚动市销率 | (指定交易日的股票收盘价/指定交易日的每股销售额)=(指定交易日的股票收盘价 * 截至当日公司总股本)/营业总收入TTM |
| pcNcfTTM      | 滚动市现率 | (指定交易日的股票收盘价/指定交易日的每股现金流TTM)=(指定交易日的股票收盘价 * 截至当日公司总股本)/现金以及现金等价物净增加额TTM |

