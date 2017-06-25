import sys
from utilities import Utility
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import urllib3
import json

class WeatherUI(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Weather Widget'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 240
        self.initUI()

    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createGridLayout()

    def createGridLayout(self):

        forecast = self.getData()

        http = urllib3.PoolManager()
        response = http.request('GET', forecast[0].icon_url)

        img_data = response.data
        pixmap = QPixmap()
        pixmap.loadFromData(img_data)
        # weather_icon = QIcon(pixmap)

        weather_image = QLabel(self)
        weather_image.setPixmap(pixmap)

        weather_label = QLabel(forecast[0].fcttext_metric, self)

        self.weather_layout = QGridLayout()

        self.weather_layout.addWidget(weather_image, 0, 0)
        self.weather_layout.addWidget(weather_label, 1, 0) 

    def getLayout(self):
        return self.weather_layout

    def getData(self):
        locs = Utility.getLocation()
        url = 'http://api.wunderground.com/api/7f1df5eb2105d68f/forecast/q/'
        url = url + locs + ".json"

        http = urllib3.PoolManager()
        res = http.request('GET', url)
        data = json.loads(res.data)

        forecast = data['forecast']
        txt_forecast = forecast['txt_forecast']
        time = txt_forecast['date']

        forecast_day = txt_forecast['forecastday']
        cast_infos = []

        for cast in forecast_day:
            temp = ForecastInfo()
            temp.icon_url = cast['icon_url']
            temp.title = cast['title']
            temp.fcttext = cast['fcttext']
            temp.fcttext_metric = cast['fcttext_metric']
            cast_infos.append(temp)

        return cast_infos

class ForecastInfo:
    icon_url=""
    title=""
    fcttext=""
    fcttext_metric=""

        


        

