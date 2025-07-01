import tkinter
import requests
import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import re
import json

requestedDate: str = str(datetime.datetime.now())
# 2025-06-30 19:22:45.018807
geolocator = Nominatim(user_agent="geoapiExcercises")
with open("region.txt", "r") as f:
    location = geolocator.geocode(f.read())

if location:
    lat = location.latitude
    lon = location.longitude
    # Latitude: 43.6534817, Longitude: -79.3839347
else:
    print("City not found")
    raise LookupError

tf = TimezoneFinder()
timezone = tf.timezone_at(lng=lon, lat=lat)
# Timezone: America/Toronto

date: list = re.split("- | ", requestedDate)
strDate = str(date.pop(0))
strDateReversed = "-".join(reversed(strDate.split("-")),)
# 01-07-2025


link = "https://api.aladhan.com/v1/timings"
date = strDateReversed


officialLink = f"{link}/{date}?latitude={lat}&longitude={lon}&method=3&shafaq=general&tune=0%2C0%2C5%2C7%2C9%2C-1%2C0%2C8%2C-6&school=1&timezonestring={timezone}&calendarMethod=UAQ"
print(officialLink)
response = requests.get(officialLink)
if response.status_code == 200:
    data = response.text
else:
    print(f"Error: {response}")
    raise LookupError