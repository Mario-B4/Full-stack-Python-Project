# Import the necessary modules.
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import jwt
# Create a Flask app.
app = Flask(__name__)
# Create a database connection.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
db = SQLAlchemy(app)
# Create a user model.
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
# Define the login route.
@app.route('/login', methods=['POST'])
def login():
    # Get the username and password from the request body.
    username = request.json['username']
    password = request.json['password']
    # Find the user in the database.
    user = User.query.filter_by(username=username).first()
    # If the user is not found, return an error message.
    if user is None:
        return jsonify({'error': 'Invalid username or password.'})
    # If the password is incorrect, return an error message.
    if user.password != password:
        return jsonify({'error': 'Invalid username or password.'})
    # The user is authenticated, so generate a JWT token and return it.
    token = jwt.encode({'user_id': user.id}, app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'token': token})
# Run the app.
if __name__ == '__main__':
    app.run(port= 5000, debug=True)