from flask import Blueprint, render_template, request, redirect, url_for, session

view = Blueprint("view", __name__, static_folder="static", template_folder="templates")
## declaring routes function

@view.route('/sign_up', methods=["GET","POST"])
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

		return render_template('signup.html')

		
		



@view.route('/')
def home_page():
	return render_template('home_page.html')




@view.route('/login',methods=["GET","POST"])
def login_user():

	if request.method == "POST":
		search_log = User.query.filter_by(email =request.form["email"]).all()
		search_pass = User.query.filter_by(password = request.form["pass_one"]).all()

		if (search_pass and search_log):
			return render_template('user.html', values=Passwords.query.all())
		
	return render_template('login.html')
		

				


@view.route('/user_home', methods=["POST"])
def user_home():
	commit = Passwords(request.form["website"],request.form["email"],request.form["pass_one"] )
	db.session.add(commit,'')
	db.session.commit()
	return render_template('user.html',values=Passwords.query.all())



@view.route('/logout', methods=["POST"])
def log_out():
	return redirect(url_for('login_user'))




@view.route('/delete_pass', methods=["POST"])
def delete_pass():
	req = request.form['del']
	col = Passwords.query.filter_by(id=req).one()
	db.session.delete(col)
	db.session.commit()
	return render_template('user.html',values=Passwords.query.all())



@view.route('/recover', methods=["GET", "POST"])
def pass_recover():
	if request.method == "POST":
		return redirect(url_for('login_user'))

	return render_template('recover.html')
