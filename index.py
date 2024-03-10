from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from werkzeug.security import generate_password_hash,  check_password_hash



app = Flask(__name__)
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
	link_id = db.Column(db.String, nullable=False)


	def __init__(self,website,web_email,web_pass,link_id):
		self.website = website
		self.web_email = web_email
		self.web_pass = web_pass
		self.link_id = link_id


session["emails"] 

## declaring routes function

@app.route('/sign_up', methods=["GET","POST"])
def signup_user():
	if request.method == "POST":
		user_name = request.form["full_name"]
		user_email = request.form["email"]
		user_password = request.form["pass_one"]
		user_password_two = request.form["pass_two"]
		checked = str(user_password)
		check = len(checked)

		if (user_password == user_password_two):
			if (check >= 7):
				search_log = User.query.filter_by(email =request.form["email"]).first()
				if (search_log == None):
					signed = User(user_name,user_email,user_password)
					db.session.add(signed,'')
					db.session.commit()
					return redirect(url_for('login_user'))
				else:
					return render_template('signup.html')
			else:
				return render_template('signup.html')
		else:
			return render_template('signup.html')
	else:
		return render_template('signup.html')
		



@app.route('/')
def home_page():
	return render_template('home_page.html')




@app.route('/login',methods=["GET","POST"])
def login_user():

	if request.method == "POST":
		search_log = User.query.filter_by(email =request.form["email"]).all()
		search_pass = User.query.filter_by(password = request.form["pass_one"]).all()

		if (search_pass and search_log):
			session["emails"] = "logged"
			return render_template('user.html', values=Passwords.query.all())
		
		else:
			return render_template('login.html')
	
	else:
		if "logged" in session["emails"]:
			return render_template('user.html', values=Passwords.query.all())
		else:
			return render_template('login.html')

				


@app.route('/user_home', methods=["POST"])
def user_home():
	commit = Passwords(request.form["website"],request.form["email"],request.form["pass_one"] ,user_link)
	db.session.add(commit,'')
	db.session.commit()
	return render_template('user.html',values=Passwords.query.all())



@app.route('/logout', methods=["POST"])
def log_out():
	session.pop("emails",None)
	return redirect(url_for('login_user'))




@app.route('/delete_pass', methods=["POST"])
def del_pass():
	req = request.form['del']
	col = Passwords.query.filter_by(website= request.form['del']).delete()
	db.session.commit()
	return render_template('user.html',values=Passwords.query.all())



@app.route('/recover', methods=["GET", "POST"])
def pass_recover():
	if request.method == "POST":
		return redirect(url_for('login_user'))

	return render_template('recover.html')


with app.app_context():	
    db.create_all()



if __name__ == ('__main__'):
	app.run(debug=True)