from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Users(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True, nullable=False)
	password = db.Column(db.String(50), nullable=False)

	security_question_one = db.Column(db.String(100), nullable=False)
	security_answer_one = db.Column(db.String(100), nullable=False)
	security_question_two = db.Column(db.String(100), nullable=True)
	security_answer_two = db.Column(db.String(100), nullable=True)

class Earnings(db.Model):
	__tablename__ = 'earnings'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(50), nullable=False)
	occurrence = db.Column(db.String(50), nullable=False)
	amount = db.Column(db.Numeric(10,2), nullable=False)

class Expenses(db.Model):
	__tablename__ = 'expenses'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(50), nullable=False)
	occurrence = db.Column(db.String(50), nullable=False)
	dedicated_amount = db.Column(db.Numeric(10,2), nullable=False)
	actual_spend_amount = db.Column(db.Numeric(10,2), nullable=False)

