#!/usr/bin/python
from base_base import *

class base_contacts(base_base):
	_name 	= 'base.contacts'
	_columns 	= (
		{'name': 'name', 'type':'varchar', 'size': 50, 'default': 'User', 'Null': False, 'desc': 'Nombre del usuario'},
		{'name': 'phone', 'type':'varchar', 'size': 15, 'Null': True, 'desc': 'Telefono del usuario'},
		{'name': 'cell', 'type':'varchar', 'size': 15, 'Null': True, 'desc': 'Celular del usuario'},
		{'name': 'age', 'type':'int', 'Null': True, 'desc': 'Edad del usuario'},
		{'name': 'email', 'type':'varchar', 'size': 60, 'Null': False, 'desc': 'Correo del usuario', 'default':'correo@correo.com'},
	)

base = base_contacts()
base.check_table(1)
