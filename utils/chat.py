#!/usr/bin/env python3
import re, sys, json, time, threading, curses.textpad, curses, requests
from colorama import Fore, Back, Style

msgFormat = '{author} {badges}| {msg}'
badgesFormat = '[{badge}] '
spacingFormat = '\n'
username = 'zsadroh'

filterMsg = ''
filterName = ''
blockedUsers = ['','']

msgColor = Fore.WHITE
modNameColor = Fore.BLUE
membersNameColor = Fore.GREEN

showMsg = True
showPoll = False
showAuthor = True
showBadges = True
showBanner = False
showWarning = False

showBadgedOnly = False
showMemberOnly = False # args when this or this \/ autoset badgedOnly
showBadgedNotMemberOnly = False

ytKey = 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8'
chatUrl = 'https://www.youtube.com/live_chat?v={}'
msgUrl = 'https://www.youtube.com/youtubei/v1/live_chat/send_message?key={}'.format(ytKey)
contChatUrl = 'https://www.youtube.com/youtubei/v1/live_chat/get_live_chat?key={}'.format(ytKey)
ytUrlRgx = '^(?:https?:)?//[^/]*(?:youtube(?:-nocookie)?\.com|youtu\.be).*[=/]([-\\w]{11})(?:\\?|=|&|$)'
postData = '{{"context":{{"client":{{"hl":"en","gl":"US","clientName":"WEB","clientVersion":"2.20211221.00.00"}}}},"continuation":"{}"}}'
msgHeaders={'User-Agent':'Firefox/100','Authorization': 'SAPISIDHASH 1641299520_151984bf767826c38957b10505d354c42fb0aed0','X-Goog-AuthUser': '2','Origin': 'https://www.youtube.com','Cookie': 'VISITOR_INFO1_LIVE=3WuA5Llspl0; PREF=tz=UTC&gl=US&f6=400&f5=20000; SID=FggjwoapweMUy4gtiek7RYXtm9pWdzW1VgkYSVGrib84mJ2tafy-ArGpnHfrZqG3HBVY-g.; __Secure-1PSID=FggjwoapweMUy4gtiek7RYXtm9pWdzW1VgkYSVGrib84mJ2tDe7kqjbBuFydCdCp5mnL1g.; __Secure-3PSID=FggjwoapweMUy4gtiek7RYXtm9pWdzW1VgkYSVGrib84mJ2ta7GjVysBL9MZT0BykEYt5A.; HSID=ANFP1f-apZ_pDNnBo; SSID=AoMF8GPRzyXvVRriM; APISID=Oh9MOa7GC1eXaaiS/AElP75BYvg9-8Dl1V; SAPISID=mEiqE0u2oIdSZy-X/ANzuqQdKuRGGdRBBK; __Secure-1PAPISID=mEiqE0u2oIdSZy-X/ANzuqQdKuRGGdRBBK; __Secure-3PAPISID=mEiqE0u2oIdSZy-X/ANzuqQdKuRGGdRBBK; LOGIN_INFO=AFmmF2swRQIgfcmsJaNhc_sQlCKYx23CM0hgOCh63sspUz4-pwxB-KsCIQCPhkXbectNNlWsjDu7sP3VTcPS3LnLfG7N72YfdgeVRg:QUQ3MjNmd1BPUXJIVFB0WkhoVkw2R051QlNDeUhfVTIyTUpCZFdydV9jYWlZaEVROWlUNnp3X1ZMNkplZzhKNWNSbXRfUG1sUXZrbTF2bnNoN0IxcnRqeXJyMmhIOGhzaG5qeTA1Mm9zQlE4ZVpCOG5OVHk1ald3eGlSWUNBbHo5VmtiUXNXQklsdWNLZ0N2cmduWnNpZ1A2cWJ0VW1uOHVB; SIDCC=AJi4QfGr3htfnQAQ2G9VXELZRFBmqetpRUBX5Opbv9W7aBl69Hr1-sF-QdnGjwPfUoN-9ptu-Js; __Secure-3PSIDCC=AJi4QfHi4Qs5ZasCYqo3JkCbbBUs9ljIb-oxZDn2qJaIA-vYUBwKfc_jK7d2v4adtuJeG9UZcCA; YSC=u6zO_ijHnJA'}
msgData = '{{"context": {{"client": {{"clientName": "WEB","clientVersion": "2.20211221.00.00"}}}},"params": "{}","richMessage": {{"textSegments": [{{"text": "{}"}}]}}}}'

Sleep = lambda i:time.sleep(i)
screen = ''

def Help():
    print('W')

def Request(url, cont='', msg=''):
    if msg:
        return requests.post(url,headers=msgHeaders,data=msg).status_code
    if cont:
        return requests.post(contChatUrl,postData.format(cont)).text
    return requests.get(url, headers=msgHeaders).text

def J(j, opt):
    return {
    }.get(opt)(j)

def InitialData(url):
    html = Request(url)
    start = html.find('ytInitialData') + 18
    end = html.find('};', start)
    return json.loads(html[start:end] + '}')

def ContinuationData(i,json):
    j = J(J(json,i),'d')
    if list(j.keys())[0] == 'invalidationContinuationData':
        j = J(j,'I')
    else:
        j = J(j,'i')
    return j

def TextContent(item):
    key = list(item.keys())[0]
    return {
        'text': lambda i:J(i,'x'),
        'emoji': lambda i:re.sub(r'^UC+\S+','⬚', J(i,'e'))
    }.get(key)(item)

def Id(url):
    try:
        return re.findall(ytUrlRgx, url)[0]
    except:
        print("Error: Invalid URL.")

def Banner(item):
    if not showBanner:
        return ''
    msg = ''
    for part in J(item,'b'):
        msg = msg + TextContent(part)
    return msg + spacingFormat + '\n'

def Pool(item):
    entry = ''
    for part in J(J(item,'j'),'Q'):
        entry = entry + TextContent(part)
    entry = entry + '\n'
    for part in J(item,'q'):
        string = ''
        for i in J(part,'0'):
            string = string + TextContent(i)
        entry = entry + string + '\n'
    return entry

def Ticker(item):
    key = list(item.keys())[0]
    try:
        if key == 'liveChatTickerSponsorItemRenderer':
            item = J(item,'S')
            string = 'New member: ' + J(item,'n') + '. '
            for part in J(item,'H'):
                string = string + TextContent(part)
            return string
        elif key == 'liveChatTickerPaidStickerItemRenderer':
            print('www')
            print(J(item,'H'))
        else:
            print('*******************')
            return key
    except:
        print('WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW')
        print(item)

def Msg(item):
    key = list(item.keys())[0]
    if key == 'liveChatViewerEngagementMessageRenderer' and showWarning:
        return J(J(J(item,'g'),'r')[0],'x') + spacingFormat + '\n'
    elif key == 'liveChatTextMessageRenderer':
        item = J(item,'h')
        author = ''
        try: author = J(item,'n')
        except KeyError: pass

        if author in blockedUsers: return ''
        if filterName != '' and author != filterName: return ''

        badges = ''
        try:
            for badge in J(item,'u'):
                badges = badges + badgesFormat.format(badge=J(badge,'w'))
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
        for part in J(item,'r'):
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
    if key == 'clickTrackingParams':
        key = list(item.keys())[1]
    match key: # if to support < 3.10?
        case 'addBannerToLiveChatCommand':
            return Banner(item)
        case 'addChatItemAction':
            return Msg(J(item,'l'))
        case 'showLiveChatActionPanelAction':
            return Pool(J(item,'k'))
        case 'addLiveChatTickerItemAction':
            return Ticker(J(item,'M'))
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
    url = chatUrl.format(id)
    json_ = InitialData(url)
    params = J(J(json_,'f'),'p')
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

def Curses(stdscr): # refactor
    global screen
    screen = stdscr
    height, width = screen.getmaxyx()

    screen = curses.initscr()
    screen.keypad(True)
    screen.nodelay(1)
    scroll = True
    maxLines = curses.LINES

    id = Id('https://www.youtube.com/watch?v=5qap5aO4i9A')
    url = chatUrl.format(id)
    json_ = InitialData(url)

    j = ContinuationData('f',json_)
    cont = J(j,'c')

    items = []
    #for item in J(J(json_,'f'),'a'):
        #items.append(ChatItem(item))
        #items.append('')

    top = 0
    bottom = len(items)
    while True:
        request = Request(url,cont)
        json_ = json.loads(request)
        actions = ''
        timeout = J(j,'t')
        timeout = timeout/1000
        maxlines = curses.LINES

        j = ContinuationData('v',json_)
        cont = J(j,'c')

        try:
            actions = J(J(json_,'v'),'a')
        except KeyError:
            time.sleep(timeout)
            continue

        delay = timeout/len(actions)
        td = threading.Thread(target=Sleep, args=(timeout,))
        td.daemon = True
        td.start()

        ch = screen.getch()
        if ch == curses.KEY_UP:
            scroll = False
            top = Scroll(top, -1, bottom)
        elif ch == curses.KEY_DOWN:
            scroll = True

        for item in actions:
            items.append(ChatItem(item))
            items.append('\n\n')

        Display(top, items, maxLines, delay)
        bottom = len(items)
        if scroll:
            top = Scroll(top, 1, maxLines, bottom)

        td.join()

def MainLoop():
    print()

def Main(): # refactor
    id = Id(sys.argv[1])
    url = chatUrl.format(id)
    json_ = InitialData(url)

    j = ContinuationData('f',json_)
    cont = J(j,'c')

    for item in J(J(json_,'f'),'a'):
        print(ChatItem(item), end='')

    while True:
        request = Request(url,cont)
        json_ = json.loads(request)
        actions = ''
        timeout = J(j,'t')
        timeout = timeout/1000

        j = ContinuationData('v',json_)
        cont = J(j,'c')

        try:
            actions = J(J(json_,'v'),'a')
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

if __name__ == '__main__' and len(sys.argv) > 1:
    args = sys.argv[1:]
    if '-s' in args or '--send' in args:
        SendMsg(args[0], args[args.index('-s') + 1] if '-s' in args else args[args.index('--send') + 1])
    elif '-c' in args:
        curses.wrapper(Curses)
    else:
        if '-sp' in args or '--show-poll' in args:
            showPoll = True
        if '-sb' in args or '--show-banner' in args:
            showBanner = True
        if '-sw' in args or '--show-warning' in args:
            showWarning = True
        if '-fm' in args or '--filter-msg' in args:
            filterMsg = args[args.index('-fm') + 1 if '-fm' in args else args.index('--filter-msg') + 1]
        if '-fn' in args or '--filter-name' in args:
            filterName = args[args.index('-fn') + 1 if '-fn' in args else args.index('--filter-name') + 1]
        try:
            Main()
        except KeyboardInterrupt:
            sys.exit()
else:
    Help()
