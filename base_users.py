#!/usr/bin/python
# -*- coding: utf-8 -*-
from base_base import *
import hashlib

class base_users(base_base):
	_name 		= 'base.users'
	_columns 	= (
		{'name': 'name', 'type':'varchar', 'size': 50, 'default': 'User', 'Null': False, 'desc': 'Nombre del usuario'},
		{'name': 'age', 'type':'int', 'Null': True, 'desc': 'Edad del usuario'},
		{'name': 'email', 'type':'varchar', 'size': 60, 'Null': False, 'desc': 'Correo del usuario', 'default':'correo@correo.com'},
	)

	def create(self, conn, data, context={}):
		if 'passw' in data.keys():
			h = hashlib.new("md5", data['passw'])
			data['passw'] = h.hexdigest()
		super(base_users, self).create(conn, data, context)

	def update(self, conn, ids, data, context={}):
		if 'passw' in data.keys():
			h = hashlib.new("md5", data['passw'])
			data['passw'] = h.hexdigest()
		super(base_users, self).update(conn, ids, data, context)


base = base_users()
base.check_table(1)
