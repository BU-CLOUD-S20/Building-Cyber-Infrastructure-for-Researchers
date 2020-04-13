
from flask import Flask, render_template, request, redirect, url_for

from flask_pymongo import PyMongo

from pymongo import MongoClient

from flask_wtf import FlaskForm

from wtforms import Form, StringField, PasswordField

from wtforms.validators import Email, Length, InputRequired

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from flask_user import UserManager

from flask_mail import Mail

from flask_mail import Message

import helloworld as helloworld

import datetime

import json

# PyMongo Mongodb settings
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://admin:ec528bcifr@localhost:27017/admin"
mongo = PyMongo(app)
db = mongo.db
collection = db['tempusers']
collection2 = db['temproles']
collection3 = db['projects']
collection4 = db['wsk_results']

app.config['SECRET_KEY'] = '...'

mail = Mail(app)

# Session Management array: [username, email, role]
session = ['', '', '']


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Email(message='Invalid username'), Length(max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=20)])


class RegForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Email(message='Invalid username'), Length(max=30)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=20)])


class ProjectForm(FlaskForm):
    name = StringField('name')
    lead = StringField('lead')
    size = StringField('size')
    member = StringField('member')


class CodeForm(FlaskForm):
    code = StringField('')


class SearchForm(Form):
    search = StringField('')


@app.route("/")
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # Handle Register Form
    if request.method == "POST":
        result = request.form
        username = result['username']
        email = result['email']
        hashing = generate_password_hash(result['password'], method='sha256')
        new_entry = {'username': username,
                     'email': email,
                     'hash_pass': hashing,
                     'role': 'student'
                     }
        collection.insert_one(new_entry)
        return render_template('login.html', form=form)

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegForm()
    return render_template('register.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    global session
    bigger_match = collection.find_one({'username': session[0]})
    form = CodeForm()

    # Handle Login Form
    if request.method == "POST":
        login_result = request.form
        login_username = login_result['username']
        login_password = login_result['password']
        match = collection.find_one({'username': login_username})
        if match is None:
            return redirect(url_for('login'))
        else:
            if check_password_hash(match['hash_pass'], login_password):
                session[0] = match['username']
                session[1] = match['email']
                session[2] = match['role']
                form = CodeForm()
                if session[2] == 'student':
                    return render_template('submit_new_code.html', name=session[0], form=form)
                elif session[2] == 'lead':
                    return render_template('lead_submit_new_code.html', name=session[0], form=form)
                elif session[2] == 'admin':
                    return render_template('admin_submit_new_code.html', name=session[0], form=form)
            else:
                return redirect(url_for('login'))

    if bigger_match['role'] == 'student':
        return render_template('submit_new_code.html', name=session[0], form=form)
    elif bigger_match['role'] == 'lead':
        return render_template('lead_submit_new_code.html', name=session[0], form=form)
    elif bigger_match['role'] == 'admin':
        return render_template('admin_submit_new_code.html', name=session[0], form=form)
    else:
        return render_template('submit_new_code.html', name=session[0], form=form)


@app.route("/hello_world", methods=['GET', 'POST'])
def hello_world():
    global session
    result = helloworld.helloworld()
    new_entry = {'author': session[0],
                 'date': datetime.datetime.utcnow(),
                 'result': str(result)
                 }
    collection4.insert_one(new_entry)
    if session[2] == 'student':
        return render_template('show_result.html', result=result['response']['result']['greeting'], name=session[0])
    elif session[2] == 'lead':
        return render_template('lead_show_result.html', result=result['response']['result']['greeting'], name=session[0])
    elif session[2] == 'admin':
        return render_template('admin_show_result.html', result=result['response']['result']['greeting'], name=session[0])
    else:
        return render_template('show_result.html', result=result['response']['result']['greeting'], name=session[0])


@app.route("/submit_code", methods=['POST'])
def submit_code():
    global session
    result = ''

    # Handle Code Form
    if request.method == "POST":
        code = request.form['code']
        new_entry = {'author': session[0],
                     'date': str(datetime.datetime.utcnow()),
                     'code': code,
                     'result': result
                    }
        if helloworld.create('test', code):
            result = helloworld.invoke('test', "{\"name\":\"World\"}")
        elif helloworld.update('test', code):
            result = helloworld.invoke('test', "{\"name\":\"World\"}")
        else:
            result = 'null'
        collection4.insert_one(new_entry)

    # Need to change result later
    if session[2] == 'student':
        return render_template('show_result.html', result=result['response']['result']['greeting'], name=session[0])
    elif session[2] == 'lead':
        return render_template('lead_show_result.html', result=result['response']['result']['greeting'], name=session[0])
    elif session[2] == 'admin':
        return render_template('admin_show_result.html', result=result['response']['result']['greeting'], name=session[0])
    else:
        return render_template('show_result.html', result=result['response']['result']['greeting'], name=session[0])


@app.route("/dashboard/previous_computations", methods=['GET', 'POST'])
def previous_computations():
    global session
    computation_entries = []
    computation_entry = ["", "", "", ""]
    for computation in collection4.find():
        if computation['author'] == session[0]:
            computation_entry[0] = computation['author']
            computation_entry[1] = computation['date']
            computation_entry[2] = computation['code']
            computation_entry[3] = computation['result']
            computation_entries.append(computation_entry)
            computation_entry = ["", "", "", ""]
    if session[2] == 'student':
        return render_template('previous_computations.html', computations=computation_entries, name=session[0])
    elif session[2] == 'lead':
        return render_template('lead_previous_computations.html', computations=computation_entries, name=session[0])
    elif session[2] == 'admin':
        return render_template('admin_previous_computations.html', computations=computation_entries, name=session[0])
    else:
        return render_template('previous_computations.html', computations=computation_entries, name=session[0])


@app.route("/previous_code/<timestamp>", methods=['GET', 'POST'])
def show_previous_code(timestamp):
    global session
    timestamp.replace("%", " ")
    match = collection4.find_one({'date': str(timestamp)})
    result = json.dumps(match['code'], indent=2)
    if session[2] == 'student':
        return render_template('show_result.html', result=result, name=session[0])
    elif session[2] == 'lead':
        return render_template('lead_show_result.html', result=result, name=session[0])
    elif session[2] == 'admin':
        return render_template('admin_show_result.html', result=result, name=session[0])
    else:
        return render_template('show_result.html', result=result, name=session[0])


@app.route("/previous_result/<timestamp>", methods=['GET', 'POST'])
def show_previous_result(timestamp):
    global session
    timestamp.replace("%", " ")
    match = collection4.find_one({'date': str(timestamp)})
    result = json.dumps(match['result'], indent=2)
    if session[2] == 'student':
        return render_template('show_result.html', result=result, name=session[0])
    elif session[2] == 'lead':
        return render_template('lead_show_result.html', result=result, name=session[0])
    elif session[2] == 'admin':
        return render_template('admin_show_result.html', result=result, name=session[0])
    else:
        return render_template('show_result.html', result=result, name=session[0])


@app.route('/dashboard/new_project', methods=['GET', 'POST'])
def new_project():
    global session
    search = SearchForm(request.form)
    # if request.method == 'POST':
    #    return search_results(search)
    return render_template('new_project.html', name=session[0], form=search)


@app.route('/dashboard/profile', methods=['GET', 'POST'])
def profile():
    global session
    if session[2] == 'student':
        return render_template('profile.html', name=session[0], username=session[0], email=session[1], role="Student")
    elif session[2] == 'lead':
        return render_template('lead_profile.html', name=session[0], username=session[0], email=session[1],
                               role="Project Lead")
    elif session[2] == 'admin':
        return render_template('admin_profile.html', name=session[0], username=session[0], email=session[1],
                               role="System Administrator")
    else:
        return render_template('profile.html', name=session[0], username=session[0], form=search, email=session[1],
                               role="Student")


@app.route('/dashboard/all_projects', methods=['GET', 'POST'])
def all_projects():
    global session
    form = ProjectForm()

    project_entries = []
    # name, lead, size, member
    project_entry = ["", "", "", []]

    for project in collection3.find():
        project_entry[0] = project['name']
        project_entry[1] = project['lead'][0]
        project_entry[2] = str(project['size'])
        for mem in project['member']:
            project_entry[3].append(mem[0])
        project_entries.append(project_entry)
        project_entry = ["", "", "", [""]]

    if request.method == "POST":
        new_project = request.form
        name = new_project['name']
        lead = new_project['lead']
        find_lead = collection.find_one({'username': lead})
        size = new_project['size']
        members = []
        member_str = new_project['member']
        member_names = member_str.split()
        for name in member_names:
            find_member = collection.find_one({'username': name})
            members.append([name, find_member['email']])
        new_entry = {'name': name,
                     'lead': [lead, find_lead['email']],
                     'size': size,
                     'member': members
                     }
        collection3.insert_one(new_entry)
        return render_template('admin_all_projects.html', name=session[0], projects=project_entries, form=form)
    return render_template('admin_all_projects.html', name=session[0], projects=project_entries, form=form)


@app.route('/dashboard/all_users', methods=['GET', 'POST'])
def all_users():
    global session
    user_entries = []
    # name, email, role
    user_entry = ["", "", ""]
    for user in collection.find():
        user_entry[0] = user['username']
        user_entry[1] = user['email']
        user_entry[2] = user['role']
        user_entries.append(user_entry)
        user_entry = ["", "", ""]
    return render_template('admin_all_users.html', name=session[0], users=user_entries)


@app.route('/dashboard/my_projects', methods=['GET', 'POST'])
def my_projects():
    global session
    # name, lead, size, member
    project_entry = ["", "", "", []]
    lead_project_entries = []
    member_project_entries = []
    member_flag = False
    for project in collection3.find():
        if project['lead'][0] == session[0]:
            project_entry[0] = project['name']
            project_entry[1] = project['lead'][0]
            project_entry[2] = str(project['size'])
            for mem in project['member']:
                project_entry[3].append(mem[0])
            lead_project_entries.append(project_entry)
            project_entry = ["", "", "", [""]]
        else:
            for mem in project['member']:
                if session[0] == mem[0]:
                    member_flag = True
            if member_flag:
                project_entry[0] = project['name']
                project_entry[1] = project['lead'][0]
                project_entry[2] = str(project['size'])
                for mem in project['member']:
                    project_entry[3].append(mem[0])
                member_project_entries.append(project_entry)
                project_entry = ["", "", "", [""]]
    if session[2] == 'student':
        return render_template('show_my_projects.html', name=session[0], lead_projects=lead_project_entries,
                               member_projects=member_project_entries)
    elif session[2] == 'lead':
        return render_template('lead_show_my_projects.html', name=session[0], lead_projects=lead_project_entries,
                               member_projects=member_project_entries)
    elif session[2] == 'admin':
        return render_template('admin_show_my_projects.html', name=session[0], lead_projects=lead_project_entries,
                               member_projects=member_project_entries)
    else:
        return render_template('show_my_projects.html', name=session[0], lead_projects=lead_project_entries,
                               member_projects=member_project_entries)


@app.route("/dashboard/new_project/email_request")
def email_request():
    msg = Message("Hello! Could I join your project?",
                  sender="...",
                  recipients=["..."])
    mail.send(msg)
    return render_template('email_request.html')


@app.route('/logout', methods=['GET'])
def logout():
    global session
    session = ['', '', '']
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
