import json
from fetcher import Fetcher


class Common:


    def __init__(self):
        self._fetcher = Fetcher()
        self.key = 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8'


    def getKey(self):
        return self.key


    def initialData(self, url):
        html = self._fetcher.fetch(url)
        start = html.find('var ytInitialData = ') + 20
        end = html.find('};', start)
        return json.loads(html[start:end] + '}')
    #'ytUrlRgx':'^(?:https?:)?//[^/]*(?:youtube(?:-nocookie)?\.com|youtu\.be).*[=/]([-\\w]{11})(?:\\?|=|&|$)',