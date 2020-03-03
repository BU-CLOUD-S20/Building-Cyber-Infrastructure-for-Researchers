from flask import Flask, render_template, request, redirect, url_for

from flask_mongoengine import MongoEngine, Document

from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField

from wtforms.validators import Email, Length, InputRequired

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from flask_user import UserManager

fgsdgfd
ljhl

class ConfigClass(object):
    """ Flask application config """

    # Flask settings
    SECRET_KEY = '...'

    # Flask-MongoEngine settings
    MONGODB_SETTINGS = {
        'db': 'user_db',
        'host': 'mongodb://localhost:27017/user_db'
    }

    # Flask-User settings
    USER_APP_NAME = "Flask-User MongoDB App"  # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = False  # Disable email authentication
    USER_ENABLE_USERNAME = True  # Enable username authentication
    USER_REQUIRE_RETYPE_PASSWORD = False  # Simplify register form


app = Flask(__name__)

app.config.from_object(__name__ + '.ConfigClass')

db = MongoEngine(app)
app.config['SECRET_KEY'] = '<---YOUR_SECRET_FORM_KEY--->'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Document):
    meta = {'collection': '<---YOUR_COLLECTION_NAME--->'}
    email = db.StringField(max_length=30)
    password = db.StringField(max_length=30)


@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Email(message='Invalid username'), Length(max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=20)])


class RegForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Email(message='Invalid username'), Length(max=30)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=20)])


# Setup Flask-User and specify the User data-model
user_manager = UserManager(app, db, User)


@app.route("/")
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('/dashboard'))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            check_user = User.objects(email=form.email.data).first()
            if check_user:
                if check_password_hash(check_user['password'], form.password.data):
                    login_user(check_user)
                    return redirect(url_for('dashboard'))
        if request.form['register_button'] == 'Register':
            return redirect(url_for('/register'))
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if request.method == 'POST':
        if form.validate():
            existing_user = User.objects(email=form.email.data).first()
            if existing_user is None:
                hash_pass = generate_password_hash(form.password.data, method='sha256')
                hey = User.save(form.email.data, hash_pass)
                login_user(hey)
                return redirect(url_for('/dashboard'))
    return render_template('register.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html', name="currentuser.email")


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
