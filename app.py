from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Database configuration (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User table (Model)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    contact_number = db.Column(db.String(10), nullable=False, unique=True)

    #Added validation for Phone Number
    @validates("contact_number")
    def validate_contact_number(self, key, number):
        if not re.fullmatch(r'\d{10}",number):
                            raise ValueError("Contact number must be exactly 10 digits")
        return number
        

    def __repr__(self):
        return f"<User {self.name}>"

# Create database & table
@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return "User table created successfully!"

if __name__ == '__main__':
    app.run(debug=True)
