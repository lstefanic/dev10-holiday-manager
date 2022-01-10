import datetime
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass


# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------
class Holiday:
      
    def __init__(self,name, date):
        self._name = name
        self._date = date
    
    def __str__ (self):
        date_string = self._date.strftime("%Y-%m-%d")
        return "%s (%s)" % (self._name, date_string)

    def __eq__(self, other):
        if ( self._name != other._name ):
            return False
        self_date = self._date.strftime("%Y-%m-%d")
        other_date = other._date.strftime("%Y-%m-%d")
        return (self_date == other_date )

    @property
    def name(self):
        return self._name
    
    @property
    def date(self):
        return self._date
          
           
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------
class HolidayList:
    def __init__(self):
        self.innerHolidays = []

    def addHoliday(self, holidayObj):
        if ( isinstance(holidayObj,Holiday) ):
            self.innerHolidays.append(holidayObj)
            print("Holiday added")

    def findHoliday(self, HolidayName, Date):
        for holidayObj in self.innerHolidays:
            if ( holidayObj.name == HolidayName and holidayObj.date == Date ):
                return holidayObj
        return None

    def removeHoliday(self, HolidayName, Date):
        holidayObj = self.findHoliday(HolidayName, Date)
        self.innerHolidays.remove(holidayObj)
        print("Holiday deleted")

    def read_json(self, filelocation):
        f = open(filelocation)
        data = json.load(f)
        f.close()
        for holiday_dict in data["holidays"]:
            name = holiday_dict["name"]
            date = datetime.datetime.strptime(holiday_dict["date"], "%Y-%m-%d")
            self.addHoliday(Holiday(name,date))

    def save_to_json(self, filelocation):
        holiday_list = []
        for holidayObj in self.innerHolidays:
            name = holidayObj.name
            date = holidayObj.date.strftime("%Y-%m-%d")
            holiday_dict = {"name": name, "date": date}
            holiday_list.append(holiday_dict)
        data = {"holidays": holiday_list}
        f = open(filelocation, "w")
        json.dump(data, f, indent=4)
        f.close()
        
    def scrapeHolidays(self):
        current_year = datetime.datetime.now().year
        for year in range(current_year-2,current_year+3):
            url = "https://www.timeanddate.com/holidays/us/%u" % year
            response = requests.get(url)
            html = response.text
            soup = BeautifulSoup(html, "html.parser")
            table = soup.find("table", attrs = {"id": "holidays-table"})
            body = table.find("tbody")
            for row in body.find_all("tr"):
                if ( "data-mask" in row.attrs ):
                    link = row.find("a").attrs["href"]
                    if ( link.count("holidays/us") > 0 ):
                        date_string = "%s, %u" % (row.find("th").string, year)
                        date = datetime.datetime.strptime(date_string, "%b %d, %Y")
                        name = row.find_all("td")[1].find("a").string
                        if ( self.findHoliday(name, date) is None ):
                            self.addHoliday(Holiday(name,date))

    def numHolidays(self):
        return len(innerHolidays)
    
    def filter_holidays_by_week(self, year, week_number):
        date_string = "%u, %s" % (year, week_number)
        return list(filter(lambda x: x.date.strftime("%U") == week_number and x.date.year == year, self.innerHolidays))

    def displayHolidaysInWeek(self, holidayList):
        for holidayObj in holidayList:
            print(holidayObj)

    def getWeather(self, weekNum):
        # Convert weekNum to range between two days
        # Use Try / Except to catch problems
        # Query API for weather in that week range
        # Format weather information and return weather string./

        # city = "Minneapolis"
        # current_year = datetime.datetime.now().year
        # start_date = # YYYY-MM-DD
        # end_date = # YYYY-MM-DD
        # url = "https://weatherapi-com.p.rapidapi.com/history.json"
        # query = {"q": city, "dt": start_date, "end_dt": end_date, "lang":"en"}
        # headers = {
        #     'x-rapidapi-host': "weatherapi-com.p.rapidapi.com",
        #     'x-rapidapi-key': "a2261de387mshd22f0a8befc952bp133a57jsn302de7132003"
        # }
        # response = requests.request("GET", url, headers=headers, params=query)
        # print(response.text)
        return "Here's the weather"

    def viewCurrentWeek(self):
        current_date = datetime.datetime.now()
        current_year = current_date.year
        current_week = current_date.strftime("%U")
        holidayList = self.filter_holidays_by_week(current_year, current_week)
        self.displayHolidaysInWeek(holidayList)
        while ( True ):
            action = input("Would you like to see this week's weather? (y/n): ")
            if ( action == "y" ):
                print(getWeather(current_week))
                break
            if ( action == "n" ):
                break
    
    def displayMenu(self):
        f = open("menu.txt")
        menu = f.read()
        f.close()
        print(menu)

def main():
    holidays = HolidayList()
    holidays.read_json("holidays.json")
    holidays.scrapeHolidays()
    while ( True ):
        holidays.displayMenu()
        action = input("Choose an action (1-5): ")
        if ( action == "1" ):
            name = input("Enter a holiday name: ")
            date_string = input("Enter a holiday date (YYYY-MM-DD): ")
            date = datetime.datetime.strptime(date_string, "%Y-%m-%d")
            if ( holidays.findHoliday(name, date) is None ):
                holidays.addHoliday(Holiday(name,date))
        if ( action == "2" ):
            name = input("Enter a holiday name: ")
            date_string = input("Enter a holiday date (YYYY-MM-DD): ")
            date = datetime.datetime.strptime(date_string, "%Y-%m-%d")
            holidays.removeHoliday(name,date)
        if ( action == "3" ):
            year = int(input("Enter a year: "))
            week = input("Enter a week (1-52, leave blank for current week): ")
            if (week == ""):
                holidays.viewCurrentWeek()
            else:
                holidays.displayHolidaysInWeek(holidays.filter_holidays_by_week(year,week))
        if ( action == "4" ):
            save_anyway = input("Are you sure you want to save your changes? (y/n): ")
            if (save_anyway == "y"):
                holidays.save_to_json("output.json")
        if ( action == "5" ):
            break


if __name__ == "__main__":
    main();


# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files 
# and use placeholder values with the format option.
# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders 
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.





