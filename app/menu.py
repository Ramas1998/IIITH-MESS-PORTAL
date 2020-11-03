import sqlite3 as sql

def get_menu_day_wise(meal):
	menus = {}
	s=""
	t=""
	days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
	try:
		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			
			query = "select " + meal + " from yuktahar_menu"
			cur.execute(query)
			rows = cur.fetchall()
			i=0
			s="Yuktahar"
			while i<len(rows):
				t = "" + s + "_" + days[i]
				menus[t] = rows[i][0]
				i=i+1
			
			query = "select " + meal + " from north_menu"
			cur.execute(query)
			rows = cur.fetchall()
			i=0
			s="North"
			while i<len(rows):
				t = "" + s + "_" + days[i]
				menus[t] = rows[i][0]
				i=i+1
			
			query = "select " + meal + " from south_menu"
			cur.execute(query)
			rows = cur.fetchall()
			i=0
			s="South"
			while i<len(rows):
				t = "" + s + "_" + days[i]
				menus[t] = rows[i][0]
				i=i+1
			
			query = "select " + meal + " from kadamba_menu"
			cur.execute(query)
			rows = cur.fetchall()
			i=0
			s="Kadamba"
			while i<len(rows):
				t = "" + s + "_" + days[i]
				menus[t] = rows[i][0]
				i=i+1

	except:
		print ("error")

	return menus

