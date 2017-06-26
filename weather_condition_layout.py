import sys
from utilities import Utility
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import urllib3
import json

class WeatherConditionUI(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Weather Widget'
        self.left = 10
        self.top = 10
        self.width = 100
        self.height = 100
        self.initUI()

    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createGridLayout()

    def createGridLayout(self):

        condition = self.getData()

        http = urllib3.PoolManager()
        response = http.request('GET', condition.icon_url)

        pixmap = QPixmap()
        pixmap.loadFromData(response.data)
        weather_image = QLabel(self)
        weather_image.setPixmap(pixmap)

        self.weather_layout2 = QVBoxLayout()
        weather_header = QLabel("Weather: ", self)
        weather_header.setFont(QFont("Times", 20, weight=QFont.Bold))

        self.weather_layout2.addWidget(weather_header)

        self.weather_layout = QHBoxLayout()

        layout1 = QVBoxLayout()
        layout2 = QVBoxLayout()

        # self.weather_layout = QGridLayout()

        layout1.addWidget(weather_image)
        layout1.addWidget(QLabel(condition.temp_c +"˚C" , self))
        layout1.addWidget(QLabel(condition.weather, self))
        layout2.addWidget(QLabel("Humidity: " + condition.relative_humidity, self))
        layout2.addWidget(QLabel("Visibility " + condition.visibility_km + "Km", self))
        layout2.addWidget(QLabel(condition.wind_string, self))
        # self.weather_layout.addWidget(QLabel("Feels like: " + condition.feelslike_c +"˚C", self), 1, 1)
        layout2.addWidget(QLabel("Elevation: " + condition.observation_elevation, self))

        self.weather_layout.addLayout(layout1)
        self.weather_layout.addLayout(layout2)

        self.weather_layout2.addLayout(self.weather_layout)


    def getLayout(self):
        return self.weather_layout2

    def getData(self):
        locs = Utility.getLocation()
        url = 'http://api.wunderground.com/api/7f1df5eb2105d68f/conditions/q/'
        url = url + locs + ".json"

        http = urllib3.PoolManager()
        res = http.request('GET', url)
        data = json.loads(res.data)

        forecast = data['current_observation']
        observation_location = forecast['observation_location']

        condition = ConditionInfo()

        condition.observation_time = str(forecast['observation_time'])
        condition.weather = str(forecast['weather'])
        condition.temp_c = str(forecast['temp_c'])
        condition.relative_humidity = str(forecast['relative_humidity'])
        condition.wind_string = str(forecast['wind_string'])
        condition.heat_index_c = str(forecast['heat_index_c'])
        condition.feelslike_c = str(forecast['feelslike_c'])
        condition.visibility_km = str(forecast['visibility_km'])
        condition.uv_index = str(forecast['UV'])
        condition.icon_url = str(forecast['icon_url'])
        condition.observation_location_full = str(observation_location['full'])
        condition.observation_elevation = str(observation_location['elevation'])
        condition.lat = str(observation_location['latitude'])
        condition.lat = str(observation_location['longitude'])

        return condition


class ConditionInfo:
    observation_time=""
    weather=""
    temp_c=""
    relative_humidity=""
    wind_string=""
    heat_index_c=""
    feelslike_c=""
    visibility_km=""
    uv_index=""
    icon_url=""
    observation_location_full=""
    observation_elevation=""
    lat=""
    loc=""


        


        

