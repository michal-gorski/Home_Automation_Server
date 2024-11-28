import requests
import urllib3
import datetime


import logging
logger = logging.getLogger(__name__)


class SchoolPlan:
    planData = ''
    dayOfWeek = 0
    currentPlan = ''
    tests = ''
    lastUpdate = ''
    def __init__(self) -> None:
        self.UpdatePlan()

    def CurrentPlan(self):
        import datetime        
        dayOfWeek = datetime.datetime.today().weekday()
        time = datetime.datetime.now().hour
        
        if time > 12:
            dayOfWeek += 1

        if dayOfWeek >= 6:
            dayOfWeek = 0
        
        self.dayOfWeek = dayOfWeek
        logger.info("Getting plan for current day: " + str(dayOfWeek))

        self.currentPlan = self.PlanForDay(dayOfWeek)
        return self.currentPlan

    def PlanForDay(self,day):
        if (day < 0 or day > 4):
            return self.planData['0']
        else:
            return self.planData[str(day)]

    def PrintPlan(self):    
        print(self.WordDay(),': ',self.currentPlan)
        for test in self.tests:
            print(test)

    def UpdatePlan(self):
        logger.info("Getting plan data")
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get(
            "https://michal-gorski.github.io/Weather-Station/plan.json", verify=False
        )
        self.planData = response.json()    
        self.tests = self.planData["sprawdziany"]
        self.lastUpdate = datetime.datetime.now()


    def ReturnSchoolPlan(self):
        if self.lastUpdate + datetime.timedelta(minutes = 10) < datetime.datetime.now():
            self.UpdatePlan()
            self.CurrentPlan()

        plan = {"day": self.WordDay(),"classes": dict()}
        
        counter = 0
        for lekcja in self.PlanForDay(self.dayOfWeek):
            
            plan["classes"][self.planData["lekcje"][counter]] = lekcja 
            counter += 1

        return plan
    
    def ReturnTests(self):
        return self.tests
    
    def WordDay(self):
        if self.dayOfWeek == 0: return "poniedziałek"
        elif self.dayOfWeek == 1: return "wtorek"
        elif self.dayOfWeek == 2: return "środa"
        elif self.dayOfWeek == 3: return "czwartek"
        elif self.dayOfWeek == 4: return "piątek"
        elif self.dayOfWeek > 4: return "poniedziałek"
        else: return ''

if __name__ == "__main__":
    myPlan = SchoolPlan()
    myPlan.UpdatePlan()
    plan = myPlan.ReturnSchoolPlan()

    print(plan)