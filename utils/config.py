import os
import configparser


class Config:


    def __init__(self):
        pass


    def _getConfig(self):
        pass


    def _setConfig(self, config):
        with open('config.ini', 'w') as configfile:
            config.write(configfile)


    def setDefaultConfig(self):
        config = configparser.ConfigParser()
        config['DEFAULT'] = {
            'showMsg':'True',
            'showPoll':'False',
            'showAuthor':'True',
            'showBadges':'True',
            'showBanner':'False',
            'showWarning':'False',
            'showBadgedOnly':'False',
            'showMemberOnly':'False',
            'showBadgedNotMemberOnly':'False',
            'msgFormat':'author badges | msg',
            'badgesFormat':'[badge]',
            'spacingFormat':'\n',
            'filterMsg':'',
            'filterName':'',
            'blockedUsers':'',
            'msgColor':'Fore.WHITE',
            'modNameColor':'Fore.BLUE',
            'membersNameColor':'Fore.GREEN',
            'ytKey':'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
            'chatUrl':'https://www.youtube.com/live_chat?v=',
            'msgUrl':'https://www.youtube.com/youtubei/v1/live_chat/send_message?key={}'.format(ytKey),
            'contChatUrl': 'https://www.youtube.com/youtubei/v1/live_chat/get_live_chat?key={}'.format(ytKey),
            'ads':'False',
            'didYouMean':'False',
        }
        self._setConfig(config)


    def loadConfigFile():
        pass


    def readConfigFile():
        pass
    

    def updateConfigFile():
        pass


    def checkConfigFile():
        if os.path.isfile('config.ini'):
            return True
        return False