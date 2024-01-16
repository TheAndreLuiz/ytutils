from .common import Common


class Channel:


    def __init__(self):
        self.common = Common()


    #cUrl = 'https://www.youtube.com/channel/'
    def ChannelId(self, url): #TODO url check
        json = self.common.initialData(url)
        yield parser.parseJson(json,'mc')


    def MainRelatedChannels(self, url): #TODO url check
        if not '/channels' in url: url += '/channels'
        json_ = initialData(url)
        channels = RelatedChannels(json_, False)
        for channel in channels: print(channel + ' ' + channels[channel])
        cont = ContChannel(json_, False)
        while cont:
            json_ = Request(browseKey, cont)
            json_ = json.loads(json_)
            channels = RelatedChannels(json_)
            for channel in channels: print(channel + ' ' + channels[channel])
            cont = ContChannel(json)


    def SearchChannel(self, args):
        global sUrl
        for a in args: sUrl += a + '+'
        sUrl = sUrl[:-1]

        json = initialData(sUrl)
        json = parser.parseJson(parser.parseJson(parser.parseJson(json,'ct'),'c'),'ic')[0]

        key = list(json.keys())[0]
        if key == 'channelRenderer':
            yield parser.parseJson(parser.parseJson(json,'cr'),'ts') + ' ' + cUrl + parser.parseJson(parser.parseJson(json,'cr'),'cd')
        else: yield 'O canal nao foi encontrado'