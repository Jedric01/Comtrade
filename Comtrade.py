import requests
import json
from pprint import pprint

from contextlib import closing
import csv
from codecs import iterdecode


class Comtrade:
    apiRequest = "http://comtrade.un.org/api//refs/da/view"
    apiResponse = "http://comtrade.un.org/api/get"
    paURI = "https://comtrade.un.org/Data/cache/partnerAreas.json"
    rURI = "https://comtrade.un.org/Data/cache/reporterAreas.json"

    partnerAreas = {}
    reportingAreas = {}

    def __init__(self) -> None:
        self.getReportingAreas()
        self.getPartnerAreas()
        pass

    def getRequest(self, parameters):
        return self.__get(self.apiRequest, parameters)
        
    def getResponse(self, parameters):
        return self.__get(self.apiResponse, parameters)

    def getPartnerAreas(self):
        print("Retrieving list of partner areas")
        response = self.__get(self.paURI, {})
        paList = response.json()["results"]
        for obj in paList:
            if obj['id'] == 'all':
                continue
            self.partnerAreas[obj["id"]] = obj["text"]

    def getReportingAreas(self):
        print("Retrieving list of reporting areas")
        response = self.__get(self.rURI, {})
        rText = response.text.encode().decode("utf-8-sig")
        responseDict = json.loads(rText)
        rList = responseDict["results"]
        for obj in rList:
            if obj['id'] == 'all':
                continue
            self.reportingAreas[obj["id"]] = obj["text"]


    # private method
    def __get(self, api, parameters):
        response = requests.get(api, params=parameters)
        print("Response with status:", response.status_code)
        print(response.text)

        return response

        

    
