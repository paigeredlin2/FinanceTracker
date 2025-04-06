from models import Users, Earnings, Expenses

def initialize_db(app, db):
	with app.app_context():
		db.create_all()