from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from flask_login import login_user

from livereload import Server
from dotenv import load_dotenv
import os

load_dotenv(override=True) #load our own env file, override disallows caching

from models import db, migrate, login_manager, Users, Earnings, Expenses

environment = os.getenv("ENV", "production")

def create_app(enviro = "production"):
	app = Flask(__name__)

	# database connections
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
	app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
	app.config["DEBUG"] = enviro == "development"
	app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

	db.init_app(app) #bind db and app

	login_manager.init_app(app)
	login_manager.login_view = "login"

	# initialize db (moved from utilities.py)
	with app.app_context():
		migrate.init_app(app, db)

	return app

app = create_app(environment)

#routes
@app.route('/')
def index():
	return render_template("index.html", user=current_user)

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		confirm_password = request.form['confirm_password']

		security_question_one = request.form['security_question_one']
		security_answer_one = request.form['security_answer_one']
		security_question_two = request.form['security_question_two']
		security_answer_two = request.form['security_answer_two']

		if password != confirm_password:
			flash("Passwords do not match", "danger")
			return render_template("register.html")

		user = Users.query.filter_by(username=username).first()
		if user:
			flash("Username already in use", "danger")
		else:
			new_user = Users(username=username, security_question_one=security_question_one, security_question_two=security_question_two)
			new_user.set_password(password)
			new_user.set_answer_one(security_answer_one)
			new_user.set_answer_two(security_answer_two)

			db.session.add(new_user)
			db.session.commit()
			flash("Account created successfully", "success")
			return redirect(url_for('login'))
	return render_template("register.html", user=current_user)



@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		user = Users.query.filter_by(username=username).first()
		if user and user.check_password(password):
			login_user(user)
			return redirect(url_for("tracksheet"))
		else:
			flash("Invalid username or password", "danger")
	return render_template("login.html", user=current_user)

@app.route("/logout")
@login_required
def logout():
	logout_user()
	flash("Logged out successfully!", "info")
	return redirect(url_for("login"))

@app.route('/tracksheet', methods=["GET", "POST"])
@login_required
def tracksheet():
	return render_template("tracksheet.html",
	                       earnings=current_user.earnings,
	                       expenses=current_user.expenses,
	                       user=current_user
	)

@app.route("/earnings", methods=["POST"])
@login_required
def create_earn():
	title = request.form['title']
	occurrence = request.form['occurrence']
	amount = request.form['amount']

	if current_user.is_authenticated:
		user_id = current_user.id  # Get the logged-in user's ID
	else:
		flash("You need to log in first.", "danger")
		return redirect(url_for('login'))

	if not title:
		flash("Title is required.", "danger")

	new_earn = Earnings(title=title, occurrence=occurrence, amount=amount, user_id=user_id)
	db.session.add(new_earn)
	db.session.commit()

	flash("Income added!", "success")
	return redirect(url_for("tracksheet"))

@app.route("/manage_earn/<int:earn_id>", methods=["POST"])
@login_required
def manage_earn(earn_id):
	action = request.form['action']

	earn = Earnings.query.filter_by(id=earn_id).first()

	if action == "delete":
		db.session.delete(earn)
		db.session.commit()

	elif action == "update":
		title = request.form['title']
		occurrence = request.form['occurrence']
		amount = request.form['amount']

		if not title:
			flash("Title is required.", "danger")
			return redirect(url_for("tracksheet"))

		if not amount:
			flash("Amount is required.", "danger")
			return redirect(url_for("tracksheet"))

		earn.title = title
		earn.occurrence = occurrence
		earn.amount = amount
		db.session.commit()
		flash("Earning updated successfully!", "success")

	else:
		flash("Something is wrong with this income!", "danger")

	return redirect(url_for("tracksheet"))


@app.route("/expenses", methods=["POST"])
@login_required
def create_expense():
	title = request.form['title']
	occurrence = request.form['occurrence']
	dedicated_amount = request.form['dedicated_amount']
	actual_spend_amount = request.form['actual_spend_amount']

	if current_user.is_authenticated:
		user_id = current_user.id  # Get the logged-in user's ID
	else:
		flash("You need to log in first.", "danger")
		return redirect(url_for('login'))

	if not title:
		flash("Title is required.", "danger")

	if not actual_spend_amount:
		actual_spend_amount = None

	if not dedicated_amount:
		dedicated_amount = None

	new_expense = Expenses(title=title, occurrence=occurrence, dedicated_amount=dedicated_amount, actual_spend_amount=actual_spend_amount, user_id=user_id)
	db.session.add(new_expense)
	db.session.commit()

	flash("Expense added!", "success")
	return redirect(url_for("tracksheet"))

@app.route("/manage_expense/<int:expense_id>", methods=["POST"])
@login_required
def manage_expense(expense_id):
	action = request.form['action']

	expense = Expenses.query.filter_by(id=expense_id).first()

	if expense is None:
		flash("Expense not found.", "error")  # Display error message to user
		return redirect(url_for('tracksheet'))

	if action == "delete":
		db.session.delete(expense)
		db.session.commit()

	elif action == "update":
		title = request.form['title']
		occurrence = request.form['occurrence']
		dedicated_amount = request.form['dedicated_amount']
		actual_spend_amount = request.form['actual_spend_amount']

		if not title:
			flash("Title is required.", "danger")
			return redirect(url_for("tracksheet"))

		expense.title = title
		expense.occurrence = occurrence
		expense.dedicated_amount = dedicated_amount
		expense.actual_spend_amount = actual_spend_amount

		db.session.commit()
		flash("Expense updated successfully!", "success")

	else:
		flash("Something is wrong with this expense!", "danger")

	return redirect(url_for("tracksheet"))


#running server
if __name__ == "__main__":
	if environment == "development":	# Use livereload for development environment
		server = Server(app.wsgi_app)
		server.watch("core/**/*.py")
		server.watch("core/**/*.html")
		server.watch("core/**/*.css")
		server.serve(port=5000)  # Start the server with livereload
	else:
		app.run(port=5000)	# Run in standard mode for production