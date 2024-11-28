import requests
from bs4 import BeautifulSoup
import urllib3
import re
import datetime
import logging
logger = logging.getLogger(__name__)

class Forecast:
    forecast = {}
    hourForecast = {}
    lastUpdate = ''
    icons = {
        "Mostly Cloudy": "mostly_cloudy",
        "Partly Cloudy Night": "partly_cloudy_night",
        "Scattered Showers Night": "scattered_showers_night",
        "Scattered Showers": "scattered_showers",
        "Partly Cloudy": "partly_cloudy",
        "Sunny": "sunny",
        "Rain and Snow": "rain_and_snow",
        "Snow": "snow",
        "Cloudy": "cloudy",
        "Rain": "rain",
        "Mostly Cloudy Night": "mostly_cloudy_night",
        "Scattered Snow Night": "scattered_snow_night",
        "Clear Night": "clear_night",
        "Mostly Sunny": "mostly_sunny",
        "Mostly Clear Night": "mostly_clear_night",
        "Foggy":'foggy'
    }

    def __init__(self):
        self.UpdateForecast()
        
    def PrintForecast(self):
        for forecastDay in self.forecast:
            for dayPart in self.forecast[forecastDay]:
                print(
                    forecastDay,
                    " | ",
                    dayPart,
                    ": temperatura: ",
                    self.forecast[forecastDay][dayPart]["temperature"],
                    " | wiatr: ",
                    self.forecast[forecastDay][dayPart]["wind"],
                    " | deszcz: ",
                    self.forecast[forecastDay][dayPart]["rain"],
                    " | opis: ",
                    self.forecast[forecastDay][dayPart]["icon"],
                    ":",
                    self.icons[self.forecast[forecastDay][dayPart]["icon"]],
                )
                print("-------")
        
    
    def UpdateForecast(self):
        try:
            url="https://weather.com/pl-PL/weather/tenday/l/93409ef628e2eccc8fe84493beb24470c722d12ef4632a9c49250af345ba81ef"   
            
            logger.info("Getting forecast")
            self.forecast = {}
            self.hourForecast = {}
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            response = requests.get(url, verify=False)
            soup = BeautifulSoup(response.text, "html.parser")
            mydivs = soup.find_all("div")

            filteredDivs = []
            for div in mydivs:
                testId = div.get("data-testid")
                if testId == "DailyContent":
                    filteredDivs.append(div)

            for div in filteredDivs:
                day = div.h2.text.split("|")[0].strip()
                dayPart = div.h2.text.split("|")[1].strip()
                if day not in self.forecast:
                    self.forecast[day] = dict()
                self.forecast[day][dayPart] = dict()
                self.forecast[day][dayPart]["temperature"] = div.find_all(
                    attrs={"data-testid": "TemperatureValue"}
                )[0].text
                self.forecast[day][dayPart]["wind"] = div.find_all(
                    attrs={"data-testid": "Wind"}
                )[0].text.replace("\xa0", " ")
                try:
                    self.forecast[day][dayPart]["rain"] = div.find_all(
                        attrs={"data-testid": "PercentageValue"}
                    )[0].text.replace("\xa0", " ")
                except:
                    self.forecast[day][dayPart]["rain"] = '0'

                self.forecast[day][dayPart]["icon"] = div.find_all(
                    attrs={"data-testid": "weatherIcon"}
                )[0].text

            logger.info("Getting hourly forecast")
            url = "https://weather.com/pl-PL/pogoda/godzinowa/l/93409ef628e2eccc8fe84493beb24470c722d12ef4632a9c49250af345ba81ef"
           
            response = requests.get(url, verify=False)
            soup = BeautifulSoup(response.text, "html.parser")
            mydivs = soup.find_all("div")

            filteredDivs = []
            for div in mydivs:
                testId = div.get("data-testid")
                if testId == "DetailsSummary":
                    filteredDivs.append(div)

            for div in filteredDivs[:23]:
                hour = div.h2.text
                self.hourForecast[hour] = dict()
                self.hourForecast[hour]["temperature"] = div.find_all(
                    attrs={"data-testid": "TemperatureValue"}
                )[0].text
                self.hourForecast[hour]["wind"] = div.find_all(
                    attrs={"data-testid": "Wind"}
                )[0].text.replace("\xa0", " ")
                try:
                    self.hourForecast[hour]["rain"] = div.find_all(
                        attrs={"data-testid": "PercentageValue"}
                        )[0].text.replace("\xa0", " ")
                except:
                    self.hourForecast[hour]["rain"] = '0'

                self.hourForecast[hour]["icon"] = div.find_all(
                    attrs={"data-testid": "Icon"}
                )[0].text

        except Exception as e:
            logger.info("Exception loading forecast: " + str(e))
            

        self.lastUpdate = datetime.datetime.now()

    def ReturnForecast(self):
        if self.lastUpdate + datetime.timedelta(minutes = 10) < datetime.datetime.now():
            self.UpdateForecast()
        forecast = dict()
        forecast["10day"] = self.forecast
        forecast["hourly"] = self.hourForecast
        return forecast

if __name__ == "__main__":
    myForecast = Forecast()
    myForecast.UpdateForecast()
    forecast = myForecast.ReturnForecast()

    print(forecast["10day"])
    print("----------------------------")
    print(forecast["hourly"])