from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

from os import getenv
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

uri = getenv('DATABASE_URI', None)
assert uri 

client = MongoClient(uri, server_api=ServerApi('1'))

db = client['upravtok']  # Replace with your MongoDB database name
users_collection = db['users']
data_collection = db['electro_data']

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

@app.route("/")
@app.route("/user")
def user_view():
    return "Hello, Flask!"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        if users_collection.find_one({'username': username}):
            flash('Username already exists. Choose a different one.', 'danger')
        else:
            users_collection.insert_one({'username': username, 'password': password})
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.')


def fetch_data_by_date_time(date_str, time):
    # Convert date string to datetime object
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    
    # Query for document matching the date and time
    document = data_collection.find_one({
        'date': date_obj,
        'time': time
    })
    
    if document:
        # Convert ObjectId to string
        document['_id'] = str(document['_id'])
        # Convert document to dictionary
        document = dict(document)
    return document

def fetch_consumption_by_date_time(date_str, time):
    document = fetch_data_by_date_time(date_str, time)
    if document:
        return document.get('consumption')
    return None

def fetch_price_by_date_time(date_str, time):
    document = fetch_data_by_date_time(date_str, time)
    if document:
        return document.get('price')
    return None

# #basal usage of the method: http://localhost:5000/fetch_data?date=2024-03-12&time=1
# @app.route('/fetch_data', methods=['GET'])
# def fetch_data():
#     date_str = request.args.get('date')
#     time = int(request.args.get('time'))

#     if not date_str or not time:
#         return jsonify({'error': 'Date and time are required parameters'}), 400

#     try:
        # data = fetch_data_by_date_time(date_str, time) #exchange func name if other functionality needed here
#         if data:
#             return jsonify(data)
#         else:
#             return jsonify({'error': 'No document found for the specified date and time'}), 404
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
