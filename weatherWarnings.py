import requests
import urllib3
import datetime

import logging
logger = logging.getLogger(__name__)

class WeatherWarnings: 
    weatherWarning = []
    lastUpdate = ''
    def __init__(self) -> None:
        self.UpdateWarnings()

    def PrintWarnings(self):   
        for warning in self.weatherWarning:
            print(warning)
            print('//////////')

    def UpdateWarnings(self):
        logger.info("Getting weather warnings")
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get('https://danepubliczne.imgw.pl/api/data/warningsmeteo',verify=False)
        parsed = response.json()
        if hasattr(parsed,'status') and parsed['status'] != False:
            filteredEvent = [event for event in parsed if "2261" in event['teryt']]
            
            for event in filteredEvent:            
                self.weatherWarning.append(event['tresc'])   
        self.lastUpdate = datetime.datetime.now()
        logger.info("Received " + str(len(self.weatherWarning)) + " warnings.")
    
    def ReturnWarnings(self):
        if self.lastUpdate + datetime.timedelta(minutes = 10) < datetime.datetime.now():
            self.UpdateWarnings()

        return self.weatherWarning