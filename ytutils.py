#!/usr/bin/env python3
import argparse
from utils.chat import Chat
from utils.video import Video
from utils.config import Config


def help():
    print('w')


def parseArguments():
    parser = argparse.ArgumentParser(description='Your script description')

    parser.add_argument('-s', '--search', nargs='+', help='a list of strings to search for')
    parser.add_argument('-c', '--chat', nargs=1, help='chat')
    parser.add_argument('-sp', '--show-poll', help='Show poll', action='store_true')
    parser.add_argument('-sb', '--show-banner', help='Show banner', action='store_true')
    parser.add_argument('-sw', '--show-warning', help='Show warning', action='store_true')
    parser.add_argument('-fm', '--filter-msg', help='Filter message', metavar='FILTER_MSG')
    parser.add_argument('-fn', '--filter-name', help='Filter name', metavar='FILTER_NAME')
    parser.add_argument('--debug', help='Test', metavar='FILTER_NAME')

    return parser.parse_args()


def mode(args):
    if args.search:
        video = Video()
        results = video.search(args.search)
        for result in results:
            print(result)
    elif args.chat:
        chat = Chat()
        chat.show()
    #else:
    #    if args.show_poll:
    #        showPoll = True
    #    if args.show_banner:
    #        showBanner = True
    #    if args.show_warning:
    #        showWarning = True
    #    if args.filter_msg:
    #        filterMsg = args.filter_msg
    #    if args.filter_name:
    #        filterName = args.filter_name

    #if args.thumbs:
    #    if not os.path.isdir(thumbsPath): os.mkdir(thumbsPath)
    #    while True:
    #        video = next(func)
    #        if '/channel' in video or '/playlist' in video: continue
    #        split = video.split(vUrl)
    #        name = split[0].replace('/','')
    #        videoId = split[1]
    #        print(name + vUrl + videoId) #async
    #        DownloadImage(videoId, thumbsPath + ''' + name + videoId + ''')
    #else:
    #    while True: print(next(func))


def main():
    config = Config()
    if not config.loadConfigIfOk():
        config.setDefaultConfig()

    args = parseArguments()

    try:
        mode(args)
    except KeyboardInterrupt:
        exit(0)
    

if __name__ == '__main__':
    main()