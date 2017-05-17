import sys
import logging
import os
import sqlite3

import bot


def __init(entry_point):
	logging.basicConfig(stream=sys.stdout, level=logging.INFO)
	log = logging.getLogger('run.py')
	
	def __check_db(check_db_name):
		def __create_db(create_db_name):
			create_db_conn = sqlite3.connect('./assets/.storage/data/' + create_db_name + '.db')
			create_db_file = open('./assets/.storage/scripts/' + create_db_name + '.sql')
			create_db_commands = create_db_file.read().split(';')
			create_db_file.close()
			create_db_cursor = create_db_conn.cursor()
			for create_db_command in create_db_commands:
				create_db_cursor.execute(create_db_command)
			create_db_cursor.close()
			create_db_conn.close()
		
		if not os.path.exists('./assets/.storage/data/' + check_db_name + '.db'):
			if not os.path.exists('./assets/.storage/scripts/' + check_db_name + '.sql'):
				log.error('      FAIL - failed to find a valid sql schema for ' + check_db_name + ' database')
				exit(1)
			log.info('      WARN - failed to find ' + check_db_name + ' database...')
			log.info('    - creating ' + check_db_name + ' database...')
			__create_db(check_db_name)
			log.info('      WARN - rebooting script...')
			log.info('.')
			__init(entry_point=entry_point)
	
	log.info('starting initialization...')
	log.info('checking assets structure...')
	
	log.info('- checking config...')
	if os.path.exists('./assets/config.ini'):
		log.info('  DONE - found config file at \'./assets/config.ini\'')
	else:
		log.error('  FAIL - failed to find config file')
		exit(1)
	
	log.info('- checking storage...')
	if not os.path.exists('./assets/.storage'):
		log.error('  FAIL - failed to find valid storage directory')
		exit(1)
	
	log.info('  - checking databases...')
	if not os.path.exists('./assets/.storage/data/'):
		log.error('    FAIL - failed to find valid data directory')
		exit(1)
	for name in ('perms', 'replies'):
		__check_db(name)
	log.info('    DONE - found all databases (\'perms\', \'replies\')')
	log.info('  DONE - validated storage structure')
	log.info('DONE - validated assets structure')
	
	log.info('loading entry point...')
	entry_point()


if __name__ == '__main__':
	__init(bot.start)
