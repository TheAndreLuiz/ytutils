import re
import json

from requests import JSONDecodeError
from .fetcher import Fetcher


class Common:

    _ytUrlRegex = '^(?:https?:)?//[^/]*(?:youtube(?:-nocookie)?\.com|youtu\.be).*[=/]([-\\w]{11})(?:\\?|=|&|$)'
    _key = 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8'


    def __init__(self):
        self._fetcher = Fetcher()


    def getKey(self):
        return self._key


    def getVideoId(self, url):
        print('wwwwwwwwww')
        print(self.isUrlOk(url))
        try:
            if self.isUrlOk(url):
                return url.split('=')[-1]
        except:
            print('Invalid url')
            exit(0)


    def isUrlOk(self, url):
        return re.match(self._ytUrlRegex, url) is not None


    def initialData(self, url):
        if self.isUrlOk(url):
            html = self._fetcher.fetch(url)
            start = html.find('var ytInitialData = ') + 20
            end = html.find('};', start)
            return json.loads(html[start:end] + '}')