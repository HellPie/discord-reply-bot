from os.path import realpath
from configparser import ConfigParser

__CONFIG_DEFAULT = {
	'LOGIN': {'TOKEN': '', 'USERNAME': '', 'PASSWORD': ''},
	
	'BOT': {
		'PREFIX': ':$',
		'DESCRIPTION': ''
	}
}

CONFIG = ConfigParser(defaults=__CONFIG_DEFAULT)
CONFIG.read(realpath('./assets/config.ini'))
