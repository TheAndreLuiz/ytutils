class Images():
    def __init__(self):
        pass

    def downloadImage(self, videoId, path):
        url = tUrl.format(videoId)
        data = requests.get(url).content
        open(path, 'wb').write(data)

    def mainThumbs(self, args, cont):
        func = MainVideos(args, cont)
        while True:
            try:
                split = next(func).split(vUrl)
                name = split[0]
                videoId = split[1]
                DownloadImage(videoId, '/tmp/"' + name + ' ' + videoId + "\"")
            except: pass
