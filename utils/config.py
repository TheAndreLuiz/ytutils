import os
import configparser


class Config:


    def __init__(self):
        pass


    def getConfig(self):
        return self.config


    def getSingleConfig(self, config):
        return self.config[config]


    def _setConfig(self, config):
        self.config = config


    def setDefaultConfig(self): # TODO prettfy this
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
            'ads':'False',
            'didYouMean':'False',
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
        }
        self._setConfig(config)


    def loadConfigIfOk(self):
        config = self._readConfigFile(self)
        if self._tryParseConfig(self, config):
            self._setConfig(config)
            return True
        return False


    def updateConfigFile(self):
        pass

    def _readConfigFile(self):
        with open('config.ini', 'r') as configFile:
            config = configparser.ConfigParser()
            config.read_file(configFile)
            return config

            
    def tryParseConfig(self, config):
        config = config['DEFAULT']
        return config['showMsg'] in ['True', 'False'] and \
            config['showPoll'] in ['True', 'False'] and \
            config['showAuthor'] in ['True', 'False'] and \
            config['showBadges']in ['True', 'False'] and \
            config['showBanner'] in ['True', 'False'] and \
            config['showWarning'] in ['True', 'False'] and \
            config['showBadgedOnly'] in ['True', 'False'] and \
            config['showMemberOnly'] in ['True', 'False'] and \
            config['showBadgedNotMemberOnly'] in ['True', 'False'] and \
            config['ads'] in ['True', 'False'] and \
            config['didYouMean'] in ['True', 'False'] and \
            'author' in config['msgFormat'] or 'badges' in config['msgFormat'] or 'msg' in config['msgFormat'] and \
            'badge' in config['badgesFormat'] and \
            config['msgColor'] is not '' and \
            config['modNameColor'] is not '' and \
            config['membersNameColor'] is not ''