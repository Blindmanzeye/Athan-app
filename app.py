import tkinter
import requests
import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder 

print(datetime.datetime.now())
# 2025-06-30 19:22:45.018807
geolocator = Nominatim(user_agent="geoapiExcercises")
with open("region.txt", "r") as f:
    location = geolocator.geocode(f.read())

if location:
    lat = location.latitude
    lon = location.longitude
    print(f"Latitude: {lat}, Longitude: {lon}")
else:
    print("City not found")
    raise LookupError

tf = TimezoneFinder()
timezone = tf.timezone_at(lng=lon, lat=lat)
print(f"Timezone: {timezone}")