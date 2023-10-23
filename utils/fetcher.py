import requests

class Fetcher:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def fetch(self, endpoint, params=None, method='GET'):
        url = self.base_url + endpoint
        if method == 'GET':
            response = self.session.get(url, params=params)
        elif method == 'POST':
            response = self.session.post(url, data=params)
        else:
            raise ValueError('Unsupported method provided')

        response.raise_for_status()
        
        return response.json()

    def close(self):
        self.session.close()

    #if cont:
    #    data = ('{"context":{"client":{"clientName":"WEB","clientVersion":"2.20210120.08.00", \
    #    }},"continuation":"') + cont + '"}'
    #    return requests.post(url, data=data).text