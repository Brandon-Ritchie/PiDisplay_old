"""
Imports
"""

from logging import error
from flask import Flask, flash, render_template, request
from flask.helpers import url_for
from werkzeug.datastructures import RequestCacheControl
from werkzeug.utils import redirect
from flask_login import LoginManager, login_required, login_user, UserMixin
from flask_wtf import form
from forms import CrontabForm, LoginForm, update_crontab_form_defaults, return_list_of_entries_as_lists, return_form_data_as_list_of_dict, update_display_entry # for form manipulation
from flask_sqlalchemy import SQLAlchemy # for database manipulation
from utilities import update_crontab # for updating crotab
from werkzeug.security import generate_password_hash, check_password_hash

"""
Database and app configuration
"""

app = Flask(__name__) # application instance
app.config['SECRET_KEY'] = 'Un295VTH7BFLp6U4eVS6ZXGA' # secret key that I don't think I implimented
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///display.db' # path to database and database name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # to turn off alerts
db = SQLAlchemy(app) # database instance
app_login_manager = LoginManager(app)
app_login_manager.init_app(app)

class DisplayEntry(db.Model):
    id = db.Column(db.Integer, primary_key = True) # primary key column, automatically generated IDs
    day_of_the_week = db.Column(db.String(15), index = True, unique = True) # Day of the week for the entry
    start_time = db.Column(db.String(10), index = True, unique = False) # Time for display to turn on
    switch_time = db.Column(db.String(10), index = True, unique = False) # Time for display to switch slides
    end_time = db.Column(db.String(10), index = True, unique = False) # time for display to turn off
    start_link_text = db.Column(db.String(30), index = True, unique = False) # Display link text for first slide
    switch_link_text = db.Column(db.String(30), index = True, unique = False) # Display link text for second slide

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password) 

"""
Routes
"""

@app_login_manager.user_loader
def load_user(id):
  return User.query.get(int(id))

@app_login_manager.unauthorized_handler
def unauthorized():
    return "Sorry, you must be logged in to view this page."

@app.route('/', methods = ["GET", "POST"])
def index():
    login_form = LoginForm()
    if request.method == 'POST':
        user = User.query.filter_by(username=login_form.user.data).first()
        if user:
            if user.check_password(login_form.password.data):
                login_user(user)
                return redirect(url_for('home'))
        else:
            flash('Either the username or password was incorrect.\n Please try again.', 'error')
    return render_template('index.html', template_form = login_form)

@app.route('/home', methods = ["GET", "POST"])
@login_required
def home():
    
    crontab_form = CrontabForm() # form instance
    
    if 'sunday_start_time' in request.form:
        if crontab_form.submit.data:
            entry_list = return_form_data_as_list_of_dict(crontab_form) # created as dictionaries of the form data making it easier to deal with

            for entry in entry_list:
                update_display_entry(DisplayEntry, entry) # update each entry in the DisplayEntry table with the entries from created dictionaries
            try:
                db.session.commit()
                flash('The display has been updated.')
            except Exception as e:
                db.session.rollback()
                flash('There was an error')

            update_crontab(DisplayEntry)

        if crontab_form.cancel.data:
            db.session.rollback()

    some_list = return_list_of_entries_as_lists(DisplayEntry) # create list for updating crontab form defaults
    update_crontab_form_defaults(crontab_form, some_list) # update crontab form defaults AFTER the POST request
    
    return render_template('home.html',
        template_form = crontab_form,
    )

"""
Deployment
"""

if __name__ == '__main__':
    app.run(port = 80, host='0.0.0.0') 