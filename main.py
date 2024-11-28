from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
import forecast
import schoolPlan
import sensor
import smog
import weatherWarnings

app = FastAPI()

@app.get("/init")
async def Init():
    app.state.mySmog = smog.Smog()
    app.state.myWeatherWarnings = weatherWarnings.WeatherWarnings()
    app.state.mySchoolPlan = schoolPlan.SchoolPlan()
    app.state.myForecast = forecast.Forecast()
    return {"Init OK"}

@app.get("/smog")
def GetSmog():
    return app.state.mySmog.ReturnSmog()

@app.get("/weatherwarnings")
def GetWeatherWarnings():
    return app.state.myWeatherWarnings.ReturnWarnings()

@app.get("/schoolplan")
def GetSchoolPlan():
    return app.state.mySchoolPlan.ReturnSchoolPlan()

@app.get("/schooltests")
def GetSchoolTests():
    return app.state.mySchoolPlan.ReturnTests()

@app.get("/forecast")
def GetSchoolTests():
    return app.state.myForecast.ReturnForecast()
