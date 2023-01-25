# Sphinx
A Data Driven Trading Strategy application


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
| volume         | Trading volume | |
| amount         | Trading amount | |
| adjustFlag     | 复权状态(1:后复权; 2:前复权; 3:不复权） | |
| turn            | 换手率 | |
| pctChg        | 涨跌幅 | |
| peTTM         | 滚动市盈率 | (指定交易日的股票收盘价/指定交易日的每股盈余TTM)=(指定交易日的股票收盘价 * 截至当日公司总股本)/归属母公司股东净利润TTM |
| pbMRQ | 市净率 | (指定交易日的股票收盘价/指定交易日的每股净资产)=总市值/(最近披露的归属母公司股东的权益-其他权益工具) |
| psTTM | 滚动市销率 | (指定交易日的股票收盘价/指定交易日的每股销售额)=(指定交易日的股票收盘价 * 截至当日公司总股本)/营业总收入TTM |
| pcNcfTTM      | 滚动市现率 | (指定交易日的股票收盘价/指定交易日的每股现金流TTM)=(指定交易日的股票收盘价 * 截至当日公司总股本)/现金以及现金等价物净增加额TTM |

