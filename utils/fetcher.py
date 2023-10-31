import requests

class Fetcher:
    def __init__(self):
        self.session = requests.Session()


    def fetch(self, url, cont=False):
        if cont:
            data = ('{"context":{"client":{"clientName":"WEB","clientVersion":"2.20210120.08.00", \
            }},"continuation":"') + cont + '"}'
            return requests.post(url, data=data).text
        return self.session.get(url).text


    def close(self):
        self.session.close()
