from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from pymongo.server_api import ServerApi

from os import getenv
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

uri = getenv('DATABASE_URI', None)
assert uri 

client = MongoClient(uri, server_api=ServerApi('1'))

db = client['upravtok']  # Replace with your MongoDB database name
users_collection = db['users']

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

    return render_template('register.html')
