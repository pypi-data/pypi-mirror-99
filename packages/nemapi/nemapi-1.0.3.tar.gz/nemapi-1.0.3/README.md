# nemapi
Access to public National Electricity Market data through nemAPI.

## Description & Usage
Currently users can access the following tables within the AEMO MMS Data Model <https://aemo.com.au/energy-systems/electricity/national-electricity-market-nem/data-nem/market-data-nemweb>. 

NEM Dispatch Interval Data:
    1. dispatch_price,
    2. dispatch_regionsum,
    3. dispatch_interconnectorres

NEM Trading Interval Data:
    1. trading_price,
    2. trading_regionsum,
    3. trading_interconnectorres

There are two main methods for returning data. Firstly a get_['table'] method which will return the most current data back a trailing number of dispatch/trading intervals the user defines. The second is a get_['table']_historical where the user can define a start_date and end_date in addition to selecting over either regionid (price and regionsum tables) or connectorid (interconnectorres tables).

**Note: Each data request is limited to 10,000 rows. 

## Examples
```python
from nemapi import *

nemapi = nemapi()
df = nemapi.get_dispatch_price(intervals=1)
print('dispatch prices: \n', df)

df1 = nemapi.get_dispatch_regionsum_historical(start_date='2021-01-01 00:30:00', end_date='2021-01-01 12:00:00', regionid='ALL')
print('dispatch prices: \n', df1)

df2 = nemapi.get_trading_interconnectorres_historical(start_date='2021-01-01 00:00:00', end_date='2021-01-02 00:00:00', connectorid='NSW1-QLD1')
print('trading NSW1-QLD1 interconnector historical : \n', df2)
```

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install nemapi.

```bash
pip install nemapi
pip install nemapi --upgrade
```

## Requirements
Python modules required: 'datetime', 'requests', 'pandas'.

## Compatibility
Python3

## Licence
The [MIT](https://choosealicense.com/licenses/mit/) License (MIT)

Authors
-------

`nemmarketapi` was written by `Jonathon Emerick <jonathon.emerick@uq.net.au>`_.
