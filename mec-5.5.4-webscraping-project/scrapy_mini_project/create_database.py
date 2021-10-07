import sqlite3
from sqlite3 import Error
import sys
import json

def create_connection(db_file):
	conn = None
	try:
		conn = sqlite3.connect(db_file)
		print(sqlite3.version)
	except Error as e:
		print(e)
		sys.exit(-1)

	return conn


def create_quote_table(conn):
	sql = '''
		CREATE TABLE IF NOT EXISTS quotes (
			id integer PRIMARY KEY,
			quot text NOT NULL,
			auth text NOT NULL,
			tags text NOT NULL
		);
	'''

	try:
		c = conn.cursor()
		c.execute(sql)
	except Error as e:
		print(e)
		sys.exit(-1)

def create_author_table(conn):
	sql = '''
		CREATE TABLE IF NOT EXISTS authors (
			id integer PRIMARY KEY,
			auth text NOT NULL,
			bday text NOT NULL,
			orig text NOT NULL,
			desc text NOT NULL
		);
	'''

	try:
		c = conn.cursor()
		c.execute(sql)
	except Error as e:
		print(e)
		sys.exit(-1)


def insert_quote(conn, quote, author, tags):
	sql = '''
		INSERT INTO quotes(quot,auth,tags)
			VALUES(?,?,?)
	'''

	curr = conn.cursor()
	curr.execute(sql, (quote, author, tags))
	conn.commit()


def insert_author(conn, author, birthday, origin, description):
	sql = '''
		INSERT INTO authors(auth,bday,orig,desc)
			VALUES(?,?,?,?)
	'''

	curr = conn.cursor()
	curr.execute(sql, (author, birthday, origin, description))
	conn.commit()


def read_quotes(conn):
	with open('toscrape-css.json', 'r') as f:
		data = json.loads(f.read())

		for thing in data:

			if 'auth' in thing and 'bday' in thing and 'from' in thing:
				author = thing['auth'].strip()
				birthday = thing['bday'].strip()
				origin = thing['from'].strip()
				description = thing['desc'].strip()

				insert_author(conn, author, birthday, origin, description)

				#print(author)
				#print(birthday)
				#print()

			elif 'quot' in thing:
				quote = thing['quot'].strip()
				author = thing['auth'].strip()
				tags = ','.join(t.strip() for t in thing['tags'])

				insert_quote(conn, quote, author, tags)
				#print(quote)
				#print(author)
				#print(tags)
				#print()




def init_sql():
	conn = create_connection('quotes.db')

	create_quote_table(conn)
	create_author_table(conn)


	insert_quote(
		conn, 
		"a test quote", 
		"important person", 
		"insightful,funny,humor"
	)

	insert_author(
		conn,
		"important person",
		"1970-1-1",
		"USA",
		"contributed to the plight of mankind",
	)
	return conn


read_quotes(init_sql())
