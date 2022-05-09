from bson import json_util
from flask import Flask, json, render_template, flash, url_for, redirect, request
from pymongo import MongoClient


def get_database():
    # client = MongoClient()
    # client.FileServer
    # result = users.insert_one(user)
    return user


logged_user = "none"
wrong_pass = 0
user = {
    "user": "admin2",
    "password": "admin2"
}
api = Flask(__name__)
api.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@api.route('/companies', methods=['GET'])
def get_companies():
    return json.dumps(user)


@api.route('/interface')
def interface():
    return render_template('interface.html')


@api.route('/new_user')
def new_user():
    flash('You created a new account')
    return redirect(url_for('interface'))


@api.route('/login')
def login():
    flash('You were successfully logged in')
    return redirect(url_for('interface'))


@api.route('/logout')
def logout():
    global logged_user
    if logged_user != "none":
        flash(f'You were successfully logged out {logged_user}')
    logged_user = "none"
    return redirect(url_for('index'))


@api.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        name = request.form['Uname']
        password = request.form['Pass']

        global logged_user
        client = MongoClient()
        db = client.FileServer
        users = db.users
        print(name)
        print(password)
        find = users.find({"user": name})
        counter = 0
        for x in find:
            counter = +1
            print(x)
        if counter == 0:
            newuser = {
                "user": name,
                "password": password
            }
            users.insert_one(newuser)
            logged_user = name
            flash('New user created')
            return redirect(url_for('interface'))
        elif counter != 0:
            find2 = users.find({"user": name})
            for x in find2:
                json_str = json_util.dumps(x)
                data = json.loads(json_str)
                if password == data['password']:
                    logged_user = name
                    return redirect(url_for('login'))
                else:
                    error = 'Invalid credentials'
    return render_template('index.html', error=error)


if __name__ == '__main__':
    api.run()
    # user = get_database()
