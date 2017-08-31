import sys
import logging
import os
import sqlite3

import bot


def __init(entry_point):
	logging.basicConfig(stream=sys.stdout, level=logging.INFO)
	log = logging.getLogger('run.py')
	
	log.info('starting initialization...')
	log.info('checking assets structure...')
	
	log.info('- checking config...')
	if os.path.exists('./assets/config.ini'):
		log.info('  DONE - found config file at \'./assets/config.ini\'')
	else:
		log.error('  FAIL - failed to find config file')
		exit(1)
	
	log.info('loading entry point...')
	entry_point()


if __name__ == '__main__':
	__init(bot.start)
