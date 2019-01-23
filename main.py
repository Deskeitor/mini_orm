#!/usr/bin/python
# -*- coding: utf-8 -*-
from conexion import *
from base_contacts import *
from base_users import *
from base_levels import *
import hashlib
import getpass
import os

def usuarios(conn, uid, context={}):
	os.system("clear")
	users = base_users()
	opcion 		= None
	while opcion != "0":
		os.system("clear")
		opcion = input("Que deseas hacer??\n\
	1. Ver\n\
	2. Crear\n\
	0. Regresar\n")
		if opcion == "1":
			opcion_ver = None
			while opcion_ver != "0":
				os.system("clear")
				opcion_ver = input("Que deseas ver??\n\
	1. Todos\n\
	2. Busqueda\n\
	0. Regresar\n")
				if opcion_ver == "1":
					os.system("clear")
					#cr = conn.cr()
					#cr.execute('SELECT id FROM users WHERE 1')
					_ids = users.search(uid, 1 , context)
					#cr.close()
					#conn.close()
					#print (_ids)
					print ("+----+------------------------------+-----------+----------------------+")
					print ("|-ID-|------------Nombre------------|--Usuario--|--Correo electronico--|")
					for _id in _ids:
						_obj = users.browse(uid, [_id], context)[0]
						print ("| 0{} | {} | {} | {} |".format(_obj.id, _obj.name, _obj.user, _obj.email))
					print ("+----+------------------------------+-----------+----------------------+")

					input()
		elif opcion == "2":
			pass
		else:
			print (opcion)
			print (type(opcion))

def main():
	opcion 		= None
	logged		= False
	logged_time	= None
	conn 		= Connection()
	users 		= base_users()
	uid 		= None
	context		= {}
	while not logged:
		os.system("clear")
		user 	= input("Ingresa usuario: ")
		pw 		= getpass.getpass()
		h = hashlib.new("md5", pw.encode('utf-8'))
		uid = users.search(1, [('user','=', user),('passw','=',h.hexdigest())])
		if len(uid) == 1:
			logged_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			logged = True
	context = {'user': users.browse(conn, uid, uid)[0],'logged':logged_time}

	while opcion != "0":
		os.system("clear")
		opcion = input("Bienvenido a mi sistema de usuarios\n\
	Elige una opcion escribiendo el numero de la misma\n\
	1. Usuarios\n\
	2. Niveles\n\
	3. Contactos\n\
	0. Salir\n")
		if opcion == "1":
			usuarios(conn, uid[0], context)
		elif opcion == "2":
			pass
		elif opcion == "3":
			pass
	os.system("clear")
	print ('Gracias por usar este sistema')

main()
