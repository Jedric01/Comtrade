from Comtrade import Comtrade
from Writer import Writer
from datetime import datetime as dt, timezone
import re
import time

MAX_RESULT = 10000

reqHandler = Comtrade()
writer = Writer()

availParams = {
    "type": "C", 
    "freq": "M", 
    "px": "HS", 
}

dataParams = {
    "fmt": "csv",
    "head": "M",
    "r": "842",
    "freq": "M",
    "ps": "2012",
    "px": "HS"
}
dataParams['type'] = availParams['type']
m = 3
periods = writer.readYearsAndMonths('Progress.txt')

while len(periods) > 0:
    p = periods[0]
    availParams["ps"] = p
    
    for r in reporting_desc:
        writer.write_areas('ProgressPartner1.txt', area_availability[1,])
        writer.write_areas('ProgressPartner2.txt', area_availability[1,])
        for rg in [1, 2]:
            dataParams['rg'] = rg
            partner_areas= writer.read_areas(f'ProgressPartner{rg}.txt')
            partner_code, partner_desc = partner_areas.keys(), list(partner_areas.items())
            for i in range(len(partner_areas), m):
                # get m partners from the partner_areas dictionary
                dataParams['p'] = ','.join(partner_code[i, i+m])
                dataParams['ps'] = p
                dataParams['r'] = r
                response = reqHandler.getResponse(dataParams)
                writer.writeToCSV(response, p[:4], p[4:], r, '-'.join(partner_desc[i, i+m])
                    , top_level=writer.DATA_DIR_ABOVE_10000, trade_type = dataParams['type'], rg = dataParams['rg'])
                # update partner progress
                del partner_areas[i, i+m]
                writer.write_areas(f'ProgressPartner{rg}.txt', partner_areas)
        # update reporting progress
        del reporting_desc[0]
        writer.write_areas(f'ProgressReporting.txt', reporting_desc)
    # update period progress
    del periods[0]
    writer.writeYearsAndMonths('Progress.txt', periods)

    area_availability = reqHandler.get_reporting_totalRecords(availParams)
    # filter the areas with total records greater than limit and sort descending
    area_availability = sorted(filter(lambda area: area['TotalRecords'] is not None and area['TotalRecords'] > MAX_RESULT, area_availability), key=lambda area: area['TotalRecords'], reverse=True)
    writer.write_areas('ProgressReporting.txt', area_availability)
    reporting_desc = writer.read_areas('ProgressReporting.txt')

    

exit()

# get trade records
areas = list(area_map.keys())
partner_areas = list(reqHandler.partnerAreas.keys())

req = 0
# exhaustive search, all possible combinations of years, months, reporting areas, and partner areas
for y in years:
    for m in months:
        for r in areas:
            # starting index in partner list
            start_idx = int(area_map[r])
            print(type(start_idx))
            for idx_p, p in enumerate(partner_areas[start_idx:]):
                params["ps"] = y + m
                params['r'] = r
                params['p'] = p
                while True:
                    try:
                        response = reqHandler.getResponse(params)
                        if response.status_code == 409:
                            writer.updateIndex("reporting_areas.txt", line_map[r], r+'#'+str(idx_p + start_idx))
                            next_ts_string = re.search("[0-9]{4}-[0-9]{2}-[^.]*", response.text.replace('\x00', '')).group()
                            next_ts = dt.strptime(next_ts_string, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
                            current_utc = dt.now(timezone.utc)
                            td = (next_ts - current_utc).total_seconds()
                            # suspend execution until service is available
                            print(current_utc.time())
                            print(next_ts.time())
                            if(td < 0):
                                print("current time is later than next available time. Abort")
                                quit()
                            print("Sleeping for", td, "seconds")
                            time.sleep(td)
                            print("Resuming Execution")
                    except KeyboardInterrupt:
                        print("Keyboard Interrupt")
                        writer.updateIndex("reporting_areas.txt", line_map[r], r+'#'+str(idx_p + start_idx))
                        quit()
                    except Exception as e:
                        print(e)
                        writer.updateIndex("reporting_areas.txt", line_map[r], r+'#'+str(idx_p + start_idx))
                        continue
                    break
                req += 1
                print(req)
                print(params)
                writer.writeToCSV(response, y, m, reqHandler.reportingAreas[params['r']], reqHandler.partnerAreas[params['p']])
            writer.updateIndex("reporting_areas.txt", line_map[r], r+'#'+str(len(partner_areas)))
