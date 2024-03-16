from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from werkzeug.security import generate_password_hash,  check_password_hash
from view import view



app = Flask(__name__)
app.register_blueprint(view , url_prefix="")
app.secret_key =b'\xca\x8a\x14\xf4\x7f\x04\xa0\x91\xedQ/-+y\xab\xc8'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///users_log.db'
db =SQLAlchemy(app)
##app.permanet_session_lifetime = timedelta(minutes=20)




## database initialization

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String ,nullable=False)
	email = db.Column(db.String,nullable=False)
	password = db.Column(db.String,nullable=False)


	def __init__(self,name,email,password):
		self.name = name
		self.email = email
		self.password = password



class Passwords(db.Model):
	id = db.Column(db.Integer, primary_key = True) 
	website = db.Column(db.String,nullable=False)
	web_email = db.Column(db.String,nullable=False)
	web_pass = db.Column(db.String,nullable=False)


	def __init__(self,website,web_email,web_pass):
		self.website = website
		self.web_email = web_email
		self.web_pass = web_pass



with app.app_context():	
    db.create_all()



if __name__ == ('__main__'):
	app.run(debug=True)