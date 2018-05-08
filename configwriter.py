#!/usr/bin/python3

from configparser import ConfigParser

configfile = './config.cfg'

config = ConfigParser()

config['settings'] = {
    'debug': 'true',
    'pushover_userkey': 'abc123',
    'pushover_appkey': 'cba321',
    'log_path': '/opt/testlog.log'
}

with open(configfile, 'w') as f:
    config.write(f)