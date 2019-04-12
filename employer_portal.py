from flask import Flask, render_template, request, flash, logging, url_for, redirect, jsonify, make_response, session, g
from flask_sqlalchemy import SQLAlchemy
import requests
import json
import logging
import xml.etree.ElementTree as ET

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sneha3010@localhost/projectdb'
db = SQLAlchemy(app)

employee_id = '1'

class Employee_details(db.Model):
	__tablename__ = 'emp_employee'
	username = db.Column('username', db.Unicode, primary_key=True)
	password = db.Column('password', db.Unicode)
	emp_name = db.Column('emp_name', db.Unicode)
	salary = db.Column('salary', db.Integer)
	emp_start_date = db.Column('emp_start_date', db.DateTime)


@app.route('/')
def home(): 
	return render_template('home.html')

@app.before_request
def before_request():
	g.user =None
	if 'user' in session:
		g.user = session['user']


@app.route('/login', methods=['GET', 'POST'])
def login():
	f = open("log1.txt", "a+")
	f.write("method: GET \nEnd-point: http://127.0.0.1:8001/login \nparameters: None\n" )
	f.close()
	# Employee_details1 = Employee_details.query.filter_by(username=username),first()
	
	session.pop('user', None)

	if request.method == 'POST':
		f = open("log1.txt", "a+")
		f.write("method: POST \nEnd-point: http://127.0.0.1:8001/login \nparameters: username: "+request.form['username']+", password:  ")
		f.close()
		# for i in range(1):
		# 	f.write("POST, http://127.0.0.1:8001/login, username: "+request.form['username']+", password: "+request.form['password']+" %d\r\n" % (i))
		emppass = request.form
		username = request.form['username']
		get_emp = Employee_details.query.filter_by(username=username).first()
		password = request.form['password']


		pathToXML = "Salt.xml"
		tree = ET.parse(pathToXML)
		root = tree.getroot()

		# all items data
		print('Expertise Data:'+str(root)+str(tree))
		salt = ''
		for elem in root:
			salt = elem.text


		if get_emp is None:
			error = 'User not present! Try again.'
			return render_template('login.html', error = error)
		if  get_emp.password != password+salt:
			error = 'Password do not match! Try again.'
			return render_template('login.html', error = error)
		else:
			session['user'] = username
			return redirect(url_for('addEmployer',  username=session['user']))
		
		

	return render_template('login.html')


@app.route('/employer_form/<string:username>', methods=['POST','GET'])
def addEmployer(username):
	f = open("log1.txt", "a+")
	f.write("method: GET \nEnd-point: http://127.0.0.1:8001//employer_form/<string:username> \nparameters: None\n" )
	f.close()


	if g.user == username and request.method == 'POST':
		f = open("log1.txt", "a+")
		f.write("method: POST \nEnd-point: http://127.0.0.1:8001//employer_form/<string:username> \nparameters: username: "+request.form['username']+", application_no: "+request.form['application_no']+", mbr_web_service: "+request.form['mbr_web_service']+" ")
		f.close()

		employee = Employee_details()
		employerDetails = request.form
		username = employerDetails["username"]
		application_number = employerDetails["application_no"]
		mbr_web_service_address = employerDetails["mbr_web_service"]

		get_employee = Employee_details.query.filter_by(username=g.user).first()

		try:
			r = requests.get(str(mbr_web_service_address)+'?salary='+str(get_employee.salary)+'&application_number='+str(application_number)+'&emp_name='+str(get_employee.emp_name)+'&emp_start_date='+str(get_employee.emp_start_date))
		except:
			message = 'Invalid endpoint. try again'
			return render_template('updatestatus.html', message=message)

		if r.text == 'success':

			message = 'Employee details submitted sucessfully to MBR portal.'
			return render_template('updatestatus.html', message=message)
		else:

	 		return "<h1> Error occured while submitting details to MBR portal. </h1>"
	 		db.session.close_all()
	 		db.session.add(employee)
	 		db.session.commit()

	 		return"<h1> Employee details submitted sucessfully. </h1>"
	else:
		if g.user:
			return render_template('employer_form.html', username=username)


	return redirect(url_for('login'))

@app.route('/logout', methods=['GET'])
def logout():
	f = open("log1.txt", "w+")
	f.write("method: GET \nEnd-point: http://127.0.0.1:8001/logout \nparameters: logged out\n" )
	f.close()
	session.pop('user', None)
	return redirect(url_for('login'))

if __name__ == '__main__':
	app.secret_key = 'abcdweb'
	app.run(debug=True, port=8001)