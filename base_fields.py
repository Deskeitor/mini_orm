#!/usr/bin/python
# -*- coding: utf-8 -*-
from conexion import *

class base_fields(object):
    """docstring for base_fields."""
    def _check_field(self, _field):
        print (_field)

    def create_database(self, _table):
        conn 	=  Connection()
        cr 		= conn.cr()
        _sql    = "CREATE TABLE {}.{} ( `id` INT NOT NULL AUTO_INCREMENT , `create_date` DATETIME NOT NULL , `create_uid` INT NOT NULL , `write_uid` INT NOT NULL , `write_date` DATETIME NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;".format(conn.database(), _table)
        cr.execute(_sql)
        conn.close()
        cr.close()

    def create_field(self, _field, _table):
        conn 	=  Connection()
        cr 		= conn.cr()
        _vals = {
            'default' : "0",
            'size'    : 20,
            'null'    : "NOT NULL",
            'desc'    : '',
            'AI'      : '',
        }

        _sql = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{}' AND COLUMN_NAME = '{}'".format(_table, _field['name'])
        cr.execute(_sql)
        if cr.fetchall() != []:
            return False
        for _f in _field:
            if _f in ['default','size','desc']:
                _vals[_f] = _field[_f]
            elif _f == 'null' and _field[_f]:
                _vals[_f] = 'NULL'
            elif _f == 'AI' and _field[_f]:
                _vals[_f] = 'AUTO_INCREMENT'
        _sql    = "ALTER TABLE {table} ADD {name} {type}({size}) {null} DEFAULT '{default}' {ai} COMMENT '{desc}';".format(
        table=_table, name=_field['name'], type=_field['type'].upper(), null=_vals['null'], ai=_vals['AI'] ,size=_vals['size'], default=_vals['default'], desc=_vals['desc'])
        cr.execute(_sql)
        conn.commit()
        conn.close()
        cr.close()
