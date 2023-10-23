class Channel:
    def __init__(self):
        pass


    def ChannelId(self, url): #TODO url check
        json = InitialData(url)
        yield J(json,'mc')


    def MainRelatedChannels(self, url): #TODO url check
        if not '/channels' in url: url += '/channels'
        json_ = InitialData(url)
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

        json = InitialData(sUrl)
        json = J(J(J(json,'ct'),'c'),'ic')[0]

        key = list(json.keys())[0]
        if key == 'channelRenderer':
            yield J(J(json,'cr'),'ts') + ' ' + cUrl + J(J(json,'cr'),'cd')
        else: yield 'O canal nao foi encontrado'