import csv
import os
import requests


class Writer:
    DATA_DIR_UNDER_10000 = "trade_data_under_10000"
    DATA_DIR_ABOVE_10000 = "trade_data_above_10000"
    COMMODITY_DIR = "Commodity"
    SERVICES_DIR = "Services"
    IMPORT_DIR = "Imports"
    EXPORT_DIR = "Exports"
    START_YEAR = '2014'
    START_MONTH = '1'
    def __init__(self) -> None:
        top_level_dirs = [self.DATA_DIR_UNDER_10000, self.DATA_DIR_ABOVE_10000]
        trade_type_dirs = [self.COMMODITY_DIR, self.SERVICES_DIR]
        rg_dirs = [self.IMPORT_DIR, self.EXPORT_DIR]

        for top in top_level_dirs:
            if not os.path.isdir(os.path.join(os.getcwd(), top)):
                for trade_type in trade_type_dirs:
                    for rg in rg_dirs:
                        os.makedirs(os.path.join(top, trade_type, rg))

    def resetProgress(self):
        years = [str(year) for year in range(int(self.START_YEAR), 2023)]
        months = ["{:02d}".format(month) for month in range(int(self.START_MONTH), 13)]
        periods = []
        for y in years:
            for m in months:
                periods.append(y+m)
        self.writeYearsAndMonths('Progress.txt', periods)

    def writeYearsAndMonths(self, name, periods):
        with open(name, 'w') as file:
            for p in periods:
                period = p
                file.write(period + '\n')

    def write_areas(self, name, areas):
        with open(name, 'w') as file:
            for a in areas:
                file.write(a['r'] + '#' + a['rDesc'] + '\n')

    def read_areas(self, name):
        file = open(name, 'r')
        data = file.readlines()
        area_map = {}
        for l in enumerate(data):
            l_list = l.split('#')
            area_map[l_list[0]] = l_list[1].replace('\n', '')
        file.close()

        return area_map

    def readYearsAndMonths(self, name):
        file = open(name, 'r')
        data = file.readlines()
        data = [l.replace('\n', '') for l in data]
        print(data)
        return data

    # write to a txt file
    def writeToFile(self, name, list):
        with open(name, "w") as file:
            file.write("2012#01\n")
            for l in list:
                if l == 'all#0':
                    continue
                file.write(l + '\n')

    # parses file written by writeToFile method, returns the year, month, reporting areas and partner areas, from which to continue scraping
    def parseFile(self, name):
        file = open(name, "r")
        data = file.readlines()
        first_line = data[0].split('#')
        area_map = {}
        line_map = {}

        for idx, l in enumerate(data[1:]):
            current = l.split("#")
            area_map[current[0]] = current[1].replace('\n', '')
            line_map[current[0]] = idx + 1

        file.close()

        return first_line[0], first_line[1], area_map, line_map

    # update content of file, based on the line number
    def updateIndex(self, name, line_num, newContent):
        with open(name, 'r') as file:
            content = file.readlines()
        content[line_num] = newContent + '\n'
        
        with open(name, 'w') as file:
            print(content[line_num])
            file.writelines(content)
            file.close()
    
    # download csv file
    def writeToCSV(self, response, year, month, reportingArea, partner, *, top_level, trade_type , rg): 
        trade_type_dir = self.COMMODITY_DIR if trade_type == 'C' else self.SERVICES_DIR
        rg_dir = self.IMPORT_DIR if rg == 1 else self.EXPORT_DIR
        data_dir = os.path.join(os.getcwd(), top_level, trade_type_dir, rg_dir)
        
        if not os.path.isdir(os.path.join(os.getcwd(), data_dir, year, reportingArea + '_r', partner + '_p')):
            os.makedirs(os.path.join(data_dir, year, reportingArea + '_r', partner + '_p'))

        with open(f"{data_dir}/{year}/{reportingArea}_r/{partner}_p/{month}.csv", "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
            file.flush()


