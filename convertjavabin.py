#coding: utf8
import sys 
reload(sys) 
sys.setdefaultencoding("utf-8")

import MySQLdb as mdb

DB_HOST = '127.0.0.1'
DB_USER = 'root'
DB_PASS = 'root'
DB_NAME =  'databasename'

def convertjavabin():
	dbconn = mdb.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME, charset='utf8')
	dbcurr = dbconn.cursor()
	tablelistsql = 'SELECT table_name FROM information_schema.tables where table_type="BASE TABLE" AND table_schema="'+DB_NAME+'"'
	dbcurr.execute(tablelistsql)
	items = dbcurr.fetchall()

	for item in items:
		filename = item[0]+'.java'
		f = open(filename, "w")
		startline = 'class    '+item[0]+'    {\r\n'
		f.write(startline)

		try:
			dbcurr.execute('SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = %s', item);
			structlist = dbcurr.fetchall();
			for struct in structlist:
				type = 'String';
				if struct[1].find('int') != -1:
					type = 'int'
				elif struct[1].find('real') != -1:
					type = 'double'
				line = '        public    '+type+'    '+str(struct[0])+';'
				f.write(line)
				f.write('\r\n')

			f.write('}')
			f.close()
		except Exception as e:
			raise
		else:
			pass
		finally:
			pass
	dbcurr.close()
	dbconn.close()

if __name__ == '__main__':
	convertjavabin()


