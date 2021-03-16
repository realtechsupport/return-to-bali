# Python program to get weather data of Ubud
# local independent  Vantage Point station in Ubud
# view-source:https://www.ubudweather.com/welcome/weather_data
# rain in mm, humidity in %, temp in C
# RTS march 2021
# ------------------------------------------------------------------------------
import os, sys
import aiohttp, asyncio
import math, json, re, csv
from bs4 import BeautifulSoup
from datetime import datetime
import xml.etree.ElementTree as ET

weather_file = 'weather.csv'
#-------------------------------------------------------------------------------

async def main():
    s_name = ''
    async with aiohttp.ClientSession() as session:
        now = datetime.now().strftime("%Y-%m-%d_%H:%M")

        #Bangli coordinates. 28km from Ubud
        longitude = 115.346; latitude = -8.454;

        #current conditions
        name = 'ubudweather.com'
        url_string = 'https://www.ubudweather.com/welcome/weather_data'

        async with session.get(url_string) as response:
            if(response.status == 200):
                report = await response.content.read()

                weather_info = {}; info = []
                humidity = ''; max_T = ''; min_T = ''; cur_T = ''; rain = ''
                lltime = ''; zone = ''

                tags = ['Rain', 'Humidity', 'High', 'Low']
                soup = BeautifulSoup(report, 'html.parser')

                #specifically current temp
                items = soup.find_all("div", {'class' : 'weatherdata'})
                for item in items:
                    t = item.getText()
                    if('°C' in t):
                        cur_T = (t.split('°')[0]).strip()

                items = soup.find_all("p", class_="gmt")
                for item in items:
                    t = item.getText()
                    time = t.split('@')[-1]
                    ltime = (time.split('Local Time')[0]).strip()
                    oltime = datetime.strptime(ltime, "%d/%m/%y %H:%M:%S")
                    lltime = oltime.strftime("%Y-%m-%d_%H:%M")
                    zone = time.split('Local Time')[-1].strip()
                    #print('\n\nchecking local time:', ltime, lltime)

                #here the other ones...
                items = soup.find_all(attrs={'class': 'innerwhitebox'})
                for item in items:
                    if(len(item.find_all('p')) > 0):
                        t = item.getText()
                        info.append(t)

                items = soup.find_all(attrs={'class': 'whitebox100per'})
                for item in items:
                    if(len(item.find_all('span')) > 0):
                        t = item.getText()
                        info.append(t)

                for thing in info:
                    for term in tags:
                        if(term in thing):
                            result = thing.split()
                            if(term == 'Rain'):
                                rain = thing.split()[2]
                            elif(term == 'Humidity'):
                                humidity = thing.split()[1]
                                humidity = re.sub("[^\d\.]", "", humidity)
                            elif(term == 'High'):
                                max_T = thing.split()[0]
                                max_T = re.sub("[^\d\.]", "", max_T)
                            elif(term == 'Low'):
                                min_T = thing.split()[0]
                                min_T = re.sub("[^\d\.]", "", min_T)

                weather_info.update({'humidity [%]': humidity})
                weather_info.update({'max_temperature [C]': max_T})
                weather_info.update({'min_temperature [C]': min_T})
                weather_info.update({'current_temperature [C]': cur_T})
                weather_info.update({'rainfall [mm]': rain})
                weather_info.update({'localtime': lltime})
                weather_info.update({'timezone': zone})

#-------------------------------------------------------------------------------

        weather_info.update({'source': name})
        weather_info.update({'timestamp': now})
        print(weather_info)

        with open(weather_file, 'w') as f:
            w = csv.writer(f)
            w.writerows(weather_info.items())

        print('WROTE weather file: ', weather_file)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

#-------------------------------------------------------------------------------
