from configparser import ConfigParser

configfile = './galaxymediatools.conf'

#log = logging.getLogger(__name__)
config = ConfigParser()
config.read(configfile)

print(config.get('pushover', 'user_key'))