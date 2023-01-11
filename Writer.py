import csv
import os
import requests


class Writer:
    DATA_DIR = "trade_data"
    def __init__(self) -> None:
        if not os.path.isdir(os.path.join(os.getcwd(), self.DATA_DIR)):
            os.makedirs(os.path.join(self.DATA_DIR))

    # write to a txt file
    def writeToFile(self, name, list):
        with open(name, "w") as file:
            file.write("2012#01\n")
            for l in list:
                if l == 'all#0':
                    continue
                file.write(l + '\n')
            file.close()

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
    def writeToCSV(self, response, year, month, reportingArea, partner):
        if not os.path.isdir(os.path.join(os.getcwd(), self.DATA_DIR, year, reportingArea + '_r', partner + '_p')):
            os.makedirs(os.path.join(self.DATA_DIR, year, reportingArea + '_r', partner + '_p'))

        with open(f"{self.DATA_DIR}/{year}/{reportingArea}_r/{partner}_p/{month}.csv", "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
            file.flush()


