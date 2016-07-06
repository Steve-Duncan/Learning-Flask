from flask import Flask, render_template, request, redirect , flash
from mysqlconnection import MySQLConnector
import re, datetime

#regex for valid email format
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

app=Flask(__name__)
mysql = MySQLConnector(app,'email')

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/process',methods=['POST'])
def submit():
	#set initial value of condition to valid
	isvalid = 'valid'	
	#get the value entered from the form
	email=request.form['email']
	#validate no blank fields
	if len(email)<1:
		return redirect('/')		
	#validate email address
	if not EMAIL_REGEX.match(email):
		#set condition to not valid
		isvalid = 'notvalid'
		#message to return
		msg = 'Email is not valid!'
		return render_template('index.html',isvalid=isvalid,msg=msg)
	else:
		#set contidion to valid
		isvalid = 'valid'
		#SQL query to add email address to database
		query = "INSERT INTO email_addresses (email) VALUES (:email)"
		#create a dictionary of data from the POST data received.
		data = {'email': email}
		# Run query, with dictionary values injected into the query.
		mysql.query_db(query, data)
		#SQL query to return all addresses
		#query = "SELECT email, DATE_FORMAT(create_time,'%m %d %Y %p') FROM email_addresses"
		query = "SELECT email,DATE_FORMAT(create_time,'%m/%d/%Y %l:%m%p') AS 'date' FROM email_addresses;"
		#put all email addresses in variable
		addresses=mysql.query_db(query, data)


		# email_list=''
		# for address in addresses:
		# 	when = address['create_time'].strftime('%m/%d/%Y %H:%M %p')
		# 	#print when
		# 	email_list=email_list + (address['email']) + '\t' + when + '\n'
		# 	print email_list
		return render_template('process.html',email=email,email_list=addresses)
		#return render_template('process.html',email=email,wtf='fuck you')
		#return render_template('process.html',msg=email,addresses=addresses)
		# return render_template('index.html',isvalid=isvalid)

	return redirect('/')

app.run(debug=True)