#!/usr/bin/env python3


import argparse
from utils import *


def help():
    print('w')


def parseArguments():
    parser = argparse.ArgumentParser(description="Your script description")

    parser.add_argument("-s", "--send", help="Send a message", nargs=2, metavar=('MESSAGE', 'DEST'))
    parser.add_argument("-c", "--curses", help="Use curses", action="store_true")
    parser.add_argument("-sp", "--show-poll", help="Show poll", action="store_true")
    parser.add_argument("-sb", "--show-banner", help="Show banner", action="store_true")
    parser.add_argument("-sw", "--show-warning", help="Show warning", action="store_true")
    parser.add_argument("-fm", "--filter-msg", help="Filter message", metavar="FILTER_MSG")
    parser.add_argument("-fn", "--filter-name", help="Filter name", metavar="FILTER_NAME")

    return parser.parse_args()


def main():
    args = parseArguments()

    if args.send:
        pass
    else:
        if args.show_poll:
            showPoll = True
        if args.show_banner:
            showBanner = True
        if args.show_warning:
            showWarning = True
        if args.filter_msg:
            filterMsg = args.filter_msg
        if args.filter_name:
            filterName = args.filter_name


if __name__ == '__main__':
    main()