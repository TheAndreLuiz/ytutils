from fetcher import Fetcher

class Common:
    def __init__(self):
        self._fetcher = Fetcher()

    def InitialData(self, url):
        html = self._fetcher.fetch(url)
        start = html.find('var ytInitialData = ') + 20
        end = html.find('};', start)
        return json.loads(html[start:end] + '}')