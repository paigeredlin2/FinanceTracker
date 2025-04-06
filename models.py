from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

class Users(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(100), unique=True, nullable=False)
	password = db.Column(db.String(200), nullable=False)

	security_question_one = db.Column(db.String(400), nullable=False)
	security_answer_one = db.Column(db.String(400), nullable=False)
	security_question_two = db.Column(db.String(400), nullable=True)
	security_answer_two = db.Column(db.String(400), nullable=True)

	earnings = db.relationship('Earnings', back_populates='user', cascade='all, delete-orphan')
	expenses = db.relationship('Expenses', back_populates='user', cascade='all, delete-orphan')

	def set_password(self, password):
		self.password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

	def check_password(self, password):
		return check_password_hash(self.password, password)

	def set_answer_one(self, answer_one):
		self.security_answer_one = generate_password_hash(answer_one, method='pbkdf2:sha256', salt_length=16)

	def check_answer_one(self, answer_one):
		return check_password_hash(self.security_question_one, answer_one)

	def set_answer_two(self, answer_two):
		self.security_answer_two = generate_password_hash(answer_two, method='pbkdf2:sha256', salt_length=16)

	def check_answer_two(self, answer_two):
		return check_password_hash(self.security_question_two, answer_two)

@login_manager.user_loader #find user record of user_id
def load_user(user_id):
	return Users.query.get(int(user_id))

class Earnings(db.Model):
	__tablename__ = 'earnings'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(50), nullable=False)
	occurrence = db.Column(db.String(50), nullable=True)
	amount = db.Column(db.Float, nullable=False)

	#establish fk relationship with Users
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	user = db.relationship('Users', back_populates='earnings')

class Expenses(db.Model):
	__tablename__ = 'expenses'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(50), nullable=False)
	occurrence = db.Column(db.String(50), nullable=True)
	dedicated_amount = db.Column(db.Float, nullable=True)
	actual_spend_amount = db.Column(db.Float, nullable=True)

	#establish fk relationship with Users
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	user = db.relationship('Users', back_populates='expenses')

