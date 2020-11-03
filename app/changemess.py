import sqlite3 as sql
import datetime
from datetime import timedelta, date

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def set_default_mess(roll_no, default_breakfast_mess, default_lunch_mess, default_dinner_mess):
	flag = False
	try:
		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			query = "update student_profile set default_breakfast='" + default_breakfast_mess +"', default_lunch ='" + default_lunch_mess +"', default_dinner =' " + default_dinner_mess +"' where roll_no =" + str(roll_no)
			cur.execute(query)
			flag = True
	except:
		flag = False

	if flag == True:
		set_default_mess_all_for_student(roll_no, default_breakfast_mess, default_lunch_mess, default_dinner_mess)
		return "success"
	else:
		return "failure"

def set_default_mess_all_for_student(roll_no, default_breakfast, default_lunch, default_dinner):
	start_date = date(2018, 8, 1)
	end_date = date(2019, 7, 1)
	try:
		print( start_date)
		print( end_date)
		with sql.connect("mess_portal.db") as con:
			
			for single_date in daterange(start_date, end_date):
				con.row_factory = sql.Row
				cur = con.cursor()
				d = single_date.strftime("%Y-%m-%d")
				dates = d.split('-')
				dates[2]=dates[2].lstrip("0")
				dates[1]=dates[1].lstrip("0")
				print( dates[1])
				print( dates[2])

				day = single_date.strftime("%A")
				print( "fineee")
				print( day)
				query = "insert into meal_registration values ('" + str(roll_no) + "', '" + str(dates[2]) + "', '" + str(dates[1]) +"', '" + str(dates[0]) + "','" + str(default_breakfast) +"', '" + str(default_lunch) +"', '" + str(default_dinner) +"', '0', '0', '0', '" + str(day) + "')"
				print( query)
				cur.execute(query)
			
			con.commit()
	except:
		print( "wwweee error")


def daywisemesschange(roll_no, meal, mess, day):

	now = datetime.datetime.now()
	start_day=now.day+1
	start_month=now.month
	start_year=now.year
	end_day=start_day+7
	end_month=now.month
	end_year=now.year					
	
	try:
		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			print( "fineee")
			query="UPDATE meal_registration SET bbit ='0'," + meal + " = "+"'"+ mess +"'"+" WHERE (roll_no="+str(roll_no)+" and dayname="+"'"+str(day)+"'"+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
			print( query)
			cur.execute(query)
			con.commit()
	except:
		print( "wwweee error")
