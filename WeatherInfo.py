from urllib.request import urlopen
from enum import Enum
from collections import namedtuple
import xml.etree.ElementTree as ET

class DownfallType(Enum):
    eRain       = 1
    eStrongRain = 2
    eWeakRain   = 3
    eSnow       = 4

class SkyType(Enum):
    eSunny      = 1
    eCloudy     = 2
    eNeutral    = 3

class WeatherDayPart(Enum):
    eRain       = 1
    eStrongRain = 2
    eWeakRain   = 3
    eSnow       = 4


# name tuples is like struct, but all data should be set in constructor and can not be modified later ?
DayWeatherInfo = namedtuple("DayWeatherInfo",
                            "precipitationValue precipitationType windDirection windSpeed temperature pressure clouds")


# class WeatherSearch - class to search for weather data on Web
class WeatherSearch:
        #def __init__(self):

        def getWeatherData(self, location):
            """returns => Weather Data.
            This function makes search for weather data on web.
            To do so, it uses data from  http://openweathermap.org/ website.
            Please read http://www.codeproject.com/Articles/630248/WPF-OpenWeather
            to find out more on how to get weather data"""

            appID = "4251690bbc6a44a1cdeb631f31cfb543"
            url = "http://api.openweathermap.org/data/2.5/forecast/daily?q=%slocation&type=accurate&mode=xml&units=metric&cnt=3&appid=%s" % (location, appID)

            htmlFile = urlopen(url)
            htmlByteText = htmlFile.read()
            htmlText = htmlByteText.decode()

            tree = ET.ElementTree(ET.fromstring(htmlText))
            root = tree.getroot()

            threeDaysWeatherInfo = list()
            for dayInfo in root.iter('time'):
                precipitation = dayInfo.find('precipitation')
                precipitationValue = precipitation.get('value')
                precipitationType  = precipitation.get('type')

                windDirectionData = dayInfo.find('windDirection')
                windDirection = windDirectionData.get('name')

                windSpeedData = dayInfo.find('windSpeed')
                windSpeed = windSpeedData.get('mps')

                temperatureData = dayInfo.find('temperature')
                temperature = temperatureData.get('eve')

                pressureData = dayInfo.find('pressure')
                pressure = pressureData.get('value')

                cloudsData = dayInfo.find('clouds')
                clouds = cloudsData.get('value')

                currentData = DayWeatherInfo(precipitationValue,
                            precipitationType,
                            windDirection,
                            windSpeed,
                            temperature,
                            pressure,
                            clouds)

                threeDaysWeatherInfo.append(currentData)

            return threeDaysWeatherInfo

ws = WeatherSearch()
location = "Washington"
print(ws.getWeatherData(location))