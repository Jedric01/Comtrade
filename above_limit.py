from Comtrade import Comtrade
from Writer import Writer
from datetime import datetime as dt, timezone
import re
import time

MAX_RESULT = 10000

reqHandler = Comtrade()
writer = Writer()

# first run, initialize reporting areas and partner areas
# writer.writeToFile("reporting_areas.txt", [area + '#0' for area in reqHandler.reportingAreas])
# writer.writeToFile("partner_areas.txt", reqHandler.partnerAreas)

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

# get start year, start month and maps
start_year, start_month, area_map, line_map = writer.parseFile("reporting_areas.txt")
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
