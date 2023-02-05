from Comtrade import Comtrade
from Writer import Writer
from datetime import datetime as dt, timezone
import re
import time

MAX_RESULT = 10000

reqHandler = Comtrade()
writer = Writer()

# params for data availability
availParams = {
    'type': 'C',
    "freq": "M", 
    "px": "HS", 
}

# params for data request
dataParams = {
    "fmt": "csv",
    "head": "M",
    "r": "842",
    "freq": "M",
    "ps": "2012",
    "px": "HS"
}
dataParams['type'] = availParams['type']

# reset progress
# writer.resetProgress()

# read progress
periods = writer.readYearsAndMonths('Progress.txt')

while len(periods) > 0:
    p = periods[0]
    availParams["ps"] = p
    print("params:", availParams)
    area_availability = reqHandler.get_reporting_totalRecords(availParams)
    area_availability = filter(lambda area: area['TotalRecords'] is not None and area['TotalRecords'] <= MAX_RESULT, area_availability)
    for a in area_availability:
        print("area:", a['rDesc'])
        print('Total Records:', a['TotalRecords'])
        print(type(a))
        total_records = a['TotalRecords']
        # assign parameters
        dataParams['ps'] = availParams['ps']
        dataParams['r'] = a['r']
        dataParams['p'] = 'all'
        for rg in [1, 2]:
            dataParams['rg'] = rg
            response = reqHandler.getDataResponse(dataParams)
            writer.writeToCSV(response, p[:4], p[4:], a['rDesc'], "all"
                , top_level=writer.DATA_DIR_UNDER_10000, trade_type = dataParams['type'], rg = dataParams['rg'])
    del periods[0]
    writer.writeYearsAndMonths('Progress.txt', periods)