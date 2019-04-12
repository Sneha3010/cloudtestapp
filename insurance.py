from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
import requests
import logging

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sneha3010@localhost/cloudproject'
db = SQLAlchemy(app)

@app.route('/insurance', methods=['GET'])
def Insurance_Company():
	Name = request.args['Name']
	M1sID = request.args['M1sID']
	# ded_value = request.args['ded_value']
	# ins_value = request.args['ins_value']
	# Value = request.args['Value']
	# mbr_insurance = request.args['mbr_insurance']

	get_value = re_Details.query.filter_by(M1sID=M1sID).first()


	ded_value = 0.05 * Value
	ins_value = Value - ded_value


	return 'Name :' +Name+ 'M1sID :' +M1sID+ 'ded_value :' +ded_value+ 'ins_value :' +ins_value

	r = requests.get(str('http://127.0.0.1:8001/mbr/insurance')+'?Name='+str(Name)+ '&M1sID='+str(M1sID)+ '&ded_value='+str(ded_value)+'&ins_value='+str(ins_value))

	if r.text == 'success':
			return "<h1> Updated </h1>"
	else:
		return "<h1> Error occured while submitting details to MBR portal. </h1>"

	# get_M1sID = re_Details.query.filter_by(M1sID=M1sID).first()
	# r = requests.get(str('http://127.0.0.1:8004/insurance')+'?Name='+str(Name)+ '&M1sID='+str(M1sID)+ '&ded_value='+str(ded_value)+'&ins_value='+str(ins_value))
	 	
	# if r.text == 'success':
	# 	return "<h1> Updated </h1>"
	# else:
	# 	return "<h1> Error occured while submitting details to MBR portal. </h1>"
	# return render_template('property1.html', name=name, ded_value=ded_value, ins_value=ins_value)

if __name__ == '__main__':
	app.run(debug=True, port=8004)