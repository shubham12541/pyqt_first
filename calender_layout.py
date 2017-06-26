from __future__ import print_function
import sys
from utilities import Utility
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import urllib3
import json
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

""" TODO: refresh every hour"""


class CalenderUI(QWidget):

    def __init__(self):
        super().__init__()

        self.title = 'Calender Widget'
        self.left = 10
        self.top = 10
        self.width = 100
        self.height = 100

        try:
            import argparse
            self.flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        except ImportError:
            self.flags = None

        # If modifying these scopes, delete your previously saved credentials
        # at ~/.credentials/calendar-python-quickstart.json
        self.SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
        self.CLIENT_SECRET_FILE = 'client_secret.json'
        self.APPLICATION_NAME = 'Python pyQt'

        # self.connectCalender()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createGridLayout()

    def createGridLayout(self):
        events = self.getCalenderData()

        self.layout = QVBoxLayout()

        calender_header = QLabel("Agenda: ", self)
        calender_header.setFont(QFont("Times", 20, weight=QFont.Bold))

        self.layout.addWidget(calender_header)

        if not events or len(events)==0:
            label = QLabel("No Upcoming Event", self)
            self.layout.addWidget(label)

        for event in events:
            self.layout.addWidget(QLabel(event.startTime + " " + event.summary, self))
        
    def getLayout(self):
        return self.layout

    def getCalenderData(self):
        """Shows basic usage of the Google Calendar API.

        Creates a Google Calendar API service object and outputs a list of the next
        10 events on the user's calendar.
        """
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        eventsResult = service.events().list(
            calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])

        eventsDetail=[]

        if not events:
            print('No upcoming events found.')
        for event in events:
            temp = EventInfo()
            temp.startTime = event['start'].get('dateTime', event['start'].get('date'))
            temp.summary = event['summary']
            temp.creatorName = event['creator'].get('displayName')
            # print(start, event['summary'])
            eventsDetail.append(temp)
        
        return eventsDetail


    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                    'calendar-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            if self.flags:
                credentials = tools.run_flow(flow, store, self.flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials


class EventInfo:
    startTime=""
    summary=""
    creatorName=""

