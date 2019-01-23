#!/usr/bin/python

import mysql.connector
#from mysql.connector import (connection)

class Connection(object):
	___connection 	= None
	___db			= None
	def __init__(self):
		try:
			_file = open('system.config', "+r")
		except Exception as e:
			_file = open('system.config', "+w")
			#Editar segun los datos de nuestro servidor SQL
			_file.write("host: localhost\n")
			_file.write("user: phpmyadmin\n")
			_file.write("password: phpmyadmin\n")
			_file.write("database: curso")
			_file.close()
		finally:
			_file = open('system.config', "+r")
			config = {}
			for _line in _file.readlines():
				_tmp = _line.replace("\n","").replace(" ","").split(":")
				config[_tmp[0]] = _tmp[1]
			self.___connection	= mysql.connector.connect(host=config["host"], user=config["user"], password=config["password"], database=config["database"])
			self.___db			= config["database"]
			_file.close()

	def cr(self):
		return self.___connection.cursor()

	def database(self):
		return self.___db

	def commit(self):
		if self.___connection:
			self.___connection.commit()
			return True
		else:
			return False
	def close(self):
		if self.___connection:
			self.___connection.close()
			return True
		else:
			return False
