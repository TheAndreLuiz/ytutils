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
            'a': 'false',
            'b': 'true',
            'c': 'false'
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