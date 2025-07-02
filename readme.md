This is an Athan App

Takes live times from the data provided by aladhan.com
Displays it using tkinter

enter your city into the region.txt file. JUST YOUR CITY

Please Make sure you adjust the "tune" parameter in the link, the format is as follows numbers are in minutes
also note that ismak got ommited from the data during the parsing section
also, each part is separated by %2C
Imsak,Fajr,Sunrise,Dhuhr,Asr,Maghrib,Sunset,Isha,Midnight
so if you want to adjust ismak by +1 min, fajr by 0 min, sunrise by 0 min, dhuhr by +20 min, asr by +20 min, maghrib by +5 min, sunset by 0 min, isha by -5 min, and midnight by -10min, your link would be

&tune=1%2C0%2C0%2C20%2C20%2C5%2C0%2C-5%2C-10&
or, use this formatted string
ismakadj = 1
fajradj = 0
sunriseadj = 0
dhuhradj = 20
asradj = 20
maghribadj = 5
sunsetadj = 0
ishaadj = -5
midnightadj = -10
link = rf"&tune={ismakadj}%2C{fajradj}%2C{sunriseadj}%2C{dhuhradj}%2C{asradj}%2C{maghribadj}%2C{sunsetadj}%2C{ishaadj}%2C{midnightadj}&"