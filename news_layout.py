import sys
from utilities import Utility
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import urllib3
import json

""" TODO: refresh every hour"""

class NewsUI(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'News Widget'
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
        articles = self.getData()

        self.layout = QVBoxLayout()

        news_header = QLabel("News: ", self)
        news_header.setFont(QFont("Times", 20, weight=QFont.Bold))

        self.layout.addWidget(news_header)
        for article in articles:
            self.layout.addWidget(QLabel(article.title, self))

    def getLayout(self):
        return self.layout

    def getData(self):
        url="https://newsapi.org/v1/articles?source=the-verge&sortBy=top&apiKey=61d2bac5da354fbe88f176ff16a32fc4"

        http = urllib3.PoolManager()
        res = http.request('GET', url)

        data = json.loads(res.data)
        data_articles = data['articles']
        articles=[]

        for article in data_articles:
            temp = News()
            temp.author = article['author']
            temp.title = article['title']
            temp.description = article['description']
            temp.url = article['url']
            temp.urlToImage = article['urlToImage']
            temp.publishedAt = article['publishedAt']

            articles.append(temp)

        return articles



class News:
    author=""
    title=""
    description=""
    url=""
    urlToImage=""
    publishedAt=""