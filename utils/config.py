import os
import configparser


class Config:

    _config = {}

    _instance = None


    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance


    def getConfig(self):
        return self._config


    def getSingleConfig(self, config):
        return self._config['DEFAULT'][config]


    def _setConfig(self, config):
        self._config = config


    def setDefaultConfig(self): # TODO prettfy this # TODO change color logic so no need to save Fore.
        ytKey = 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8'

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
        }
        self._writeConfigFile(config)
        self._setConfig(config)


    def loadConfigIfOk(self):
        config = self._readConfigFile()
        if not config:
            return False

        if self._tryParseConfig(config):
            self._setConfig(config)
            return True
        return False


    def updateConfigFile(self):
        pass


    def _readConfigFile(self):
        if not os.path.isfile('config.ini'):
            return False

        with open('config.ini', 'r') as configFile:
            config = configparser.ConfigParser()
            config.read_file(configFile)
            return config


    def _tryParseConfig(self, config):
        if config.sections() == []:
            return False

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
            config['msgColor'] != '' and \
            config['modNameColor'] != '' and \
            config['membersNameColor'] != ''
    

    def _writeConfigFile(self, config): # TODO option to change config file path
        with open('config.ini', 'w') as configFile:
            config.write(configFile)