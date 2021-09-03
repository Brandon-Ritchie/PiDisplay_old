"""
Imports
"""

from flask import Flask, render_template, request
from flask_wtf import form # for web app creation and handling
from forms import CrontabForm, update_crontab_form_defaults, return_list_of_entries_as_lists, return_form_data_as_list_of_dict, update_entry # for form manipulation
from flask_sqlalchemy import SQLAlchemy # for database manipulation
from utilities import update_crontab

"""
Database and app configuration
"""

app = Flask(__name__) # application instance
app.config['SECRET_KEY'] = 'Un295VTH7BFLp6U4eVS6ZXGA' # secret key that I don't think I implimented
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///display.db' # path to database and database name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # to turn off alerts
db = SQLAlchemy(app) # database instance

class DisplayEntry(db.Model):
    
    id = db.Column(db.Integer, primary_key = True) # primary key column, automatically generated IDs
    day_of_the_week = db.Column(db.String(15), index = True, unique = True) # Day of the week for the entry
    start_time = db.Column(db.String(10), index = True, unique = False) # Time for display to turn on
    switch_time = db.Column(db.String(10), index = True, unique = False) # Time for display to switch slides
    end_time = db.Column(db.String(10), index = True, unique = False) # time for display to turn off
    start_link_text = db.Column(db.String(30), index = True, unique = False) # Display link text for first slide
    switch_link_text = db.Column(db.String(30), index = True, unique = False) # Display link text for second slide

"""
Routes
"""

@app.route('/', methods = ["GET", "POST"])
def index():
    
    crontab_form = CrontabForm() # form instance
    
    if request.method == 'POST':
        if crontab_form.submit.data:
            entry_list = return_form_data_as_list_of_dict(crontab_form) # created as dictionaries of the form data making it easier to deal with

            for entry in entry_list:
                update_entry(DisplayEntry, entry) # update each entry in the DisplayEntry table with the entries from created dictionaries
            try:
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
            update_crontab(DisplayEntry)

        if crontab_form.cancel.data:
            db.session.rollback()

    some_list = return_list_of_entries_as_lists(DisplayEntry) # create list for updating crontab form defaults
    update_crontab_form_defaults(crontab_form, some_list) # update crontab form defaults AFTER the POST request
    
    return render_template('index.html',
        template_form = crontab_form,
    )

"""
Deployment
"""

if __name__ == '__main__':
    app.run(port = 80, host='0.0.0.0') 