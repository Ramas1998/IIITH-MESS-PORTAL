import sqlite3 as sql
import datetime



def datewise_pie(date):
	date=date.split("-")

	day=date[2]
	month=date[1]
	year=date[0]
	try:
		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			query="select breakfast, count(*) from meal_registration where day=" + day + " and month=" + month + " and year=" + year + " GROUP BY breakfast"
			cur.execute(query)
			breakfast = cur.fetchall()
			

			con.row_factory = sql.Row
			cur = con.cursor()
			query="select lunch, count(*) from meal_registration where day=" + day + " and month=" + month + " and year=" + year + " GROUP BY lunch"
			cur.execute(query)
			lunch = cur.fetchall()
			

			con.row_factory = sql.Row
			cur = con.cursor()
			query="select dinner, count(*) from meal_registration where day=" + day + " and month=" + month + " and year=" + year + " GROUP BY dinner"
			cur.execute(query)
			dinner = cur.fetchall()

			ldict={}
			bdict={}
			ddict={}

			for i in breakfast:
				bdict[i[0]]=i[1]
			for i in lunch:
				ldict[i[0]]=i[1]
			for i in dinner:
				ddict[i[0]]=i[1]

			return bdict, ldict, ddict


	except:
		print( "connection datewise_pie fail")
		return "connection datewise_piefail "

def monthwise_pie(month):
	try:
		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			query="select breakfast, count(*) from meal_registration where month=" + month + " GROUP BY breakfast"
			cur.execute(query)
			breakfast = cur.fetchall()
			

			con.row_factory = sql.Row
			cur = con.cursor()
			query="select lunch, count(*) from meal_registration where month=" + month +" GROUP BY lunch"
			cur.execute(query)
			lunch = cur.fetchall()
			

			con.row_factory = sql.Row
			cur = con.cursor()
			query="select dinner, count(*) from meal_registration where month=" + month + " GROUP BY dinner"
			cur.execute(query)
			dinner = cur.fetchall()


			ldict={}
			bdict={}
			ddict={}

			for i in breakfast:
				bdict[i[0]]=i[1]
			for i in lunch:
				ldict[i[0]]=i[1]
			for i in dinner:
				ddict[i[0]]=i[1]

			return bdict, ldict, ddict


	except:
		print( "connection monthwise_pie fail")
		return "connection monthwise_piefail "

def daywise_line():
	try:
		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			query="select breakfast, count(*) from meal_registration where dayname='" + day + "' GROUP BY breakfast"
			cur.execute(query)
			breakfast = cur.fetchall()
			

			con.row_factory = sql.Row
			cur = con.cursor()
			query="select lunch, count(*) from meal_registration where dayname='" + day + "' GROUP BY lunch"
			cur.execute(query)
			lunch = cur.fetchall()
			

			con.row_factory = sql.Row
			cur = con.cursor()
			query="select dinner, count(*) from meal_registration where dayname='" + day + "' GROUP BY dinner"
			cur.execute(query)
			dinner = cur.fetchall()

			print( breakfast, lunch, dinner)

	except:
		print( "connection daywise_line fail")
		return "connection daywise_linefail "

def monthwise_line(month):
	try:
		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			query="select breakfast, count(*) from meal_registration where month=" + month + " GROUP BY breakfast"
			cur.execute(query)
			breakfast = cur.fetchall()
			

			con.row_factory = sql.Row
			cur = con.cursor()
			query="select lunch, count(*) from meal_registration where month=" + month +" GROUP BY lunch"
			cur.execute(query)
			lunch = cur.fetchall()
			

			con.row_factory = sql.Row
			cur = con.cursor()
			query="select dinner, count(*) from meal_registration where month=" + month + " GROUP BY dinner"
			cur.execute(query)
			dinner = cur.fetchall()


			print( breakfast, lunch, dinner)

	except:
		print( "connection monthwise_linefail")
		return "connection monthwise_linefail "