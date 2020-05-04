from flask import Flask, render_template, request, redirect, url_for, flash

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

app = Flask(__name__)

# PyMongo Mongodb settings
app.config["MONGO_URI"] = "..."
mongo = PyMongo(app)
db = mongo.db
collection = db['tempusers']
collection2 = db['temproles']
collection3 = db['projects']
collection4 = db['wsk_results']

app.config['SECRET_KEY'] = '...'

# Flask Mail Settings
app.config.update(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    # Configure the sender info
    MAIL_USERNAME='...',
    MAIL_PASSWORD='...'
)
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
    project_name = StringField('project_name')
    lead = StringField('lead')
    size = StringField('size')
    member = StringField('member')


class CodeForm(FlaskForm):
    code = StringField('')


class MemberForm(FlaskForm):
    project_name = StringField('')
    member_name = StringField('')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('')
    new_password = PasswordField('')
    confirm_new_password = PasswordField('')


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
        return render_template('lead_show_result.html', result=result['response']['result']['greeting'],
                               name=session[0])
    elif session[2] == 'admin':
        return render_template('admin_show_result.html', result=result['response']['result']['greeting'],
                               name=session[0])
    else:
        return render_template('show_result.html', result=result['response']['result']['greeting'], name=session[0])


@app.route("/submit_code", methods=['POST'])
def submit_code():
    global session
    form = CodeForm()

    # Handle Code Form
    if request.method == "POST":
        code = request.form['code']
        result = ""
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
    project_entries = []
    # name, lead, size, member
    project_entry = ["", "", "", []]

    for project in collection3.find():
        project_entry[0] = project['project_name']
        project_entry[1] = project['lead'][0]
        project_entry[2] = str(project['size'])
        for mem in project['member']:
            project_entry[3].append(mem[0])
        project_entries.append(project_entry)
        project_entry = ["", "", "", [""]]

    if session[2] == 'student':
        return render_template('new_project.html', name=session[0], projects=project_entries)
    elif session[2] == 'lead':
        return render_template('lead_new_project.html', name=session[0], projects=project_entries)
    elif session[2] == 'admin':
        return render_template('admin_new_project.html', name=session[0], projects=project_entries)
    else:
        return render_template('new_project.html', name=session[0], projects=project_entries)


@app.route("/new_project/email_request/<project_name>/<project_lead>")
def email_request(project_name, project_lead):
    global session
    lead_match = collection.find_one({'username': project_lead})
    lead_email = lead_match['email']
    try:
        msg = Message("Send Mail Tutorial!",
                      sender=session[1],
                      recipients=[lead_email])
        msg.body = "Hi, " + project_lead + "! I am " + session[0] + ". Could I join your project " + project_name + "?"
        mail.send(msg)
        flash('Email has been sent successfully')
        return redirect(url_for('new_project'))
    except Exception as e:
        return str(e)


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


@app.route('/dashboard/change_password', methods=['GET', 'POST'])
def change_password():
    global session
    error = None
    form = ChangePasswordForm()

    # Handle ChangePasswordForm
    if request.method == "POST":
        passwords = request.form
        current_password = passwords['current_password']
        new_password = passwords['new_password']
        new_password_2 = passwords['confirm_new_password']
        match = collection.find_one({'username': session[0]})
        if not check_password_hash(match['hash_pass'], current_password):
            error = 'Incorrect password'
        else:
            if new_password != new_password_2:
                error = 'Passwords do not match'
            else:
                hashing = generate_password_hash(new_password, method='sha256')
                new_entry = {'username': session[0],
                             'email': session[1],
                             'hash_pass': hashing,
                             'role': session[2]
                             }
                collection.remove({'username': session[0]})
                collection.insert_one(new_entry)
                flash('You have successfully changed your password!')
        if session[2] == 'student':
            return render_template('change_password.html', name=session[0], form=form, error=error)
        elif session[2] == 'lead':
            return render_template('lead_change_password.html', name=session[0], form=form, error=error)
        elif session[2] == 'admin':
            return render_template('admin_change_password.html', name=session[0], form=form, error=error)

    if session[2] == 'student':
        return render_template('change_password.html', name=session[0], form=form)
    elif session[2] == 'lead':
        return render_template('lead_change_password.html', name=session[0], form=form)
    elif session[2] == 'admin':
        return render_template('admin_change_password.html', name=session[0], form=form)
    else:
        return render_template('change_password.html', name=session[0], form=form)


@app.route('/dashboard/help', methods=['GET', 'POST'])
def help():
    global session
    if session[2] == 'student':
        return render_template('help.html', name=session[0])
    elif session[2] == 'lead':
        return render_template('lead_help.html', name=session[0])
    elif session[2] == 'admin':
        return render_template('admin_help.html', name=session[0])
    else:
        return render_template('help.html', name=session[0])


@app.route('/dashboard/all_projects', methods=['GET', 'POST'])
def all_projects():
    global session
    form = ProjectForm()

    project_entries = []
    # name, lead, size, member
    project_entry = ["", "", "", []]

    for project in collection3.find():
        project_entry[0] = project['project_name']
        project_entry[1] = project['lead'][0]
        project_entry[2] = str(project['size'])
        for mem in project['member']:
            project_entry[3].append(mem[0])
        project_entries.append(project_entry)
        project_entry = ["", "", "", [""]]

    if request.method == "POST":
        new_project = request.form
        project_name = new_project['project_name']
        lead = new_project['lead']
        find_lead = collection.find_one({'username': lead})
        size = new_project['size']
        members = []
        member_str = new_project['member']
        member_names = member_str.split()
        for name in member_names:
            find_member = collection.find_one({'username': name})
            members.append([name, find_member['email']])
        new_entry = {'project_name': project_name,
                     'lead': [lead, find_lead['email']],
                     'size': size,
                     'member': members
                     }
        collection3.insert_one(new_entry)
        return render_template('admin_all_projects.html', name=session[0], projects=project_entries, form=form)
    return render_template('admin_all_projects.html', name=session[0], projects=project_entries, form=form)


@app.route('/all_projects/<project_name>', methods=['GET', 'POST'])
def remove_project(project_name):
    collection3.remove({'project_name': project_name})
    return redirect(url_for('all_projects'))


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


@app.route('/all_users/<username>', methods=['GET', 'POST'])
def remove_user(username):
    collection.remove({'username': username})
    return redirect(url_for('all_users'))


@app.route('/dashboard/my_projects', methods=['GET', 'POST'])
def my_projects():
    global session
    # name, lead, size, member
    project_entry = ["", "", "", []]
    lead_project_entries = []
    member_project_entries = []
    member_flag = False
    form = MemberForm()

    if request.method == "POST":
        form = request.form
        project_name = form['project_name']
        member_name = form['member_name']
        find_member = collection.find_one({'username': member_name})
        find_project = collection3.find_one({'project_name': project_name})
        new_member_entry = [member_name, find_member['email']]
        new_member_list = find_project['member']
        if new_member_list is not None:
            new_member_list.append(new_member_entry)
        else:
            new_member_list = [new_member_entry]
        updated_entry = {'project_name': project_name,
                         'lead': find_project['lead'],
                         'size': find_project['size'],
                         'member': new_member_list
                         }
        collection3.remove({'project_name': project_name})
        collection3.insert_one(updated_entry)

    for project in collection3.find():
        if project['lead'][0] == session[0]:
            project_entry[0] = project['project_name']
            project_entry[1] = project['lead'][0]
            project_entry[2] = str(project['size'])
            if project['member'] is not None:
                for mem in project['member']:
                    project_entry[3].append(mem[0])
            lead_project_entries.append(project_entry)
            project_entry = ["", "", "", [""]]
        else:
            for mem in project['member']:
                if session[0] == mem[0]:
                    member_flag = True
            if member_flag:
                project_entry[0] = project['project_name']
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
                               member_projects=member_project_entries, form=form)
    elif session[2] == 'admin':
        return render_template('admin_show_my_projects.html', name=session[0], lead_projects=lead_project_entries,
                               member_projects=member_project_entries)
    else:
        return render_template('show_my_projects.html', name=session[0], lead_projects=lead_project_entries,
                               member_projects=member_project_entries)


@app.route('/my_projects/<project_name>/<member_name>', methods=['GET', 'POST'])
def remove_member(project_name, member_name):
    project_match = collection3.find_one({'project_name': project_name})
    new_member_list = []
    for mem in project_match['member']:
        if mem[0] != member_name:
            find_member = collection.find_one({'username': mem[0]})
            new_member_list.append([mem[0], find_member['email']])
    updated_entry = {'project_name': project_name,
                     'lead': project_match['lead'],
                     'size': project_match['size'],
                     'member': new_member_list
                     }
    collection3.remove({'project_name': project_name})
    collection3.insert_one(updated_entry)
    return redirect(url_for('my_projects'))


@app.route('/logout', methods=['GET'])
def logout():
    global session
    session = ['', '', '']
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
