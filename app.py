from customtkinter import *
import requests
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import re
import json
import sys

window = CTk()
window.geometry("500x500")
window.title("Athan App") # type: ignore
set_appearance_mode("dark")


sunKeys = ["Sunrise", "Sunset", "Midnight"]

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


def findTime() -> str:
    hms = (datetime.now().hour, datetime.now().minute, datetime.now().second)
    formatHms = []
    for timeParam in hms:
        if len(str(timeParam)) == 1:
            formatHms.append("0" + str(timeParam))
        else:
            formatHms.append(str(timeParam))
    time = ":".join(map(str, formatHms))
    return time


def increment():
    time = findTime()
    if time == "00:00:00":
        os.execv(sys.executable, ['python'] + sys.argv)
    textLabel.configure(text=time)
    prayerTimeAthan(time)
    window.after(1000, increment)


def pullData() -> dict | None:
    date = findDate()
    coordinates = findCoordinates()
    lat = coordinates[0]
    lon = coordinates[1]
    timezone = findTimezone(lat, lon)
    link = "https://api.aladhan.com/v1/timings"
    officialLink = f"{link}/{date}?latitude={lat}&longitude={lon}&method=3&shafaq=general&tune=0%2C32%2C-2%2C0%2C0%2C0%2C0%2C-20%2C0&school=1&timezonestring={timezone}&calendarMethod=UAQ"
    response = requests.get(officialLink)
    if response.status_code == 200:
        print("Data Pulled from API")
        data = json.loads(response.text)
        return data
    else:
        print(f"Error: {response}, Check region.txt to see if you inputted a valid city")
        raise LookupError


def prayerTimeAthan(time: str):
    # time: HH:MM:SS
    # data Time: HH:MM
    # Problem: make shore it doesnt go off the entire time for the full min
    tokenTime = time.split(":")
    localAthanForTheMin = True

    if tokenTime[-1] == "00":
        localAthanForTheMin = False
    tokenTime.pop(-1)
    formatTime = ":".join(tokenTime)
    

    data = loadJson()
    times: dict = data["times"]
    listOfTimes = [times[key] for key in times if key not in sunKeys]
    if not localAthanForTheMin and formatTime in listOfTimes :
        os.system("athan.mp3")
        localAthanForTheMin = True



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
    font = ("Times New Roman", 20)
    color = "#A7A7A7"

    date: str = parsedData["date"]
    islamicDate: str = parsedData["islamicData"]["date"]
    islamicMonth: str = parsedData["islamicData"]["month"]["en"]
    weekday: str = parsedData["weekday"]
    prayerTimes: dict = parsedData["times"]
    prayerTimesAmPm = {key: timeConvert(prayerTimes[key]) for key in prayerTimes}

    weekdayLabel = CTkLabel(master=window, text=weekday, font=font, text_color=color)
    weekdayLabel.place(x=210, y=20)

    dateLabel = CTkLabel(master=window, text=dateConvert(date), font=font, text_color=color)
    dateLabel.place(x=200, y=50)

    islamicDateLabel = CTkLabel(master=window, text=f"{islamicMonth} {" ".join(dateConvert(islamicDate).split(" ")[1:])} AH", font=font, text_color=color)
    islamicDateLabel.place(x=160, y=80)

    currTime = findTime()
    global textLabel
    textLabel = CTkLabel(window, text=currTime, font=font, text_color=color)
    textLabel.place(x=210, y=125)

    
    sunTuples = []
    for key in sunKeys:
        sunTuples.append(prayerTimesAmPm.pop(key))
    
    globalTimeDict: dict = {sunKeys[x]: sunTuples[x] for x in range(len(sunKeys))}

    for newkey in globalTimeDict:
        time = globalTimeDict[newkey]
        globalTimeLabel = CTkLabel(master=window, text=f"{newkey}: {time}", font=font, text_color=color)
        globalTimeLabel.place(x=70, y=(190 + (30 * sunKeys.index(newkey))))

    for num, key in enumerate(prayerTimesAmPm):
        offset = 170
        timeLabel = CTkLabel(master=window, text=f"{key}: {prayerTimesAmPm[key]}", font=font, text_color=color)
        timeLabel.place(x=250, y=(offset + (30 * num)))
    
    window.after(1000, increment)
    window.mainloop()


def main() -> None:
    date = findDate()
    tempData = loadJson()
    if date == tempData["date"]:
        print("Data Pulled from Local File")
        parsedData: dict = tempData
    else:
        data = pullData()
        parsedData = parseData(data)
    writeToJson(parsedData)
    displayData(parsedData)



if __name__ == "__main__":
    main()