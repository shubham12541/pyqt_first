import sys
import re
import json
import urllib3

class Utility:
    def getLocation():
        url = 'http://ipinfo.io/json'
        http = urllib3.PoolManager()
        response = http.request('GET', url)
        # response = requests.get(url)
        data = json.loads(response.data)

        location = data['loc']
        city = data['city']
        country = data['country']
        print(location + " " + city + " " + country)
        return location