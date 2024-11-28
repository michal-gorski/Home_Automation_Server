import requests
import urllib3
import json
import datetime
import logging
logger = logging.getLogger(__name__)

class Smog:
    smog25 = ""
    smog10 = ""
    lastUpdate = ""

    def __init__(self) -> None:
        self.UpdateSmog()

    def UpdateSmog(self):
        logger.info("Getting data on smog")
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get(
            "https://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/736", verify=False
        )
        parsed = response.json()
        self.smog10 = parsed["pm10IndexLevel"]["indexLevelName"]
        self.smog25 = parsed["pm25IndexLevel"]["indexLevelName"]
        self.lastUpdate = datetime.datetime.now()
        
        logger.info("Smog collected: " + self.smog10 + " | " + self.smog25)
        

    def ReturnSmog(self):
        #if not updated for more than 10 minutes, update data
        if self.lastUpdate + datetime.timedelta(minutes = 10) < datetime.datetime.now():
            self.UpdateSmog()
        
        # define dictionary
        smog_details ={  
            "smog25": self.smog25,  
            "smog10": self.smog10,  
            "updateTime": self.lastUpdate
        }  
     
        # Convert Python to JSON  
        return smog_details
      
    def PrintSmog(self):
        print("Pył PM 2.5: ", self.smog25)
        print("Pył PM 10: ", self.smog10)

    