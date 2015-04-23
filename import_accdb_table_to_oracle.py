# -*- coding: utf-8 -*-
# Author: Vika Zhou
# Date: 2015/04/23

import cx_Oracle
import pypyodbc
pypyodbc.lowercase = False

DB_USER = 'xx'
DB_PASSWORD = 'xx'
DB_CONN_URL = 'xx'

def create_acccdb_connect(accdb_file):
    conn = pypyodbc.connect(
        r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};' +
        r'Dbq=' + accdb_file + ';')
    return conn

def show_tables(accdb_file, ttype='ALL'):
    conn = create_acccdb_connect(accdb_file)
    cur = conn.cursor()
    cur.tables()
    # print cur.description
    while True:
        row = cur.fetchone()
        if row is None:
            break
        if ttype == 'ALL' or ttype == row[3]:
            # TABLE or VIEW
            print('Table: {0}\n\t{1}\n\t{2}'.format(row[2], row[3], row[4]))
    cur.close()
    conn.close()

def conv_identity(name):
    return name.replace(' ', '_').replace('-', '_').upper()

def conv_acol_sql(column):
    type_map = {'VARCHAR':'VARCHAR2',
                'BIT': 'NUMBER',
                'COUNTER': 'NUMBER',
                'DATETIME': 'DATE'
                }
    no_size = ['DATE']
    column_name = conv_identity(column.get('COLUMN_NAME'))
    type_name = type_map.get(column.get('TYPE_NAME'), column.get('TYPE_NAME'))
    if type_name in no_size:
        return '{} {}'.format(column_name, type_name)
    else:
        return '{} {}({})'.format(column_name, type_name, column.get('COLUMN_SIZE'))

def gen_create_sql(table_name, columns):
    table_name = conv_identity(table_name)
    sql_columns = [conv_acol_sql(c) for c in columns]
    return 'CREATE TABLE {}(\n\t{}\n)\n'.format(table_name, ',\n\t'.join(sql_columns))

def gen_insert_sql(table_name, columns):
    table_name = conv_identity(table_name)
    column_names = [conv_identity(c.get('COLUMN_NAME')) for c in columns]
    return 'INSERT INTO {}({})\nVALUES({})\n'.format(table_name,
            ', '.join(column_names),
            ', '.join([':' + str(i) for i in range(1, len(column_names) + 1)]))
    
def show_table_columns(accdb_file, table, show_create=False, show_insert=False):
    conn = create_acccdb_connect(accdb_file)
    cur = conn.cursor()
    cur.columns(table)
    # print cur.description
    print('COLUMN_NAME\tDATA_TYPE\tTYPE_NAME\tCOLUMN_SIZE\tSQL_DATA_TYPE\tSQL_DATETIME_SUB')
    columns = []
    while True:
        row = cur.fetchone()
        if row is None:
            break
        columns.append(row)
        print('{}\t{}\t{}\t{}\t{}\t{}'.format(row.get('COLUMN_NAME'),
                row.get('DATA_TYPE'),
                row.get('TYPE_NAME'),
                row.get('COLUMN_SIZE'),
                row.get('SQL_DATA_TYPE'),
                row.get('SQL_DATETIME_SUB')))
    if show_create:
        print('Create Table:')
        print(gen_create_sql(table, columns))
    if show_insert:
        print('Insert:')
        print(gen_insert_sql(table, columns))
    cur.close()
    conn.close()

def import_accdb_table(accdb_file, table):
    db_conn = cx_Oracle.connect(DB_USER, DB_PASSWORD, DB_CONN_URL)
    db_cursor = db_conn.cursor()
    
    acc_conn = create_acccdb_connect(accdb_file)
    acc_cur = acc_conn.cursor()
    acc_cur.columns(table)
    acc_columns = acc_cur.fetchall()
    acc_column_names = [c.get('COLUMN_NAME') for c in acc_columns]
    # create table
    try:
        db_cursor.execute(gen_create_sql(table, acc_columns))
    except cx_Oracle.DatabaseError as e:
        if 'ORA-00955' in str(e):
            print(e)
            print('Skip Create Table for [{}]'.format(table))
        else:
            raise e

    # import data
    insert_sql = gen_insert_sql(table, acc_columns)
    acc_cur.execute('SELECT * FROM [{}]'.format(table))
    while True:
        row = acc_cur.fetchone()
        if row is None:
            break
        insert_values = [row.get(col) for col in acc_column_names]
        db_cursor.execute(insert_sql, insert_values)
    db_conn.commit()
    
    db_cursor.close()
    db_conn.close()
    acc_cur.close()
    acc_conn.close()
