import sqlite3 as sql
import json
from . import model
import datetime
import bcrypt
import smtplib
from app import app
from flask import session


def authenticate_student(request):

	# server = smtplib.SMTP('smtp.gmail.com', 587)
	# print( "fine 1"
	# server.starttls()
	# print( "fine 2"
	# #Next, log in to the server
	# server.login("anuragcodejam@gmail.com", "MyIcici@06")

	# #Send the mail
	# mesg = "hello"
	# print( "fine 3"
	# server.sendmail("anuragcodejam@gmail.com", "anurag.chaturvedi@students.iiit.ac.in", mesg)
	# print( "fine 4"
	# server.quit()

	print( "in authenticate student : ")
	msg={}
	dynamic_salt=""
	hashed=""
	try:
		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			
			# query_args = [request.form['email'],]
			# print( query_args
			# cur.execute("select * from student_profile where email='" + request.form['email'] + "'")
			
			# row = cur.fetchone()

			# if(len(row)>0):
			# 	dynamic_salt = row[7]
			# 	hashed = row[8]
			# else:
			# 	raise ValueError('')

			# print( "cur execute 1"
			# static_salt=app.static_salt
			# print( "cur execute 2"
			# password = request.form['password']
			# print( "cur execute 3"
			# salted_password = static_salt + password
			# print( "cur execute 4"
			# calculated_hashed = bcrypt.hashpw(salted_password, dynamic_salt)
			# print( "calculated_hashed : ", calculated_hashed
			# print( "hashed : ", hashed 

			query_args = [request.form['email'], request.form['password']]
			print( query_args)
			cur.execute("select * from student_profile where (email=? and password=?)", query_args)
			
			row = cur.fetchone()
			# if(calculated_hashed == hashed):
			if(len(row) > 0):
				roll_no = row[0]
				msg["roll_no"]=roll_no
				msg["name"]=row[1]
				msg["authenticate"]=True

				if(row[4] == "NA"):
					msg["first_login"] = True
					return msg
				else:
					msg["first_login"] = False
				
				
				meals = model.get_meal_registration_for_month(roll_no, datetime.datetime.now().month, datetime.datetime.now().year)

				msg["breakfast"]=meals["breakfast"]
				msg["lunch"]=meals["lunch"]
				msg["dinner"]=meals["dinner"]
				msg["bcancel"]=meals["bcancel"]
				msg["lcancel"]=meals["lcancel"]
				msg["dcancel"]=meals["dcancel"]

	except:
		print( "connection fails authenticate_student")
		msg["authenticate"]=False
	return msg

def authenticate_admin(request):
	print( "in authenticate admin : ")
	msg={}
	dynamic_salt=""
	hashed=""
	try:
		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			
			# query_args = [request.form['email'],]
			# print( query_args
			# cur.execute("select * from student_profile where email='" + request.form['email'] + "'")
			
			# row = cur.fetchone()

			# if(len(row)>0):
			# 	dynamic_salt = row[7]
			# 	hashed = row[8]
			# else:
			# 	raise ValueError('')

			# print( "cur execute 1"
			# static_salt=app.static_salt
			# print( "cur execute 2"
			# password = request.form['password']
			# print( "cur execute 3"
			# salted_password = static_salt + password
			# print( "cur execute 4"
			# calculated_hashed = bcrypt.hashpw(salted_password, dynamic_salt)
			# print( "calculated_hashed : ", calculated_hashed
			# print( "hashed : ", hashed 

			query_args = [request.form['email'], request.form['password']]
			print( query_args)
			cur.execute("select * from admin_profile where (email=? and password=?)", query_args)
			
			row = cur.fetchone()
			# if(calculated_hashed == hashed):
			if(len(row) > 0):
				
				msg["admin_id"]=row[0]
				msg["name"]=row[1]
				msg["authenticate"]=True
				msg["mess"] = row[3]
				msg["name"] = row[4]

	except:
		print( "connection fails authenticate_student")
		msg["authenticate"]=False
	return msg

def next_month(roll_no, month, year):
	msg={}
	
	try:
		with sql.connect("mess_portal.db") as con:
			meals = model.get_meal_registration_for_month(roll_no, month, year)
			msg["breakfast"]=meals["breakfast"]
			msg["lunch"]=meals["lunch"]
			msg["dinner"]=meals["dinner"]
			msg["bcancel"]=meals["bcancel"]
			msg["lcancel"]=meals["lcancel"]
			msg["dcancel"]=meals["dcancel"]
	except:
		print( "connection fails next_month")
		msg["authenticate"]=False
	return msg

