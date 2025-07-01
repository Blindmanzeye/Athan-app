import tkinter
import requests
import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import re
import json


def findTimezone(lat: float, lon: float) -> str:
    tf = TimezoneFinder()
    timezone = tf.timezone_at(lng=lon, lat=lat)


def findDate() -> str:
    requestedDate: str = str(datetime.datetime.now())
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


def main() -> None:
    link = "https://api.aladhan.com/v1/timings"
    date = findDate()
    coordinates = findCoordinates()
    lat = coordinates[0]
    lon = coordinates[1]
    timezone = findTimezone(lat, lon)

    officialLink = f"{link}/{date}?latitude={lat}&longitude={lon}&method=3&shafaq=general&tune=0%2C0%2C5%2C7%2C9%2C-1%2C0%2C8%2C-6&school=1&timezonestring={timezone}&calendarMethod=UAQ"
    print(officialLink)
    response = requests.get(officialLink)
    if response.status_code == 200:
        data = response.text
    else:
        print(f"Error: {response}")
        raise LookupError

if __name__ == "__main__":
    main()