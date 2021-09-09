from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from app import db

class CrontabForm(FlaskForm):
    # Create all TimeField variables
    sunday_start_time = StringField('Sunday Start Time')
    sunday_switch_time = StringField('Sunday Switch Time')
    sunday_end_time = StringField('Sunday End Time')

    monday_start_time = StringField('Monday Start Time')
    monday_switch_time = StringField('Monday Switch Time')
    monday_end_time = StringField('Monday End Time')

    tuesday_start_time = StringField('Tuesday Start Time')
    tuesday_switch_time = StringField('Tuesday Switch Time')
    tuesday_end_time = StringField('Tuesday End Time')

    wednesday_start_time = StringField('Wednesday Start Time')
    wednesday_switch_time = StringField('Wednesday Switch Time')
    wednesday_end_time = StringField('Wednesday End Time')

    thursday_start_time = StringField('Thursday Start Time')
    thursday_switch_time = StringField('Thursday Switch Time')
    thursday_end_time = StringField('Thursday End Time')

    friday_start_time = StringField('Friday Start Time')
    friday_switch_time = StringField('Friday Switch Time')
    friday_end_time = StringField('Friday End Time')

    saturday_start_time = StringField('Saturday Start Time')
    saturday_switch_time = StringField('Saturday Switch Time')
    saturday_end_time = StringField('Saturday End Time')
    
    # Create link text fields
    sunday_start_text = StringField('Sunday Start Text')
    sunday_switch_text = StringField('Sunday Switch Text')
    
    monday_start_text = StringField('Monday Start Text')
    monday_switch_text = StringField('Monday Switch Text')
    
    tuesday_start_text = StringField('Tuesday Start Text')
    tuesday_switch_text = StringField('Tuesday Switch Text')
    
    wednesday_start_text = StringField('Wednesday Start Text')
    wednesday_switch_text = StringField('Wednesday Switch Text')
    
    thursday_start_text = StringField('Thursday Start Text')
    thursday_switch_text = StringField('Thursday Switch Text')
    
    friday_start_text = StringField('Friday Start Text')
    friday_switch_text = StringField('Friday Switch Text')
    
    saturday_start_text = StringField('Saturday Start Text')
    saturday_switch_text = StringField('Saturday Switch Text')

    # Create cancel submit field
    cancel = SubmitField('Cancel')

    # Create update submit field
    submit = SubmitField('Update')

def update_crontab_form_defaults(form, list):
    form.sunday_start_time.default = list[0][0]
    form.sunday_switch_time.default = list[0][1]
    form.sunday_end_time.default = list[0][2]
    form.sunday_start_text.default = list[0][3]
    form.sunday_switch_text.default = list[0][4]

    form.monday_start_time.default = list[1][0]
    form.monday_switch_time.default = list[1][1]
    form.monday_end_time.default = list[1][2]
    form.monday_start_text.default = list[1][3]
    form.monday_switch_text.default = list[1][4]

    form.tuesday_start_time.default = list[2][0]
    form.tuesday_switch_time.default = list[2][1]
    form.tuesday_end_time.default = list[2][2]
    form.tuesday_start_text.default = list[2][3]
    form.tuesday_switch_text.default = list[2][4]

    form.wednesday_start_time.default = list[3][0]
    form.wednesday_switch_time.default = list[3][1]
    form.wednesday_end_time.default = list[3][2]
    form.wednesday_start_text.default = list[3][3]
    form.wednesday_switch_text.default = list[3][4]

    form.thursday_start_time.default = list[4][0]
    form.thursday_switch_time.default = list[4][1]
    form.thursday_end_time.default = list[4][2]
    form.thursday_start_text.default = list[4][3]
    form.thursday_switch_text.default = list[4][4]

    form.friday_start_time.default = list[5][0]
    form.friday_switch_time.default = list[5][1]
    form.friday_end_time.default = list[5][2]
    form.friday_start_text.default = list[5][3]
    form.friday_switch_text.default = list[5][4]

    form.saturday_start_time.default = list[6][0]
    form.saturday_switch_time.default = list[6][1]
    form.saturday_end_time.default = list[6][2]
    form.saturday_start_text.default = list[6][3]
    form.saturday_switch_text.default = list[6][4]

    form.process()

def return_list_of_entries_as_lists(database):
    def return_list_of_values_from_entry(entry):
        value_list = [] # create empty list to append entry data to
        value_list.append(entry.start_time)
        value_list.append(entry.switch_time)
        value_list.append(entry.end_time)
        value_list.append(entry.start_link_text)
        value_list.append(entry.switch_link_text)
        value_list.append(entry.id)
        return value_list
    
    db_list = []
    returned_list = []
    
    for x in range(7): # loop through database entries, ?? might be able to do this with database.query.all() ??
        db_list.append(database.query.get(x + 1))
    
    for entry in db_list: # convert database entries into lists for updating default values
        returned_list.append(return_list_of_values_from_entry(entry))
    
    return returned_list

def return_form_data_as_list_of_dict(form):
    sunday_entry = {
        'id': 1,
        'day_of_the_week': 'Sunday',
        'start_time': form.sunday_start_time.data,
        'switch_time': form.sunday_switch_time.data,
        'end_time': form.sunday_end_time.data,
        'start_link_text': form.sunday_start_text.data,
        'switch_link_text': form.sunday_switch_text.data
    }

    monday_entry = {
        'id': 2,
        'day_of_the_week': 'Monday',
        'start_time': form.monday_start_time.data,
        'switch_time': form.monday_switch_time.data,
        'end_time': form.monday_end_time.data,
        'start_link_text': form.monday_start_text.data,
        'switch_link_text': form.monday_switch_text.data
    }

    tuesday_entry = {
        'id': 3,
        'day_of_the_week': 'Tuesday',
        'start_time': form.tuesday_start_time.data,
        'switch_time': form.tuesday_switch_time.data,
        'end_time': form.tuesday_end_time.data,
        'start_link_text': form.tuesday_start_text.data,
        'switch_link_text': form.tuesday_switch_text.data
    }

    wednesday_entry = {
        'id': 4,
        'day_of_the_week': 'Wednesday',
        'start_time': form.wednesday_start_time.data,
        'switch_time': form.wednesday_switch_time.data,
        'end_time': form.wednesday_end_time.data,
        'start_link_text': form.wednesday_start_text.data,
        'switch_link_text': form.wednesday_switch_text.data
    }

    thursday_entry = {
        'id': 5,
        'day_of_the_week': 'Thursday',
        'start_time': form.thursday_start_time.data,
        'switch_time': form.thursday_switch_time.data,
        'end_time': form.thursday_end_time.data,
        'start_link_text': form.thursday_start_text.data,
        'switch_link_text': form.thursday_switch_text.data
    }

    friday_entry = {
        'id': 6,
        'day_of_the_week': 'Friday',
        'start_time': form.friday_start_time.data,
        'switch_time': form.friday_switch_time.data,
        'end_time': form.friday_end_time.data,
        'start_link_text': form.friday_start_text.data,
        'switch_link_text': form.friday_switch_text.data
    }

    saturday_entry = {
        'id': 7,
        'day_of_the_week': 'Saturday',
        'start_time': form.saturday_start_time.data,
        'switch_time': form.saturday_switch_time.data,
        'end_time': form.saturday_end_time.data,
        'start_link_text': form.saturday_start_text.data,
        'switch_link_text': form.saturday_switch_text.data
    }


    entry_list = [sunday_entry, monday_entry, tuesday_entry, wednesday_entry, thursday_entry, friday_entry, saturday_entry]
    return entry_list

def update_display_entry(database, entry):
    updated_entry = db.session.query(database).get(entry['id']) # find entry to be updated
    updated_entry.start_time = entry['start_time'] # update start time
    updated_entry.switch_time = entry['switch_time'] # update switch time
    updated_entry.end_time = entry['end_time'] # update end time
    updated_entry.start_link_text = entry['start_link_text'] # update start link text
    updated_entry.switch_link_text = entry['switch_link_text'] # update switch link text

class LoginForm(FlaskForm):
    user = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')