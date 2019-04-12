from flask import Flask, render_template, request, flash, logging, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import json
import random
import xml.etree.ElementTree as ET
#from sqlalchemy.orm import scoped_session, sessionmaker
# from passlib.apps import custom_app_context as pwd_context
# from passlib.hash import sha256_crypt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sneha3010@localhost/cloudproject'
db = SQLAlchemy(app)

class Mortgage_details(db.Model):
	__tablename__ = 'mbr_mortgage_details'
	id = db.Column('id', db.Unicode, primary_key=True)
	name = db.Column('name', db.Unicode)
	address = db.Column('address', db.Unicode)
	phone_number = db.Column('phone_number', db.Unicode)
	employer_info = db.Column('employer_info', db.Unicode)
	salary = db.Column('salary', db.Unicode)
	start_date=db.Column('start_date',db.DateTime)
	mortgage_value=db.Column('mortgage_value',db.Unicode)
	mortid=db.Column('mortid', db.Unicode)
	M1sid=db.Column('m1sid',db.Unicode)
	ins_value=db.Column('ins_value',db.Unicode)
	ded_value=db.Column('ded_value',db.Unicode)
	password = db.Column('password', db.Unicode)
	application_status = db.Column('application_status', db.Unicode)

class re_Details(db.Model):
	__tablename__ = 'realestate'
	m1sid= db.Column('m1sid', db.Unicode, primary_key=True)
	value= db.Column('value', db.Unicode)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		userid = request.form['name']
		get_user = Mortgage_details.query.filter_by(name=userid).first()

		pathToXML = "Salt.xml"
		tree = ET.parse(pathToXML)
		root = tree.getroot()
		print('Expertise Data:'+str(root)+str(tree))

		salt = ''
		for elem in root:
			salt = elem.text
		password = request.form['password'] + salt
		
		if get_user.password==password :
			if get_user.name == None or get_user.address == None or get_user.phone_number == None or get_user.employer_info == None or get_user.salary == None or get_user.mortgage_value == None or get_user.misid == None : 
				get_user.application_status='Incomplete'
			else: 
				get_user.application_status='Complete'

			
			return render_template('updatemessage2.html',mo=get_user)
		else:
			error = 'Employee ID and password do not match! Try again.'
			return render_template('login.html', error = error)

	return render_template('login.html')



@app.route('/mbr/registration', methods=['GET', 'POST'])
def addEmployer():
	if request.method == 'POST':
	 	mbr=Mortgage_details()

	 	mbrDetails = request.form
	 	mbr.name=str(mbrDetails['name'])
	 	mbr.address=mbrDetails['address']
	 	mbr.phone_number=mbrDetails['contact_no']
	 	mbr.employer_info=mbrDetails['employer_name']

	 	pathToXML = "Salt.xml"
	 	tree = ET.parse(pathToXML)
	 	root = tree.getroot()
	 	print('Expertise Data:'+str(root)+str(tree))

	 	salt = ''
	 	for elem in root:
	 		salt = elem.text

	 	mbr.password=mbrDetails['password'] + salt
	 	mbr.application_status='Incomplete'
	 	
	 	for x in range(1):
	 		_id= random.randint(1,100)
	 	mbr.id = str(_id)
	 	db.session.add(mbr)
	 	db.session.commit()
	 	return render_template('updatemessage1.html', mbr1 = _id)

	return render_template('registration.html')




@app.route('/application_status', methods=['GET'])
def addEmployeeDetails():
	salary = request.args['salary']
	aplication_number = request.args['application_number']
	emp_start_date = request.args['emp_start_date']
	emp_name = request.args['emp_name']
	print(salary,aplication_number,emp_start_date, emp_name)
	mbr_details = Mortgage_details.query.filter_by(id=aplication_number).first()
	print(mbr_details is None)
	mbr_details.salary = salary
	mbr_details.name=emp_name
	mbr_details.start_date=emp_start_date
	
 	db.session.add(mbr)
	db.session.commit()

	return 'success'



@app.route('/mbr/mortgage_request', methods=['GET','POST'])
def addMortgageRequest():
	if request.method == 'POST':

		emppass = request.form
		name = request.form['name']
		get_mbr = Mortgage_details.query.filter_by(name=name).first()
		get_mbr.mortgage_value = request.form['mortgage_value']
		get_mbr.m1sid = 'M1sidA'

		for x in range(1):
	 		_mortid= random.randint(1,100)
		get_mbr.id = str(_mortid)

		db.session.close_all()
		db.session.add(get_mbr)
		db.session.commit()


		return render_template('updatemessage3.html', mbr1 = get_mbr.id)
	get_re= re_Details.query.all()
	# print(get_re.M1sID)
	return render_template('mor_registration.html',  mbr2 = get_re)




@app.route('/mbr/insurance', methods=['GET', 'POST'])
def addInsurance():
	ins_value = request.args['ins_value']
	ded_value = request.args['ded_value']
	name = request.args['name']
	misid=request.args['misid']

	mbr_details = Mortgage_details.query.filter_by(id=name).first()
	mbr_details.ins_value = ins_value
	mbr_details.name=name
	mbr_details.ded_value=ded_value
	mbr_details.misid=misid
	
	get_details = Mortgage_details.query.filter_by(name=name).first()
	r = requests.get('?ins_value='+str(get_details.ins_value)+'?ins_value='+str(get_details.ins_value)+'&name='+str(name))
	 	#r = requests.get('127.0.0.1:8001/login?salary='+str(get_employee.salary)+'&department='+str(get_employee.department))
	if r.text == 'success':
	 	return render_template('updatemessage4.html')
	 		#return "<h1> Employee details submitted sucessfully to MBR portal. </h1>"
	else:
	 	return "<h1> Error occured while submitting details to MBR portal. </h1>"

	db.session.commit()



if __name__ == '__main__':
	app.secret_key = 'abcdweb'
	app.run(debug=True, port=8000)
