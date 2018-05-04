"""
 general tools module

 various custom general functions created for my own use

 cachetofile(data, file) - cache (pickle) any object to a file
 cachefromfile(file) - uncache (un-pickle) pickled file back to an object
 pushover(appkey,title,message) - pushover notifications
 whatosami(detail) - returns operating system type, detail true more granular
 elapsedTime(starttime,endtime)
 diskspace(path) - returns dict of total and free space of drive
 crc32_of_string(data) - returns crc of a string
 crc32_compare_string(data, crc) - bool returned if crc matches string
 crc32_of_string(file) - returns crc of a file
 crc32_compare_string(file, crc) - bool returned if crc matches file
 float_trunc_1dec(num) - returns 1 decimal place float, truncated not rounded
 float_trunc_2dec(num) - returns 2 decimal place float, truncated not rounded
"""

import sys
import os
import logging
from zlib import crc32

import dill
from pushover import Client

__author__ = "Ian Perry"
__copyright__ = "Copyright 2018, Galaxy Media"
__license__ = "GPL"
__version__ = "1.0.2"
__maintainer__ = "Ian Perry"
__email__ = "ianperry99@gmail.com"

log = logging.getLogger(__name__)


def cachetofile(dilldata, dillfile):
    try:
        with open(dillfile, 'wb') as fp:
            dill.dump(dilldata, fp)
    except:
        log.error('Serialization to file failed: {}'.format(dillfile))
        return False
    else:
        log.debug('Serialization to file completed: {}'.format(dillfile))
        return True
    finally:
        dillfile.close()


def cachefromfile(dillfile):
    try:
        with open(dillfile, 'rb') as fp:
            dilldata = dill.load(fp)
    except:
        log.critical('Serialization from file failed: {}'.format(dillfile))
        exit()
    else:
        log.debug('Serialization from file completed: {}'.format(dillfile))
        return dilldata
    finally:
        dillfile.close()


def pushover(app_key, ptitle, message):
    try:
        client = Client('ut5A4ejy2dY6HgVBeEaouYHw6uUFpH', api_token=app_key)
        client.send_message(message, title=ptitle)
    except Exception as e:
        log.error('Pushover notification failed. Error: %s' % str(e))
        return False
    else:
        log.debug('Pushover notification sent. Title: {}'.format(ptitle))
        return True


def whatosami(detail):
    if detail is True:
        if sys.platform.startswith('win32'):
            log.debug('Windows platform detected.')
            return 'windows'
        elif sys.platform.startswith('linux'):
            log.debug('Linux platform detected.')
            return 'linux'
        elif sys.platform.startswith('freebsd'):
            log.debug('FreeBSD platform detected.')
            return 'bsd'
        elif sys.platform.startswith('darwin'):
            log.debug('Apple/Mac platform detected.')
            return 'mac'
        else:
            log.warning('Could not determine platform type')
            return 'unknown'
    else:
        if os.name == 'nt':
            log.debug('Windows OS detected.')
            return 'windows'
        elif os.name == 'posix':
            log.debug('Posix OS detected.')
            return 'posix'
        else:
            log.warning('Could not determine OS type')
            return 'unknown'


def elapsedTime(start_time, stop_time, lshort=False):
    diff_time = stop_time - start_time
    days = diff_time.days
    if days == 1:
        daystring = 'Day'
    else:
        daystring = 'Days'
    total_secs = diff_time.seconds
    seconds = total_secs % 60
    if seconds == 1:
        if lshort is False:
            secstring = 'Second'
        else:
            secstring = 'Sec'
    else:
        if lshort is False:
            secstring = 'Seconds'
        else:
            secstring = 'Secs'
    total_min = total_secs / 60
    minutes = int(total_min % 60)
    if minutes == 1:
        if lshort is False:
            minstring = 'Minute'
        else:
            minstring = 'Min'
    else:
        if lshort is False:
            minstring = 'Minutes'
        else:
            minstring = 'Mins'
    hours = int(total_min / 60)
    if hours == 1:
        if lshort is False:
            hourstring = 'Hour'
        else:
            hourstring = 'Hr'
    else:
        if lshort is False:
            hourstring = 'Hours'
        else:
            hourstring = 'Hrs'
    if days != 0:
        return('{} {}, {} {}, {} {}'.format(days, daystring, hours, hourstring, minutes, minstring))
    elif hours != 0:
        return('{} {}, {} {}'.format(hours, hourstring, minutes, minstring))
    elif minutes != 0:
        return('{} {}, {} {}'.format(minutes, minstring, seconds, secstring))
    elif minutes == 0:
        return('{} {}'.format(seconds, secstring))
    else:
        log.error('Elapsed time function failed. Could not convert.')
        return('Error')


def crc32_of_string(data):
    if isinstance(data, str):
        encodeddata = str.encode(data)
        log.debug('crc32_of_string completed. string: {} crc: [{}]'.format(data, crc32(encodeddata)))
        return crc32(encodeddata)
    else:
        raise ValueError('crc32_of_string recieved non-string as data')
        log.exception('crc32_of_string recieved non-string as data: {}'.format(data))
        exit()


def crc32_compare_string(data, crc):
    if not isinstance(crc, int):
        raise ValueError('crc32_compare_string recieved non-int as crc')
        log.exception('crc32_compare_string recieved non-int as crc: {}'.format(crc))
        exit()
    else:
        if isinstance(data, str):
            encodeddata = str.encode(data)
            newcrc = crc32(encodeddata)
            if newcrc != crc:
                log.debug('crc32_compare_string completed and returned FALSE')
                return False
            else:
                log.debug('crc32_compare_string completed and returned TRUE')
                return True
        else:
            raise ValueError('crc32_compare_string recieved non-string as data')
            log.exception('crc32_compare_string recieved non-string as data: {}'.format(data))
            exit()


def crc32_from_file(filename):
    try:
        fd = open(filename, "rb")
        content = fd.readlines()
    except IOError:
        log.exception('crc32_from_file error. Cannont open file {}'.format(filename))
    else:
        fd.close()
        prev = None
        for eachLine in content:
            if not prev:
                prev = crc32(eachLine)
            else:
                prev = crc32(eachLine, prev)
        log.debug('crc32_from_file complete. {} > [{}]'.format(filename, prev))
        return prev

def crc32_compare_file(filename, crc):
    if not isinstance(crc, int):
        raise ValueError('crc32_compare_file recieved non-int as crc')
        log.exception('crc32_compare_file recieved non-int as crc: {}'.format(crc))
        exit()
    else:
        try:
            fd = open(filename, "rb")
            content = fd.readlines()
        except IOError:
            log.exception('crc32_compare_file error. Cannont open file {}'.format(filename))
        else:
            fd.close()
            prev = None
            for eachLine in content:
                if not prev:
                    prev = crc32(eachLine)
                else:
                    prev = crc32(eachLine, prev)
            if prev != crc:
                log.debug('crc32_compare_file completed and returned FALSE')
                return False
            else:
                log.debug('crc32_compare_file completed and returned TRUE')
                return True


def float_trunc_1dec(num):
    try:
        tnum = num // 0.1 / 10
    except:
        log.exception('Error truncating float to 1 decimal: {}'.format(num))
        return False
    else:
        return tnum


def float_trunc_2dec(num):
    try:
        tnum = num // 0.01 / 100
    except:
        log.exception('Error truncating float to 2 decimals: {}'.format(num))
        return False
    else:
        return tnum


def diskspace(path):
    if not os.path.exists(path):
        log.error('Invalid path specified for diskspace check: {}'.format(path))
    else:
        if not os.name == 'posix':
            log.error('Diskspace check only supports Linux/Unix environments')
        else:
            try:
                osstatvfs = os.statvfs(path)
                fsbytes = osstatvfs.f_frsize * osstatvfs.f_blocks     # Size of filesystem in bytes
                fsfree = osstatvfs.f_frsize * osstatvfs.f_bavail     # Number of free bytes that ordinary users
                fsmb = fsbytes / 1000000  # convert to MB
                fsmbfree = fsfree / 1000000  # convert to MB
                fskb = fsbytes / 1000
                fskbfree = fsfree / 1000
                fsgb = fsbytes / 1000000000
                fsgbfree = fsfree / 1000000000
            except:
                log.exception('Error while trying to determine disk space for {}'.format(path))
                return False
            else:
                fsreturn = {}
                fsreturn['GBfree'] = round(fsgbfree, 1)
                fsreturn['GBtotal'] = round(fsgb, 1)
                fsreturn['MBfree'] = round(fsmbfree, 1)
                fsreturn['MBtotal'] = round(fsmb, 1)
                fsreturn['KBfree'] = round(fskbfree, 1)
                fsreturn['KBtotal'] = round(fskb, 1)
                fsreturn['Bytesfree'] = round(fsfree, 1)
                fsreturn['Bytestotal'] = round(fsbytes, 1)
                return fsreturn
