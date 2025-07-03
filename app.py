from customtkinter import *
import requests
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import re
import json


def dateConvert(dateStr: str) -> str:
    date_obj = datetime.strptime(dateStr, "%d-%m-%Y")
    formatted_date = date_obj.strftime("%B %#d, %Y")
    return formatted_date


def timeConvert(time_str) -> str:
    time_obj = datetime.strptime(time_str, "%H:%M")
    return time_obj.strftime("%I:%M %p").lstrip("0")


def loadJson() -> dict:
    with open("data.json", "r") as jsonData:
        data = json.load(jsonData)
        return data


def writeToJson(data: dict) -> None:
    with open("data.json", "w") as jsonObj:
        json.dump(data, jsonObj, indent=4)


def findTimezone(lat: float, lon: float) -> str:
    tf = TimezoneFinder()
    timezone = tf.timezone_at(lng=lon, lat=lat)
    return timezone


def findDate() -> str:
    requestedDate: str = str(datetime.now())
    date: list = re.split("- | ", requestedDate)
    strDate = str(date.pop(0))
    strDateReversed = "-".join(reversed(strDate.split("-")))
    return strDateReversed


def findCoordinates() -> tuple:
    geolocator = Nominatim(user_agent="geoapiExcercises")
    with open("region.txt", "r") as f:
        location = geolocator.geocode(f.read())

    if location:
        lat = location.latitude
        lon = location.longitude
    else:
        print("City not found")
        raise LookupError
    return (lat, lon)


def parseData(data: dict) -> dict:
    times: dict = data["data"]["timings"]
    dateData: dict = data["data"]["date"]

    islamicDateData: dict = dateData["hijri"]
    islamicMonthData: dict = islamicDateData["month"]
    islamicDate: str = islamicDateData["date"]
    islamicData  = {
        "month" : islamicMonthData,
        "date": islamicDate
    }

    weekday: str = dateData["gregorian"]["weekday"]["en"]
    date: str = dateData["gregorian"]["date"]
    
    del times["Imsak"]
    del times["Firstthird"]
    del times["Lastthird"]

    returnData = {"islamicData": islamicData, "weekday": weekday, "times": times, "date": date}
    return returnData


def displayData(parsedData: dict):
    date: str = parsedData["date"]
    islamicDate: str = parsedData["islamicData"]["date"]
    islamicMonth: str = parsedData["islamicData"]["month"]["en"]
    weekday: str = parsedData["weekday"]
    prayerTimes: dict = parsedData["times"]
    prayerTimesAmPm = {key: timeConvert(prayerTimes[key]) for key in prayerTimes}

    window = CTk()
    window.geometry("500x500")
    set_appearance_mode("dark")

    dateLabel = CTkLabel(master=window, text=dateConvert(date), font=("Times New Roman", 20), text_color="#A7A7A7")
    dateLabel.place(x=200, y=20)
    window.mainloop()


def main() -> None:
    link = "https://api.aladhan.com/v1/timings"
    date = findDate()
    coordinates = findCoordinates()
    lat = coordinates[0]
    lon = coordinates[1]
    timezone = findTimezone(lat, lon)

    officialLink = f"{link}/{date}?latitude={lat}&longitude={lon}&method=3&shafaq=general&tune=0%2C32%2C-2%2C0%2C0%2C0%2C0%2C-20%2C0&school=1&timezonestring={timezone}&calendarMethod=UAQ"
    tempData = loadJson()
    if date == tempData["date"]:
        print("Data Pulled from Local File")
        parsedData = tempData
    else:
        response = requests.get(officialLink)
        if response.status_code == 200:
            print("Data Pulled from API")
            data = json.loads(response.text)
            parsedData: dict = parseData(data)
        else:
            print(f"Error: {response}")
            raise LookupError
    
    writeToJson(parsedData)
    displayData(parsedData)



if __name__ == "__main__":
    main()