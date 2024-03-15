import ast
import json
from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

from os import getenv
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = getenv('SECRET_KEY', None)

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
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        if users_collection.find_one({'username': username}):
            flash('Username already exists. Choose a different one.', 'danger')
        else:
            users_collection.insert_one({'username': username, 'password': password, 'node_count' : 0, 'nodes' : []})
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))

    else:
        # Render the registration form for GET requests
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password match
        user = users_collection.find_one({'username': username, 'password': password})
        if user:
            flash('Login successful.', 'success')
            return redirect(url_for('user_view', user_id=user["_id"]))
            # Add any additional logic, such as session management
        else:
            flash('Invalid username or password. Please try again.', 'danger')
            return render_template('login.html')

    else:
        # Render the login form for GET requests
        return render_template('login.html')

@app.route("/user")
def user_view():
    user = users_collection.find_one({"_id" : ObjectId(str(request.args['user_id']))})
   
    if user:
        return render_template('user.html', user_id=user["_id"], name=user["username"], n=user["node_count"])

@app.route("/user/configure/<user_id>", methods=['GET'])
def user_configure(user_id):
    user = users_collection.find_one({"_id" : ObjectId(str(user_id))})   
    return render_template('node.html', user_id=user["_id"])

@app.route("/user/add_node/<user_id>", methods=['GET', 'POST'])
def add_node(user_id):
    user = users_collection.find_one({"_id" : ObjectId(str(user_id))})
    if request.method == 'POST':
        type_name = request.form['type_name']
        priority = request.form['priority']
        status = request.form['status']
        consumption = request.form['consumption']
        
        node_data = {
            'type_name': type_name,
            'priority': priority,
            'status': status,
            'consumption': consumption
        }
        
        if user:
            # Add the node data to the user's 'nodes' array
            users_collection.update_one({"_id" : ObjectId(str(user_id))},{'$push': {'nodes': node_data}, '$inc': {'node_count': 1}})
            user = users_collection.find_one({"_id" : ObjectId(str(user_id))})
            print(user["node_count"])
            
        return render_template('user.html', user_id=user["_id"], name=user["username"], n=user["node_count"], node_data=user["nodes"])

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

#basal usage of the method: http://localhost:5000/fetch_data?date=2024-03-12&time=1
@app.route('/fetch_data', methods=['GET'])
def fetch_data():
    date_str = request.args.get('date')
    time = int(request.args.get('time'))

    if not date_str or not time:
        return jsonify({'error': 'Date and time are required parameters'}), 400

    try:
        data = fetch_data_by_date_time(date_str, time) #exchange func name if other functionality needed here
        if data:
            return jsonify(data)
        else:
            return jsonify({'error': 'No document found for the specified date and time'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
