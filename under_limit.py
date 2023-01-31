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
    "type": "C", 
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

# years = [str(year) for year in range(int(start_year), 2023)]
# months = ["{:02d}".format(month) for month in range(int(start_month), 13)]
# periods = []
# for y in years:
#     for m in months:
#         periods.append(y+m)
# writer.writeYearsAndMonths('Progress.txt', periods)

periods = writer.readYearsAndMonths('Progress.txt')


# past 10 years
# currentYear = dt.today().year
# periods = [currentYear - i - 1 for i in range(11)]
# periods.sort()
# periodStr = (str(p) for p in periods)

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
        # check if total records is over limit
        if total_records <= MAX_RESULT:
            dataParams['ps'] = availParams['ps']
            dataParams['r'] = a['r']
            dataParams['p'] = 'all'
            response = reqHandler.getResponse(dataParams)
            writer.writeToCSV(response, p[:4], p[4:], a['rDesc'], "all", True)
    del periods[0]
    writer.writeYearsAndMonths('Progress.txt', periods)