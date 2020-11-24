#!/usr/bin/python

import sqlite3
from sqlite3 import Error

def connection(DB):
	try:
		conn = sqlite3.connect(DB)
		return conn
	except Error as e:
		print(e)
	return None

def main():
	database = "/home/admin/website/db.sqlite3"
	conn = connection(database)
	with conn:
		cur = conn.cursor()
		cur.execute("SELECT username, password FROM user_profile_airpactuser")
		rows = cur.fetchall()
		for row in rows:
			print("Username = " + row[0])
			print("Password = " + row[1])

if __name__ == '__main__':
	main()
