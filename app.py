from flask import Flask, render_template, request
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from utilities import return_list_of_entries_as_lists, return_form_data_as_list_of_dict, update_entry

# database and app configuration
app = Flask(__name__) # application instance
app.config['SECRET_KEY'] = 'Un295VTH7BFLp6U4eVS6ZXGA' # path to database and database name
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///display.db' # to supress warnings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # database instance
db = SQLAlchemy(app)

class DisplayEntry(db.Model):
    id = db.Column(db.Integer, primary_key = True) # primary key column, automatically generated IDs
    day_of_the_week = db.Column(db.String(15), index = True, unique = True) # Day of the week for the entry
    start_time = db.Column(db.String(10), index = True, unique = False) # Time for display to turn on
    switch_time = db.Column(db.String(10), index = True, unique = False) # Time for display to switch slides
    end_time = db.Column(db.String(10), index = True, unique = False) # time for display to turn off
    start_link_text = db.Column(db.String(30), index = True, unique = False) # Display link text for first slide
    switch_link_text = db.Column(db.String(30), index = True, unique = False) # Display link text for second slide

class CrontabForm(FlaskForm):
    some_list = return_list_of_entries_as_lists(DisplayEntry)

    # Create all TimeField variables
    sunday_start_time = StringField('Sunday Start Time', default=some_list[0][0])
    sunday_switch_time = StringField('Sunday Switch Time', default=some_list[0][1])
    sunday_end_time = StringField('Sunday End Time', default=some_list[0][2])

    monday_start_time = StringField('Monday Start Time', default=some_list[1][0])
    monday_switch_time = StringField('Monday Switch Time', default=some_list[1][1])
    monday_end_time = StringField('Monday End Time', default=some_list[1][2])

    tuesday_start_time = StringField('Tuesday Start Time', default=some_list[2][0])
    tuesday_switch_time = StringField('Tuesday Switch Time', default=some_list[2][1])
    tuesday_end_time = StringField('Tuesday End Time', default=some_list[2][2])

    wednesday_start_time = StringField('Wednesday Start Time', default=some_list[3][0])
    wednesday_switch_time = StringField('Wednesday Switch Time', default=some_list[3][1])
    wednesday_end_time = StringField('Wednesday End Time', default=some_list[3][2])

    thursday_start_time = StringField('Thursday Start Time', default=some_list[4][0])
    thursday_switch_time = StringField('Thursday Switch Time', default=some_list[4][1])
    thursday_end_time = StringField('Thursday End Time', default=some_list[4][2])

    friday_start_time = StringField('Friday Start Time', default=some_list[5][0])
    friday_switch_time = StringField('Friday Switch Time', default=some_list[5][1])
    friday_end_time = StringField('Friday End Time', default=some_list[5][2])

    saturday_start_time = StringField('Saturday Start Time', default=some_list[6][0])
    saturday_switch_time = StringField('Saturday Switch Time', default=some_list[6][1])
    saturday_end_time = StringField('Saturday End Time', default=some_list[6][2])
    
    # Create link text fields
    sunday_start_text = StringField('Sunday Start Text', default=some_list[0][3])
    sunday_switch_text = StringField('Sunday Switch Text', default=some_list[0][4])
    
    monday_start_text = StringField('Monday Start Text', default=some_list[1][3])
    monday_switch_text = StringField('Monday Switch Text', default=some_list[1][4])
    
    tuesday_start_text = StringField('Tuesday Start Text', default=some_list[2][3])
    tuesday_switch_text = StringField('Tuesday Switch Text', default=some_list[2][4])
    
    wednesday_start_text = StringField('Wednesday Start Text', default=some_list[3][3])
    wednesday_switch_text = StringField('Wednesday Switch Text', default=some_list[3][4])
    
    thursday_start_text = StringField('Thursday Start Text', default=some_list[4][3])
    thursday_switch_text = StringField('Thursday Switch Text', default=some_list[4][4])
    
    friday_start_text = StringField('Friday Start Text', default=some_list[5][3])
    friday_switch_text = StringField('Friday Switch Text', default=some_list[5][4])
    
    saturday_start_text = StringField('Saturday Start Text', default=some_list[6][3])
    saturday_switch_text = StringField('Saturday Switch Text', default=some_list[6][4])

    # Create cancel submit field
    cancel = SubmitField('Cancel')

    # Create update submit field
    submit = SubmitField('Update')

@app.route('/', methods = ["GET", "POST"])
def index():
    crontab_form = CrontabForm() # form instance
    
    if request.method == 'POST':
        entry_list = return_form_data_as_list_of_dict(crontab_form)
        i = 1
        for entry in entry_list:
            update_entry(DisplayEntry, entry, i)
            i += 1
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
    return render_template('index.html',
        template_form = crontab_form,
    )