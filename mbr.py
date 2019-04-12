from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
import logging

app = Flask(__name__)

# Connecting to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sneha3010@localhost/cloudproject'
db = SQLAlchemy(app)

class Mortgage_details(db.Model):
	__tablename__ = 'mbr_mortgage_details'
	id = db.Column('id', db.Unicode, primary_key=True)
	name = db.Column('name', db.Unicode)
	address = db.Column('address', db.Unicode)
	phone_number = db.Column('phone_number', db.Integer)
	employer_info = db.Column('employer_info', db.Unicode)
	password = db.Column('password', db.Unicode)
	salary = db.Column('salary', db.Unicode)
	mortgage_value=db.Column('mortgage_value',db.Unicode)
	M1sID=db.Column('M1sID',db.Unicode)
	ins_value=db.Column('ins_value',db.Unicode)
	ded_value=db.Column('ded_value',db.Unicode)
	application_status = db.Column('application_status', db.Unicode)

@app.route('/mbr/insurance', methods=['GET', 'POST'])
def addInsurance():
	ins_value = request.args['ins_value']
	ded_value = request.args['ded_value']
	name = request.args['name']
	misid=request.args['M1sID']

	mbr1_details = Mortgage_details.query.filter_by(name=name).first()
	
	mbr1_details.ins_value = ins_value
	
	mbr1_details.name=name
	mbr1_details.ded_value=ded_value
	mbr1_details.M1sID=misid
	# mbr1_details.application_status = 'Complete'

	db.session.commit()
	return render_template('updatemessage4.html')

if __name__ == '__main__':
	app.run(debug=True, port=8001, host='24.224.230.51')