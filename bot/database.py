from os.path import realpath
import sqlite3
from enum import Enum

__PERMS = realpath('./assets/.storage/data/perms.db')
__REPLIES = realpath('./assets/.storage/data/perms.db')
__SERVERS = realpath('./assets/.storage/data/servers.db')


class Permission(Enum):
	NONE = 0
	ADD = 1
	EDIT = 2
	DELETE = 3


def __update(path, query, *args):
	connection = sqlite3.connect(path)
	print(connection.execute(query, *args))
	connection.commit()
	connection.close()


def __query(path, query, *args):
	connection = sqlite3.connect(path)
	cursor = connection.execute(query, *args)
	rows = cursor.fetchone()
	connection.close()
	return rows[0]


def add_reply(id_, in_, out):
	__update(__REPLIES, "INSERT OR REPLACE INTO `replies` (server_id, input, output) VALUES (?, ?, ?)", [id_, in_, out])


def get_reply(id_, in_):
	return __query(__REPLIES, "SELECT output FROM `replies` WHERE input=?", [id_, in_])


def del_reply(id_, out):
	__update(__REPLIES, "DELETE FROM `replies` WHERE server_id=? AND output=?", [id_, out])


def add_permission(id_, r, p):
	__update(__PERMS, "INSERT OR REPLACE INTO `perms` (server_id, role_id, perm) VALUES (?, ?, ?)", [id_, r, p])


def get_permission(id_, r):
	return __query(__PERMS, "SELECT perm FROM `perms` WHERE server_id=? AND role_id=?", [id_, r])


def del_permission(id_, r):
	__update(__PERMS, "DELETE FROM `perms` WHERE server_id=? AND role_id=?", [id_, r])
