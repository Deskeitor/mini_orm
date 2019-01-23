#!/usr/bin/python
from conexion import *
import datetime
from base_fields import *

class base_base(object):
	_name 		= 'base.base'

	def __init__(self, **arg):
		self._table = type(self).__name__
		self.check_table(1)

	def show_name(self, context={}):
		print(  self._name)
		print(  type(self).__name__)


	def check_table(self, uid, context={}):
		base_field = base_fields()
		if not self._columns:
			raise Exception('Error!', "Columns are necessary to ORM")
		_sql 	= "SELECT table_name FROM information_schema.tables WHERE table_schema = '{}' AND table_name = '{}';".format("{}",self._table)
		_result	= self.execute(_sql)
		if _result == []:
			base_field.create_database(self._table)

		for _c in self._columns:
			base_field.create_field(_c, self._table)

	def cr(self, conn):
		if not conn:
			raise Exception("Connection must be necessary")
			return False
		else:
			return conn.cr()

	def delete(self, uid, _ids, context={}):
		conn =  Connection()
		cr = self.cr(conn)
		if not _ids:
			return False
		for _id in _ids:
			cr.execute('SELECT * FROM {} WHERE id={}'.format(self._table, _id))
			_exist = cr.fetchall()
			print( _exist)
			if _exist:
				try:
					cr.execute('DELETE FROM {} WHERE id={}'.format(self._table, _id))
				except Exception as e:
					cr.close()
					raise Exception(e)
					return False
			else:
				cr.close()
				conn.close()
				raise Exception('Error', 'ID <{}> not exist in <{}> table'.format(_id, self._table))
				return False
		conn.commit()
		cr.close()
		conn.close()
		return True

	def search(self, uid, conditions=None, context={},limit=None, offset=None):
		conn =  Connection()
		cr = self.cr(conn)
		_cond_to_get = ''
		if not conditions or not cr:
			raise Exception('Error', 'Conditions and crare necessary')

		if type(conditions) is list:
			for _c in conditions:
				if type(_c) is not tuple:
					raise Exception('Error', 'Conditions muts be tuples')
				if _c[1].upper() == 'LIKE':
					_cond_to_get += "{} LIKE '%{}%' AND ".format(_c[0], _c[2])
				else:
					_cond_to_get += '{} {} "{}" AND '.format(_c[0], _c[1], _c[2])
			_cond_to_get = _cond_to_get[:-5]
		elif conditions==1:
			_cond_to_get += str(conditions)
		else:
			cr.close()
			conn.close()
			raise Exception('Error', 'Is not list')

		_all = []

		if limit and offset:
			sql = "SELECT id FROM {} WHERE {} LIMIT {} OFFSET {}".format(self._table, _cond_to_get ,limit, offset)
		elif limit:
			sql = "SELECT id FROM {} WHERE {} LIMIT {}".format(self._table, _cond_to_get, limit)
		else:
			sql = "SELECT id FROM {} WHERE {}".format(self._table, _cond_to_get)

		cr.execute(sql)
		for _data in cr.fetchall():
			_all.append(int(_data[0]))
		conn.commit()
		cr.close()
		conn.close()
		return _all

	def browse(self, uid, ids, context={}, fields=None,limit=None, offset=None):
		conn =  Connection()
		cr = self.cr(conn)
		_fields_to_get = ''
		if not fields:
			_fields_to_get = '*'
		elif type(fields) is list:
			for _f in fields:
				_fields_to_get += str(_f) + ', '
			_fields_to_get = _fields_to_get[:-2]
		else:
			cr.close()
			conn.close()
			raise Exception('Error', 'Is not list')
		if not ids or not cr:
			raise Exception('Error', 'Ids and cr are necessary')


		_fields = []
		_all = []
		sql = "SELECT {} FROM {}".format(_fields_to_get,self._table)
		cr.execute(sql)
		for field in cr.description:
			_fields.append(field[0])

		for _id in ids:
			if limit and offset:
				sql = "SELECT {} FROM {} WHERE id={} LIMIT {} OFFSET {}".format(_fields_to_get, self._table, _id, limit, offset)
			elif limit:
				sql = "SELECT {} FROM {} WHERE id={} LIMIT {}".format(_fields_to_get, self._table, _id, limit)
			else:
				sql = "SELECT {} FROM {} WHERE id={}".format(_fields_to_get, self._table, _id)

			cr.execute(sql)
			for _data in cr.fetchall():
				obj 	= base_base()
				for x, _d in enumerate(_data):
					if type(_d) is datetime.datetime:
						_d = _d.strftime('%d/%m/%Y %H:%M:%S')
					if type(_d) is long:
						_d = int(_d)
					setattr(obj, _fields[x], _d)
				_all.append(obj)
		conn.commit()
		cr.close()
		conn.close()
		return _all

	def create(self, uid, data, context={}):
		conn =  Connection()
		cr = self.cr(conn)
		if not data or not conn:
			raise Exception("Data and Connection are necessary")

		if type(data) is not dict:
			raise Exception("Data must be a dictionary")

		now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		_columns 	= 'create_uid, create_date, write_uid, write_date'
		_values		= '"{}", "{}", "{}", "{}"'.format(uid, now, uid, now)
		for _key in data.keys():
			_columns	+= ', {}'.format(_key)
			_values		+= ', "{}"'.format(data[_key])
		sql = 'INSERT INTO {} ( {} ) VALUES ( {} )'.format(self._table,_columns, _values)

		cr.execute(sql)
		_create_id = cr.lastrowid
		if cr.lastrowid:
			print( 'Insert record in {} with ID: {}'.format(self._table, cr.lastrowid))
		else:
			raise Exception('Error, register not Inserted')
		conn.commit()
		cr.close()
		conn.close()
		return _create_id

	def update(self, uid, ids, data, context={}):
		conn =  Connection()
		cr = self.cr(conn)
		if not data or not conn or not ids:
			raise Exception("Data, IDS and Connection are necessary")

		if type(data) is not dict:
			raise Exception("Data must be a dictionary")

		now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		_values 	= 'write_uid="{}", write_date="{}"'.format(uid, now)
		for _key in data.keys():
			_values		+= ', {}="{}"'.format(_key, data[_key])

		for _id in ids:
			try:
				sql = 'UPDATE {} SET {} WHERE id={}'.format(self._table, _values, _id)
				cr.execute(sql)
				conn.commit()
			except Exception as e:
				raise Exception(e)
				return False

		cr.close()
		conn.close()
		return True

	def execute(self, _sql, context={}):
		if not _sql:
			raise Exception('Error!','SQL sentence are necessary')
			return False
		conn 	=  Connection()
		cr 		= conn.cr()

		_sql = _sql.format(conn.database())
		cr.execute(_sql)
		_result = cr.fetchall()

		conn.close()
		cr.close()

		return _result
