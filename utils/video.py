key = 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8'
keyUrl = 'https://www.youtube.com/youtubei/v1/{}?key=' + key

searchKey = keyUrl.format('search')
browseKey = keyUrl.format('browse')
nextKey = keyUrl.format('next')

sUrl = 'https://www.youtube.com/results?search_query='
tUrl = 'https://img.youtube.com/vi/{}/mqdefault.jpg'
pUrl = 'https://youtube.com/playlist?list='
cUrl = 'https://www.youtube.com/channel/'
vUrl = 'https://youtu.be/'

ads = False
didYouMean = False

def Request(url, cont=''):
    if cont:
        data = ('{"context":{"client":{"clientName":"WEB","clientVersion":"2.20210120.08.00", \
        }},"continuation":"') + cont + '"}'
        return requests.post(url, data=data).text
    return requests.get(url).text

def DownloadImage(videoId, path):
    url = tUrl.format(videoId)
    data = requests.get(url).content
    open(path, 'wb').write(data)

def InitialData(url):
    html = Request(url)
    start = html.find('var ytInitialData = ') + 20
    end = html.find('};', start)
    return json.loads(html[start:end] + '}')

def PlaylistCount(url):
    if not '/playlist?' in url: url = pUrl + 'UU' + url.split('/UC')[1]
    json = InitialData(url)
    yield J(J(json,'co'),'rt')

def ChannelId(url): #TODO url check
    json = InitialData(url)
    yield J(json,'mc')

def ContRelatedVideos(json, cont=True):
    try:
        if cont: json = J(json,'ea')
        else: json = J(json,'tr')
        return J(json[-1],'cc')
    except: return ''

def ContSearch(json, cont=True): # n vai dar pro richItemRenderer, o continuationItem eh o ultimo pq eh tudo junto, n um [0] e um [1]
    try:
        if cont: return J(J(json,'oa')[1],'cc')
        else: return J(J(J(json,'ct'),'c')[1],'cc')
    except: return ''

def ContVideos(json, cont=True):
    try:
        if cont: json = J(json,'aa')
        else: json = J(J(J(json,'tc'),'sc'),'c')
        return J(json[len(json)-1],'cc')
    except: return ''

def RelatedVideos(json, cont=True):
    videos = {}
    try:
        if cont: json = J(json,'ea')
        else: json = J(json,'tr')
    except: pass
    for item in json:
        key = list(item)[0]
        if key == 'compactVideoRenderer':
            videos[J(J(item,'cv'),'ts')] = vUrl + J(J(item,'cv'),'vd')
        elif key == 'compactRadioRenderer':
            videos[J(J(item,'ca'),'ts')] = pUrl + J(J(item,'ca'),'pd')
    return videos

def SearchChannel(args):
    global sUrl
    for a in args: sUrl += a + '+'
    sUrl = sUrl[:-1]

    json = InitialData(sUrl)
    json = J(J(J(json,'ct'),'c'),'ic')[0]

    key = list(json.keys())[0]
    if key == 'channelRenderer':
        yield J(J(json,'cr'),'ts') + ' ' + cUrl + J(J(json,'cr'),'cd')
    else: yield 'O canal nao foi encontrado'

def SearchResultsParser(item):
    key = list(item.keys())[0]
    results = {}
    if key == 'videoRenderer':
        results[J(J(J(item,'vr'),'t'),'rt')] = vUrl + J(J(item,'vr'),'vd')
    elif key == 'playlistRenderer':
        results[J(J(item,'pr'),'ts')] = pUrl + J(J(item,'pr'),'pd')
    elif key == 'radioRenderer':
        results[J(J(item,'rr'),'ts')] = pUrl + J(J(item,'rr'),'pd')
    elif key == 'channelRenderer':
        results[J(J(item,'cr'),'ts')] = cUrl + J(J(item,'cr'),'cd')
    elif key == 'horizontalCardListRenderer':
        text = ''
        for card in item['horizontalCardListRenderer']['cards']:
            text += J(card['searchRefinementCardRenderer']['query'],'rt') + ' '
            try:
                query = item['horizontalCardListRenderer']['header']['richListHeaderRenderer']['title']['runs'][1]['text']
                results['Pesquisas relacionadas a: "' + query + '"'] = text
            except:
                results['Tambem pesquisaram por: '] = text
    elif key == 'shelfRenderer':
        string = J(J(item,'sr'),'ts')
        for item in J(J(item,'sr'),'vi'):
            results[string + ': ' + J(J(J(item,'vr'),'t'),'rt')] \
            = vUrl + J(J(item,'vr'),'vd')
    elif key == 'searchPyvRenderer': # do like didYouMeanRenderer
        if ads:
            results['Ad: '+J(J(item,'ap'),'ts')] = vUrl + J(item,'ap')['videoId']
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

def SearchResults(json, cont=True): # aqui
    results = {}
    if cont:
        json = J(json,'oa') # try except pass? printar nessa situacao se ele foi pro richItemRenderer 'rc', fica dando erro no 'ao'
        if len(json) > 2:
            print('----------------------')
            input()
            for item in json: results.update(SearchResultsParser(J(item,'rc')))
            return results
        else:
            json = J(json,'ic')
    else:
        json = J(J(J(json,'ct'),'c'),'ic') # richGridRenderer, q num for com numeros 0 1 2 tem richItemRenderer content e dai videoRenderer
        #print(list(json)[-1])
    for item in json: results.update(SearchResultsParser(item))
    return results

def Videos(json, cont=True):
    videos = {}
    if cont: json = J(json,'aa')
    else: json = J(J(J(json,'tc'),'sc'),'c')
    try:
        for item in json: videos[J(J(item['playlistVideoRenderer'],'t'),'rt')] \
        = vUrl + item['playlistVideoRenderer']['videoId']
    except: pass
    return videos

def MainRelatedChannels(url): #TODO url check
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

def MainRelatedVideos(url):
    json_ = InitialData(url)
    videos = RelatedVideos(json_, False)
    for video in videos: yield video + ' ' + videos[video]
    cont = ContRelatedVideos(json_, False)
    while cont:
        json_ = Request(nextKey, cont)
        json_ = json.loads(json_)
        videos = RelatedVideos(json_)
        for video in videos: yield video + ' ' + videos[video]
        cont = ContRelatedVideos(json_)

def MainSearch(args, count=-1):
    opts = {'-exact':'&sp=QgIIAQ','-playlists':'&sp=EgIQAw','-channels':'&sp=EgIQAg','-date':'&sp=CAI'}
    for opt in opts:
        if opt in args:
            args.remove(opt)
            args.append(opts[opt])

    global sUrl
    for a in args: sUrl += a + '+'
    sUrl = sUrl[:-1]

    json_ = InitialData(sUrl)
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

def MainVideos(args, count=-1):
    url = args[-1]
    if not '/playlist?' in args[-1]: url = pUrl + 'UU' + url.split('/UC')[1]

    json_ = InitialData(url)
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

def MainThumbs(args, cont):
    func = MainVideos(args, cont)
    while True:
        try:
            split = next(func).split(vUrl)
            name = split[0]
            videoId = split[1]
            DownloadImage(videoId, '/tmp/"' + name + ' ' + videoId + "\"")
        except: pass

def Main(func, thumbs=False):
    if thumbs:
        if not os.path.isdir(thumbsPath): os.mkdir(thumbsPath)
        while True:
            video = next(func)
            if '/channel' in video or '/playlist' in video: continue
            split = video.split(vUrl)
            name = split[0].replace("/","")
            videoId = split[1]
            print(name + vUrl + videoId) #async
            DownloadImage(videoId, thumbsPath + '"' + name + videoId + '"')
    else:
        while True: print(next(func))

def Mode(args):
    cont = -1
    if '-less' in args:
        args.remove('-less')
        cont = 0
    elif '-cont' in args: cont = int(args[args.index('-cont') + 1])

    if args[0] in ('-v'): func = MainVideos(args[1:], cont)
    elif args[0] in ('-c'): func = PlaylistCount(args[1])
    elif args[0] in ('-r'): func = MainRelatedVideos(args[1])
    elif args[0] in ('-sc'): func = SearchChannel(args)
    elif args[0] in ('-id'): func = ChannelId(args[1])
    else:
        if '-ads' in args:
            args.remove('-ads')
            global ads
            ads = True
        func = MainSearch(args, cont)

    try:
        if '-t' in args: Main(func,True)
        else: Main(func)
    except StopIteration:
        pass

if __name__ == '__main__' and len(sys.argv) > 1:
    Mode(sys.argv[1:])
else:
    Help()