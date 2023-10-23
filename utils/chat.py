import re, sys, json, time, threading, curses.textpad, curses, requests
from utils.config import Config
from utils.parser import Parser
from colorama import Fore, Back, Style


class Chat:


    def __init__(self):
        self.sleep = lambda i:time.sleep(i)
        self.screen = ''


    def ContinuationData(i,json):
        parser = Parser()
        j = parser.parseJson(parser.parseJson(json,i),'d')
        if list(j.keys())[0] == 'invalidationContinuationData':
            j = parser.parseJson(j,'I')
        else:
            j = parser.parseJson(j,'i')
        return j


    def TextContent(item):
        key = list(item.keys())[0]
        parser = Parser()
        return {
            'text': lambda i:parser.parseJson(i,'x'),
            'emoji': lambda i:re.sub(r'^UC+\S+','⬚', parser.parseJson(i,'e'))
        }.get(key)(item)


    def Id(url):
        parser = Parser()
        try:
            return re.findall(ytUrlRgx, url)[0]
        except:
            print("Error: Invalid URL.")


    def Banner(item):
        if not showBanner:
            return ''
        msg = ''
        for part in parser.parseJson(item,'b'):
            msg = msg + TextContent(part)
        return msg + spacingFormat + '\n'


    def Pool(item):
        entry = ''
        parser = Parser()
        for part in parser.parseJson(parser.parseJson(item,'j'),'Q'):
            entry = entry + TextContent(part)
        entry = entry + '\n'
        for part in parser.parseJson(item,'q'):
            string = ''
            for i in parser.parseJson(part,'0'):
                string = string + TextContent(i)
            entry = entry + string + '\n'
        return entry


    def Ticker(item):
        key = list(item.keys())[0]
        parser = Parser()
        try:
            if key == 'liveChatTickerSponsorItemRenderer':
                item = parser.parseJson(item,'S')
                string = 'New member: ' + parser.parseJson(item,'n') + '. '
                for part in parser.parseJson(item,'H'):
                    string = string + TextContent(part)
                return string
            elif key == 'liveChatTickerPaidStickerItemRenderer':
                print('www')
                print(parser.parseJson(item,'H'))
            else:
                print('*******************')
                return key
        except:
            print('WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW')
            print(item)


    def Msg(item):
        key = list(item.keys())[0]
        parser = Parser()
        if key == 'liveChatViewerEngagementMessageRenderer' and showWarning:
            return parser.parseJson(parser.parseJson(parser.parseJson(item,'g'),'r')[0],'x') + spacingFormat + '\n'
        elif key == 'liveChatTextMessageRenderer':
            item = parser.parseJson(item,'h')
            author = ''
            try: author = parser.parseJson(item,'n')
            except KeyError: pass

            if author in blockedUsers: return ''
            if filterName != '' and author != filterName: return ''

            badges = ''
            try:
                for badge in parser.parseJson(item,'u'):
                    badges = badges + badgesFormat.format(badge=parser.parseJson(badge,'w'))
                if showMemberOnly and 'Member' not in badges:
                    return ''
                if showBadgedNotMemberOnly and 'Member' in badges:
                    return ''
            except KeyError:
                if showBadgedOnly: return ''

            if 'ember' in badges: # to also grab New member
                author = membersNameColor + author + Style.RESET_ALL
            if 'Mod' in badges:
                author = modNameColor + author + Style.RESET_ALL

            msg = ''
            for part in parser.parseJson(item,'r'):
                msg = msg + TextContent(part)
            if filterMsg != '' and filterMsg not in msg: return ''

            msg = msgColor + msg + Style.RESET_ALL
            msg = msgFormat.format(author=author if showAuthor else '',badges=badges if showBadges else '',msg=msg if showMsg else '')
            msg = msg.replace('@'+username, Style.BRIGHT + Back.RED + '@'+username + Style.RESET_ALL)
            msg = msg.replace('#'+username, Style.BRIGHT + Back.RED + '#'+username + Style.RESET_ALL)
            # regex support?
            return msg + spacingFormat + '\n'
        return ''


    def ChatItem(item): # TODO
        key = list(item.keys())[0]
        parser = Parser()
        if key == 'clickTrackingParams':
            key = list(item.keys())[1]
        match key: # if to support < 3.10?
            case 'addBannerToLiveChatCommand':
                return Banner(item)
            case 'addChatItemAction':
                return Msg(parser.parseJson(item,'l'))
            case 'showLiveChatActionPanelAction':
                return Pool(parser.parseJson(item,'k'))
            case 'addLiveChatTickerItemAction':
                return Ticker(parser.parseJson(item,'M'))
            case 'liveChatViewerEngagementMessageRenderer':
                return item
            case 'showLiveChatTooltipCommand':
                return ''
            case 'updateLiveChatPollAction':
                return ''
            case 'markChatItemAsDeletedAction':
                return ''
            case 'markChatItemsByAuthorAsDeletedAction':
                return ''
            case _:
                return item


    def SendMsg(url, msg):
        id = Id(url)
        parser = Parser()
        url = chatUrl.format(id)
        json_ = initialData(url)
        params = parser.parseJson(parser.parseJson(json_,'f'),'p')
        Request(msgUrl,'',msgData.format(params,msg))


    def Scroll(top, direction, maxLines, bottom):
        if (direction == -1) and top > 0:
            top += direction
        elif (direction == 1) and (top + maxLines < bottom):
            top += direction
        return top


    def Display(top, items, maxLines, delay):
        for i, item in enumerate(items[top:top + maxLines]):
            try:
                screen.addstr(i, 0, item)
            except:
                pass
            time.sleep(delay)


    def Main():
        parser = Parser()
        id = Id(sys.argv[1])
        url = chatUrl.format(id)
        json_ = initialData(url)

        j = ContinuationData('f',json_)
        cont = parser.parseJson(j,'c')

        for item in parser.parseJson(parser.parseJson(json_,'f'),'a'):
            print(ChatItem(item), end='')

        while True:
            request = Request(url,cont)
            json_ = json.loads(request)
            actions = ''
            timeout = parser.parseJson(j,'t')
            timeout = timeout/1000

            j = ContinuationData('v',json_)
            cont = parser.parseJson(j,'c')

            try:
                actions = parser.parseJson(parser.parseJson(json_,'v'),'a')
            except KeyError:
                time.sleep(timeout)
                continue

            delay = timeout/len(actions)
            td = threading.Thread(target=Sleep, args=(timeout,))
            td.daemon = True
            td.start()
            for item in actions:
                print(ChatItem(item), end='')
                time.sleep(delay)
            td.join()
#'msgHeaders':'{'User-Agent':'Firefox/100','Authorization': 'SAPISIDHASH 1641299520_151984bf767826c38957b10505d354c42fb0aed0','X-Goog-AuthUser': '2','Origin': 'https://www.youtube.com','Cookie': 'VISITOR_INFO1_LIVE=3WuA5Llspl0; PREF=tz=UTC&gl=US&f6=400&f5=20000; SID=FggjwoapweMUy4gtiek7RYXtm9pWdzW1VgkYSVGrib84mJ2tafy-ArGpnHfrZqG3HBVY-g.; __Secure-1PSID=FggjwoapweMUy4gtiek7RYXtm9pWdzW1VgkYSVGrib84mJ2tDe7kqjbBuFydCdCp5mnL1g.; __Secure-3PSID=FggjwoapweMUy4gtiek7RYXtm9pWdzW1VgkYSVGrib84mJ2ta7GjVysBL9MZT0BykEYt5A.; HSID=ANFP1f-apZ_pDNnBo; SSID=AoMF8GPRzyXvVRriM; APISID=Oh9MOa7GC1eXaaiS/AElP75BYvg9-8Dl1V; SAPISID=mEiqE0u2oIdSZy-X/ANzuqQdKuRGGdRBBK; __Secure-1PAPISID=mEiqE0u2oIdSZy-X/ANzuqQdKuRGGdRBBK; __Secure-3PAPISID=mEiqE0u2oIdSZy-X/ANzuqQdKuRGGdRBBK; LOGIN_INFO=AFmmF2swRQIgfcmsJaNhc_sQlCKYx23CM0hgOCh63sspUz4-pwxB-KsCIQCPhkXbectNNlWsjDu7sP3VTcPS3LnLfG7N72YfdgeVRg:QUQ3MjNmd1BPUXJIVFB0WkhoVkw2R051QlNDeUhfVTIyTUpCZFdydV9jYWlZaEVROWlUNnp3X1ZMNkplZzhKNWNSbXRfUG1sUXZrbTF2bnNoN0IxcnRqeXJyMmhIOGhzaG5qeTA1Mm9zQlE4ZVpCOG5OVHk1ald3eGlSWUNBbHo5VmtiUXNXQklsdWNLZ0N2cmduWnNpZ1A2cWJ0VW1uOHVB; SIDCC=AJi4QfGr3htfnQAQ2G9VXELZRFBmqetpRUBX5Opbv9W7aBl69Hr1-sF-QdnGjwPfUoN-9ptu-Js; __Secure-3PSIDCC=AJi4QfHi4Qs5ZasCYqo3JkCbbBUs9ljIb-oxZDn2qJaIA-vYUBwKfc_jK7d2v4adtuJeG9UZcCA; YSC=u6zO_ijHnJA'},
#msgData': '{{"context": {{"client": {{"clientName": "WEB","clientVersion": "2.20211221.00.00"}}}},"params": "{}","richMessage": {{"textSegments": [{{"text": "{}"}}]}}}}',
#'postData':'{{"context":{{"client":{{"hl":"en","gl":"US","clientName":"WEB","clientVersion":"2.20211221.00.00"}}}},"continuation":"{}"}}',