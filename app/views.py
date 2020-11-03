from flask import Flask, render_template, request, session
from . import model
from . import login as loginp
import json
import datetime
import sqlite3 as sql
from flask import make_response
from app import app
from . import graphs
from . import menu
from . import changemess

from flask_uploads import UploadSet, configure_uploads, IMAGES
#from flask.ext.uploads import UploadSet, configure_uploads, IMAGES
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'app/static/Images'
configure_uploads(app, photos)

@app.route("/")
def login():
	msg={}
	email = request.cookies.get('email')
	first_login = request.cookies.get('first_login')
	
	if email in session:

		if session["user"] != "student":
			return "Not authorized"
		if first_login == "True":
			session["first_login"] = "True"
			return render_template("set_default_mess.html")
		roll_no = session[email]
		msg["roll_no"] = roll_no
		
		name = request.cookies.get('name')
		msg["name"]=name
		msg["authenticate"]=True
		meals = model.get_meal_registration_for_month(roll_no, datetime.datetime.now().month, datetime.datetime.now().year)

		msg["breakfast"]=meals["breakfast"]
		msg["lunch"]=meals["lunch"]
		msg["dinner"]=meals["dinner"]
		msg["bcancel"]=meals["bcancel"]
		msg["lcancel"]=meals["lcancel"]
		msg["dcancel"]=meals["dcancel"]
		json_obj = json.dumps(msg)
		return render_template("dashboard.html", message=json_obj)
	else:
		return render_template("login.html")

@app.route("/admin")
def login_admin():
	msg={}
	email = request.cookies.get('email')
	
	if email in session:
		if session["user"] != "admin":
			return "Not authorized"
		admin_id = session[email]
		name = request.cookies.get('name')
		msg["name"]=name
		msg["authenticate"]=True
		json_obj = json.dumps(msg)
		return render_template("admin_dashboard.html", message=json_obj)
	else:
		return render_template("login_admin.html")

@app.route("/logout")
def logout():
	email = request.cookies.get('email')
	session.pop(email,None)
	session.pop("name",None)
	if session["user"] == "student":
		session.pop("roll_no",None)
		session.pop("first_login",None)

	session.pop("user",None)
	return render_template("logout.html")

@app.route("/authenticate", methods=['POST'])
def authenticate():
	email = request.form['email']
	msg={}

	if request.method == 'POST':
			
			msg = loginp.authenticate_student(request)

			if msg['authenticate'] == False:
				return render_template('login.html', status=1)
			else:
				
				json_obj = json.dumps(msg)
				
				session[email] = msg["roll_no"]
				session["name"] = msg["name"]
				session["roll_no"] = msg["roll_no"]
				session["user"] = "student"
				roll_no=msg["roll_no"]

				if msg["first_login"] == True:
					print("first login is true")
					session["first_login"] = "True"
					resp = make_response(render_template("set_default_mess.html", message=json_obj))
					resp.set_cookie('first_login', "True")
				else:
					print("first login is false")
					resp = make_response(render_template("dashboard.html", message=json_obj))
					session["first_login"] = "False"
					resp.set_cookie('first_login', "False")
					print("success")
				resp.set_cookie('email', email)
				resp.set_cookie('name', msg["name"])

			return resp

@app.route("/authenticate_admin", methods=['POST'])
def authenticate_admin():
	email = request.form['email']
	msg={}

	if request.method == 'POST':
			
			msg = loginp.authenticate_admin(request)
			
			if msg['authenticate'] == False:
				return render_template('login_admin.html', status=1)
			else:
				
				json_obj = json.dumps(msg)
				
				session[email] = msg["admin_id"]
				session["name"] = msg["name"]
				session["user"] = "admin"
				session["mess"] = msg["mess"]
				
				resp = make_response(render_template("admin_dashboard.html", message=json_obj))

				resp.set_cookie('email', email)
				resp.set_cookie('name', msg["name"])

			return resp

@app.route("/firstlogin", methods=['POST'])
def first_login():
	if not session.get('name'):
		return render_template('login.html')

	email = request.form['email']
	msg={}

	if request.method == 'POST':
			msg = loginp.authenticate_student(request)
			
			if msg['authenticate'] == False:
				return render_template('login.html')
			else:
				
				json_obj = json.dumps(msg)
				
				session[email] = msg["roll_no"]
				session["name"] = msg["name"]
				session["roll_no"] = msg["roll_no"]
				roll_no=msg["roll_no"]

				if msg["first_login"] == True:
					resp = make_response(render_template("set_default_mess.html", message=json_obj))
				else:
					resp = make_response(render_template("dashboard.html", message=json_obj))

				resp.set_cookie('email', email)
				resp.set_cookie('name', msg["name"])

	#return resp
	return ""

@app.route("/nextmonth", methods=['POST'])
def nextmonth():
	msg={}
	email = request.cookies.get('email')
	json_obj = request.form['mydata']
	json_data = json.loads(json_obj)

	if request.method == 'POST':
		
		msg = loginp.next_month(session['roll_no'], int(json_data['month'])+1, int(json_data['year']))
		jso = json.dumps(msg)
		return jso

@app.route("/getmessmenu", methods=['POST'])
def get_mess_menu():
	msg={}
	email = request.cookies.get('email')
	json_obj = request.form['mydata_mess_menu']
	json_data = json.loads(json_obj)
	breakfast = json_data['breakfast']
	lunch = json_data['lunch']
	dinner = json_data['dinner']
	day = json_data['day']
	if request.method == 'POST':
		
		msg = model.get_mess_menu(breakfast, lunch, dinner, day)
		jso = json.dumps(msg)
		return jso

@app.route("/getmealmenu", methods=['POST'])
def get_meal_menu():
	print("getmealmenu")
	msg={}
	email = request.cookies.get('email')
	print()
	print()
	print("**************************************")
	print("email : ", session[email])
	json_obj = request.form['mydata_mess_menu']
	json_data = json.loads(json_obj)
	meal = json_data['meal']
	day = json_data['day']
	button_name= json_data['bname']
	print("in get_meal_menu")
	print(day)
	if request.method == 'POST':
		
		msg = model.get_meal_menu(meal, day,button_name)
		jso = json.dumps(msg)
		return jso


@app.route("/cancelmeals.html")
def cancelmeal():
	if not session.get('name'):
		return render_template('login.html')
	if session["user"] != "student":
		return "Not authorized"
	print("&&&^^%&&&&&&&&&&&&&&&&&&&&&&&&&&&&7")
	print(session)
	if session["first_login"] == "True":
		return render_template("set_default_mess.html")

	return render_template("cancel_meals.html")	

@app.route("/cancelmealstatus", methods=['POST'])
def cancelmealstatus():
	now = datetime.datetime.now()
	hours=now.hour
	curr_day=now.day
	curr_month=now.month
	curr_year=now.year
   
	formdate=request.form['demo']
	datearr=formdate.split('-')
	starting_date=datearr[0]
	ending_date_space=datearr[1].split(' ')
	ending_date=ending_date_space[1]
	start_arr=starting_date.split('/')
	end_arr=ending_date.split('/')
	start_day=start_arr[0]
	start_month=start_arr[1]
	start_year=start_arr[2]
	end_day=end_arr[0]
	end_month=end_arr[1]
	end_year=end_arr[2]

	if(int(curr_year)!=int(end_year)):
		return render_template("cancel_meals.html", status=2)
	
	if(int(curr_year)>int(start_year) or int(curr_year)>int(end_year)):
		return render_template("cancel_meals.html", status=2)

	if(int(curr_year)==int(start_year)):
		if(int(curr_month)>int(start_month)):
							return render_template("cancel_meals.html", status=2)
		if(int(curr_month)==int(start_month)):
		             if(int(curr_day)>int(start_day)):
		             	return render_template("cancel_meals.html", status=2)
	if(int(start_year)>int(end_year)):
		return render_template("cancel_meals.html", status=2)

	breakfast = request.form.get('meal_type_1')
	lunch = request.form.get('meal_type_2')
	dinner = request.form.get('meal_type_3')
	with sql.connect("mess_portal.db") as con:

				con.row_factory = sql.Row
				cur = con.cursor()
				if(int(start_day)>int(end_day) or int(start_month)<int(end_month)):
							if breakfast:
								if(int(start_day)==int(curr_day)):
								     return render_template("cancel_meals.html", status=2)

								if(int(start_day)==int(curr_day+1) and hours>=19 and hours<=23):
								    return render_template("cancel_meals.html", status=2)	
								        
								else:
											query="UPDATE meal_registration SET bbit ='1' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(31)+" and month>="+str(start_month)+" and month<="+str(start_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
											cur.execute(query)
											query="UPDATE meal_registration SET bbit ='1' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(1)+" and day<="+str(end_day)+" and month>="+str(end_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
											cur.execute(query)
											con.commit()
							if lunch:
									if(int(start_day)==int(curr_day) and hours>=7):
									        return render_template("cancel_meals.html", status=2)
									else:	

											query="UPDATE meal_registration SET lbit ='1' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(31)+" and month>="+str(start_month)+" and month<="+str(start_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
											cur.execute(query)
											query="UPDATE meal_registration SET lbit ='1' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(1)+" and day<="+str(end_day)+" and month>="+str(end_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
											cur.execute(query)
											con.commit()
							if dinner:
									if(int(start_day)==int(curr_day) and hours>=15):
									      return render_template("cancel_meals.html", status=2)
									else:	      
											query="UPDATE meal_registration SET dbit ='1' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(31)+" and month>="+str(start_month)+" and month<="+str(start_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
											cur.execute(query)
											query="UPDATE meal_registration SET dbit ='1' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(1)+" and day<="+str(end_day)+" and month>="+str(end_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
											cur.execute(query)
											con.commit()                    

				else:
							if breakfast:
								print(start_day)
								print(curr_day)

								if(int(start_day)==int(curr_day)):
								     return render_template("cancel_meals.html", status=2)

								if(int(start_day)==int(curr_day+1) and hours>=19 and hours<=23):
								    return render_template("cancel_meals.html", status=2)	
								        
								else:
															query="UPDATE meal_registration SET bbit = '1' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
															cur.execute(query)
															con.commit()
							if lunch:
								if(int(start_day)==int(curr_day) and hours>=7):
								      return render_template("cancel_meals.html")
								else:
															query="UPDATE meal_registration SET lbit= '1' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
															cur.execute(query)
															con.commit()
							if dinner:
								if(int(start_day)==int(curr_day) and hours>=15):
									      return render_template("cancel_meals.html", status=2)
								else:
															query="UPDATE meal_registration SET dbit= '1' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"    
															cur.execute(query)
															con.commit()                    
															print("working")

				return render_template("cancel_meals.html", status=3)

@app.route("/uncancelmealstatus", methods=['POST'])
def uncancelmealstatus():
		now = datetime.datetime.now()
		hours=now.hour
		curr_day=now.day
		curr_month=now.month
		curr_year=now.year

		formdate=request.form['demo']
		datearr=formdate.split('-')
		starting_date=datearr[0]
		ending_date_space=datearr[1].split(' ')
		ending_date=ending_date_space[1]
		start_arr=starting_date.split('/')
		end_arr=ending_date.split('/')
		start_day=start_arr[0]
		start_month=start_arr[1]
		start_year=start_arr[2]
		end_day=end_arr[0]
		end_month=end_arr[1]
		end_year=end_arr[2]
		if(int(curr_year)!=int(end_year)):
			return render_template("cancel_meals.html", status=2)
	
		if(int(curr_year)>int(start_year) or int(curr_year)>int(end_year)):
		            return render_template("cancel_meals.html", status=2)

		if(int(curr_year)==int(start_year)):
		    if(int(curr_month)>int(start_month)):
		    	return render_template("cancel_meals.html", status=2)
		if(int(curr_month)==int(start_month)):
		    if(int(curr_day)>int(start_day)):
		    	return render_template("cancel_meals.html", status=2)
		if(int(start_year)>int(end_year)):
			return render_template("cancel_meals.html", status=2)
		breakfast = request.form.get('meal_type_1')
		lunch = request.form.get('meal_type_2')
		dinner = request.form.get('meal_type_3')
		with sql.connect("mess_portal.db") as con:
				con.row_factory = sql.Row
				cur = con.cursor()
				if(start_day>end_day or start_month<end_month):
							if breakfast:


											query="UPDATE meal_registration SET bbit ='0' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(31)+" and month>="+str(start_month)+" and month<="+str(start_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
											cur.execute(query)
											query="UPDATE meal_registration SET bbit ='0' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(1)+" and day<="+str(end_day)+" and month>="+str(end_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
											cur.execute(query)
											con.commit()
							if lunch:
											query="UPDATE meal_registration SET lbit ='0' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(31)+" and month>="+str(start_month)+" and month<="+str(start_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
											cur.execute(query)
											query="UPDATE meal_registration SET lbit ='0' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(1)+" and day<="+str(end_day)+" and month>="+str(end_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
											cur.execute(query)
											con.commit()
							if dinner:
											query="UPDATE meal_registration SET dbit ='0' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(31)+" and month>="+str(start_month)+" and month<="+str(start_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
											cur.execute(query)
											query="UPDATE meal_registration SET dbit ='0' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(1)+" and day<="+str(end_day)+" and month>="+str(end_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
											cur.execute(query)
											con.commit()                    

				else:
							if breakfast:
															query="UPDATE meal_registration SET bbit = '0' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
															cur.execute(query)
															con.commit()
							if lunch:
															query="UPDATE meal_registration SET lbit= '0' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
															cur.execute(query)
															con.commit()
							if dinner:
															query="UPDATE meal_registration SET dbit= '0' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"    
															cur.execute(query)
															con.commit()                    
															print("working")

				return render_template("cancel_meals.html", status=4)
# @app.route("/home.html")
# def index():
# 	return render_template("index.html")

@app.route("/studentprofile", methods = ['GET'])
def get_student_profile():
	if request.method == "GET":
		res = model.get_student_profile(2018201022)
	return render_template("test.html", result = res, message = request.method)

@app.route("/mealregistration", methods = ['GET'])
def get_meal_registration():
	if request.method == "GET":
		res = model.get_meal_registration()
	return render_template("test.html", result = res, message = request.method)



@app.route("/cancelcurrI", methods=['POST'])
def cancelcurrI():
				now = datetime.datetime.now()
				hours=now.hour
				start_day=now.day
				start_month=now.month
				start_year=now.year
				end_day=now.day
				end_month=now.month
				end_year=now.year
                
				if(hours>=22 and hours<=23):
					start_day+=1
					end_day+=1
					mybit="bbit"
					checkcancel="bcancel"

				if(hours>=0 and hours<=9):
				     mybit="bbit" 
				     checkcancel="bcancel"

				if(hours>=10 and hours<=14):
				     mybit="lbit"
				     checkcancel="lcancel"   

				if(hours>=15 and hours<=21):
				   mybit="dbit"
				   checkcancel="dcancel"

				meals = model.get_meal_registration_for_month(str(session['roll_no']), datetime.datetime.now().month, datetime.datetime.now().year)
				val=meals[checkcancel][start_day-1]
				with sql.connect("mess_portal.db") as con:
						con.row_factory = sql.Row
						cur = con.cursor()
						if(val=="0"):
						     query="UPDATE meal_registration SET "+mybit+" = '1' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
						else:
							 query="UPDATE meal_registration SET "+mybit+" = '0' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
					
						cur.execute(query)
						con.commit()
				msg={}
				email = request.cookies.get('email')
				print("email : ", email)
				print("session : ", session)
				print("cookies : ", request.cookies)

				roll_no = session[email]
				msg["roll_no"] = roll_no

				name = request.cookies.get('name')
				msg["name"]=name
				msg["authenticate"]=True
				meals = model.get_meal_registration_for_month(roll_no, datetime.datetime.now().month, datetime.datetime.now().year)

				msg["breakfast"]=meals["breakfast"]
				msg["lunch"]=meals["lunch"]
				msg["dinner"]=meals["dinner"]
				msg["bcancel"]=meals["bcancel"]
				msg["lcancel"]=meals["lcancel"]
				msg["dcancel"]=meals["dcancel"]
				json_obj = json.dumps(msg)
				return render_template("dashboard.html", message=json_obj)

@app.route("/cancelcurrII", methods=['POST'])
def cancelcurrII():
				now = datetime.datetime.now()
				hours=now.hour
				start_day=now.day
				start_month=now.month
				start_year=now.year
				end_day=now.day
				end_month=now.month
				end_year=now.year
				if(hours>=22 and hours<=23):
					start_day+=1
					end_day+=1
					mybit="lbit"
					checkcancel="lcancel"

				if(hours>=0 and hours<=9):
				    mybit="lbit"
				    checkcancel="lcancel"

				if(hours>=10 and hours<=14):
				    mybit="dbit"
				    checkcancel="dcancel"   

				if(hours>=15 and hours<=21):
					start_day+=1
					end_day+=1
					mybit="bbit"
					checkcancel="bcancel"
				meals = model.get_meal_registration_for_month(str(session['roll_no']), datetime.datetime.now().month, datetime.datetime.now().year)
				val=meals[checkcancel][start_day-1]
				with sql.connect("mess_portal.db") as con:
						con.row_factory = sql.Row
						cur = con.cursor()
						if(val=="0"):
						     query="UPDATE meal_registration SET "+mybit+" = '1' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
						else:
							 query="UPDATE meal_registration SET "+mybit+" = '0' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
						cur.execute(query)
						con.commit()
				msg={}
				email = request.cookies.get('email')
				print("email : ", email)
				print("session : ", session)
				print("cookies : ", request.cookies)

				roll_no = session[email]
				msg["roll_no"] = roll_no

				name = request.cookies.get('name')
				msg["name"]=name
				msg["authenticate"]=True
				meals = model.get_meal_registration_for_month(roll_no, datetime.datetime.now().month, datetime.datetime.now().year)

				msg["breakfast"]=meals["breakfast"]
				msg["lunch"]=meals["lunch"]
				msg["dinner"]=meals["dinner"]
				msg["bcancel"]=meals["bcancel"]
				msg["lcancel"]=meals["lcancel"]
				msg["dcancel"]=meals["dcancel"]
				json_obj = json.dumps(msg)
				return render_template("dashboard.html", message=json_obj)

@app.route("/cancelcurrIII", methods=['POST'])
def cancelcurrIII():
				now = datetime.datetime.now()
				hours=now.hour
				start_day=now.day
				start_month=now.month
				start_year=now.year
				end_day=now.day
				end_month=now.month
				end_year=now.year
				if(hours>=22 and hours<=23):
					start_day+=1
					end_day+=1
					mybit="dbit"
					checkcancel="dcancel"

				if(hours>=0 and hours<=9):
				    mybit="dbit"
				    checkcancel="dcancel"

				if(hours>=10 and hours<=14):
					start_day+=1
					end_day+=1
					mybit="bbit"
					checkcancel="bcancel"  

				if(hours>=15 and hours<=21):
					start_day+=1
					end_day+=1
					mybit="lbit"
					checkcancel="lcancel"
				meals = model.get_meal_registration_for_month(str(session['roll_no']), datetime.datetime.now().month, datetime.datetime.now().year)
				val=meals[checkcancel][start_day-1]
				with sql.connect("mess_portal.db") as con:
						con.row_factory = sql.Row
						cur = con.cursor()
						if(val=="0"):
						     query="UPDATE meal_registration SET "+mybit+" = '1' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
						else:
							 query="UPDATE meal_registration SET "+mybit+" = '0' WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
						cur.execute(query)
						con.commit()
				msg={}
				email = request.cookies.get('email')
				print("email : ", email)
				print("session : ", session)
				print("cookies : ", request.cookies)

				roll_no = session[email]
				msg["roll_no"] = roll_no

				name = request.cookies.get('name')
				msg["name"]=name
				msg["authenticate"]=True
				meals = model.get_meal_registration_for_month(roll_no, datetime.datetime.now().month, datetime.datetime.now().year)

				msg["breakfast"]=meals["breakfast"]
				msg["lunch"]=meals["lunch"]
				msg["dinner"]=meals["dinner"]
				msg["bcancel"]=meals["bcancel"]
				msg["lcancel"]=meals["lcancel"]
				msg["dcancel"]=meals["dcancel"]
				json_obj = json.dumps(msg)
				return render_template("dashboard.html", message=json_obj)

				
@app.route("/change_mess_registration.html")
def change_mess_registration():
	if not session.get('name'):
		return render_template('login.html')
	if session["user"] != "student":
		return "Not authorized"
	if session["first_login"] == "True":
		return render_template("set_default_mess.html")
	return render_template("change_mess_registration.html")	

@app.route("/default_mess.html")
def default_mess():
	if not session.get('name'):
		return render_template('login.html')
	if session["user"] != "student":
		return "Not authorized"
	if session["first_login"] == "True":
		return render_template("set_default_mess.html")
	return render_template("default_mess.html")	

@app.route("/dashboard.html")
def show_dashboard():
	if not session.get('name'):
		return render_template('login.html')
	if session["user"] != "student":
		return "Not authorized"
	print("*****************************************")
	print(session)
	if session["first_login"] == "True":
		return render_template("set_default_mess.html")
	msg={}
	email = request.cookies.get('email')
	if email in session:

		roll_no = session[email]
		msg["roll_no"] = roll_no
		
		name = request.cookies.get('name')
		msg["name"]=name
		msg["authenticate"]=True
		meals = model.get_meal_registration_for_month(roll_no, datetime.datetime.now().month, datetime.datetime.now().year)

		msg["breakfast"]=meals["breakfast"]
		msg["lunch"]=meals["lunch"]
		msg["dinner"]=meals["dinner"]
		msg["bcancel"]=meals["bcancel"]
		msg["lcancel"]=meals["lcancel"]
		msg["dcancel"]=meals["dcancel"]
		json_obj = json.dumps(msg)
		return render_template("dashboard.html", message=json_obj)
	else:
		return render_template("login.html")	


@app.route("/change_mess_menu.html")
def show_change_mess_menu():
	if not session.get('name'):
		return render_template('login_admin.html')
	if session["user"] != "admin":
		return "Not authorized"

	return render_template("change_mess_menu.html")	

@app.route("/changemenu", methods=['POST'])
def change_menu():
	msg={}
	
	mess = request.form['mess']+"_menu";
	day = request.form['day']
	meal = request.form['meal']
	newmenu = request.form['newmenu']
	
	msg["mess"]=mess
	msg["day"]=day;
	msg["meal"]=meal;
	msg["newmenu"]=newmenu;
	json_obj=json.dumps(msg)

	model.change_menu(mess,day,meal,newmenu)
	return render_template("change_mess_menu.html",status=5)

@app.route("/change_default_mess_admin.html")
def show_change_default_mess_admin():
	if not session.get('name'):
		return render_template('login_admin.html')
	if session["user"] != "admin":
		return "Not authorized"
	return render_template("change_default_mess_admin.html")	

@app.route("/change_default_mess", methods=['POST'])
def change_default_mess():
	msg={}
	
	student_rollno = request.form['student_rollno'];
	default_breakfast_mess = request.form['default_breakfast_mess']
	default_lunch_mess = request.form['default_lunch_mess']
	default_dinner_mess = request.form['default_dinner_mess']
	
	model.change_default_mess(student_rollno,default_breakfast_mess,default_lunch_mess,default_dinner_mess)
	return render_template("change_default_mess_admin.html",status=6)


@app.route("/datewisemesschange", methods=['POST'])
def datewisemesschange():
		now = datetime.datetime.now()
		hours=now.hour
		curr_day=now.day
		curr_month=now.month
		curr_year=now.year

		formdate=request.form['demo']
		datearr=formdate.split('-')
		starting_date=datearr[0]
		ending_date_space=datearr[1].split(' ')
		ending_date=ending_date_space[1]
		start_arr=starting_date.split('/')
		end_arr=ending_date.split('/')
		start_day=start_arr[0]
		start_month=start_arr[1]
		start_year=start_arr[2]
		end_day=end_arr[0]
		end_month=end_arr[1]
		end_year=end_arr[2]
		if(int(curr_year)!=int(end_year)):
			return render_template("cancel_meals.html", status=2)
	

		if(int(curr_year)>int(start_year) or int(curr_year)>int(end_year)):
		            return render_template("change_mess_registration.html", status=2)

		if(int(curr_year)==int(start_year)):
		    if(int(curr_month)>int(start_month)):
		    	return render_template("change_mess_registration.html", status=2)

		if(int(curr_month)==int(start_month)):
				if(int(curr_day)>int(start_day)):
				       return render_template("change_mess_registration.html", status=2)
				if(int(start_day)<int(curr_day+2)):		    
				      return render_template("change_mess_registration.html", status=2)
		if(int(start_year)>int(end_year)):
		    return render_template("change_mess_registration.html", status=2)
		breakfast = request.form.get('meal_type_1')
		lunch = request.form.get('meal_type_2')
		dinner = request.form.get('meal_type_3')
		messname1=request.form['messname']
		with sql.connect("mess_portal.db") as con:
					con.row_factory = sql.Row
					cur = con.cursor()
					print(start_day)
					print(end_day)
					print(start_month)
					print(end_month)
					if(start_day>end_day or start_month<end_month):
								if breakfast:


												query="UPDATE meal_registration SET bbit ='0',breakfast = "+"'"+str(messname1)+"'"+" WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(31)+" and month>="+str(start_month)+" and month<="+str(start_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
												cur.execute(query)
												query="UPDATE meal_registration SET bbit ='0',breakfast = "+"'"+str(messname1)+"'"+" WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(1)+" and day<="+str(end_day)+" and month>="+str(end_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
												cur.execute(query)
												con.commit()
								if lunch:
												query="UPDATE meal_registration SET lbit ='0',lunch = "+"'"+str(messname1)+"'"+" WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(31)+" and month>="+str(start_month)+" and month<="+str(start_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
												cur.execute(query)
												query="UPDATE meal_registration SET lbit ='0',lunch = "+"'"+str(messname1)+"'"+" WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(1)+" and day<="+str(end_day)+" and month>="+str(end_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
												cur.execute(query)
												con.commit()
								if dinner:
												query="UPDATE meal_registration SET dbit ='0',dinner = "+"'"+str(messname1)+"'"+" WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(31)+" and month>="+str(start_month)+" and month<="+str(start_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
												cur.execute(query)
												query="UPDATE meal_registration SET dbit ='0',dinner = "+"'"+str(messname1)+"'"+" WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(1)+" and day<="+str(end_day)+" and month>="+str(end_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
												cur.execute(query)
												con.commit()                    

					else:


							if breakfast:


										query="UPDATE meal_registration SET bbit ='0',breakfast = "+"'"+str(messname1)+"'"+" WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
										print(query)
										cur.execute(query)
										con.commit()
							if lunch:
										query="UPDATE meal_registration SET lbit ='0',lunch = "+"'"+str(messname1)+"'"+" WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
										cur.execute(query)
										con.commit()
							if dinner:
										query="UPDATE meal_registration SET dbit ='0',dinner = "+"'"+str(messname1)+"'"+" WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"    
										cur.execute(query)
										con.commit()                    

					return render_template("change_mess_registration.html", status=7)

@app.route("/cancelmealdaywise", methods=['POST'])
def cancelmealdaywise():
			now = datetime.datetime.now()
			hours=now.hour
			start_day=now.day
			start_month=now.month
			start_year=now.year
			end_day=31
			end_month=now.month
			end_year=now.year					
			daycancel=request.form['cancelday']
			breakfast = request.form.get('meal_type_1')
			lunch = request.form.get('meal_type_2')
			dinner = request.form.get('meal_type_3')
			with sql.connect("mess_portal.db") as con:
					con.row_factory = sql.Row
					cur = con.cursor()
					if breakfast:
							start_day+=1
							query="UPDATE meal_registration SET bbit = '1' WHERE (roll_no="+str(session['roll_no'])+" and dayname="+"'"+str(daycancel)+"'"+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
							print(query)
							cur.execute(query)
							con.commit()
					if lunch:                   
							if(hours>=7):
								start_day+=1
							query="UPDATE meal_registration SET lbit = '1' WHERE (roll_no="+str(session['roll_no'])+" and dayname="+"'"+str(daycancel)+"'"+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
							cur.execute(query)
							con.commit()
					if dinner:                  
							if(hours>=15):
								start_day+=1
							query="UPDATE meal_registration SET dbit = '1' WHERE (roll_no="+str(session['roll_no'])+" and dayname="+"'"+str(daycancel)+"'"+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
							cur.execute(query)
							con.commit()                    
														

			return render_template("cancel_meals.html", status=3)

@app.route("/uncancelmealdaywise", methods=['POST'])
def uncancelmealdaywise():
			now = datetime.datetime.now()
			hours=now.hour
			start_day=now.day
			start_month=now.month
			start_year=now.year
			end_day=31
			end_month=now.month
			end_year=now.year					
			daycancel=request.form['cancelday']
			breakfast = request.form.get('meal_type_1')
			lunch = request.form.get('meal_type_2')
			dinner = request.form.get('meal_type_3')
			with sql.connect("mess_portal.db") as con:
					con.row_factory = sql.Row
					cur = con.cursor()
					if breakfast:
							start_day+=1
							query="UPDATE meal_registration SET bbit = '0' WHERE (roll_no="+str(session['roll_no'])+" and dayname="+"'"+str(daycancel)+"'"+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
							print(query)
							cur.execute(query)
							con.commit()
					if lunch:                   
							if(hours>=7):
								start_day+=1
							query="UPDATE meal_registration SET lbit = '0' WHERE (roll_no="+str(session['roll_no'])+" and dayname="+"'"+str(daycancel)+"'"+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
							cur.execute(query)
							con.commit()
					if dinner:                  
							if(hours>=15):
								start_day+=1
							query="UPDATE meal_registration SET dbit = '0' WHERE (roll_no="+str(session['roll_no'])+" and dayname="+"'"+str(daycancel)+"'"+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
							cur.execute(query)
							con.commit()                    
														

			return render_template("cancel_meals.html", status=4)			

@app.route("/daywisemesschange", methods=['POST'])
def daywisemesschange():
		now = datetime.datetime.now()
		start_day=now.day
		start_month=now.month
		start_year=now.year
		end_day=31
		end_month=now.month
		end_year=now.year					
		daychange=request.form['changeday']
		breakfast = request.form.get('meal_type_1')
		lunch = request.form.get('meal_type_2')
		dinner = request.form.get('meal_type_3')
		messname1=request.form['messname1']
		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			if breakfast:
											query="UPDATE meal_registration SET bbit ='0',breakfast = "+"'"+str(messname1)+"'"+" WHERE (roll_no="+str(session['roll_no'])+" and dayname="+"'"+str(daychange)+"'"+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
											
											cur.execute(query)
											con.commit()
			if lunch:
											query="UPDATE meal_registration SET lbit ='0',lunch = "+"'"+str(messname1)+"'"+" WHERE (roll_no="+str(session['roll_no'])+" and dayname="+"'"+str(daychange)+"'"+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
											cur.execute(query)
											con.commit()
			if dinner:
											query="UPDATE meal_registration SET dbit ='0',dinner = "+"'"+str(messname1)+"'"+" WHERE (roll_no="+str(session['roll_no'])+" and dayname="+"'"+str(daychange)+"'"+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"    
											cur.execute(query)
											con.commit()                    

		return render_template("change_mess_registration.html",status=7)

@app.route("/generate_mess_report.html")
def show_generate_report():
	if not session.get('name'):
		return render_template('login_admin.html')
	if session["user"] != "admin":
		return "Not authorized"
	return render_template("generate_mess_report.html")


@app.route("/generatereport",methods=['POST'])
def generatereport():
	msg={}
	name_of_mess=request.form['name_of_mess']
	report_date=request.form['report_date']

	report_date=report_date.split("-")

	day=report_date[2]
	month=report_date[1]
	year=report_date[0]

	bdata,ldata,ddata=model.generatereport(name_of_mess,day,month,year)

	msg["breakfast_list"]=(bdata)
	msg["lunch_list"]=(ldata)
	msg["dinner_list"]=(ddata)
	msg["mess"]=name_of_mess
	msg["date"]=day+"/"+month+"/"+year
	json_obj = json.dumps(msg)
	return render_template("display_report_data.html", message=json_obj)

@app.route("/mess_registration_stats.html")
def show_mess_registration_stats():
	
	return render_template("/mess_registration_stats.html")

@app.route("/showmessstats")
def messstats():
	msg={}
	

	data=model.messstats()

	# msg["breakfast_list"]=(bdata)
	# msg["lunch_list"]=(ldata)
	# msg["dinner_list"]=(ddata)
	# msg["mess"]=name_of_mess
	# msg["date"]=day+"/"+month+"/"+year
	# json_obj = json.dumps(msg)
	# return render_template("display_report_data.html", message=json_obj)


	return "Hello"#render_template("/mess_registration_stats.html")

@app.route("/admin_dashboard.html")
def show_admin_dashboard():
	if not session.get('name'):
		return render_template('login_admin.html')
	if session["user"] != "admin":
		return "Not authorized"
	return render_template("/admin_dashboard.html")

@app.route("/logout.html")
def show_logout_page():
	return render_template("/logout.html")

@app.route("/login.html")
def show_login_page():
	if not session.get('name'):
		return render_template('login.html')
	if session["user"] != "student":
		return "Not authorized"
	return render_template("/login.html")

@app.route("/getdefaultmess")
def get_def_mess():
	print("----------------------------------------------")
	if session["user"] != "student":
			return "Not authorized"
	if session["first_login"] == "True":
			return render_template("set_default_mess.html")
	a,b,c=model.getdefaultmess(session["roll_no"])

	return render_template("/default_mess.html",mess1=a,mess2=b,mess3=c)



@app.route("/monthlymesssubscribe", methods=['POST'])
def monthlymesssubscribe():

			formdate=request.form['monthname']
			datearr=formdate.split('/')
			start_day=1
			start_month=datearr[0]
			start_year=datearr[1]
			end_day=31
			end_month=datearr[0]
			end_year=datearr[1]
			breakfast = True
			lunch = True
			dinner = True
			messname1=request.form['messname1']
			with sql.connect("mess_portal.db") as con:
					con.row_factory = sql.Row
					cur = con.cursor()
					if breakfast:
						query="UPDATE meal_registration SET bbit ='0',breakfast = "+"'"+str(messname1)+"'"+" WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
						print(query)
						cur.execute(query)
						con.commit()
					if lunch:
						query="UPDATE meal_registration SET lbit ='0',lunch = "+"'"+str(messname1)+"'"+" WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"
						cur.execute(query)
						con.commit()
					if dinner:
						query="UPDATE meal_registration SET dbit ='0',dinner = "+"'"+str(messname1)+"'"+" WHERE (roll_no="+str(session['roll_no'])+" and day>="+str(start_day)+" and day<="+str(end_day)+" and month>="+str(start_month)+" and month<="+str(end_month)+" and year>="+str(start_year)+" and year<="+str(end_year)+")"    
						cur.execute(query)
					con.commit()
					query="UPDATE monthly_registration SET rbit ='1',mess = "+"'"+str(messname1)+"'"+" WHERE (roll_no="+str(session['roll_no'])+" and month="+str(start_month)+" and year="+str(start_year)+")" 
					cur.execute(query)
			return render_template("change_mess_registration.html",status=15)

@app.route("/monthlymessunsubscribe", methods=['POST'])
def monthlymessunsubscribe():

			formdate=request.form['monthname']
			datearr=formdate.split('/')
			start_day=1
			start_month=datearr[0]
			start_year=datearr[1]
			end_day=31
			end_month=datearr[0]
			end_year=datearr[1]
			breakfast = True
			lunch = True
			dinner = True
			messname1=request.form['messname1']
			with sql.connect("mess_portal.db") as con:
					con.row_factory = sql.Row
					cur = con.cursor()
					query="UPDATE monthly_registration SET rbit ='0',mess = "+"'"+str(messname1)+"'"+" WHERE (roll_no="+str(session['roll_no'])+" and month="+str(start_month)+" and year="+str(start_year)+")" 
					cur.execute(query)
			return render_template("change_mess_registration.html",status=16)

@app.route("/bill")
def billing():
	if not session.get('name'):
		return render_template('login.html')
	if session["user"] != "student":
		return "Not authorized"
	if session["first_login"] == "True":
		return render_template("set_default_mess.html")
	msg = model.get_bill_details(session['roll_no'], datetime.datetime.now().month, datetime.datetime.now().year)
	canc = model.get_cancellations()
	rate = model.get_rates()
	json_obj = json.dumps(msg)
	cancel = json.dumps(canc)
	rate = json.dumps(rate)
	resp = make_response(render_template("billing.html", message=json_obj, canc=cancel, rate=rate))
	return resp			
		
@app.route("/feedback.html")
def feedback_page():
	if not session.get('name'):
		return render_template('login.html')
	if session["user"] != "student":
		return "Not authorized"
	if session["first_login"] == "True":
		return render_template("set_default_mess.html")
	return render_template("/feedback.html")
	
@app.route("/feedback",methods=['POST'])
def feedback():
	mess = request.form['mess']
	subject = request.form['subject']	
	args = [session['roll_no'],session['name'],mess,subject,""]
	if request.method == 'POST' and 'fileToUpload' in request.files:
		filename = photos.save(request.files['fileToUpload'])
		args[4] = filename
	comm = str(args[0])
	for i in range(1,len(args)):
		comm = comm + ",'"+str(args[i])+"'"
		print(comm)
	try:
		with sql.connect("mess_portal.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			comm = "insert into feedbacks values (" + comm + ")"
			print(comm)
			cur.execute(comm)
			print("Hi")
	except:
		print("Feedback Submission Fails..")
	return render_template("/feedback.html",status=8)

@app.route("/day_wise_gui.html")
def day_wise_gui():
	if not session.get('name'):
		return render_template('login.html')
	if session["user"] != "student":
		return "Not authorized"
	if session["first_login"] == "True":
		return render_template("set_default_mess.html")

	return render_template("/day_wise_gui.html",status=10)

@app.route("/set_menu_day_wise", methods=['POST'])
def set_menu_day_wise():
	
	meal = request.form['mydata']
	menus = menu.get_menu_day_wise(meal)
	json_obj = json.dumps(menus)
	
	return json_obj

@app.route("/change_mess_for_day", methods=['POST'])
def change_mess_for_day():
	json_obj = request.form['mydata_mess_day']
	json_data = json.loads(json_obj)
	changemess.daywisemesschange(session['roll_no'], json_data['meal'], json_data['mess'], json_data['day'])
	return "working"

@app.route("/view_student_list.html")
def show_student_list():
	if not session.get('name'):
		return render_template('login_admin.html')
	if session["user"] != "admin":
		return "Not authorized"
	
	return render_template("/view_student_list.html")

@app.route("/populatelist",methods=["POST"])
def populatelist():
	filter=request.form["filter"]

	print(filter)
	data=model.populatelist(filter)
	
	json_obj = json.dumps(data)

	return render_template("/view_student_list.html",data=json_obj)

@app.route("/visualization.html")
def show_visualization():
	if not session.get('name'):
		return render_template('login_admin.html')
	if session["user"] != "admin":
		return "Not authorized"
	
	return render_template("/visualization.html")

@app.route("/datewise_piechart",methods=["POST"])
def datewise_piechart():
	date=request.form["pie_date"]
	bdata,ldata,ddata=graphs.datewise_pie(date)
	bdata=json.dumps(bdata)
	ldata=json.dumps(ldata)
	ddata=json.dumps(ddata)
	return render_template("/pie_chart_datewise.html",bdata=bdata,ldata=ldata,ddata=ddata,date=date)



@app.route("/monthwise_piechart",methods=["POST"])
def monthwise_piechart():
	month=request.form["pie_month"]
	bdata,ldata,ddata=graphs.monthwise_pie(month)
	bdata=json.dumps(bdata)
	ldata=json.dumps(ldata)
	ddata=json.dumps(ddata)
	return render_template("/pie_chart_monthwise.html",bdata=bdata,ldata=ldata,ddata=ddata,month=month)

@app.route("/daywise_linechart")
def daywise_linechart():
	graph_data=graphs.daywise_line(day)
	return render_template("/line_chart_.html")

@app.route("/monthwise_linechart",methods=["POST"])
def monthwise_linechart():
	month=request.form["line_month"]
	print(month)
	graph_data=graphs.monthwise_line(month)
	return render_template("/visualization.html")

@app.route("/setdefaultmess", methods=['POST'])
def set_default_mess():
	if request.method == 'POST':
		roll_no = session["roll_no"]
		default_breakfast_mess = request.form["default_breakfast_mess"]
		default_lunch_mess = request.form["default_lunch_mess"]
		default_dinner_mess = request.form["default_dinner_mess"]
		print("before")
		result = changemess.set_default_mess(roll_no, default_breakfast_mess, default_lunch_mess, default_dinner_mess)
		print("after")
		if result == "success":
			msg={}
			email = request.cookies.get('email')
			roll_no = session[email]
			msg["roll_no"] = roll_no
			msg["name"]=session["name"]
			msg["authenticate"]=True
			meals = model.get_meal_registration_for_month(roll_no, datetime.datetime.now().month, datetime.datetime.now().year)
			msg["breakfast"]=meals["breakfast"]
			msg["lunch"]=meals["lunch"]
			msg["dinner"]=meals["dinner"]
			msg["bcancel"]=meals["bcancel"]
			msg["lcancel"]=meals["lcancel"]
			msg["dcancel"]=meals["dcancel"]
			json_obj = json.dumps(msg)
			session["first_login"] = "False"
			
			resp = make_response(render_template("dashboard.html", message=json_obj))
			resp.set_cookie('first_login', "False")
		else:
			session["first_login"] = "True"
			resp = make_response(render_template("set_default_mess.html", message=json_obj))
			resp.set_cookie('first_login', "True")
		return resp

@app.route("/read_feedback.html")
def show_feedback():
	if not session.get('name'):
		return render_template('login_admin.html')
	if session["user"] != "admin":
		return "Not authorized"
	
	msg = model.show_feedback()
	json_obj = json.dumps(msg)
	return render_template("/read_feedback.html", feedback=json_obj)

@app.route("/generate_bill.html")
def show_generate_bill():
	if not session.get('name'):
		return render_template('login_admin.html')
	if session["user"] != "admin":
		return "Not authorized"
	return render_template("/generate_bill.html")


@app.route("/genbill")
def generate_student_bill():
	if not session.get('name'):
		return render_template('login_admin.html')
	if session["user"] != "admin":
		return "Not authorized"
	model.generate_student_bill()
	return render_template("/generate_bill.html",status=9)