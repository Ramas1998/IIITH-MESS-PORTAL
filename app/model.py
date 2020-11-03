import sqlite3 as sql
import datetime

def get_meal_registration_for_today(roll_no, day, month, year):
	print( "Hey get_meal_registration for a student")
	try:

		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			query="select * from meal_registration where roll_no=" + str(roll_no) 
			+ " and day=" + day + " and month=" + month + " and year=" + year
			cur.execute(query)
			print( "here **")
			rows = cur.fetchall()
			for row in rows:
				print( "row=",  row)
			return rows
	except:
		print( "connection fails")
		return "connection fails"

def get_meal_registration_for_month(roll_no, month, year):
	print( "Hey get_meal_registration for a student for month")
	try:

		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			print( "roll_no : ", roll_no)
			
			query="select * from meal_registration where roll_no=" + str(roll_no) + " and month=" + str(month) + " and year=" + str(year)
			
			cur.execute(query)
			
			rows = cur.fetchall()
			breakfast = {}
			lunch = {}
			dinner = {}
			bcancel = {}
			lcancel = {}
			dcancel = {}
			i=0
			obj={}
			print( "print(ing rows")
			for row in rows:

				breakfast[i]=row[4]
				lunch[i]=row[5]
				dinner[i]=row[6]
				bcancel[i]=row[7]
				lcancel[i]=row[8]
				dcancel[i]=row[9]
				i=i+1
			obj["breakfast"]=breakfast
			obj["lunch"]=lunch
			obj["dinner"]=dinner
			obj["bcancel"]=bcancel
			obj["lcancel"]=lcancel
			obj["dcancel"]=dcancel
			return obj
	except:
		print( "connection fails get_meal_registration_for_month")
		return "connection fails get_meal_registration_for_month"

def get_mess_menu(breakfast, lunch, dinner, day):

	print( "inside model get_mess_menu")
	menu={}

	breakfast = breakfast.lower()
	lunch = lunch.lower()
	dinner = dinner.lower()

	print( breakfast)
	print( lunch)
	print( dinner)
	print( day)

	try:
		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			query="select breakfast from " + breakfast + "_menu " + "where day='" + day + "'"
			cur.execute(query)
			rows = cur.fetchall()
			menu["breakfast_menu"] = rows[0][0]

			query="select lunch from " + lunch + "_menu " + "where day='" + day + "'"
			cur.execute(query)
			rows = cur.fetchall()
			menu["lunch_menu"] = rows[0][0]

			query="select dinner from " + dinner + "_menu " + "where day='" + day + "'"
			cur.execute(query)
			rows = cur.fetchall()
			menu["dinner_menu"] = rows[0][0]

	except:
		print( "connection fails get_mess_menu")
		return "connection fails get_mess_menu"
	return menu

def get_meal_menu(meal, day,bname):

	print( "inside model get_mess_menu")
	menu={}

	try:
		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			now = datetime.datetime.now()
			hours=now.hour

			date = datetime.datetime.now().day
			month = datetime.datetime.now().month
			year = datetime.datetime.now().year
			print( "Welcome to my page")
			if(hours>=22 and hours<=23):
			      	date+=1

			if(hours>=10 and hours<=14):
				if(bname=="menuIII"):
			      	    date=date+1  

			if(hours>=15 and hours<=21):
				if(bname=="menuII"):
				     date=date+1

				if(bname=="menuIII"):
				    date=date+1  
  	     

			query="select "+ meal +" from  meal_registration where day=" + str(date) + " and month=" + str(month) + " and year=" + str(year)

			print( query)
			cur.execute(query)
			rows = cur.fetchall()
			mess = rows[0][0]
			print( mess)

			query="select "+ meal +" from " + mess + "_menu " + "where day='" + day + "'"
			cur.execute(query)
			rows = cur.fetchall()
			menu["meal_menu"] = rows[0][0]
			menu["mess"] = mess
			print( menu)

	except:
		print( "connection fails get_mess_menu")
		return "connection fails get_mess_menu"
	return menu


def change_menu(mess,day,meal,newmenu):
	try:
		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			print( "this query")
			query="update "+ mess +" set "+meal+"='" + newmenu + "' where day = '" + day+"'";
			print( query)
			cur.execute(query)
			

	except:
		print( "connection fails change_menu")
		return "connection fails change_menu"

def change_default_mess(student_rollno,default_breakfast_mess,default_lunch_mess,default_dinner_mess):
	try:
		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			print( "this query")
			query="update "+ "student_profile" +" set default_breakfast='"+default_breakfast_mess+"', default_lunch='"+default_lunch_mess+"', default_dinner='"+default_dinner_mess+"' where roll_no = "+ student_rollno

			print( query)
			cur.execute(query)
			

	except:
		print( "connection fails change_default_mess")
		return "connection fails change_default_mess"

def generatereport(name,day,month,year):
	try:
		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			query="select roll_no from meal_registration where day='"+day+"' and month='"+month+"' and year='"+year+"' and breakfast='"+name+"'" 
			cur.execute(query)
			breakfast=(cur.fetchall())
			
			con.row_factory = sql.Row
			cur = con.cursor()
			query="select roll_no from meal_registration where day="+day+" and month="+month+" and year="+year+" and lunch='"+name+"'" 
			cur.execute(query)
			lunch=(cur.fetchall())
			
			con.row_factory = sql.Row
			cur = con.cursor()
			query="select roll_no from meal_registration where day="+day+" and month="+month+" and year="+year+" and dinner='"+name+"'" 
			cur.execute(query)
			dinner=(cur.fetchall())
			
			breakfast_data=[]
			lunch_data=[]
			dinner_data=[]

			for i in breakfast:
				breakfast_data.append(str(i[0]))
			for i in lunch:
				lunch_data.append(str(i[0]))
			for i in dinner:
				dinner_data.append(str(i[0]))

			print( breakfast_data)
			print( lunch_data)
			print( dinner_data)

			return breakfast_data,lunch_data,dinner_data

	except:
		print( "connection fails generatereport")
		return "connection fails generatereport"

def getdefaultmess(roll):

	try:
		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			query="select default_breakfast, default_lunch, default_dinner from student_profile where roll_no='"+str(roll)+"'"
			cur.execute(query)
			breakfast=(cur.fetchall())
			
			return breakfast[0][0], breakfast[0][1], breakfast[0][2]

	except:
		print( "connection fails getdefaultmess")
		return "connection fails getdefaultmess"


def get_bill_details(roll_no,month,year):
	try:
		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			print( "roll_no : ", roll_no)
			query="select * from bill where roll_no=" + str(roll_no)
			cur.execute(query)
			rows = cur.fetchall()
			# print( rows
			if month<7:
				year=year-1
			obj={}
			temp=[roll_no,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
			month_inc=[]
			for row in rows:
				if((row["month"]>6 and row["year"]==year) or (row["month"]<7 and row["year"]==year+1)):
					obj[row["month"]-1]=list(row)
					month_inc.append(row["month"])
			for i in range(1,13):
				if i not in month_inc:
					if(i>6):
						temp=[roll_no,0,year,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
					else:
						temp=[roll_no,0,year+1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
					obj[i-1]=temp
			return obj
	except:
		print( "connection fails get_bill_details")
		return

def calculate_bill(roll_no):
	month = datetime.datetime.now().month
	year = datetime.datetime.now().year
	if month == 1:
		month = 12
		year = year - 1 
	else:
		month = month - 1
	meals = get_meal_registration_for_month(roll_no, month, year)
	can = get_cancellations()
	rates = get_rates()
	can = can[month-1]
	bill = 0
	bcancel = lcancel = dcancel = 0
	sb = sl = sd = nb = nl = nd = kvl = kvb = kvd = yb = yl = yd = knb = knl = knd = bc = lc = dc = 0 
	data=meals["breakfast"]
	cancel=meals["bcancel"]
	for x in data:
		if cancel[x]=='1' and bcancel<=can[1]:
			bcancel = bcancel +1
		else:
			if data[x] == 'North':
				bill = bill + rates['North'][1]
				nb+=1
			elif data[x] == 'South':
				bill = bill + rates['South'][1]
				sb+=1
			elif data[x] == 'Yuktahar':
				bill = bill + rates['Yuktahar'][1]
				yb+=1
			elif data[x] == 'Kadamba':
				bill = bill + rates['Kadamb-V'][1]
				kvb+=1
			elif data[x] == 'Kadamba-NV':
				bill = bill + rates['Kadamb-NV'][1]
				knb+=1
		if cancel[x] == '1':
			bc = bc + 1
	
	data=meals["lunch"]
	cancel=meals["lcancel"]
	for x in data:
		if cancel[x]=='1' and lcancel<=can[2]:
			lcancel = lcancel +1
		else:
			if data[x] == 'North':
				bill = bill + rates['North'][2]
				nl+=1
			elif data[x] == 'South':
				bill = bill + rates['South'][2]
				sl+=1
			elif data[x] == 'Yuktahar':
				bill = bill + rates['Yuktahar'][2]
				yl+=1
			elif data[x] == 'Kadamba':
				bill = bill + rates['Kadamb-V'][2]
				kvl+=1
			elif data[x] == 'Kadamba-NV':
				bill = bill + rates['Kadamb-NV'][2]
				knl+=1
		if cancel[x] == '1':
			lc = lc + 1
	
	data=meals["dinner"]
	cancel=meals["dcancel"]
	for x in data:
		if cancel[x]=='1' and dcancel<=can[3]:
			dcancel = dcancel +1
		else:
			if data[x] == 'North':
				bill = bill + rates['North'][3]
				nd+=1
			elif data[x] == 'South':
				bill = bill + rates['South'][3]
				sd+=1
			elif data[x] == 'Yuktahar':
				bill = bill + rates['Yuktahar'][3]
				yd+=1
			elif data[x] == 'Kadamba':
				bill = bill + rates['Kadamb-V'][3]
				kvd+=1
			elif data[x] == 'Kadamba-NV':
				bill = bill + rates['Kadamb-NV'][3]
				knd+=1
		if cancel[x] == '1':
			dc = dc + 1
	args = [roll_no,month,year,sb,sl,sd,nb,nl,nd,yb,yl,yd,kvb,kvl,kvd,knb,knl,knd,bc,lc,dc,bill]
	print( roll_no)
	comm = ""
	for i in args:
		comm = comm + str(i) + ","
	comm = comm[:-1]
	try:
		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			comm = "insert into bill values (" + comm + ")"
			cur.execute(comm)
	except:
		print( "Insertion Fails..")
	return

def get_cancellations():
	try:
		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			query="select * from cancellations"
			cur.execute(query)
			rows = cur.fetchall()
			obj={}
			for row in rows:
				obj[row[0]-1]=list(row)
			return obj
	except:
		print( "connection fails get_cancellations")
		return

def get_rates():
	try:
		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			query="select * from meal_rates"
			cur.execute(query)
			rows = cur.fetchall()
			obj={}
			for row in rows:
				obj[row[0]]=list(row)
			return obj
	except:
		print( "connection fails get_cancellations")
		return

def populatelist(filter):
	try:
		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			query="select roll_no, name, email, default_breakfast, default_lunch, default_dinner from student_profile where roll_no LIKE '"+filter+"%' or UPPER(name) LIKE UPPER('%"+filter+"%')"           
			print( query)
			cur.execute(query)
			data=(cur.fetchall())
			data_list=[]

			for i in data:
				data_list.append(list(i))


			return data_list;

	except:
		print( "connection fails getdefaultmess")
		return "connection fails getdefaultmess"
	
def show_feedback():
	try:
		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			query="select * from feedbacks"
			cur.execute(query)
			rows = cur.fetchall()
			obj={}
			for i in range (0,len(rows)):
				obj[i] = list(rows[i])
			print( obj)
			return obj
	except:
		print( "Connection Failed..")
		return "Connection Failed.."

def generate_student_bill():
	try:
		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			query="select roll_no from student_profile"
			cur.execute(query)
			rows = cur.fetchall()

		for i in rows:
			calculate_bill(i[0])	
			
	except:
		print( "Connection Failed..")
		return "Connection Failed.."