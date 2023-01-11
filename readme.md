# Comtrade Data Collection Script

# Setup

**Activate Python Virtual Environment**
In the root directory, run the following command to activate virtual environment.
```
source env/bin/activate
```

**Install required dependencies**
```
pip install -r requirements.txt
```

# Project Structure

```
.
├── Comtrade.py
├── Writer.py
├── areas.txt
├── env
├── partner_areas.txt
├── reporting_areas.txt
├── requirements.txt
├── script.py
├── test.py
└── trade_data
```

- Comtrade.py: Class for making requests to API. See https://comtrade.un.org/data/doc/api, for more details
- Writer.py: Class for writing and reading text, csv files
- script.py: Main entry point. 
- reporting_areas.txt: file for saving progress of data collection. 
- trade_data: Trade Data. Divided into years and months, reporting areas, with suffix, _r and partner areas, with suffix, _p. Trade data is saved in csv format, with the file name indicating the month. e.g. 01.csv indicates the trade data corresponding to the current directory, in which it is in, for the month of January. 

# Sample Response - Data Availability
```
{
        "type": "COMMODITIES",
        "freq": "MONTHLY",
        "px": "HS",
        "r": "76",
        "rDesc": "Brazil",
        "ps": "201607",
        "TotalRecords": 126827,
        "IsOriginal": 1,
        "IsPartnerDetail": 1,
        "UploadTime": "2016-08-05T00:00:00"
},
```

# Sample Response - Data Request
```
{
   "validation":{
      "status":{
         "name":"Ok",
         "value":0,
         "category":0,
         "description":"",
         "helpUrl":""
      },
      "message":null,
      "count":{
         "value":17559,
         "started":"2015-05-11T11:29:41.6096178-04:00",
         "finished":"2015-05-11T11:29:57.4572024-04:00",
         "durationSeconds":15.8475846
      },
      "datasetTimer":{
         "started":"2015-05-11T11:29:41.6096178-04:00",
         "finished":"2015-05-11T11:30:39.6044167-04:00",
         "durationSeconds":57.9947989
      }
   },
   "dataset":[
      {
         "pfCode":"HS",
         "yr":2013,
         "period":2013,
         "periodDesc":"2013",
         "aggrLevel":2,
         "IsLeaf":0,
         "rgCode":1,
         "rgDesc":"Import",
         "rtCode":826,
         "rtTitle":"United Kingdom",
         "rt3ISO":"GBR",
         "ptCode":0,
         "ptTitle":"World",
         "pt3ISO":"WLD",
         "ptCode2":null,
         "ptTitle2":"",
         "pt3ISO2":"",
         "cstCode":"",
         "cstDesc":"",
         "motCode":"",
         "motDesc":"",
         "cmdCode":"01",
         "cmdDescE":"Live animals",
         "qtCode":1,
         "qtDesc":"No Quantity",
         "qtAltCode":null,
         "qtAltDesc":"",
         "TradeQuantity":null,
         "AltQuantity":null,
         "NetWeight":null,
         "GrossWeight":null,
         "TradeValue":638496202,
         "CIFValue":null,
         "FOBValue":null,
         "estCode":0
      },
      {
         "pfCode":"HS",
         "yr":2013,
         "period":2013,
         "periodDesc":"2013",
         "aggrLevel":2,
         "IsLeaf":0,
         "rgCode":2,
         "rgDesc":"Export",
         "rtCode":826,
         "rtTitle":"United Kingdom",
         "rt3ISO":"GBR",
         "ptCode":0,
         "ptTitle":"World",
         "pt3ISO":"WLD",
         "ptCode2":null,
         "ptTitle2":"",
         "pt3ISO2":"",
         "cstCode":"",
         "cstDesc":"",
         "motCode":"",
         "motDesc":"",
         "cmdCode":"01",
         "cmdDescE":"Live animals",
         "qtCode":1,
         "qtDesc":"No Quantity",
         "qtAltCode":null,
         "qtAltDesc":"",
         "TradeQuantity":null,
         "AltQuantity":null,
         "NetWeight":null,
         "GrossWeight":null,
         "TradeValue":618257677,
         "CIFValue":null,
         "FOBValue":null,
         "estCode":0
      },
      ...
   ]
}
```

# Usage Limit
Public users are subject to the following restrictions: 
* Rate limit (guest): 1 request every second (per IP address or authenticated user). Rate limit (authenticated): 1 request every second (per IP address or authenticated user).

* Usage limit (guest): 100 requests per hour (per IP address or authenticated user).

* Usage limit (authenticated): 10,000 requests per hour (per IP address or authenticated user).

* Parameter combination limit: ps, r and p are limited to 5 codes each. Only one of the above codes may use the special ALL value in a given API call. Classification codes (cc) are limited to 20 items. ALL is always a valid classification code.

On successful request, a 200 status code is returned.

An error code of 409 will be returned, if any of the following conditions are violated, along with a message describing which of these violations were caught. 