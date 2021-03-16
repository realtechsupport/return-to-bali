# Python program to get weather data of Ubud or Gianyar
# local independent  Vantage Point station in Ubud
# Ubud station not updated since Fe 7 2021...
# view-source:https://www.ubudweather.com/welcome/weather_data
# rain in mm, humidity in %, temp in C
# RTS march 2021
# ------------------------------------------------------------------------------
import os, sys
import aiohttp, asyncio
import math, json, re, csv
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import xml.etree.ElementTree as ET
weather_file = 'weather.csv'
#-------------------------------------------------------------------------------
def get_local_weather(station_loc):

    now = datetime.now().strftime("%Y-%m-%d_%H:%M")
    #Bangli coordinates. 28km from Ubud
    longitude = 115.346; latitude = -8.454;

    if(station_loc == 'Ubud'):
        name = 'ubudweather.com'
        url_string = 'https://www.ubudweather.com/welcome/weather_data'

        #s_name = ''
        weather_info = {}; info = []
        humidity = ''; max_T = ''; min_T = ''; cur_T = ''; rain = ''
        lltime = ''; zone = ''
        tags = ['Rain', 'Humidity', 'High', 'Low']

        report= requests.get(url_string).text
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
        weather_info.update({'source': name})
        weather_info.update({'timestamp': now})

    #--------------------------------------------------------------------------
    elif(station_loc == 'BMKG'):
        weather_info = {}
        place_id = '501165'                 # 'Gianyar'

        name = 'BMKG_3dayforecast'
        url_string = 'https://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-Bali.xml'

        report= requests.get(url_string).text
        soup = BeautifulSoup(report, 'html.parser')

        tree = ET.fromstring(report)
        for m in tree.iter('area'):
            if(m.attrib['id'] == place_id):
                #print(m.attrib)
                for child1 in m.iter('parameter'):
                    infos = child1.attrib
                    #print('child1 attrib: ', infos)
                    for child2 in child1.iter('timerange'):
                        infos2 = child2.attrib
                        if(list(infos2.values())[1] == '0'):
                            #print('got zero hour')
                            for child3 in child2.iter('value'):
                                #print('child3 attrib: ', child3.attrib)
                                unit = list(child3.attrib.values())[0]
                                parameter = list(infos.values())[1]
                                datapoint = child3.text
                                #print('checking: ', parameter, datapoint, unit)
                                if((parameter == 'Humidity') and (unit == '%')):
                                    weather_info.update({'humidity': datapoint})
                                elif((parameter == 'Temperature') and (unit == 'C')):
                                    weather_info.update({'temperature' : datapoint})
                                elif((parameter == 'Wind direction') and (unit == 'CARD')):
                                    weather_info.update({'wind_dir' : datapoint})
                                elif((parameter == 'Wind speed') and (unit == 'MS')):
                                    weather_info.update({'wind_sp' : datapoint})


#-----------------------------
    try:
        with open(weather_file, 'w') as f:
            w = csv.writer(f)
            w.writerows(weather_info.items())
        print('WROTE weather file: ', weather_file, station_loc)
    except:
        print('weather update failed...')
#-------------------------------------------------------------------------------
