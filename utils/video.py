from utils.common import Common
from utils.config import Config
from utils.parser import Parser


class Video:

    #sUrl = 'https://www.youtube.com/results?search_query='
    #tUrl = 'https://img.youtube.com/vi/{}/mqdefault.jpg'
    #pUrl = 'https://youtube.com/playlist?list='
    #vUrl = 'https://youtu.be/'


    def __init__(self):
        keyUrl = 'https://www.youtube.com/youtubei/v1/{}?key=' + self.common.getKey()
        self.searchKey = self.keyUrl.format('search')
        self.browseKey = self.keyUrl.format('browse')
        self.nextKey = self.keyUrl.format('next')


    def DownloadImage(self, videoId, path):
        url = tUrl.format(videoId)
        data = requests.get(url).content
        open(path, 'wb').write(data)

    def ContRelatedVideos(self, json, cont=True):
        parser = Parser()
        try:
            if cont: json = parser.parseJson(json,'ea')
            else: json = parser.parseJson(json,'tr')
            return parser.parseJson(json[-1],'cc')
        except: return ''

    def ContSearch(self, json, cont=True): # n vai dar pro richItemRenderer, o continuationItem eh o ultimo pq eh tudo junto, n um [0] e um [1]
        parser = Parser()
        try:
            if cont: return parser.parseJson(parser.parseJson(json,'oa')[1],'cc')
            else: return parser.parseJson(parser.parseJson(parser.parseJson(json,'ct'),'c')[1],'cc')
        except: return ''


    def ContVideos(self, json, cont=True):
        parser = Parser()
        try:
            if cont: json = parser.parseJson(json,'aa')
            else: json = parser.parseJson(parser.parseJson(parser.parseJson(json,'tc'),'sc'),'c')
            return parser.parseJson(json[len(json)-1],'cc')
        except: return ''

    def RelatedVideos(self, json, cont=True):
        videos = {}
        parser = Parser()
        try:
            if cont: json = parser.parseJson(json,'ea')
            else: json = parser.parseJson(json,'tr')
        except: pass
        for item in json:
            key = list(item)[0]
            if key == 'compactVideoRenderer':
                videos[parser.parseJson(parser.parseJson(item,'cv'),'ts')] = vUrl + parser.parseJson(parser.parseJson(item,'cv'),'vd')
            elif key == 'compactRadioRenderer':
                videos[parser.parseJson(parser.parseJson(item,'ca'),'ts')] = pUrl + parser.parseJson(parser.parseJson(item,'ca'),'pd')
        return videos

    def SearchResultsParser(self, item):
        key = list(item.keys())[0]
        results = {}
        parser = Parser()
        if key == 'videoRenderer':
            results[parser.parseJson(parser.parseJson(parser.parseJson(item,'vr'),'t'),'rt')] = vUrl + parser.parseJson(parser.parseJson(item,'vr'),'vd')
        elif key == 'playlistRenderer':
            results[parser.parseJson(parser.parseJson(item,'pr'),'ts')] = pUrl + parser.parseJson(parser.parseJson(item,'pr'),'pd')
        elif key == 'radioRenderer':
            results[parser.parseJson(parser.parseJson(item,'rr'),'ts')] = pUrl + parser.parseJson(parser.parseJson(item,'rr'),'pd')
        elif key == 'channelRenderer':
            results[parser.parseJson(parser.parseJson(item,'cr'),'ts')] = cUrl + parser.parseJson(parser.parseJson(item,'cr'),'cd')
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
                = vUrl + parser.parseJson(parser.parseJson(item,'vr'),'vd')
        elif key == 'searchPyvRenderer': # do like didYouMeanRenderer
            if ads:
                results['Ad: '+parser.parseJson(parser.parseJson(item,'ap'),'ts')] = vUrl + parser.parseJson(item,'ap')['videoId']
        elif key == 'movieRenderer': print('movie')
        elif key == 'backgroundPromoRenderer': print('Nenhum resuldado encontrado')
        elif key == 'didYouMeanRenderer': print('todo') if didYouMean else print('-')
        elif key == 'showingResultsForRenderer':
            print('Mostrando resultados para: "', end=' \n')
            open('/home/a/'+key,'w').write(str(item))
            print(key)
            input()
            #print(item['showingResultsForRenderer']['correctedQuery']['runs']['text'], end='"\n')
        elif key == 'messageRenderer': pass # No more results
        else:
            open('/home/a/'+key,'w').write(str(item))
            print(item)
            print(key)
            input()
        return results

    def SearchResults(self, json, cont=True): # aqui
        results = {}
        parser = Parser()
        if cont:
            json = parser.parseJson(json,'oa') # try except pass? printar nessa situacao se ele foi pro richItemRenderer 'rc', fica dando erro no 'ao'
            if len(json) > 2:
                print('----------------------')
                input()
                for item in json: results.update(SearchResultsParser(parser.parseJson(item,'rc')))
                return results
            else:
                json = parser.parseJson(json,'ic')
        else:
            json = parser.parseJson(parser.parseJson(parser.parseJson(json,'ct'),'c'),'ic') # richGridRenderer, q num for com numeros 0 1 2 tem richItemRenderer content e dai videoRenderer
            #print(list(json)[-1])
        for item in json: results.update(SearchResultsParser(item))
        return results

    def Videos(self, json, cont=True):
        videos = {}
        parser = Parser()
        if cont: json = parser.parseJson(json,'aa')
        else: json = parser.parseJson(parser.parseJson(parser.parseJson(json,'tc'),'sc'),'c')
        try:
            for item in json: videos[parser.parseJson(parser.parseJson(item['playlistVideoRenderer'],'t'),'rt')] \
            = vUrl + item['playlistVideoRenderer']['videoId']
        except: pass
        return videos

    def MainRelatedVideos(self, url):
        json_ = initialData(url)
        videos = RelatedVideos(json_, False)
        for video in videos: yield video + ' ' + videos[video]
        cont = ContRelatedVideos(json_, False)
        while cont:
            json_ = Request(nextKey, cont)
            json_ = json.loads(json_)
            videos = RelatedVideos(json_)
            for video in videos: yield video + ' ' + videos[video]
            cont = ContRelatedVideos(json_)

    def MainSearch(self, args, count=-1):
        opts = {'-exact':'&sp=QgIIAQ','-playlists':'&sp=EgIQAw','-channels':'&sp=EgIQAg','-date':'&sp=CAI'}
        for opt in opts:
            if opt in args:
                args.remove(opt)
                args.append(opts[opt])

        global sUrl
        for a in args: sUrl += a + '+'
        sUrl = sUrl[:-1]

        json_ = initialData(sUrl)
        results = SearchResults(json_, False)
        for result in results: yield result + ' ' + results[result]
        cont = ContSearch(json_, False)
        while cont and count:
            json_ = Request(searchKey, cont)
            json_ = json.loads(json_)
            results = SearchResults(json_)
            for result in results: yield result + ' ' + results[result]
            cont = ContSearch(json_)
            count -= 1

    def MainVideos(self, args, count=-1):
        url = args[-1]
        if not '/playlist?' in args[-1]: url = pUrl + 'UU' + url.split('/UC')[1]

        json_ = initialData(url)
        videos = Videos(json_, False)
        for video in videos: yield video + ' ' + videos[video]
        cont = ContVideos(json_, False)
        while cont and count:
            json_ = Request(browseKey, cont)
            json_ = json.loads(json_)
            videos = Videos(json_)
            for video in videos: yield video + ' ' + videos[video]
            cont = ContVideos(json_)
            count -= 1

    def MainThumbs(self, args, cont):
        func = MainVideos(args, cont)
        while True:
            try:
                split = next(func).split(vUrl)
                name = split[0]
                videoId = split[1]
                DownloadImage(videoId, '/tmp/"' + name + ' ' + videoId + "\"")
            except: pass