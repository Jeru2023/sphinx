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
| Column        | Description |
| ------------- | ------------- |
| code          | Stock code  |
| date          | Trading date |
| open          | Open price |
| high          | Highest price |
| low           | Lowest price |
| close         | Close price |
| volume         | Trading volume |
| amount         | Trading amount |
