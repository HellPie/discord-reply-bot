import logging
from sys import stdout
from os.path import exists

from bot import start


def __init(entry_point):
	logging.basicConfig(stream=stdout, level=logging.INFO)
	log = logging.getLogger('run.py')
	
	log.info('starting initialization...')
	log.info('checking assets structure...')
	
	log.info('- checking config...')
	if exists('./assets/config.ini'):
		log.info('  DONE - found config file at \'./assets/config.ini\'')
	else:
		log.error('  FAIL - failed to find config file')
		exit(1)
	
	log.info('loading entry point...')
	entry_point()


if __name__ == '__main__':
	__init(start)
