from configparser import ConfigParser

configfile = '/etc/galaxymediatools.cfg'

#log = logging.getLogger(__name__)
config = ConfigParser()
config.read(configfile)

print(config.get('pushover', 'user_key'))