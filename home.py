import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from utilities import Utility
from weather_condition_layout import WeatherConditionUI
from news_layout import NewsUI
from calender_layout import CalenderUI

class HomeScreen(QDialog):

    def __init__(self):
        super().__init__()
        self.title = 'First App'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.layout = QGridLayout()

        weather = WeatherConditionUI()
        self.weather_layout = weather.getLayout()

        news = NewsUI()
        self.news_layout = news.getLayout()

        calender = CalenderUI()
        self.calender_layout = calender.getLayout()
        

        self.layout.addLayout(self.weather_layout, 0, 0)
        self.layout.addLayout(self.news_layout, 1, 0)
        self.layout.addLayout(self.calender_layout, 0, 1)

        self.setLayout(self.layout)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = HomeScreen()
    sys.exit(app.exec_())