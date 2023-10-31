import json
from .common import Common
from .config import Config
from .parser import Parser
from .fetcher import Fetcher


class Video:

    sUrl = 'https://www.youtube.com/results?search_query='
    tUrl = 'https://img.youtube.com/vi/{}/mqdefault.jpg'
    pUrl = 'https://youtube.com/playlist?list='
    vUrl = 'https://youtu.be/'


    def __init__(self):
        common = Common()
        keyUrl = 'https://www.youtube.com/youtubei/v1/{}?key=' + common.getKey()

        self.searchKey = keyUrl.format('search')
        self.browseKey = keyUrl.format('browse')
        self.nextKey = keyUrl.format('next')


    def contRelatedVideos(self, json, cont=True):
        parser = Parser()
        try:
            if cont: json = parser.parseJson(json,'ea')
            else: json = parser.parseJson(json,'tr')
            return parser.parseJson(json[-1],'cc')
        except: return ''


    def contSearch(self, json, cont=True): # n vai dar pro richItemRenderer, o continuationItem eh o ultimo pq eh tudo junto, n um [0] e um [1]
        parser = Parser()
        try:
            if cont: return parser.parseJson(parser.parseJson(json,'oa')[1],'cc')
            else: return parser.parseJson(parser.parseJson(parser.parseJson(json,'ct'),'c')[1],'cc')
        except: return ''


    def contVideos(self, json, cont=True):
        parser = Parser()
        try:
            if cont: json = parser.parseJson(json,'aa')
            else: json = parser.parseJson(parser.parseJson(parser.parseJson(json,'tc'),'sc'),'c')
            return parser.parseJson(json[len(json)-1],'cc')
        except: return ''


    def relatedVideos(self, json, cont=True):
        videos = {}
        parser = Parser()
        try:
            if cont: json = parser.parseJson(json,'ea')
            else: json = parser.parseJson(json,'tr')
        except: pass
        for item in json:
            key = list(item)[0]
            if key == 'compactVideoRenderer':
                videos[parser.parseJson(parser.parseJson(item,'cv'),'ts')] = self.vUrl + parser.parseJson(parser.parseJson(item,'cv'),'vd')
            elif key == 'compactRadioRenderer':
                videos[parser.parseJson(parser.parseJson(item,'ca'),'ts')] = self.pUrl + parser.parseJson(parser.parseJson(item,'ca'),'pd')
        return videos


    def searchResultsParser(self, item):
        config = Config()
        print(config.getConfig())
        ads = config.getSingleConfig('ads')
        didYouMean = config.getSingleConfig('didYouMean')

        key = list(item.keys())[0]
        results = {}
        parser = Parser()
        if key == 'videoRenderer':
            results[parser.parseJson(parser.parseJson(parser.parseJson(item,'vr'),'t'),'rt')] = self.vUrl + parser.parseJson(parser.parseJson(item,'vr'),'vd')
        elif key == 'playlistRenderer':
            results[parser.parseJson(parser.parseJson(item,'pr'),'ts')] = self.pUrl + parser.parseJson(parser.parseJson(item,'pr'),'pd')
        elif key == 'radioRenderer':
            results[parser.parseJson(parser.parseJson(item,'rr'),'ts')] = self.pUrl + parser.parseJson(parser.parseJson(item,'rr'),'pd')
        elif key == 'channelRenderer':
            results[parser.parseJson(parser.parseJson(item,'cr'),'ts')] = self.cUrl + parser.parseJson(parser.parseJson(item,'cr'),'cd')
        elif key == 'horizontalCardListRenderer':
            text = ''
            for card in item['horizontalCardListRenderer']['cards']:
                text += parser.parseJson(card['searchRefinementCardRenderer']['query'],'rt') + ' '
                try:
                    query = item['horizontalCardListRenderer']['header']['richListHeaderRenderer']['title']['runs'][1]['text']
                    results['Pesquisas relacionadas a: "' + query + '"'] = text
                except:
                    results['Tambem pesquisaram por: '] = text
        elif key == 'shelfRenderer':
            string = parser.parseJson(parser.parseJson(item,'sr'),'ts')
            for item in parser.parseJson(parser.parseJson(item,'sr'),'vi'):
                results[string + ': ' + parser.parseJson(parser.parseJson(parser.parseJson(item,'vr'),'t'),'rt')] \
                = self.vUrl + parser.parseJson(parser.parseJson(item,'vr'),'vd')
        elif key == 'searchPyvRenderer': # do like didYouMeanRenderer
            if ads:
                results['Ad: '+parser.parseJson(parser.parseJson(item,'ap'),'ts')] = self.vUrl + parser.parseJson(item,'ap')['videoId']
        elif key == 'movieRenderer': print('movie')
        elif key == 'backgroundPromoRenderer': print('Nenhum resuldado encontrado')
        elif key == 'didYouMeanRenderer': print('todo') if didYouMean else print('-')
        elif key == 'showingResultsForRenderer':
            print('Mostrando resultados para: "', end=' \n')
            open('/home/a/'+key,'w').write(str(item))
            print(key)
            input()
        elif key == 'messageRenderer': pass # No more results
        else:
            open('/home/a/'+key,'w').write(str(item))
            print(item)
            print(key)
            input()
        return results


    def searchResults(self, json, cont=True): # aqui
        results = {}
        parser = Parser()
        if cont:
            json = parser.parseJson(json,'oa') # try except pass? printar nessa situacao se ele foi pro richItemRenderer 'rc', fica dando erro no 'ao'
            if len(json) > 2:
                print('----------------------')
                input()
                for item in json: results.update(self.searchResultsParser(parser.parseJson(item,'rc')))
                return results
            else:
                json = parser.parseJson(json,'ic')
        else:
            json = parser.parseJson(parser.parseJson(parser.parseJson(json,'ct'),'c'),'ic') # richGridRenderer, q num for com numeros 0 1 2 tem richItemRenderer content e dai videoRenderer
            #print(list(json)[-1])
        for item in json: results.update(self.searchResultsParser(item))
        return results


    def videos(self, json, cont=True):
        videos = {}
        parser = Parser()
        if cont: json = parser.parseJson(json,'aa')
        else: json = parser.parseJson(parser.parseJson(parser.parseJson(json,'tc'),'sc'),'c')
        try:
            for item in json: videos[parser.parseJson(parser.parseJson(item['playlistVideoRenderer'],'t'),'rt')] \
            = self.vUrl + item['playlistVideoRenderer']['videoId']
        except: pass
        return videos


    def mainRelatedVideos(self, url):
        common = Common()
        fetcher = Fetcher()

        json_ = common.initialData(url)
        videos = self.relatedVideos(json_, False)
        for video in videos: yield video + ' ' + videos[video]
        cont = self.contRelatedVideos(json_, False)
        while cont:
            json_ = fetcher.fetch(self.nextKey, cont)
            json_ = json.loads(json_)
            videos = self.relatedVideos(json_)
            for video in videos: yield video + ' ' + videos[video]
            cont = self.contRelatedVideos(json_)


    def search(self, args, count=-1):
        common = Common()
        opts = {'-exact':'&sp=QgIIAQ','-playlists':'&sp=EgIQAw','-channels':'&sp=EgIQAg','-date':'&sp=CAI'}
        for opt in opts:
            if opt in args:
                args.remove(opt)
                args.append(opts[opt])

        for a in args: self.sUrl += a + '+'
        self.sUrl = self.sUrl[:-1]

        json_ = common.initialData(self.sUrl)
        results = self.searchResults(json_, False)
        for result in results: yield result + ' ' + results[result]
        cont = self.contSearch(json_, False)
        while cont and count:
            json_ = self.request(self.searchKey, cont)
            json_ = json.loads(json_)
            results = self.searchResults(json_)
            for result in results: yield result + ' ' + results[result]
            cont = self.contSearch(json_)
            count -= 1


    def mainVideos(self, args, count=-1):
        url = args[-1]
        fetcher = Fetcher()
        if not '/playlist?' in args[-1]: url = self.pUrl + 'UU' + url.split('/UC')[1]

        json_ = self.initialData(url)
        videos = videos(json_, False)
        for video in videos: yield video + ' ' + videos[video]
        cont = self.contVideos(json_, False)
        while cont and count:
            json_ = fetcher.fetch(self.browseKey, cont)
            json_ = json.loads(json_)
            videos = videos(json_)
            for video in videos: yield video + ' ' + videos[video]
            cont = self.contVideos(json_)
            count -= 1