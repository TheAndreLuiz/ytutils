class Playlist:


    def __init__(self):
        pass

    def PlaylistCount(self, url):
        if not '/playlist?' in url: url = pUrl + 'UU' + url.split('/UC')[1]
        json = initialData(url)
        yield parser.parseJson(parser.parseJson(json,'co'),'rt')