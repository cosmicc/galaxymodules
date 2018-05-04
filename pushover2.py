#!/usr/bin/python2

import logging
import urllib
import urllib2
import json

log = logging.getLogger(__name__)


def pushover(app_key, title='', msg=''):
    user_key = 'ut5A4ejy2dY6HgVBeEaouYHw6uUFpH'
    config = {
    'api': 'https://api.pushover.net/1/messages.json',
    'user': user_key,
    'token': app_key
    }

    data = urllib.urlencode({
        'user': config['user'],
        'token': config['token'],
        'title': title,
        'message': msg
    })

    try:
        req = urllib2.Request(config['api'], data)

        response = urllib2.urlopen(req)
    except urllib2.HTTPError:
        log.error('Pushover notification failed. HTTPError')
        return False

    res = json.load(response)

    if res['status'] == 1:
        log.info('Pushover notification successfully sent')
    else:
        log.error('Pushover notification failed')
