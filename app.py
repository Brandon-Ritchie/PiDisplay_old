"""
Imports
"""

from logging import error
from flask import Flask, flash, render_template, request, redirect
from flask.helpers import url_for
from flask_login import LoginManager, login_required, login_user
from flask_sqlalchemy import SQLAlchemy # for database manipulation


app = Flask(__name__) # application instance
app.config['SECRET_KEY'] = 'Un295VTH7BFLp6U4eVS6ZXGA' # secret key that I don't think I implimented
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///display.db' # path to database and database name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # to turn off alerts
db = SQLAlchemy(app) # database instance
app_login_manager = LoginManager(app)
app_login_manager.init_app(app)

import models
import forms
from utilities import update_crontab # for updating crotab
"""
Routes
"""

@app_login_manager.user_loader
def load_user(id):
  return models.User.query.get(int(id))

@app_login_manager.unauthorized_handler
def unauthorized():
    return "Sorry, you must be logged in to view this page."

@app.route('/', methods = ["GET", "POST"])
def index():
    login_form = forms.LoginForm()
    if request.method == 'POST':
        user = models.User.query.filter_by(username=login_form.user.data).first()
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
    crontab_form = forms.CrontabForm() # form instance
    
    try:
        if 'sunday_start_time' in request.form:
            if crontab_form.submit.data:
                entry_list = forms.return_form_data_as_list_of_dict(crontab_form) # created as dictionaries of the form data making it easier to deal with
                try:
                    for entry in entry_list:
                        forms.update_display_entry(models.DisplayEntry, entry) # update each entry in the DisplayEntry table with the entries from created dictionaries
                    db.session.commit()
                    update_crontab(models.DisplayEntry)
                    flash('The display has been updated.')
                except Exception as e:
                    db.session.rollback()
                    flash('There was an error')
                    flash(e)
                    
            if crontab_form.cancel.data:
                db.session.rollback()

    except Exception as e:
        flash('There was an error: ')
        flash(e)

    return render_template('home.html',
        template_form = crontab_form,
    )

"""
Deployment
"""

if __name__ == '__main__':
    app.run(port = 80, host='0.0.0.0') 